import json
import pymysql
from prettytable import PrettyTable
conf=json.load(open('shop_db_conf.json'))
def stock():
    table=PrettyTable(['排序','商品编号','商品名称','商品价格','商品库存'])
    conn = pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"],
                           passwd=conf["db_password"], db=conf["db_name"], charset="utf8")
    a = int(input('请输入商品编号：'))
    # b = input('请输入商品名称：')
    #     # c = int(input('请输入商品单价：'))
    # d = int(input('请输入商品入库数量：'))
    try:
        with conn.cursor() as cur:
            if cur.execute('select cnub from commodity_inventory where cid=%s' %a):
                row=cur.fetchone()
                row=int(list(row)[0])
                d = int(input('请输入商品入库数量：'))
                print(row,type(row))
                row=row+d
                cur.execute('update commodity_inventory set cnub=%s where cid=%s',(row,a))
                conn.commit()
            else:
                b = input('请输入商品名称：')
                c = int(input('请输入商品单价：'))
                d = int(input('请输入商品入库数量：'))
                cur.execute('insert into commodity_inventory (cid,cname,cprice,cnub) values (%s,%s,%s,%s)', (a,b,c,d))
                # conn.commit()
                cur.execute('insert into us_info (usid,usname,usprice) values (%s,%s,%s)',
                            (a, b, c))
                conn.commit()
    finally:
        cur.close()

    conn = pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"],
                           passwd=conf["db_password"], db=conf["db_name"], charset="utf8")
    try:
        with conn.cursor() as cur:
            # if not cur.execute('select cid from commodity_inventory where cid=%s' % a):
            #     print('该商品不存在')
            # else:
                cur.execute('select * from commodity_inventory')
                row=cur.fetchall()
                for i in row:
                    table.add_row(i)
                print(table)
    finally:
        cur.close()
# stock()
