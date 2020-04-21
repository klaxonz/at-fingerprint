import json
import urllib.parse


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
    '4007': "New finger add success",

    '8000': "Receive order response failure",
    '8001': "Receive data response failure",
    '8002': "Receive checksum failure",
    '8003': "Receive data size less than expected"


 
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

def obj2json(obj):
    return json.dumps(obj)

def json_loads(value):
    byts = urllib.parse.unquote_to_bytes(value) 
    byts = byts.decode('UTF-8') 
    return json.loads(byts)

