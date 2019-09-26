import pymysql
import json
import change

def mynub():
    id = int(input('请输入商品编号：'))
    nub = input('请输入商品现在数量：')
    try:
        with conn.cursor() as cur:
            if not cur.execute('select cid from commodity_inventory where cid=%s' % id):
                print('该商品不存在')
                mynub()
            else:
                cur.execute('update commodity_inventory set cnub=%s where cid=%s', (nub, id))
                conn.commit()
    finally:
        cur.close()

def myprice():
    id = int(input('请输入商品编号：'))
    price = int(input('请输入商品新单价：'))
    try:
        with conn.cursor() as cur:
            if not cur.execute('select cid from commodity_inventory where cid=%s' % id):
                print('该商品不存在')
                myprice()
            else:
                cur.execute('update commodity_inventory set cprice=%s where cid=%s', (price, id))
                cur.execute('update us_info set usprice=%s where usid=%s', (price, id))
                cur.execute('update sell_info set sprice=%s where sid=%s', (price, id))
                cur.execute('select snub from sell_info where sid=%s' % id)
                row = cur.fetchone()
                row = int(list(row)[0])
                s = row * price
                cur.execute('update sell_info set ssum=%s where sid=%s', (s, id))
                conn.commit()
    finally:
        cur.close()



def myname():
    id = int(input('请输入商品编号：'))
    name = input('请输入商品新名称：')
    try:
        with conn.cursor() as cur:
            if not cur.execute('select cid from commodity_inventory where cid=%s' % id):
                print('该商品不存在')
                myname()
            else:
                cur.execute('update commodity_inventory set cname=%s where cid=%s', (name, id))
                cur.execute('update us_info set usname=%s where usid=%s', (name, id))
                cur.execute('update sell_info set sname=%s where sid=%s', (name, id))
                conn.commit()
    finally:
        cur.close()



conf=json.load(open("shop_db_conf.json"))
conn=pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"],
                                   passwd=conf["db_password"], db=conf["db_name"], charset="utf8")
def increase():
    a = int(input('请输入商品编号：'))
    try:
        with conn.cursor() as cur:
            if cur.execute('select cnub from commodity_inventory where cid=%s' %a):
                print('商品已经存在')
                change.change()
            else:
                b = input('请输入商品名称：')
                c = int(input('请输入商品单价：'))
                d = int(input('请输入商品入库数量：'))
                cur.execute('insert into commodity_inventory (cid,cname,cprice,cnub) values (%s,%s,%s,%s)', (a,b,c,d))
                # conn.commit()
                cur.execute('insert into us_info (usid,usname,usprice) values (%s,%s,%s)', (a,b,c))
                conn.commit()

    finally:
        cur.close()

def delete():
    id=int(input('请输入要删除的商品编号：'))
    try:
        with conn.cursor() as cur:
            if not cur.execute('select cid from commodity_inventory where cid=%s'%id):
                print('该商品不存在')
                change.change()
            else:
                cur.execute('DELETE FROM commodity_inventory WHERE cid=%s'%id)
                cur.execute('DELETE FROM us_info WHERE usid=%s' % id)
                conn.commit()
    finally:
        cur.close()

def changes():
    print('<-----可以修改的内容如下：----->')
    print('1：商品名称  2:商品单价  3:商品库存数量  4:返回上一界面  5：结束程序')
    op=int(input('请选择你要进行的操作：'))
    if op == 1:
        myname()

    elif op == 2:
       myprice()
    elif op == 3:
        mynub()
    elif op == 4:
        change.change()
    elif op == 5:
        exit()
    else:
        print('输入有误，请重新输入！')