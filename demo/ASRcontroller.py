# encoding: utf-8
'''
Company: 深圳市幻尔科技有限公司
官网:hiwonder.com
日期:2019/9/20
by Aiden
'''
'''
 * 只能识别汉字，将要识别的汉字转换成拼音字母，每个汉字之间空格隔开，比如：幻尔科技 --> huan er ke ji
 * 最多添加50个词条，每个词条最长为79个字符，每个词条最多10个汉字
 * 每个词条都对应一个识别号（1~255随意设置）不同的语音词条可以对应同一个识别号，
 * 比如“幻尔科技”和“幻尔”都可以将识别号设置为同一个值
 * 模块上的STA状态灯：亮起表示正在识别语音，灭掉表示不会识别语音，当识别到语音时状态灯会变暗，或闪烁，等待读取后会恢复当前的状态指示
'''
#使用例程
import smbus
import time
import numpy

class ASR:

    # Global Variables
    address = None
    bus = None
    
    ASR_RESULT_ADDR = 100
    #识别结果存放处，通过不断读取此地址的值判断是否识别到语音，不同的值对应不同的语音

    ASR_WORDS_ERASE_ADDR = 101
    #擦除所有词条

    ASR_MODE_ADDR = 102
    #识别模式的地址，共有三种识别模式：
    #1：循环识别模式。状态灯常亮（默认模式）    
    #2：口令模式，以第一个词条为口令。状态灯常灭，当识别到口令词时常亮，等待识别到新的语音,并且读取识别结果后即灭掉
    #3：按键模式，按下开始识别，不按不识别。支持掉电保存。状态灯随按键按下而亮起，不按不亮

    ASR_ADD_WORDS_ADDR = 160
    #词条添加的地址，支持掉电保存

    def __init__(self, address, bus=1):
        self.address = address
        self.bus = smbus.SMBus(bus)
        
    def readByte(self):
        return self.bus.read_byte(self.address)

    def writeByte(self, val):               
        value = self.bus.write_byte(self.address, val)
        if value != 0:
            return False
        return True
    
    def writeData(self, reg, val):
        self.bus.write_byte(self.address,  reg)
        self.bus.write_byte(self.address,  val)

    def getResult(self):
        if ASR.writeByte(self, self.ASR_RESULT_ADDR):
            return -1        
        value = self.bus.read_byte(self.address)
        return value
    '''
    * 添加词条函数，
    * idNum：词条对应的识别号，1~255随意设置。识别到该号码对应的词条语音时，
    *        会将识别号存放到ASR_RESULT_ADDR处，等待主机读取，读取后清0
    * words：要识别汉字词条的拼音，汉字之间用空格隔开
    * 
    * 执行该函数，词条是自动往后排队添加的。   
    '''
    def addWords(self, idNum, words):
        buf = [idNum]       
        for i in range(0, len(words)):
            buf.append(eval(hex(ord(words[i]))))
        self.bus.write_i2c_block_data(self.address, self.ASR_ADD_WORDS_ADDR, buf)
        time.sleep(0.05)
        
    def eraseWords(self):
        result = self.bus.write_byte_data(self.address, self.ASR_WORDS_ERASE_ADDR, 0)
        time.sleep(0.06)
        if result != 0:
           return False
        return True
    
    def setMode(self, mode): 
        result = self.bus.write_byte_data(self.address, self.ASR_MODE_ADDR, mode)
        if result != 0:
           return False
        return True
        
if __name__ == "__main__":
    addr = 0x79 #传感器iic地址
    asr = ASR(addr)

    #添加的词条和识别模式是可以掉电保存的，第一次设置完成后，可以将1改为0
    if 1:
        asr.eraseWords()
        asr.setMode(1)  #设置识别模式，值范围1~3：循环识别模式、口令模式、按键模式。
        asr.addWords(1, 'ni hao')
        asr.addWords(2, 'kai shi')
        asr.addWords(2, 'ting zhi')
        asr.addWords(3, 'ke le zai na')
    while 1:
        data = asr.getResult()
        print("result:", data)
        time.sleep(0.5)