import RPi.GPIO as GPIO
from pynput import keyboard
from sensor import *
from asr import ASR
from tts_baidu import TTSBaidu

from product import Product
from user import User
from store import Store
from datetime import datetime


ACT_ENTER   = 1
ACT_EXIT    = 2

ACT_FAN_ON  = 3
ACT_FAN_OFF = 4

ACT_FORBID_UNSAFE  = 5
ACT_FORBID_SAFE    = 6

ACT_FLAME_ON  = 7
ACT_FLAME_OFF = 8

ACT_HELLO = 10
ACT_FIND_COLA = 11
ACT_FIND_MILK = 12


class SMarket:
    def __init__(self):
        self.tts = TTSBaidu()
        self.user = User()
        self.store = Store()
        self.fan_state = ACT_FAN_OFF
        self.forbid_state = ACT_FORBID_SAFE
        self.flame_state = ACT_FLAME_OFF
        self.running = False
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        self.asr = ASR(0x79) # 语音模块
        self.temper = Temperature() # 温度检测
        self.ir_enter = IRObstacle(PIN_ID_IRO_ENTER)   # 进入
        self.ir_exit = IRObstacle(PIN_ID_IRO_EXIT)     # 离开
        self.us_forbid = Ultrasonic(PIN_ID_USONIC_T, PIN_ID_USONIC_E) # 禁区

        self.flame = Flame(PIN_ID_FlAME)  # 火情
        self.buy_cola = UInterrupter(PIN_ID_BTN_BUY_1) # 买可乐
        self.buy_milk = UInterrupter(PIN_ID_BTN_BUY_2) # 买酸奶
        self.pay_btn = Reed(PIN_ID_REED_PAY) # 付款
        self.reset = ColorButton(PIN_ID_BTN_RESET) # 复位

        self.fan = Fan(PIN_ID_FAN_AIR) # 风扇
        self.red_light = Led(PIN_ID_LED_RED) # 红灯
        self.green_light = Led(PIN_ID_LED_GREEN) # 绿灯
        self.laser = Laser(PIN_ID_LASER)
        self.color_light = Led(PIN_ID_LED_COLOR) # 彩灯
        self.bizzer = Bizzer(PIN_ID_BIZZER) # 蜂鸣器
        self.last_pay = 0
        self.last_buy_cola = 0
        self.last_buy_milk = 0
        self.last_reset = 0
        self.running = False

    def start(self, gpio_callback=None):
        self.running = True

    def pause(self):
        self.running = False

    def detect(self, detect_callback=None, show_info=False):
        if not self.running:
            return {}
        
        asr_id = self.asr.getResult()
        curr_temper = self.temper.get_temper()
        dis = self.us_forbid.disMeasure()
        enter = self.ir_enter.input()
        exit = self.ir_exit.input()
        flame = self.flame.input()
        pay = self.pay_btn.input()
        buy_cola = self.buy_cola.input()
        buy_milk = self.buy_milk.input()
        reset = self.reset.input()

        message = '[{}] asr={} cola={} milk={} pay={} temp={:.1f} flame={} enter={} exit={} dis={:.3f}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], asr_id, buy_cola, buy_milk, pay, curr_temper, flame, enter, exit, dis)

        state_map = {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], 
                     'asr': asr_id,
                     'buy_cola': buy_cola == 1,
                     'buy_milk': buy_milk == 1,
                     'pay': pay == 0,
                     'flame': flame == 0,
                     'enter':enter == 0,
                     'exit': exit == 0,
                     'temp': '{:.1f}'.format(curr_temper),
                     'dist': '{:.1f}'.format(dis),
                     'message': message
                     }
        
        if show_info:
            print(message)

        if (self.last_reset != reset):
            self.last_reset = reset
            if (reset == 1):
                self.reset_all()

        if (self.last_pay != pay):
            self.last_pay = pay
            if (pay == 0):
                self.pay()

        if (self.last_buy_cola != buy_cola):
            self.last_buy_cola = buy_cola
            if (buy_cola == 1):
                self.buy(Product.COLA)

        if (self.last_buy_milk != buy_milk):
            self.last_buy_milk = buy_milk
            if (buy_milk == 1):
                self.buy(Product.MILK)

        # 语音识别
        if (asr_id == self.asr.HELLO):
            self.hello()
            if detect_callback is not None:
                detect_callback(ACT_HELLO)
            pass
        elif (asr_id == self.asr.FIND_COLA):
            self.find(Product.COLA) 
            if detect_callback is not None:
                detect_callback(ACT_FIND_COLA)
        elif (asr_id == self.asr.FIND_MILK):
            self.find(Product.MILK) 
            if detect_callback is not None:
                detect_callback(ACT_FIND_MILK) 

        # 温度检测
        init_temper = self.temper.get_init_temper()
        if (curr_temper > init_temper + 1.0):
            self.temper.init_temper = curr_temper
            if not self.fan_state == ACT_FAN_ON:
                self.fan_state = ACT_FAN_ON
                self.fan_on()
                if detect_callback is not None:
                    detect_callback(ACT_FAN_ON, curr_temper)
        else:
            if not self.fan_state == ACT_FAN_OFF:
                self.fan_state = ACT_FAN_OFF
                self.fan_off()
                if detect_callback is not None:
                    detect_callback(ACT_FAN_OFF, curr_temper)

        # 进入检测
        if (enter == 0):
            self.user_enter()
            if detect_callback is not None:
                detect_callback(ACT_ENTER)

        # 离开检测
        if (exit == 0):
            self.user_leave()
            if detect_callback is not None:
                detect_callback(ACT_EXIT)

        if (flame == 0):
            if not self.flame_state == ACT_FLAME_ON:
                self.flame_state = ACT_FLAME_ON
                self.flame_on()
                if detect_callback is not None:
                    detect_callback(ACT_FLAME_ON)
        else:
            if self.flame_state == ACT_FLAME_ON:
                self.flame_state = ACT_FLAME_OFF
                self.flame_off()
                if detect_callback is not None:
                    detect_callback(ACT_FLAME_OFF)

        # 禁区检测
        if (dis < 8.0):
            if not self.forbid_state == ACT_FORBID_UNSAFE:
                self.forbid_state = ACT_FORBID_UNSAFE
                self.forbid_on()
                if detect_callback is not None:
                    detect_callback(ACT_FORBID_UNSAFE, dis)
        else:
            if not self.forbid_state == ACT_FORBID_SAFE:
                self.forbid_state = ACT_FORBID_SAFE
                self.forbid_off()
                if detect_callback is not None:
                    detect_callback(ACT_FORBID_SAFE, dis)

        return state_map

    def fan_is_on(self):
        return self.fan.is_on()
    
    def fan_on(self, play_voice=True):
        if not self.fan_is_on():
            if play_voice:
                self.tts.say('检测到室温过高，自动开启空调。')

            self.fan.on()

    def fan_off(self, play_voice=True):
        if self.fan_is_on():
            if play_voice:
                self.tts.say('室温恢复，关闭空调。')
            self.fan.off()

    def flame_is_on(self):
        return self.red_light.is_on()
    
    def flame_on(self, play_voice=True):
        if not self.flame_is_on():
            if play_voice:
                self.tts.say('检测到火情，请立即撤离。')
            self.red_light.on()

    def flame_off(self, play_voice=True):
        if self.flame_is_on():
            self.red_light.off()
            if play_voice:
                self.tts.say('火情解除。')

    def forbid_is_on(self):
        return self.bizzer.is_on()
    
    def forbid_on(self, play_voice=True):
        if (not self.forbid_is_on()):
            self.color_light.on()
            if play_voice:
                self.tts.say("检测到非法入侵。")
            self.bizzer.on()
        
    def forbid_off(self, play_voice=True):
        if (self.forbid_is_on()):
            self.bizzer.off()
            self.color_light.off()
            if play_voice:
                self.tts.say('禁区恢复安全。')

    def pay(self):
        if (self.user.need_pay()):
            message = '你买了，'

            user_cola_total = self.user.get_total(Product.COLA)
            if (user_cola_total > 0):
                message += '{}瓶可乐，'.format(user_cola_total)

            user_milk_total = self.user.get_total(Product.MILK)
            if (user_milk_total > 0):
                message += '{}瓶酸奶，'.format(user_milk_total)
            
            message += '总计{}元，已经完成付款。'.format(user_cola_total * 2 + user_milk_total * 1)
            self.tts.say(message)
            self.user.pay()
            self.red_light.off()
            self.laser.off()
        else:
            self.tts.say('你还没有购买商品，随便买点吧。')
            
    def find(self, product_id):
        
        if (product_id == Product.COLA):
            self.tts.say('可乐在西区，第二排货架。')
        if product_id == Product.MILK:
            self.tts.say('酸奶在币区，第一排货架。')

    def buy(self, product_id):
        if (product_id == Product.COLA):
            if self.store.get_total(product_id) > 0:
                self.store.sell(product_id)
                self.user.buy(product_id)
                if self.store.get_total(product_id) > 0:
                    self.tts.say('你买了{}瓶可乐，库存还有{}瓶。'.format(self.user.get_total(product_id), self.store.get_total(product_id)))
                else:
                    self.tts.say('你买了{}瓶可乐，已经没有库存了。'.format(self.user.get_total(product_id)))
            else:
                self.tts.say('可乐卖光了，下次再来吧。')
        if product_id == Product.MILK:
            if self.store.get_total(product_id) > 0:
                self.store.sell(product_id)
                self.user.buy(product_id)
                if self.store.get_total(product_id) > 0:
                    self.tts.say('你买了{}瓶酸奶，库存还有{}瓶。'.format(self.user.get_total(product_id), self.store.get_total(product_id)))
                else:
                    self.tts.say('你买了{}瓶酸奶，已经没有库存了。'.format(self.user.get_total(product_id)))
            else:
                self.tts.say('酸奶卖光了，下次再来吧。')

    def user_enter(self):
        if (self.user.get_status() != User.ENTER):
            self.user.enter()
            self.store.reset()
            self.tts.say('欢迎光临！')


    def user_leave(self):
        if (self.user.get_status() == User.ENTER):
            if (self.user.need_pay()):
                self.red_light.on()
                self.laser.on()
                self.tts.say('你还没有付款，请不要离开。')
            else:
                self.user.leave()
                self.tts.say('谢谢惠顾，欢迎下次光临！')

    def hello(self):
        self.tts.say('你好，我是购物助手，能为您做点什么？')

    def reset_all(self):
        self.fan_off(False)
        self.flame_off(False)
        self.store.reset()
        self.user.reset()
        self.tts.say('系统复位完成。')

    def is_running(self):
        return self.running
    
    def clean(self):
        self.running = False
        GPIO.cleanup()


def smarket_detect_callback(act_id, param = None):
    print('  act_id={}, param = {}'.format(act_id, param))
    
    # # 风扇打开
    # if (act_id == ACT_FAN_ON):
    #     g_smarket.fan_on()

    # # 风扇关闭
    # if (act_id == ACT_FAN_OFF):
    #     g_smarket.fan_off()

    # # 风扇打开
    # if (act_id == ACT_FLAME_ON):
    #     g_smarket.flame_on()

    # # 风扇关闭
    # if (act_id == ACT_FLAME_OFF):
    #     g_smarket.flame_off()

    # # 进门
    # if (act_id == ACT_ENTER):
    #     g_smarket.user_enter()

    # # 出门
    # if (act_id == ACT_EXIT):
    #     g_smarket.user_leave()

    # if act_id == ACT_HELLO:
    #     g_smarket.hello()

    # # 可乐在哪里
    # if act_id == ACT_FIND_COLA:
    #     g_smarket.find(Product.COLA)
        
    # # 酸奶在哪里
    # if act_id == ACT_FIND_MILK:
    #     g_smarket.find(Product.MILK)

    # # 禁区危险
    # if act_id == ACT_FORBID_UNSAFE:
    #     g_smarket.forbid_on()

    # # 禁区安全
    # if act_id == ACT_FORBID_SAFE:
    #     g_smarket.forbid_off()
            

# def smarket_gpio_callback(pin_id):
#     print('[{}] pin={}, val={}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], pin_id, GPIO.input(pin_id)))

#     if (pin_id == PIN_ID_BTN_RESET):
#         g_smarket.reset_all()       

#     if (pin_id == PIN_ID_REED_PAY):
#         if (GPIO.input(pin_id) == 0):
#             g_smarket.pay()
        
#     if (pin_id == PIN_ID_BTN_BUY_1):
#         if (GPIO.input(pin_id) == 1):
#             g_smarket.buy(Product.COLA)
            
#     if (pin_id == PIN_ID_BTN_BUY_2):
#         if (GPIO.input(pin_id) == 1):
#             g_smarket.buy(Product.MILK)
            
def smarket_main():

    def on_press(key):
        try:
            print('{}'.format(key.char))
            if (key.char == 'f'):
                g_smarket.fan_on()
            elif (key.char == 'g'):
                g_smarket.fan_off()

        except AttributeError:
            pass


    def on_release(key):
        pass
        # if key == keyboard.Key.esc:
        #     return False
    g_smarket = SMarket()
    g_smarket.start()
    listener = keyboard.Listener(
        on_press=on_press)

    listener.start()


    try:
        while True:
            g_smarket.detect(smarket_detect_callback, show_info=True)
            time.sleep(0.2)
    except KeyboardInterrupt:
        g_smarket.clean()

if __name__ == '__main__': 
    smarket_main()
