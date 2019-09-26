import json
import pymysql
from prettytable import PrettyTable
conf=json.load(open('shop_db_conf.json'))
def cashier():
    list_g=[]
    s_1=0
    while True:
        table=PrettyTable(['ID','商品名称','商品价格','商品数量','总价'])
        print("<-------- 开始收银--------->")
        id = int(input('商品编号：'))
        num=int(input('请输入商品数量：'))
        conn = pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"],
                              passwd=conf["db_password"], db=conf["db_name"], charset="utf8")
        try:
            with conn.cursor() as cur:
                if not cur.execute('select cid from commodity_inventory where cid=%s' % id):
                    print('该商品不存在')
                else:
                    cur.execute('select * from us_info where usid=%s'%id)
                    row = cur.fetchall()  #row为元组类型数据
                    row=list(list(row)[0])      #转化为列表取出元组值
                    # print(row)
                    del row[0]
                    row=tuple(row)
                    list_g.append(row)    #将取出的元组添加到新列表中
                    # print(row)
        finally:
            cur.close()
        op=input("输入回车结账，其他操作继续: ")
        if not op:
            break
    for i in list_g:
        i = list(i)
        i.append(num)
        s = int(i[2]) * int(i[3])
        i[2]=int(i[2])
        # print(type(i[2]))
        i.append(s)

        ''' 将销售的商品记录在sell_info表中'''

        conn = pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"],
                               passwd=conf["db_password"], db=conf["db_name"], charset="utf8")
        try:
            with conn.cursor() as cur:
                if  cur.execute('select snub from sell_info where sid=%s'%int(i[0])):
                    row=int(cur.fetchone()[0])
                    row=row+i[3]    #当日销售某商品的数量
                    # print(row)
                    sm=i[2]*row     #当日销售某商品的金额
                    # print(sm)
                    # print(i[0])
                    cur.execute('UPDATE sell_info SET snub = %s ,ssum = %s WHERE sid = %s',(row,sm,i[0]))
                    conn.commit()
                else:
                    cur.execute('insert into sell_info (sid,sname,sprice,snub,ssum) values (%s,%s,%s,%s,%s)', (i[0],i[1],i[2],i[3],i[4]))
                    conn.commit()

        finally:
            cur.close()

        '''将销售出去的商品从库存中减掉'''
        conn = pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"],
                               passwd=conf["db_password"], db=conf["db_name"], charset="utf8")
        try:
            with conn.cursor() as cur:
                if not cur.execute('select cid from commodity_inventory where cid=%s' % id):
                    print('该商品不存在')
                else:
                    cur.execute('select cnub from commodity_inventory where cid=%s' % int(i[0]))
                    row = int(cur.fetchone()[0])
                    row = row - i[3]  # 当日销售某商品的数量
                    # print(row)
                    cur.execute('UPDATE commodity_inventory SET cnub = %s  WHERE cid = %s', (row,i[0]))
                    conn.commit()
        finally:
            cur.close()


        i = tuple(i)
        # print(i)
        table.add_row(i)
        s_1+=s
    print(table)
    print("总金额为：%s"%s_1)
# cashier()

