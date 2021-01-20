# !/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import select
import queue
import struct
import pickle
import datetime
import os
import numpy as np


HOST = '2001:da8:270:2020:f816:3eff:fedc:8dc3'
port=5900
"""Echo server using IPv6 """
for result in socket.getaddrinfo(HOST, port, socket.AF_INET6, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
    af, socktype, proto, canonname, sa = result
    try:
        # 创建socket对象
        serversocket = socket.socket(af, socktype, proto)
        # 设置IP地址复用
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except socket.error as err:
        print("Error: %s" % err)

    try:
        # 绑定IP地址
        serversocket.bind(sa)
        # 监听，并设置最大连接数
        serversocket.listen(100)
        print("Server lisenting on %s:%s" % (HOST, port))
    except socket.error as  msg:
        serversocket.close()
        continue
    break
    sys.exit(1)


print("服务器启动成功，监听IP：", HOST)
# 服务端设置非阻塞
serversocket.setblocking(False)
# 超时时间
timeout = 10
# 创建epoll事件对象，后续要监控的事件添加到其中
epoll = select.epoll()
# 注册服务器监听fd到等待读事件集合
epoll.register(serversocket.fileno(),select.EPOLLIN)
# 保存连接客户端消息的字典，格式为{}
message_queues = {}
# 文件句柄到所对应对象的字典，格式为{句柄：对象}
fd_to_socket = {serversocket.fileno(): serversocket, }

# 运行里程
mileage = 0
mileage_day = 0
mileage_all = 0
# 运行次数
run_times = 0
run_times_day = 0

# 静止标志 0为静止，1为加速,2为减速
run_flag = 0
# 加速度列表
a1 = []
# 减速度列表
a2 = []
# 电梯上次位置
s_before = 0
# 电梯当前位置
s_current = 0

#加速度
a_a_c=0
#上行下行
a_a_up = []
a_a_down = []
a95_c=0
a95_up = []
a95_down=[]
#减速度
a_d_c=0
a_d_up = []
a_d_down = []
d95_c=0
d95_up = []
d95_down = []
#最大速度
v_list=[]
v_max=0
v_max_list_up=[]
v_max_list_down=[]
#加速度减速度阶段标志
a_flag = 0
d_flag = 0
time_current = datetime.datetime.now()
day_before = datetime.datetime.strftime(time_current, '%Y-%m-%d')
#day_before=0
ele_quality_para_15=[]
ele_quality_para_15_key=0
while True:
    print("等待活动连接......")
    # 轮询注册的事件集合，返回值为[(文件句柄，对应的事件)，(...),....]
    events = epoll.poll(timeout)
    if not events:
        print("epoll超时无活动连接，重新轮询......")
        continue
    print( "有", len(events), "个新事件，开始处理......")

    for fd, event in events:
        socket_server = fd_to_socket[fd]
        # 如果活动socket_server为当前服务器socket，表示有新连接
        if socket_server == serversocket:
            connection, address = serversocket.accept()
            print("新连接：", address)
            # 新连接socket_server设置为非阻塞
            connection.setblocking(False)
            # 注册新连接fd到待读事件集合
            epoll.register(connection.fileno(),select.EPOLLIN)
            # 把新连接的文件句柄以及对象保存到字典
            fd_to_socket[connection.fileno()] = connection
            # 以新连接的对象为键值，值存储在队列中，保存每个连接的信息
            message_queues[connection] = queue.Queue()
        # 关闭事件
        elif event & select.EPOLLHUP:
            print('client close')
            # 在epoll中注销客户端的文件句柄
            epoll.unregister(fd)
            # 关闭客户端的文件句柄
            fd_to_socket[fd].close()
            # 在字典中删除与已关闭客户端相关的信息
            del fd_to_socket[fd]
        # 可读事件
        elif event & select.EPOLLIN:
            # 接收数据
            data = socket_server.recv(1024)
            if data:
                time_current = datetime.datetime.now()
                #转换为北京时间
                time_current=time_current+datetime.timedelta(hours=8)
                day = datetime.datetime.strftime(time_current, '%Y-%m-%d')
                print("日期：",day,"收到数据：", data, "客户端：", socket_server.getpeername())
                #解包存储数据
                s = struct.Struct('I4sddddd')
                # ele_record 值(a_kalman, v_kalman, s_kalman, a_horizontal_squre, dt)
                ele_record = s.unpack(data)
                a=ele_record[2]
                v=ele_record[3]
                a_horizontal_squre=ele_record[5]
                print("数据明细：", ele_record)
                #ele_record[1]为电梯名
                #创建文件夹,转为utf-8,、
                folder_name = str(ele_record[1],'utf-8')
                print(ele_record[1])
                root_directory = '/home/ubuntu/ele_data/'
                path=root_directory+folder_name
                #if not os.path.exists(path):
                try:
                    os.mkdir(path)
                except OSError:
                    pass
                #异常状态检测
                #alarm 0正常，1加速度异常，10速度异常，100振动能量异常
                alarm=0
                if(np.abs(a)>1.5):
                    alarm=alarm+1
                if(np.abs(v)>2.5):
                    alarm=alarm+10
                if(np.abs(a_horizontal_squre>0.35)):
                    alarm=alarm+100
                ele_record=ele_record+(alarm,)
                #覆写当前状态
                f = open(path+'/ele_state_current.pickle', 'wb+')
                pickle.dump(ele_record, f)
                # 清空缓存，将数据写入硬盘

                f.flush()
                f.close()
                #历史记录，按日期分别存储
                f = open(path+'/'+day+'_ele_state_history.pickle', 'ab+')
                pickle.dump(ele_record, f)
                f.close()

                # 有警报时通知邮件发送程序
                if(alarm>0):
                    server_address = "/tmp/mail_alarm"
                    sock_mail = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
                    try:
                        sock_mail.connect(server_address)
                        s_mail = struct.Struct('I4sdddddI')
                        packed_data = s_mail.pack(*ele_record)
                        sock_mail.send(packed_data)
                    except socket.error:
                        print("\r\nsocket error ")
                    finally:
                        print("Closing client")
                        sock_mail.close()
                        alarm=0


                # 将数据放入对应客户端的字典
                message_queues[socket_server].put(data)
                # 修改读取到消息的连接到等待写事件集合(即对应客户端收到消息后，再将其fd修改并加入写事件集合)
                epoll.modify(fd, select.EPOLLOUT)

                # 计算最大加速度，最大减速度，a95，运行次数，运行里程

                a_kalman=ele_record[2]
                v_kalman=ele_record[3]
                s_kalman=ele_record[4]
                if (v_kalman * a_kalman > 0):
                    v_list.append(v_kalman)
                    if (run_flag == 0):
                        s_before = s_kalman
                        run_flag = 1
                    if (np.abs(a_kalman) > 0.5):
                        a1.append(a_kalman)
                        a_flag = 1

                elif (v_kalman * a_kalman< 0):
                    v_list.append(v_kalman)
                    if (np.abs(a_kalman) > 0.5):
                        a2.append(a_kalman)
                        d_flag = 1
                        run_flag = 2
                else:
                    if (a_flag == 1):
                        if (np.min(a1) > 0):
                            if(len(a1)>0):
                                a_a_c = np.max(a1)
                                a95_c = np.percentile(a1, 95)
                            else:
                                a_a_c = 0
                                a95_c = 0
                            a_a_up.append(a_a_c)
                            a95_up.append(a95_c)
                        if (np.max(a1) < 0):
                            if (len(a1) > 0):
                                a_a_c = np.min(a1)
                                a95_c=np.percentile(a1, 5)
                            else:
                                a_a_c = 0
                                a95_c = 0
                            a_a_down.append(a_a_c)
                            a95_down.append(a95_c)
                        a1 = []
                        a_flag = 0
                    if (d_flag == 1):
                        if (np.min(a2) > 0):
                            if (len(a2) > 0):
                                a_d_c=np.max(a2)
                                d95_c=np.percentile(a2, 95)
                            else:
                                a_d_c = 0
                                d95_c = 0
                            a_d_down.append(a_d_c)
                            d95_down.append(d95_c)
                        if (np.max(a2) < 0):
                            if (np.max(a2) < 0):
                                if (len(a2) > 0):
                                    a_d_c = np.min(a2)
                                    d95_c = np.percentile(a2, 5)
                                else:
                                    a_d_c = 0
                                    d95_c = 0
                            a_d_c=np.min(a2)
                            a_d_up.append(a_d_c)
                            d95_c=np.percentile(a2, 5)
                            d95_up.append(d95_c)
                        a2 = []
                        d_flag = 0
                if (v_kalman== 0 and np.abs(a_kalman) == 0):
                    if (run_flag == 2):
                        if (len(v_list)>0):
                            v_max=np.max(v_list)
                            #下行
                            if(v_max<0):
                                v_max=np.min(v_list)
                            #置空开始下一次采集
                            v_list=[]
                        else:
                            v_max=0
                        if(v_max>0):
                            v_max_list_up.append(v_max)
                        if (v_max < 0):
                            v_max_list_down.append(v_max)
                        # 计算运行次数和日运行次数
                        run_times = run_times + 1
                        run_times_day=run_times_day+1
                        #计算总里程和日里程
                        s_current = s_kalman
                        mileage = np.abs(s_current - s_before)
                        mileage_day = mileage_day + mileage
                        mileage_all = mileage_all + mileage
                        s_before = s_current

                        # 覆写当前状态
                        ele_quality_para=(a_a_c,a95_c,a_d_c,d95_c,v_max,mileage_all,run_times,time_current)

                        f = open(path + '/ele_quality_current.pickle', 'wb+')
                        print('电梯质量参数：', ele_quality_para)
                        pickle.dump(ele_quality_para, f)
                        f.flush()
                        f.close()

                        ele_quality_para = list(ele_quality_para)
                        ele_quality_para[-1] = datetime.datetime.strftime(ele_quality_para[-1], '%Y-%m-%d %H:%M:%S')
                        ele_quality_para_15.append(ele_quality_para)
                        if(len(ele_quality_para_15)>15):
                            ele_quality_para_15=ele_quality_para_15[-15:]

                        f = open(path + '/ele_quality_para_15.pickle', 'wb+')
                        print('电梯质量参数15记录：',ele_quality_para_15)
                        pickle.dump([ele_quality_para_15_key,ele_quality_para_15], f)
                        ele_quality_para_15_key=ele_quality_para_15_key+1
                        f.flush()
                        f.close()
                        if(ele_quality_para_15_key>1000000):
                            ele_quality_para_15_key=0
                        # 历史记录
                        f = open(path + '/ele_quality_history.pickle', 'ab+')
                        pickle.dump(ele_quality_para, f)
                        f.close()
                        #每日统计记录
                        if(day!=day_before):

                            if(len(a_a_up)>0):
                                a_max_up_day=np.max(a_a_up)
                                a_max_up_mean=np.mean(a_a_up)
                            else:
                                a_max_up_day=0
                                a_max_up_mean=0
                            if (len(a95_up) > 0):
                                a95_up_day = np.max(a95_up)
                                a95_up_mean = np.mean(a95_up)
                            else:
                                a95_up_day = 0
                                a95_up_mean = 0

                            if (len(a_a_down) > 0):
                                a_max_down_day = np.min(a_a_down)
                                a_max_down_mean = np.mean(a_a_down)
                            else:
                                a_max_down_day = 0
                                a_max_down_mean = 0
                            if (len(a95_down) > 0):
                                a95_down_day = np.min(a95_down)
                                a95_down_mean = np.mean(a95_down)
                            else:
                                a95_down_day = 0
                                a95_down_mean = 0

                            if (len(a_d_up) > 0):
                                d_max_up_day = np.min(a_d_up)
                                d_max_up_mean = np.mean(a_d_up)
                            else:
                                d_max_up_day = 0
                                d_max_up_mean = 0
                            if (len(d95_up) > 0):
                                d95_up_day = np.min(d95_up)
                                d95_up_mean = np.mean(d95_up)
                            else:
                                d95_up_day = 0
                                d95_up_mean = 0

                            if (len(a_d_down) > 0):
                                d_max_down_day = np.max(a_d_down)
                                d_max_down_mean = np.mean(a_d_down)
                            else:
                                d_max_down_day = 0
                                d_max_down_mean = 0
                            if (len(d95_down) > 0):
                                d95_down_day = np.max(d95_down)
                                d95_down_mean = np.mean(d95_down)
                            else:
                                d95_down_day = 0
                                d95_down_mean = 0

                            if (len(v_max_list_up) > 0):
                                v_max_up_day = np.max(v_max_list_up)
                                v_max_up_mean = np.mean(v_max_list_up)
                            else:
                                v_max_up_day = 0
                                v_max_up_mean = 0
                            if (len(v_max_list_down) > 0):
                                v_max_down_day = np.max(v_max_list_down)
                                v_max_down_mean = np.mean(v_max_list_down)
                            else:
                                v_max_down_day = 0
                                v_max_down_mean = 0

                            f = open(path + '/ele_statics_day.pickle', 'ab+')
                            es=(day_before,a_max_up_day,a_max_up_mean,a95_up_day,a95_up_mean,
                                           a_max_down_day,a_max_down_mean,a95_down_day,a95_down_mean,
                                           d_max_up_day,d_max_up_mean,d95_up_day,d95_up_mean,
                                           d_max_down_day,d_max_down_mean,d95_down_day,d95_down_mean,
                                           v_max_up_day,v_max_up_mean,v_max_down_day,v_max_down_mean,
                                           mileage_day,run_times_day)
                            print("添加ele_statics_day.pickle",day_before)
                            pickle.dump(es, f)
                            f.close()
                            #清空，开始新一天记录
                            a_a_up = []
                            a_a_down = []
                            a95_up = []
                            a95_down = []

                            a_d_up = []
                            a_d_down = []
                            d95_up = []
                            d95_down = []

                            v_max_list_up = []
                            v_max_list_down = []

                            day_before = day

                            mileage_day=0
                            run_times_day=0

                    run_flag = 0

        # 可写事件
        elif event & select.EPOLLOUT:
            try:
                # 从字典中获取对应客户端的信息
                msg = message_queues[socket_server].get_nowait()
            except queue.Empty:
                print(socket_server.getpeername(), " queue empty")
                # 修改文件句柄为读事件
                epoll.modify(fd, select.EPOLLIN)
            else:
                print("发送数据：", data, "客户端：", socket_server.getpeername())
                # 发送数据
                socket_server.send(msg)

# 在epoll中注销服务端文件句柄
epoll.unregister(serversocket.fileno())
# 关闭epoll
epoll.close()
# 关闭服务器socket
serversocket.close()
