#coding=utf-8


import sys, time
import json
import urllib.parse
import argparse
import serial

from as608 import *


imageSrc = 'image/'

params = {
    'gparams'
}

message = {
    
    # 指纹模块状态
    '0'  :  "",
    '100':  "Get image success",
    '101':  "Get image failure",
    '200':  "Generate characteristic success",
    '201':  "Generate characteristic failure",
    '300':  "Match finger success",
    '301':  "Match finger failure",
    '500':  "Merge characteristic success",
    '501':  "Merge characteristic failure",
    '600':  "Store characteristic success",
    '601':  "Store characteristic failure",
    '800':  "Get characteristic success",
    '801':  "Get characteristic failure",
    '1000': "Store image success",
    '1001': "Store image failure",
    '1500': "Get the module paramter success",
    '1501': "Get the module paramter failure",

    # 自定义状态
    '4000': "Please put your finger on the module",
    '4001': "Please put your finger on the module again",
    '4002': "Please raise your finger",
    '4003': "Didn't detect your finger, please try again",
    '4004': "Didn't raise your finger, please try again",
    '4005': "Not matched, raise your finger and put it again",
    '4006': "Taking a finger image, please hold on",
    '4007': "New finger add success"
}



class Result:

    @staticmethod
    def generateSuccessResult(message, msg_code = 0, data = {}):
        result = {
            'code':      0,
            'msg_code':  msg_code,
            'message':   message,
            'error':     '',
            'data':      data
        }

        return result

    @staticmethod
    def generateFailureResult(message, msg_code = '0', data = {}):
        result = {
            'code':      -1,
            'msg_code':  msg_code,
            'message':   message,
            'error':     '',
            'data':      data
        }

        return result


class Messager:

    @staticmethod
    def sendSuccessMessage(code, data = {}):
        result = Result.generateSuccessResult(message.get(code), code, data)
        result = obj2json(result)
        print(result)

    @staticmethod
    def sendFailureMessage(code, data = {}):
        result = Result.generateFailureResult(message.get(code), code, data)
        result = obj2json(result)
        print(result)
        exit(0)

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



def obj2json(obj):
    return json.dumps(obj)

def json_loads(value):
    byts = urllib.parse.unquote_to_bytes(value) 
    byts = byts.decode('UTF-8') 
    return json.loads(byts)


if __name__ == '__main__':

    # 命令参数
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd')
    args = parser.parse_args()
    # 获取数据
    data = ''
    for i in sys.stdin:
        data += i
    data = json_loads(data)

    # data = {
    #     'port': 'COM10',
    #     'baudrate': 57600
    # }
    ser = None
    try:
        # 打开串口
        ser = serial.Serial(data['port'], baudrate=data['baudrate'], timeout=3)
        # 分析命令参数，执行相应的处理流程
        analyzeArgs(ser, args.cmd)
        # analyzeArgs(ser, 'add')

    finally:
        # 关闭串口
        if ser:
            ser.close()
        # 退出程序
        exit(0)






