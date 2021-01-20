#ivcbijfobshlbjjd
# !/usr/bin/env python
# coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import xlwt
import xlrd
import pickle
import socket
import struct
import datetime
import time
import os

root_directory = '/home/ubuntu/ele_data/'
class Mail:
    def __init__(self,receivers,content):
        # 设置服务器
        self.mail_host = "smtp.qq.com"
        # 授权码
        self.mail_pass = "ivcbijfobshlbjjd"
        self.sender = '398271297@qq.com'
        self.receivers = receivers
        self.content=content

    def send(self):
        message=MIMEMultipart()
        #发件人
        message['From'] = Header("电梯状态监测预警", 'utf-8')
        #收件人
        message['To'] = Header("电梯管理员", 'utf-8')
        subject = '电梯运行异常'
        message['Subject'] = Header(subject, 'utf-8')
        print('添加正文和附件')
        #正文
        content = self.content
        alarm=content[-1]
        #百位
        b=alarm//100
        #十位
        r=alarm%100
        s=r//10
        #个位
        g=alarm%10
        alarm_text='电梯'+str(content[1])
        alarm_text = alarm_text + '警报号：'+str(content[-1])+','
        if(g==1):
            alarm_text=alarm_text+'加速度异常，'
        if (s == 1):
            alarm_text = alarm_text + '速度异常，'
        if (b == 1):
            alarm_text = alarm_text + '振动异常，'
        alarm_text=alarm_text+'加速度为:'+str(content[2])+'米每平方秒，'
        alarm_text = alarm_text + '速度为:' + str(content[3]) + '米每秒，'
        alarm_text = alarm_text + '振动能量为:' + str(content[5]) + '平方米每四次秒，'
        alarm_text = alarm_text + '异常发生位置在' + str(content[4]) + '米。'

        message.attach(MIMEText(alarm_text, 'plain', 'utf-8'))
        # 构造附件1
        att1 = MIMEText(open('电梯运行记录.xls', 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        #附件名为中文名时
        att1.add_header("Content-Disposition", "attachment", filename=("gbk", "", "运行记录.xls"))
        #附件名为非中文时
        #att1["Content-Disposition"] = 'attachment;filename=%s' % 'test.xls'
        message.attach(att1)
        try:
            smtpObj = smtplib.SMTP_SSL(self.mail_host, 465)
            smtpObj.login(self.sender, self.mail_pass)
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())
            smtpObj.quit()
            print('邮件发送成功')
        except smtplib.SMTPException as e:
            print('邮件发送失败')

def create_excel_header(worksheet,sheet_header):
    column = 0
    for sh in sheet_header:
        worksheet.write(0, column, label=sh)
        column = column + 1

def create_excel_body(worksheet,sheet_body):
    row_num = 1
    for ele_r in sheet_body:
        column = 0
        for er in ele_r:
            print('er:', er)
            worksheet.write(row_num, column, label=er)
            column = column + 1
            print('行号：', row_num)
        row_num = row_num + 1

def create_excel(ele_name):
    # 创建一个workbook 设置编码
    workbook = xlwt.Workbook(encoding='utf-8')
    # 创建一个worksheet
    worksheet = workbook.add_sheet('运行记录')

    # 写入excel
    # 参数对应 行, 列, 值
    # worksheet.write(0,0, label = 'this is test')

    # 保存
    # workbook.save('测试.xls')

    ###返回数字1-7代表周一到周日
    dayOfWeek = datetime.datetime.now().isoweekday()
    ###返回从0开始的数字
    # day_Week = datetime.now().weekday()
    print(dayOfWeek)
    # print(day_Week )
    #创建表1，运行记录
    # 表头
    sheet_header = ['电梯名','加速度', '速度', '位置', '水平振动能量', '时间间隔','警报号']
    # 写入表头
    create_excel_header(worksheet,sheet_header)

    ele_record=[]
    path = root_directory + ele_name
    time_current = datetime.datetime.now()
    day = datetime.datetime.strftime(time_current, '%Y-%m-%d')

    print('文件路径',path + '/' + day + '_ele_state_history.pickle')
    #复制副本打开防止读写冲突
    if os.path.exists('sheet1.pickle'):
        os.remove('sheet1.pickle')
    os.system('\cp '+path + '/' + day + '_ele_state_history.pickle sheet1.pickle')
    f = open('sheet1.pickle', 'rb+')
    i=0
    while True:
        try:
            er=pickle.load(f)
            ele_record.append( [str(er[1], 'utf-8'),er[2],er[3],er[4],er[5],er[6],er[7]])
            i=i+1
        except EOFError:
            print('the num of records is', i)
            break
    f.close()
    if(len(ele_record)>10000):
        ele_record=ele_record[-10000:]
    # 写入主体
    create_excel_body(worksheet,ele_record)

    '''
    while True:
        try:
            ele_r=pickle.load(f)
            column = 0
            for er in ele_r:
                print('er:',er)
                worksheet.write(row_num, column, label=er)
                column = column + 1
            row_num=row_num+1
        except EOFError:
            print('the num of records is', row_num)
            break
    '''
    #创建表2 质量参数
    worksheet2 = workbook.add_sheet('运行质量参数')
    # 表二表头
    sheet_header = ['最大加速度', 'A95加速度', '最大减速度', 'A95减速度', '最大速度', '运行总里程','运行总次数' '时间']
    # 写入表头
    create_excel_header(worksheet2, sheet_header)
    #文件格式(a_a_c,a95_c,a_d_c,d95_c,v_max,mileage_all,run_times,time_current)
    if os.path.exists('sheet2.pickle'):
        os.remove('sheet2.pickle')
    os.system('\cp ' + path + '/' + 'ele_quality_history.pickle sheet2.pickle')
    f = open('sheet2.pickle', 'rb+')
    ele_quality=[]

    i = 0
    while True:
        try:
            eq = pickle.load(f)
            #元组转为列表
            eq=list(eq)
            #转换时间格式精确到毫秒
            if(isinstance(eq[-1], str)):
                ele_quality.append(eq)
            else:
                eq[-1]=datetime.datetime.strftime(eq[-1],'%Y-%m-%d %H:%M:%S')

            i = i + 1
        except EOFError:
            print('the num of records is', i)
            break
    f.close()
    if(len(ele_quality)>1000):
        ele_quality=ele_quality[-1000:]
    # 写入主体
    create_excel_body(worksheet2, ele_quality)

    workbook.save('电梯运行记录.xls')

content=(1,'ele',1.5,2.5,24,0.25,0.02,0)
SERVER_PATH = "/tmp/mail_alarm"
if os.path.exists(SERVER_PATH):
    os.remove(SERVER_PATH)
#SOCK_DGRAM  udp协议
server = socket.socket( socket.AF_UNIX, socket.SOCK_DGRAM )
server.bind(SERVER_PATH)
print("Listening on path: %s" %SERVER_PATH)
#时间戳
time_last=time.time()-1000
while True:
    print('等待连接')
    datagram = server.recv( 1024 )
    if not datagram:
        break
    else:
        time_now=time.time()
        print("-" * 20)
        print('delt',(time_now-time_last))
        if((time_now-time_last)>500):
            time_last=time_now
            s = struct.Struct('I4sdddddI')
            content=s.unpack(datagram)
            print('警报记录：',s.unpack(datagram))
            ele_name = str(content[1], 'utf-8')
            create_excel(ele_name)

            #receiver_list = ['2447544743@qq.com', '398271297@qq.com']
            receiver_list=[]
            readbook = xlrd.open_workbook('管理员.xls')
            # 索引的方式，从0开始
            sheet = readbook.sheet_by_index(0)
            # 名字的方式
            #sheet = readbook.sheet_by_name('admin')
            nrows = sheet.nrows
            i=1
            while(i<nrows):
                mail_adr=sheet.cell(i,1).value
                receiver_list.append(str(mail_adr))
                i=i+1
            print('管理员邮箱',receiver_list)
            mail = Mail(receiver_list, content)
            mail.send()

    if "DONE" == datagram:
        break

print ("-" * 20)
print ("Server is shutting down now...")
server.close()
os.remove(SERVER_PATH)
print("Server shutdown and path removed.")


