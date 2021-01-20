# !/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import render_template, flash, redirect, url_for, Blueprint, request
from ele_web.extensions import socketio
from threading import Lock
import pickle

ele_bp = Blueprint('ele', __name__)
async_mode = None



thread = None
thread_lock = Lock()

@ele_bp.route('/')
def ele():
    return render_template('ele.html')

@socketio.on('connect', namespace='/ele')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)

def background_thread():
    i=11
    key=100000001
    while True:
        socketio.sleep(0.5)
        ##ele_record 值(id,电梯名,a_kalman, v_kalman, s_kalman, a_horizontal_squre, dt)
        try:
            f = open('/home/ubuntu/ele_data/ele1/ele_state_current.pickle', 'rb')
            es = pickle.load(f)
            f.close()
            socketio.emit('server_response',
                          {'name': es[1],
                           'a': es[2],
                           'v': es[3],
                           's': es[4],
                           'ah': es[5],
                           'alarm':es[7]
                           }, namespace='/ele')
            print('发送数据：',es)
            i=i+1

        except EOFError:
            print("File is writing.")
            continue

        if(i>10):
            i = 0
            try:
                f = open('/home/ubuntu/ele_data/ele1/ele_quality_para_15.pickle', 'rb+')
                ep = pickle.load(f)
                f.close()
                print('-' * 50)
                if(key!=ep[0]):
                    key=ep[0]
                    print('读取质量参数表','-' * 50)
                    mileage_mean = 0
                    opt_mean=0
                    j = 0
                    f1 = open('/home/ubuntu/ele_data/ele1/ele_statics_day.pickle', 'rb+')
                    while True:
                        try:
                            eq = pickle.load(f1)
                            mileage_mean=mileage_mean+eq[-2]
                            #mileage_mean=eq[-2]
                            opt_mean=opt_mean+eq[-1]
                            #opt_mean=eq[-1]

                            j = j + 1
                        except EOFError:
                            print('the num of records is', j)
                            break
                    f1.close()
                    if (j != 0):
                        #mileage_mean=0.1
                        #opt_mean=0.1
                        mileage_mean = mileage_mean / j/10
                        opt_mean = opt_mean / j/10

                    else:
                        mileage_mean = 1000
                        opt_mean = 50
                    socketio.emit('server_response_quality',
                                  {'table': ep[1],
                                   'mileageDay': mileage_mean,
                                   'optDay': opt_mean
                                   }, namespace='/ele')

                    print('发送数据：', ep[1])
                    print('mileage_mean：', mileage_mean)
                    print('opt_mean：', opt_mean)

            except EOFError:
                print("File is writing.")
                continue



