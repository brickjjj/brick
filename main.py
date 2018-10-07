from selenium import webdriver
from selenium.common.exceptions import TimeoutException,NoSuchElementException
import time
import csv
import e_mail
import logging


def get_values(v1=0,v2=0,v3=0,v4=0):
    browser = webdriver.Chrome()
    #设置隐式等待为30秒
    browser.implicitly_wait(30)
    # browser = webdriver.PhantomJS()
    try:
        browser.get('http://www.boc.cn/sourcedb/whpj/')
    except TimeoutException:
        print('Time Out')
    try:
        extract_value = browser.find_element_by_xpath('//DIV[@class="publish"]/DIV[last()]/TABLE//TR/TD[text()="美元"]/../TD[4]').text
        boc = float(extract_value)*0.01
    except NoSuchElementException:
        boc = "None"
        print('No Element')


    #Gate
    try:
        browser.get('https://gate.io/lang/cn')
        browser.get('https://gate.io/c2c/usdt_cny')
    except TimeoutException:
        print('Time Out')
    try:
        extract_Gate1 = browser.find_element_by_id("curr_rate").text
        extract_value = browser.find_element_by_xpath('//div[@class="table-scroll"]/table//tr//span[text()="买入"]/../../td[2]').text
        extract_Gate2 = float(extract_value)
    except NoSuchElementException:
        extract_Gate1 = "None"
        extract_Gate2 = "None"
        print('No Element')

    #火币
    try:
        browser.get('https://otc.huobi.com/zh-cn/trade/buy-usdt/')
    except TimeoutException:
        print('Time Out')
    try:
        extract_HuoBuy = browser.find_element_by_css_selector("#app > div.left.fillWidth > div.trade-page-container > div > div > div.trade-content > div:nth-child(3) > div.trade-list > div > div.info-wrapper > div.price.average").text
        #extract_HuoBuy = float(extract_value)

    except NoSuchElementException:
         extract_HuoBuy = "None"
         print('No Element')

    #返回获取的值
    try:
        return boc ,extract_Gate1,extract_Gate2,extract_HuoBuy
    except TimeoutException:
        print('Time out')
    finally:
        browser.close()
# 邮件发送
def send_email(message):
    ret = e_mail.mail(message)
    if ret:
        print("邮件发送成功")
    else:
        print("邮件发送失败，请检查e_mail.py配置是否正确。")
# csv头部信息
def header():
    with open('datas.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Date","BankOFChina","Gate-current","Gate-Buy","Huo-BUy",])
# csv写入
def ex_csv(k1,k2,k3,k4):
    date = time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time()))
    #print(type(date))
    with open('datas.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([date,str(k1),str(k2),str(k3),str(k4)])
# 输入值
def input_word():
    number = input('number')
    if number.isdigit():
        number = float(number)
        return number
    else:
        print('您的输入值有误，请重新输入：')
        input_word()
# 间断时间
def input_time():
    t = input('inputtime test')
    if t.isdigit():
        t = float(t)
        return t
    elif t == "":
        t = 1
        return t
    else:
        print('您的输入时间有误，请重新输入：')
        input_time()

# 对比
def compare():
    # 发送邮件
    if ex_value >  number :
        message = "提取的值大于number."
        ex_csv("Bigger")
        #send_email(message)
        print(message)
    # 发送邮件
    elif ex_value == number:
        message = "提取的值等于number."
        ex_csv("equr")
        #send_email(message)
        print(message)
    else:
        print('提取的值小鱼number.')

if __name__ == '__main__':
    #print('test print'+'\n')
    try:
        header()
    except Exception as e:
        print(e)
    number = 1
    t = 1
    while True:
        kList = get_values()
        ex_csv(kList[0],kList[1],kList[2],kList[3])
        #compare()
        # print('afet %s secons again'%t)
        time.sleep(int(t)*60)
