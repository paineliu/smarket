import os
import time
import RPi.GPIO as GPIO

GPIO_4  = 7
GPIO_5  = 29
GPIO_6  = 31
GPIO_12 = 32
GPIO_13 = 33
GPIO_16 = 36
GPIO_17 = 11
GPIO_18 = 12
GPIO_19 = 35
GPIO_20 = 38
GPIO_21 = 40
GPIO_22 = 15
GPIO_23 = 16
GPIO_24 = 18
GPIO_25 = 22
GPIO_26 = 37
GPIO_27 = 13

# 指示类传感器
class Indicator:
    OFF = 0
    ON = 1
    def __init__(self, pin_id, on_val = 1, off_val = 0):
        self.on_val = on_val
        self.off_val = off_val
        self.pin_id = pin_id
        self.state = self.OFF
        GPIO.setup(self.pin_id, GPIO.OUT)
        self.off()

    def on(self):
        self.state = self.ON
        GPIO.output(self.pin_id, self.on_val)
    
    def off(self):
        self.state = self.OFF
        GPIO.output(self.pin_id, self.off_val)
    
    def is_on(self):
        return self.state == self.ON
    
    def is_off(self):
        return self.state == self.OFF
    
    def turn(self):
        if (self.state == self.ON):
            self.off()
        else:
            self.on()

# LED灯
class Led(Indicator):
    def __init__(self, pin_id):
        super().__init__(pin_id)

# 激光传感器
class Laser(Indicator):
    def __init__(self, pin_id):
        super().__init__(pin_id)

# 蜂鸣器
class Bizzer(Indicator):
    def __init__(self,pin_id):
        super().__init__(pin_id, on_val=0, off_val=1)
    
# 风扇
class Fan(Indicator):
    def __init__(self, pin_id):
        super().__init__(pin_id)

# 双色LED灯
class LedRG:
    def __init__(self, red_pin_id, green_pin_id):
        self.OFF = 0
        self.GREEN = 1
        self.RED = 2
        self.mode = self.OFF

        self.r = Led(red_pin_id)
        self.g = Led(green_pin_id)

    def red(self):
        self.mode = self.RED
        self.g.off()
        self.r.on()

    def green(self):
        self.mode = self.GREEN
        self.r.off()
        self.g.on()
    
    def off(self):
        self.mode = self.GREEN
        self.r.off()
        self.g.off()

    def turn(self):
        if (self.mode == self.RED):
            self.green()
        elif (self.mode == self.GREEN):
            self.red()
        else:
            self.green()

# 开关类传感器
class Switch:
    def __init__(self, pin_id, pin_callback, edge = GPIO.FALLING, pull_up_down=GPIO.PUD_UP):
        self.pin_id = pin_id
        GPIO.setup(self.pin_id, GPIO.IN, pull_up_down=pull_up_down)
        GPIO.add_event_detect(self.pin_id, edge, callback=pin_callback, bouncetime=200)

# 按钮
class Button(Switch):
    def __init__(self, pin_id, pin_callback):
        super().__init__(pin_id, pin_callback)

# 彩色按钮
class ColorButton(Switch):
    def __init__(self, pin_id, pin_callback):
        super().__init__(pin_id, pin_callback, edge = GPIO.RISING, pull_up_down = GPIO.PUD_DOWN)

# 震动开关
class Vibration(Switch):
    def __init__(self, pin_id, pin_callback):
        super().__init__(pin_id, pin_callback)

# U型光电开关
class UInterrupter(Switch):
    def __init__(self, pin_id, pin_callback):
        super().__init__(pin_id, pin_callback)

# 干簧管开关
class Reed(Switch):
    def __init__(self, pin_id, pin_callback):
        super().__init__(pin_id, pin_callback, edge = GPIO.BOTH)

# 光敏电阻传感器
class Photoresistor(Switch):
    def __init__(self, pin_id, pin_callback):
        super().__init__(pin_id, pin_callback, edge = GPIO.BOTH)

# 火焰传感器
class Flame(Switch):
    def __init__(self, pin_id, pin_callback):
        super().__init__(pin_id, pin_callback, edge = GPIO.BOTH)

# 红外避障传感器
class IRObstacle():
    def __init__(self, pin_id):
        self.pin_id = pin_id
        GPIO.setup(self.pin_id, GPIO.IN)

    def input(self):
        return GPIO.input(self.pin_id)
    
    def detect(self):
        return GPIO.input(self.pin_id) == 0

# 超声波距离传感器
class Ultrasonic():
    def __init__(self, pin_trig_id, pin_echo_id):
        self.pin_trig_id = pin_trig_id
        self.pin_echo_id = pin_echo_id
        GPIO.setup(pin_trig_id, GPIO.OUT)
        GPIO.setup(pin_echo_id, GPIO.IN)

    def disMeasure(self):

        GPIO.output(self.pin_trig_id, 0)
        time.sleep(0.000002)

        GPIO.output(self.pin_trig_id, 1)
        time.sleep(0.00001)
        GPIO.output(self.pin_trig_id, 0)

        
        while GPIO.input(self.pin_echo_id) == 0:
            us_a = 0
        us_time1 = time.time()
        while GPIO.input(self.pin_echo_id) == 1:
            us_a = 1
        us_time2 = time.time()

        us_during = us_time2 - us_time1

        return us_during * 340 / 2 * 100

# 温度传感器
class Temperature:           
    def __init__(self):
        self.ds18b20 = ''  # ds18b20 设备
        for i in os.listdir('/sys/bus/w1/devices'):
            if i != 'w1_bus_master1':
                self.ds18b20 = i       # ds18b20存放在ds18b20地址
        self.init_temper = self.get_temper()
        # print(self.init_temper)

    # 读取ds18b20地址数据
    def get_temper(self):
        location = '/sys/bus/w1/devices/' + self.ds18b20 + '/w1_slave' # 保存ds18b20地址信息
        tfile = open(location)  # 打开ds18b20 
        text = tfile.read()     # 读取到温度值
        tfile.close()                    # 关闭读取
        secondline = text.split("\n")[1] # 格式化处理
        temperaturedata = secondline.split(" ")[9]# 获取温度数据
        temperature = float(temperaturedata[2:])  # 去掉前两位
        temperature = temperature / 1000          # 去掉小数点
        return temperature                        # 返回温度值
    
    def get_init_temper(self):
        return self.init_temper
    
    def hot(self):
        temper = self.get_temper()
        if temper is not None and temper > self.init_temper:
            return True
        return False

def test_ir(pin_id):
    GPIO.setmode(GPIO.BOARD)
    ir = IRObstacle(pin_id=pin_id)
    try:
        while True:
            print(GPIO.input(pin_id))
            ir.detect()
            time.sleep(0.2)
    except KeyboardInterrupt:
        pass
    
def test_us(pin_t_id, pin_e_id):
    GPIO.setmode(GPIO.BOARD)
    ir = Ultrasonic(pin_t_id, pin_e_id)
    try:
        while True:
            print(ir.disMeasure())
            time.sleep(0.2)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__': 
    
    # test_ir(GPIO_17)
    # test_ir(GPIO_21)
    test_us(GPIO_16, GPIO_20)


    # try:
    #     while True:
    #         time.sleep(0.2)
    # except KeyboardInterrupt:

    # GPIO.setmode(GPIO.BOARD)
    # GPIO.setwarnings(False)
    # GPIO.setup(11, GPIO.IN, pull_up_down= GPIO.PUD_UP)
    # while True:
    #     print(GPIO.input(11))
    #     time.sleep(0.5)
    #     pass

