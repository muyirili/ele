#ivcbijfobshlbjjd
# !/usr/bin/env python
# coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import xlwt
import pickle
import datetime
import os
import time
import xlrd

root_directory = '/home/ubuntu/ele_data/'
class Mail:
    def __init__(self,receivers,content,excel_name):
        # 设置服务器
        self.mail_host = "smtp.qq.com"
        # 授权码
        self.mail_pass = "ivcbijfobshlbjjd"
        self.sender = '398271297@qq.com'
        self.receivers = receivers
        self.content=content
        self.excel_name=excel_name

    def send(self):
        message=MIMEMultipart()
        #发件人
        message['From'] = Header("电梯状态监测预警", 'utf-8')
        #收件人
        message['To'] = Header("电梯管理员", 'utf-8')
        subject = self.content
        message['Subject'] = Header(subject, 'utf-8')
        print('添加正文和附件')
        #正文
        content = self.content+',请查看附件'

        message.attach(MIMEText(content, 'plain', 'utf-8'))
        # 构造附件1
        att1 = MIMEText(open(self.excel_name, 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        #附件名为中文名时
        att1.add_header("Content-Disposition", "attachment", filename=("gbk", "", self.excel_name))
        #附件名为非中文时
        #att1["Content-Disposition"] = 'attachment;filename=%s' % 'test.xls'
        message.attach(att1)
        try:
            smtpObj = smtplib.SMTP_SSL(self.mail_host, 465)
            smtpObj.login(self.sender, self.mail_pass)
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())
            smtpObj.quit()
            print('邮件发送成功')
            if os.path.exists(self.excel_name):
                os.remove(self.excel_name)
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

def create_excel(ele_name,yesterday,excel_name):
    # 创建一个workbook 设置编码
    workbook = xlwt.Workbook(encoding='utf-8')
    # 创建一个worksheet
    worksheet1 = workbook.add_sheet(excel_name)

    path = root_directory + ele_name
    # 表头
    sheet_header = ['最大加速度', 'A95加速度', '最大减速度', 'A95减速度', '最大速度', '运行总里程','运行总次数' '时间']
    # 写入表头
    create_excel_header(worksheet1, sheet_header)
    #文件格式(a_a_c,a95_c,a_d_c,d95_c,v_max,mileage_all,run_times,time_current)
    if os.path.exists('sheet3.pickle'):
        os.remove('sheet3.pickle')
    os.system('\cp ' + path + '/' + 'ele_quality_history.pickle sheet3.pickle')
    f = open('sheet3.pickle', 'rb+')
    ele_quality=[]

    i = 0
    while True:
        try:
            eq = pickle.load(f)
            #元组转为列表
            eq=list(eq)
            #转换时间格式精确到毫秒
            if (isinstance(eq[-1], str)):
                eq_day=eq[-1][:len(yesterday)]
            else:
                eq_day = datetime.datetime.strftime(eq[-1], '%Y-%m-%d')
                eq[-1] = datetime.datetime.strftime(eq[-1], '%Y-%m-%d %H:%M:%S')


            if(eq_day==yesterday):
                ele_quality.append(eq)
            i = i + 1
        except EOFError:
            print('the num of records is', i)
            break
    f.close()
    if(len(ele_quality)>0):
        # 写入主体
        create_excel_body(worksheet1, ele_quality)

    workbook.save(excel_name)

def create_excel_week(ele_name,excel_name):
    # 创建一个workbook 设置编码
    workbook = xlwt.Workbook(encoding='utf-8')
    # 创建一个worksheet
    worksheet1 = workbook.add_sheet(excel_name)

    path = root_directory + ele_name
    '''
   (day_before,
    a_max_up_day,a_max_up_mean,a95_up_day,a95_up_mean,
    a_max_down_day,a_max_down_mean,a95_down_day,a95_down_mean,
    d_max_up_day,d_max_up_mean,d95_up_day,d95_up_mean,
    d_max_down_day,d_max_down_mean,d95_down_day,d95_down_mean,
    v_max_up_day,v_max_up_mean,v_max_down_day,v_max_down_mean,
    mileage_day,run_times_day)
    '''
    # 表头
    sheet_header = ['日期',
                    '当日最大上行加速度', '当日平均上行加速度','当日最大上行A95加速度', '当日平均上行A95加速度',
                    '当日最大下行加速度', '当日平均下行加速度','当日最大下行A95加速度', '当日平均下行A95加速度',
                    '当日最大上行减速度', '当日平均上行减速度','当日最大上行A95减速度', '当日平均上行A95减速度',
                    '当日最大下行减速度', '当日平均下行减速度','当日最大下行A95减速度', '当日平均下行A95减速度',
                    '当日上行最大速度', '当日上行平均速度', '当日下行最大速度', '当日下行平均速度',
                    '日运行里程','日运行次数']
    # 写入表头
    create_excel_header(worksheet1, sheet_header)
    #文件格式(a_a_c,a95_c,a_d_c,d95_c,v_max,mileage_all,run_times,time_current)
    if os.path.exists('sheet4.pickle'):
        os.remove('sheet4.pickle')
    os.system('\cp ' + path + '/' + 'ele_statics_day.pickle sheet4.pickle')
    f = open('sheet4.pickle', 'rb+')
    ele_statics=[]

    i = 0
    while True:
        try:
            eq = pickle.load(f)
            ele_statics.append(eq)
            i = i + 1
        except EOFError:
            print('the num of records is', i)
            break
    f.close()
    if(len(ele_statics)>7):
        ele_statics=ele_statics[-7:]
    if(len(ele_statics)>0):
        # 写入主体
        create_excel_body(worksheet1, ele_statics)

    workbook.save(excel_name)

ele_name='ele1'
receiver_list = ['2447544743@qq.com', '398271297@qq.com']
#yesterday=datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
yesterday='2021-01-12'
already_write=0
while True:
    print('检测')
    time_current = datetime.datetime.now()
    today = datetime.datetime.strftime(time_current, '%Y-%m-%d')
    if (today != yesterday):
        excel_name = yesterday + '日电梯运行质量参数.xls'
        create_excel(ele_name,yesterday,excel_name)
        content=yesterday+'日运行记录'
        receiver_list = []
        readbook = xlrd.open_workbook('管理员.xls')
        # 索引的方式，从0开始
        sheet = readbook.sheet_by_index(0)
        # 名字的方式
        # sheet = readbook.sheet_by_name('admin')
        nrows = sheet.nrows
        i = 1
        while (i < nrows):
            mail_adr = sheet.cell(i, 1).value
            receiver_list.append(str(mail_adr))
            i = i + 1
        print('管理员邮箱', receiver_list)
        mail = Mail(receiver_list,content,excel_name)
        mail.send()
        yesterday=today
    ###返回数字1-7代表周一到周日
    dayOfWeek = datetime.datetime.now().isoweekday()
    ###返回从0开始的数字
    # day_Week = datetime.now().weekday()
    print(dayOfWeek)
    if(dayOfWeek==3):
        if(already_write==0):
            time.sleep(100)
            excel_name = '上周运行统计记录.xls'
            create_excel_week(ele_name,excel_name)
            content='上周运行统计记录'
            receiver_list = []
            readbook = xlrd.open_workbook('管理员.xls')
            # 索引的方式，从0开始
            sheet = readbook.sheet_by_index(0)
            # 名字的方式
            # sheet = readbook.sheet_by_name('admin')
            nrows = sheet.nrows
            i = 1
            while (i < nrows):
                mail_adr = sheet.cell(i, 1).value
                receiver_list.append(str(mail_adr))
                i = i + 1
            print('管理员邮箱', receiver_list)

            mail = Mail(receiver_list,content,excel_name)
            mail.send()
            already_write = 1
    else:
        already_write=0
    time.sleep(10)





