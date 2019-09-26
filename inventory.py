import pymysql
from prettytable import PrettyTable
import json
import main
conf=json.load(open('shop_db_conf.json'))
def inventory():
    table=PrettyTable(['排序','商品编号','商品名称','商品价格','商品库存'])
    conn=pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"],
                                   passwd=conf["db_password"], db=conf["db_name"], charset="utf8")
    while True:
        print('1：查看部分商品库存   2：查看全部商品库存 3:返回上一页面  4：结束程序')
        op=int(input('请选择你要进行的操作：'))
        if op == 1:
            list_g = []
            while True:
                id=int(input('请输入你要查询的商品编号：'))
                try:
                    with conn.cursor() as cur:
                        if not cur.execute('select cid from commodity_inventory where cid=%s' % id):
                            print('该商品不存在')
                        else:
                            cur.execute('select * from commodity_inventory where cid=%s'%id)
                            row = cur.fetchall()
                            row = list(list(row)[0])
                            print(row)
                            row = tuple(row)
                            list_g.append(row)
                            print(row)
                            print(list_g)

                finally:
                    cur.close()
                op_1=input('是否继续增加查询商品的数量:按n:结束,其他键继续')
                if op_1 == 'n':
                    break
            for i in list_g:
                table.add_row(i)
            print(table)


        elif op ==2:
            try:
                with conn.cursor() as cur:
                    cur.execute('select * from commodity_inventory')
                    row = cur.fetchall()
                    # print(row)
                    for i in row:
                        table.add_row(i)
                    print(table)
            finally:
                cur.close()
        elif op ==3:
            main.main()
        elif op ==4:
            exit()
        else:
            print('输入有误，请重新输入！')

# inventory()