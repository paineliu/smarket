import RPi.GPIO as GPIO
from sensor import *
from audio import Audio
from asr import ASR
from tts import TTS
from tts_baidu import TTSBaidu
from product import Product
from user import User
from strock import Stock
from datetime import datetime

GPIO_4 = 7
GPIO_5 = 29
GPIO_6 = 31
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

PIN_ID_IRO_ENTER = GPIO_17
PIN_ID_BTN_BUY_1 = GPIO_27
PIN_ID_BTN_BUY_2 = GPIO_22 
PIN_ID_UIRP_PAY  = GPIO_5
PIN_ID_FAN_AIR   = GPIO_6
PIN_ID_LED_GREEN = GPIO_13
PIN_ID_LED_RED = GPIO_19
PIN_ID_FlAME = GPIO_26

PIN_ID_MOTOR = GPIO_12
PIN_ID_USONIC_T = GPIO_16
PIN_ID_USONIC_E = GPIO_20
PIN_ID_IRO_EXIT = GPIO_21

PIN_ID_BIZZER    = GPIO_23
PIN_ID_LED_COLOR = GPIO_24
PIN_ID_BTN_RESET = GPIO_25

ACT_ENTER = 1
ACT_EXIT = 2
ACT_FAN_ON = 3
ACT_FAN_OFF = 4
ACT_FIND_COLA = 11


class SMarket:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

    def start(self, gpio_callback):
        self.asr = ASR(0x79)
        self.temper = Temperature()
        self.ir_enter = IRObstacle(PIN_ID_IRO_ENTER)   # 进入
        self.buy_cola = UInterrupter(PIN_ID_BTN_BUY_1, gpio_callback) # 买可乐
        self.buy_milk = ColorButton(PIN_ID_BTN_BUY_2, gpio_callback) # 买牛奶
        self.pay = Reed(PIN_ID_UIRP_PAY, gpio_callback) # 付款
        self.ir_exit = IRObstacle(PIN_ID_IRO_EXIT)     # 离开
        self.fan = Fan(PIN_ID_FAN_AIR)
        self.us_forbid = Ultrasonic(PIN_ID_USONIC_T, PIN_ID_USONIC_E) # 禁区
        
        self.red_light = Led(PIN_ID_LED_RED)
        self.green_light = Led(PIN_ID_LED_GREEN)
        
        self.flame = Flame(PIN_ID_FlAME, gpio_callback)
        self.motor = Laser(PIN_ID_MOTOR)
        
        self.reset = ColorButton(PIN_ID_BTN_RESET, gpio_callback)
        self.color_light = Led(PIN_ID_LED_COLOR)
        self.bizzer = Bizzer(PIN_ID_BIZZER)

        print("\nStart completed.")

    def detect(self, detect_callback):
        asr_id = self.asr.getResult()
        # print('asr', time.time(), asr_id)
        print('dis', self.us_forbid.disMeasure())
        if (self.temper.hot()):
            detect_callback(ACT_FAN_ON)
        else:
            detect_callback(ACT_FAN_OFF)

        if (asr_id == 5):
            detect_callback(ACT_FIND_COLA)

        if (self.ir_enter.detect()):
            detect_callback(ACT_ENTER)
        if (self.ir_exit.detect()):
            detect_callback(ACT_EXIT)

    def fan_is_on(self):
        return self.fan.is_on()
    
    def fan_on(self):
        self.fan.on()

    def fan_off(self):
        self.fan.off()

    def flame_is_on(self):
        return self.red_light.is_on()
    
    def flame_on(self):
        self.red_light.on()
        self.color_light.on()

    def flame_off(self):
        self.red_light.off()
        self.color_light.off()

    def reset_all(self):
        if self.fan_is_on():
            self.fan_off()
        if self.flame_is_on():
            self.flame_off()

    def clean(self):
        GPIO.cleanup()    

g_tts = TTSBaidu()
g_audio = Audio()
g_user = User()
g_stock = Stock()
g_smarket = SMarket()

def smarket_detect_callback(act_id):
    print('[{}] act={} temp={}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], act_id, g_smarket.temper.read()))
    
    if (act_id == ACT_FAN_ON):
        if (not g_smarket.fan_is_on()):
            g_smarket.fan_on()

    if (act_id == ACT_FAN_OFF):
        if (g_smarket.fan_is_on()):
            g_smarket.fan_off()

    if (act_id == ACT_ENTER):
        if (g_user.get_status() != User.ENTER):
            g_user.enter()
            g_audio.play('./wav/welcome.wav')
    if (act_id == ACT_EXIT):
        if (g_user.need_pay()):
            g_tts.say('你还没有付款，请不要离开')
        else:
            if (g_user.get_status() == User.ENTER):
                g_user.leave()
                g_audio.play('./wav/bye.wav')
    if act_id == ACT_FIND_COLA:
        g_audio.play('./wav/find_cola.wav')


def smarket_gpio_callback(pin_id):
    print('[{}] pin={}, val={}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], pin_id, GPIO.input(pin_id)))

    if (pin_id == PIN_ID_BTN_RESET):
        # if (g_smarket.color_light.is_on()):
        #     g_smarket.color_light.off()
        #     g_smarket.motor.off()
        # else:
        g_smarket.green_light.on()
        g_smarket.color_light.on()
        g_smarket.motor.on()
        g_smarket.bizzer.on()
        

    if (pin_id == PIN_ID_FlAME):
        if (not g_smarket.flame_is_on()):
            g_tts.say('检测到火情，请迅速撤离')
            g_smarket.flame_on()

    if (pin_id == PIN_ID_UIRP_PAY):
        if (GPIO.input(pin_id) == 0):
            if (g_user.need_pay()):
                message = '你买了'

                user_cola_total = g_user.get_total(Product.COLA)
                if (user_cola_total > 0):
                    message += '{}瓶可乐，'.format(user_cola_total)

                user_milk_total = g_user.get_total(Product.MILK)
                if (user_milk_total > 0):
                    message += '{}瓶牛奶，'.format(user_milk_total)
                message += '已经完成付款'
                g_tts.say(message)
                g_user.pay()
            else:
                g_tts.say('你没有购买商品，随便买点吧')
        
    if (pin_id == PIN_ID_BTN_BUY_1):
        if (GPIO.input(pin_id) == 1):
            product_id = Product.COLA
            if g_stock.get_total(product_id) > 0:
                g_stock.sell(product_id)
                g_user.buy(product_id)
                if g_stock.get_total(product_id) > 0:
                    g_tts.say('你买了{}瓶可乐，库存还有{}瓶'.format(g_user.get_total(product_id), g_stock.get_total(product_id)))
                else:
                    g_tts.say('你买了{}瓶可乐，已经没有库存了'.format(g_user.get_total(product_id)))
            else:
                g_tts.say('可乐卖光了，下次再来吧')

    if (pin_id == PIN_ID_BTN_BUY_2):
        if (GPIO.input(pin_id) == 1):
            product_id = Product.MILK
            if g_stock.get_total(product_id) > 0:
                g_stock.sell(product_id)
                g_user.buy(product_id)
                if g_stock.get_total(product_id) > 0:
                    g_tts.say('你买了{}瓶牛奶，库存还有{}瓶'.format(g_user.get_total(product_id), g_stock.get_total(product_id)))
                else:
                    g_tts.say('你买了{}瓶牛奶，已经没有库存了'.format(g_user.get_total(product_id)))
            else:
                g_tts.say('牛奶卖光了，下次再来吧')


def smarket_main():
    g_smarket.start(smarket_gpio_callback)
    try:
        while True:
            g_smarket.detect(smarket_detect_callback)
            time.sleep(0.2)
    except KeyboardInterrupt:
        g_smarket.clean()

if __name__ == '__main__': 
    smarket_main()
