# -*- coding: utf-8 -*-

import serial
import time
# import RPi.GPIO as GPIO

# 全局变量
serial_port = 'COM6' # USB转TTL
baudRate = 57600    # 波特率


usleep = lambda x: time.sleep(x/1000000.0)
def get_now_milli_time():
        return int(time.time() * 1000)

class AS608:

    def __init__(self, ser):
        self.ser = ser

        self.status = 0 # 状态寄存器 0
        self.model = 0  # 传感器类型 0-15
        self.capacity = 300 # 指纹容量 300
        self.secure_level = 3 # 安全等级 1/2/3/4/5，默认为3
        self.packet_size = 128 # 数据包大小 32/64/128/256 bytes，默认为128
        self.baud_rate = 6 # 波特率系数，默认为6
        self.chip_addr = 0xFFFFFFFF # 芯片地址
        self.password = 0  # 通信密码
        self.product_sn = '' # 产品型号
        self.software_version = '' #软件版本号
        self.manufacture = '' # 厂家名称
        self.sensor = '' # 传感器名称

        self.detect_pin = 4 # AS608的WAK引脚连接的树莓派GPIO引脚号
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(self.detect_pin, GPIO.IN)

        self.has_password = 0 # 是否有密码

        self.g_verbose = 0  # 输出信息的详细程度
        self.g_error_desc = '' # 错误代码的含义
        self.g_error_code = 0  # 模块返回的确认码， 如果函数返回值不为true, 获取此变量

        self.g_cmd = [0] * 64 # 发送给模块的指令包
        self.g_reply= [0] * 64 # 模块的响应包

        self.score = 0 # 指纹匹配值

    def PS_Setup(self, chipAddr, password):
        self.chip_addr = chipAddr
        self.password = password

        if self.g_verbose == 1:
            print('-------------------------Initializing-------------------------')
        # 验证密码
        if self.has_password:
            if self.PS_VfyPwd(password):
                return False
            
        # 获取数据包大小、波特率
        if self.PS_ReadSysPara() and self.packet_size > 0:
            if self.g_verbose == 1:
                print('-----------------------------Done-----------------------------\n')
            return True

        if self.g_verbose == 1:
            print('-----------------------------Done-----------------------------\n')

        self.g_error_code =0xC7
        return False

    def PS_VfyPwd(self, password):
        size = self.Gen_Order(0x13, '%4d', password)
        self.Send_Order(self.g_cmd, size)

        return self.Recv_Reply(self.g_reply, size, 12)

    def PS_ReadSysPara(self):
        size = self.Gen_Order(0x0f, '')
        if self.g_verbose == 1:
            print('size: ' + str(size))
        self.Send_Order(self.g_cmd, size)

        ret_reply = self.Recv_Reply(self.g_reply, 28, 28)


        self.status = self.Merge(self.g_reply, 10, 2)
        self.model = self.Merge(self.g_reply, 12, 2)
        self.capacity = self.Merge(self.g_reply, 14, 2)
        self.secure_level = self.Merge(self.g_reply, 16, 2)
        self.chip_addr = self.Merge(self.g_reply, 18, 4)
        self.packet_size = self.Merge(self.g_reply, 22, 2)
        self.baud_rate = self.Merge(self.g_reply, 24, 2)

        self.packet_size = 32 * pow(2, self.packet_size)
        self.baud_rate *= 9600

        return ret_reply

    def PS_GetImage(self):
        size = self.Gen_Order(1, '')

        self.Send_Order(self.g_cmd, size)

        return self.Recv_Reply(self.g_reply, 12, 12)

    def PS_GenChar(self, bufferId):
        size = self.Gen_Order(2, "%d", bufferId)
        self.Send_Order(self.g_cmd, size)

        return self.Recv_Reply(self.g_reply, 12, 12)

    def PS_Match(self):
        size = self.Gen_Order(3, '')
        self.Send_Order(self.g_cmd, size)

        ret_reply = self.Recv_Reply(self.g_reply, 14, 14)
        self.score = self.Merge(self.g_reply, 10, 2)

        return ret_reply

    def PS_RegModel(self):
        size = self.Gen_Order(5, "")
        self.Send_Order(self.g_cmd, size)

        return self.Recv_Reply(self.g_reply, 12, 12)

    def PS_StoreChar(self, bufferId, pageId):
        size = self.Gen_Order(6, "%d%2d", bufferId, pageId)
        self.Send_Order(self.g_cmd, size)

        return self.Recv_Reply(self.g_reply, 12, 12)

    def PS_UpChar(self, bufferId, filename):
        size = self.Gen_Order(8, "%d", bufferId)
        self.Send_Order(self.g_cmd, size)

        # 接收应答包，核对确认码和校验和
        if self.Recv_Reply(self.g_reply, 12, 12) is False:
            return False

        # 接收应答包，将有效数据存储到pData中
        pData = [0] * 768
        if self.Recv_Package(pData, 768) == False:
            return False

        # 写入文件
        file = open(filename, 'w+')
        file.write(str(pData))
        file.close()

        return True

    def PS_UpImage(self, filename):
        size = self.Gen_Order(10, "")
        self.Send_Order(self.g_cmd, size)

        if self.Recv_Reply(self.g_reply, 12, 12) is False:
            return False

        pData = [0] * 36864

        if self.Recv_Package(pData, 36864) is False:
            return False


        file = open(filename, 'wb+')

        bmpData =[]

        header = [0] * 54
        header[0:29] = [0x42,0x4d,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x36,0x04,0x00,0x00,0x28,0x00,
                0x00,0x00,0x00,0x01,0x00,0x00,0x20,0x01,0x00,0x00,0x01,0x00,0x08]

        bmpData.extend(header)

        palette = [0] * 1024
        for i in range(0,256):
            palette[4*i]     = i
            palette[4*i+1]   = i
            palette[4*i+2]   = i
            palette[4*i+3]   = 0

        bmpData.extend(palette)

        pBody = [0] * 73728
        for i in range(0,len(pBody),2):
            pBody[i] = pData[int(i/2)] & 0xf0
  
        for i in range(1, len(pBody), 2):
            pBody[i] = (pData[int(i/2)] & 0x0f) << 4
        
        bmpData.extend(pBody)

        file.write(bytes(bmpData))

        file.close()

        return True



    def PS_DetectFinger(self):
        return self.PS_GetImage() and self.g_reply[9] != 2

    def PS_Exit(self):
        return True

    # ******************** 工具函数 ********************
    def wait_until_detect_finger(self, wait_time):
        start_time = get_now_milli_time()
        end_time   = start_time + wait_time
        while True:
            if self.PS_DetectFinger():
                return True
            else:
                time.sleep(0.1)
                if get_now_milli_time() > end_time:
                    return False

    def wait_until_not_detect_finger(self, wait_time):
        start_time = get_now_milli_time()
        end_time   = start_time + wait_time
        while True:
            if self.PS_DetectFinger() == False:
                return True
            else:
                time.sleep(0.1)
                if get_now_milli_time() > end_time:
                    return False

    def analyseArgv(self, params):
        
        if params == 'add':
            print('请将手指放入指纹模块中')
            if self.wait_until_detect_finger(5000):
                time.sleep(0.5)
                self.PS_GetImage() or self.PS_Exit()
                self.PS_GenChar(1) or self.PS_Exit()
            else:
                print("Error: Didn't detect finger!")
                exit()

            # 判断用户是否抬起了手指
            print('OK. Please raise your finger')
            time.sleep(2)
            if self.wait_until_not_detect_finger(5000):
                time.sleep(0.1)
                print('OK. Please put your finger again!')
                if self.wait_until_detect_finger(5000):
                    time.sleep(0.5)
                    self.PS_GetImage() or self.PS_Exit()
                    self.PS_GenChar(2) or self.PS_Exit()
                else:
                    print("Error: Didn't detect finger!")
                    exit()
            else:
                print("Error: Didn't raise your finger")
                exit()

            if self.PS_Match():
                print("Matched! score = " + str(self.score))
            else:
                print("Not Matched, raise your finger and put it on again.")
                exit()

            if self.g_error_code != 0:
                self.PS_Exit()
            
            # 合并特征文件
            self.PS_RegModel() or self.PS_Exit()
            self.PS_StoreChar(2, 1) or self.PS_Exit()

            # self.PS_UpChar(2)

            print("OK! New fingerprint saved to pageID=1")

            if self.PS_UpImage('finger.bmp') is False:
                print('Get finger image failure, Please try again!')
                return False
            else:
                print('Download finger image success!')

         

    # ******************** 测试函数 ********************
    def testGetIamge(self):
        # 获取图像
        # print('Put yout finger on the module!')
        # time.sleep(3)
        # if self.PS_GetImage():
        #     time.sleep(0.5)
        # else:
        #     print("Error: Didn't detect finger!")

        # print('OK! Get finger image success, Please waiting download image!')

        if self.PS_UpImage('finger.bmp') is False:
            print('Get finger image failure, Please try again!')
            return False
        else:
            print('Download finger image success!')

    def testUpChar(self):
        # 获取图像
        print('Put yout finger on the module!')
        if self.wait_until_detect_finger(5000):
                time.sleep(0.5)
                self.PS_GetImage() or self.PS_Exit()
                self.PS_GenChar(2)  or self.PS_Exit()
        else:
            print("Error: Didn't detect finger!")

        if self.PS_UpChar(1, 'data1') is False:
            print("Error: Didn't generate char!")
        

    # ******************** 辅助函数 ********************
    def RecvCallback(self, size):
        if self.Check(self.g_reply, size):
                return True

    def Gen_Order(self, cmd_code, fmt, *args):
        self.g_cmd[0] = 0xEF
        self.g_cmd[1] = 0x01
        # Todo
        self.Split(self.chip_addr, self.g_cmd, 2, 4)
        self.g_cmd[6] = 0x01
        self.g_cmd[9] = cmd_code

        # 计算参数总个数
        count = 0
        for c in fmt:
            if c == '%':
                count += 1
        
        if count == 0:
            self.Split(0x03, self.g_cmd, 7, 2)  # 包长度
            self.Split(self.Calibrate(self.g_cmd, 0x0C), self.g_cmd, 10, 2) # 检校和(如果不带参数，指令包长度为12，即0x0c)
            return 0x0C
        else:
            offset = 10 # g_cmd偏移量
            width = 1
            ai = 0
            # 处理参数
            for index in range(len(fmt)):
                width = 1
                c = fmt[index]
                
                if c == '%':
                    wi = index + 1
                    t = fmt[wi]
                    # 获取宽度
                    if t >= '0' and t <= '9':
                        width = 0
                        while True:
                            width = (ord(t) - ord('0')) + width * 10
                            wi += 1
                            t = fmt[wi]
                            if not (t >= '0' and t <= '9'):
                                break

                    if t == 'u' or t == 'd':
                        if width > 4:
                            return 0
                        val = args[ai]    
                        ai += 1
                        self.Split(val, self.g_cmd, offset, width)
                    elif t == 'c':
                        if width > 1:
                            return 0
                        val = args[ai]
                        self.g_cmd[offset] = val
                    elif t == 's':
                        val = args[ai]
                        ai += 1
                        self.Split(val, self.g_cmd, offset, width)
                    else:
                        return 0

                    offset += width

        self.Split(offset+2-9, self.g_cmd, 7, 2) # 包长度
        self.Split(self.Calibrate(self.g_cmd, offset + 2), self.g_cmd, offset, 2) # 校验和

        return offset + 2

    def Send_Order(self, order, size):
        # 输出详细信息
        if self.g_verbose == 1:
            print("=====================================================")
            print('Send Order: ')
            self.Print_Data(order[:size])
        self.g_reply = [0] * 64
        self.ser.write(order[:size])
        return size
        
    def Split(self, num, data, start, count):
        for i in range(0, count):
            data[start] = (num & 0xFF << 8 * (count-i-1)) >> 8 * (count-i-1)
            start += 1

    def Calibrate(self, data, size):
        count = 0
        for i in range(6, size - 2):
            count += data[i]

        return count

    def Print_Data(self, data, width=16):
        count = 0

        if width <= 0:
            width = 16

        for i in data:
            count = count + 1
            end = '\n' if count % width == 0 else ' '
            print("{:02X}".format(i), end = end)
        print()

    def Recv_Reply(self, buf, size, psize):
        availCount = 0
        timeCount = 0
        if self.g_verbose == 1:
            print("Need to recevie the length of data: " + str(size))

        start_time = get_now_milli_time()
        while True:
            if self.ser.inWaiting() > 0:
                buf[availCount] = int.from_bytes(self.ser.read(1), byteorder='big')

                availCount += 1

            if availCount >= size and self.RecvCallback(psize):
                break

            time.sleep(0.001)  # 等待10微秒
            timeCount += 1

            if timeCount > 3000:  # 最长阻塞3秒
                break
        
        end_time = get_now_milli_time()

        if self.g_verbose == 1:
            print('Waiting Response time: ' + str(end_time - start_time))

        # 输出详细信息
        if self.g_verbose == 1:
            print('Receviced data packet: ')
            self.Print_Data(buf[:availCount])
            print("=====================================================")
        
        # 最大阻塞时间内未接收到指定大小的数据，返回false
        if availCount < size:
            self.g_error_code = 0xff
            return False

        self.g_error_code = buf[9]

        return True

    def Recv_Package(self, pData, validDataSize):
        if self.packet_size <= 0:
            return False
        # 实际每个数据包的大小
        realPacketSize = 11 + self.packet_size
        # 总共需要接受的数据大小
        realDataSize = int(validDataSize * realPacketSize / self.packet_size)
        # 收满realPackageSize字节，说明收到了一个完整的数据包，追加到pData中
        readBuf = [0] * realPacketSize

        availSize      = 0
        readCount      = 0
        readBufSize    = 0
        offset         = 0
        timeCount      = 0
        size = 0
        while True:
            availSize = self.ser.in_waiting
          
            if availSize > 0:
         
                if availSize > realPacketSize:
                    availSize = realPacketSize
                if (readBufSize + availSize) > realPacketSize:
                    availSize = realPacketSize - readBufSize

                readBuf[readBufSize:readBufSize + availSize] = list(self.ser.read(availSize))

                readBufSize += availSize
                size        += availSize

                if readBufSize == realPacketSize:
                    readBufSize = 0

                    if self.g_verbose == 1:
                        self.Print_Data(readBuf)

                    count_ = self.Merge(readBuf, realPacketSize-2, 2)
                    if self.Calibrate(readBuf, realPacketSize) != count_:
                        print('checksum error!')
                        self.g_error_code = 1
                        return False
                
                    pData[offset:offset+self.packet_size] = readBuf[9:self.packet_size+9]
                    offset += self.packet_size


            time.sleep(0.001)
            if availSize == 0:
                timeCount += 1
            if timeCount > 3000:
                if self.g_verbose == 1:
                    print('timeCount: ' + str(timeCount))
                break
        if self.g_verbose == 1:
            print('readCount: ' + str(size))
            print('last bit: ' + str(pData[-1]))
        
        if size < realDataSize:
            self.g_error_code = 195
            return False
        
        self.g_error_code = 0

        return True

    def Check(self, data, size):
        # 模块传来的校验和
        count_ = self.Merge(data, size-2, 2)
        # 自己计算的校验和
        count = self.Calibrate(data, size)

        return count == count_ and count != 0

    def Merge(self, data, offset, count):
        num = 0
        for i in range(0, count):
            num += (data[offset + i] << (8*(count-i-1)))

        return num
        

   
if __name__ == '__main__':
    
    try:
        ser = serial.Serial('COM6', 57600, timeout=5)
        if ser.isOpen() is False:
            print('serial is not open!')

        as608 = AS608(ser)
        # ser.reset_input_buffer()
        as608.analyseArgv('add')
        # as608.testGetIamge()

        
        # time.sleep(3)
        # as608.PS_ReadSysPara()
        # as608.testUpChar()

        ser.close()
    except KeyboardInterrupt:
        print('close serial for intertupt')
        ser.close()

    

    



