#coding=utf-8


import sys, time
import json
import argparse
import serial

from as608 import *
from util import *


imageSrc = 'image/'

params = {
    'gparams'
}

def analyzeArgs(ser, args):
    
    as608 = AS608(ser)

    if args == 'gparams':
        
        if as608.PS_ReadSysPara() is True:
            data = {
                'baudrate':    as608.baud_rate,
                'packetSize':  as608.packet_size,
                'secureLevel': as608.secure_level
            }

            Messager.sendSuccessMessage('1500', data)
        else:
            Messager.sendFailureMessage('1501')

    if args == 'add':
    
        Messager.sendSuccessMessage('4000')
      
        if as608.wait_until_detect_finger(5000):
            time.sleep(0.2)
            if as608.PS_GetImage() is False:
                Messager.sendFailureMessage('101')

            if as608.PS_GenChar(1) is False:
                Messager.sendFailureMessage('200')
        else:
            Messager.sendFailureMessage('4003')
        
        Messager.sendSuccessMessage('4002')
        time.sleep(2)

        if as608.wait_until_not_detect_finger(5000):
            Messager.sendSuccessMessage('4001')
            time.sleep(0.1)

            if as608.wait_until_detect_finger(5000):
                time.sleep(0.1)
                if as608.PS_GetImage() is False:
                    Messager.sendFailureMessage('101')

                filename = imageSrc +  'finger_' + str(int(time.time())) + '.bmp'
                data = {'filename' : filename}

                Messager.sendSuccessMessage('4006') 

                if as608.PS_UpImage(filename) is False:
                    Messager.sendFailureMessage('1001')
                else:
                    Messager.sendSuccessMessage('1000', data)

                if as608.PS_GenChar(2) is False:
                    Messager.sendFailureMessage('8001')
            else:
                Messager.sendFailureMessage('4003')

        else:
            Messager.sendFailureMessage('4004')

        if as608.PS_Match() is False:
            Messager.sendFailureMessage('4005')

        if as608.PS_RegModel() is False:
            Messager.sendFailureMessage('501')


        if as608.PS_StoreChar(2, 1) is False:
            Messager.sendFailureMessage('601')

        Messager.sendSuccessMessage('4007')




if __name__ == '__main__':

    debug = False

    # 命令参数
    if debug is False:
        parser = argparse.ArgumentParser()
        parser.add_argument('cmd')
        args = parser.parse_args()
    # 获取数据
    if debug is False:
        data = ''
        for i in sys.stdin:
            data += i
        data = json_loads(data)

    if debug is True:
        data = {
            'port': 'COM10',
            'baudrate': 57600
        }
    ser = None
    try:
        # 打开串口
        ser = serial.Serial(data['port'], baudrate=data['baudrate'], timeout=3)
        # 分析命令参数，执行相应的处理流程
        if debug is False:
            analyzeArgs(ser, args.cmd)
        else:
            analyzeArgs(ser, 'add')

    finally:
        # 关闭串口
        if ser:
            ser.close()
        # 退出程序
        exit(0)






