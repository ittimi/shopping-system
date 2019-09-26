import json
import pymysql
import main
import change_child
def change():
    while True:
        print('<-------以下内容可供修改------->')
        print('i:增加商品  d:删除商品  c:修改商品   e:返回上一界面  o:结束程序')
        op=input('请输入你想进行的操作：')
        if op == 'i':
            change_child.increase()
        elif op == 'd':
            change_child.delete()
        elif op == 'c':
            change_child.changes()
        elif op == 'e':
            main.main()
        elif op == 'o':
            exit()
        else:
            print('输入有误请重新输入')