import pymysql
import json
conf = json.load(open("shop_db_conf.json"))  # 加载配置信息
def reg_login():
    print("1：登录")
    print("2: 注册")
    choose=int(input("请输入你的选择："))
    while True:
        if choose == 1:
            id=input("请输入用户名：")
            password = input("请输入密码：")
            conn = pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"],
                                   passwd=conf["db_password"], db=conf["db_name"], charset="utf8")
            try:
                with conn.cursor() as cur:
                    cur.execute('select uname from user where uname=%s and passwd=password(%s)',(id,password))
                    rows = cur.fetchone()
            finally:
                cur.close()
            if rows:
                print("%s你好,欢迎使用"%id)
                break
            else:
                print("登录失败，请重新输入")
        elif choose == 2:
            id=input("请输入用户名：")
            password=input("请输入密码：")
            phone=int(input("请输入手机号码："))
            idcard=int(input("请输入身份证号码："))
            conn = pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"],
                                   passwd=conf["db_password"], db=conf["db_name"], charset="utf8")
            try:
                with conn.cursor() as cur:  # 获取一个游标对象(Cursor类)，用于执行SQL语句
                    # 执行任意支持的SQL语句
                    cur.execute("insert into user (uname, passwd, phone, idcard) values (%s, password(%s), %s, %s)",
                                (id, password, phone, idcard))
                    r = cur.rowcount
                    conn.commit()
                    print("注册成功")
            finally:
                # 关闭数据库连接
                conn.close()
            reg_login()
            break
        else:
            print("输入有误，请重新输入")
# reg_login()