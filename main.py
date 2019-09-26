import json
import reg_login
import selltoday
import cashier as csr
import inventory
import change
import stock
conf = json.load(open("shop_db_conf.json"))  # 加载配置信息
def main():
    while True:
        print("你可以进行如下操作：")
        print("c:收银系统  i:库存系统  s:进货系统  t:今日销量  g:修改商品信息  e:退出")
        op=input("请输入你的选择：")
        if op=='c':
            csr.cashier()
            # break
        elif op=='i':
            inventory.inventory()
            # break
        elif op=='s':
            stock.stock()
            # break
        elif op == 't':
            selltoday.selltoday()
            # break
        elif op == 'g':
            change.change()
        elif op=='e':
            exit()
        else:
            print("操作不正确，请重新输入")

if __name__=='__main__':
    reg_login.reg_login()
    main()