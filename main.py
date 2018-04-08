#-*-coding:utf-8-*-

import time
from threading import Timer
import smtplib
import datetime
import requests
import re
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
total = 0
lastesttitle =""
oneDaySeconds = 60 * 60 * 24

subject = "来自韩博的每日监控提醒"


class EmailSend(object):
    def __init__(self, msgTo, data2, Subject):
        self.msgTo= msgTo
        self.data2 = data2
        self.Subject = Subject

    def sendEmail(self):
        msg = MIMEText(self.data2, 'plain', 'utf-8')
        msg['Subject'] = self.Subject
        msg['From'] = 'hanbo_ph@163.com' #'hmhanbo@outlook.com'
        msg['To'] = self.msgTo
        try:
            smtp = smtplib.SMTP()
            smtp.connect('smtp.163.com', 25)
            smtp.login(msg['From'], 'zgsxhm111')  #'Hb4289197'
            smtp.sendmail(msg['From'], msg['To'].split(','), msg.as_string())
            print('邮件发送成功')
        except Exception as e:
            print('--------------sss------', e)


def pbc_req(url):
    import requests
    import re

    from bs4 import BeautifulSoup

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
        "Accept": "text/html, application/xhtml+xml, image/jxr, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-Hans-CN, zh-Hans; q=0.8, en-US; q=0.5, en; q=0.3",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "www.pbc.gov.cn",
        "Referer": "diagnostics://4/",
        "Cookie": "_gscu_1042262807=749843495iifnl11; wzwsconfirm=b74c293f291ae99b352e78f1121cda10; wzwsvtime=1522897327; wzwstemplate=Mw==; wzwschallenge=V1pXU19DT05GSVJNX1BSRUZJWF9MQUJFTDMxMjQwNzU=; ccpassport=e71a727e8fa68227bd438986e154f0fb",
    }

    req = requests.get(url, headers=headers)
    #req = requests.get(url)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, "lxml")

    return soup.find_all(name='a', attrs={"href": re.compile(r"/zhengcehuobisi/125207/125213/125431/125469/\d+/index\.html")})

pbc_url = 'http://www.pbc.gov.cn/zhengcehuobisi/125207/125213/125431/index.html'



def worker():
    global total
    global lastesttitle
    total += 1
    if total < 10:
        print(u"现在是", nowTime, "第几次执行：", total)
        fd = pbc_req(pbc_url)
        if lastesttitle == fd[0].get_text():
            bodypart = "跟昨天一样" "发现更新，请注意！！！"
        else:
            bodypart = "发现更新，请注意！！！"

        lastesttitle = fd[0].get_text()
        body = bodypart + '\n\n最新的公告为：' + lastesttitle
        sendtask = EmailSend("hmhanbo@outlook.com", body, subject)
        sendtask.sendEmail()
        Timer(oneDaySeconds, worker).start()

print(u'程序启动时刻：', time.time())
worker()
