import time
import RPi.GPIO as GPIO

class Switch:
    def __init__(self, pin_id, button_callback, pull_up_down=GPIO.PUD_UP):
        self.pin_id = pin_id
        GPIO.setup(self.pin_id, GPIO.IN, pull_up_down=pull_up_down)
        GPIO.add_event_detect(self.pin_id, GPIO.BOTH, callback=button_callback, bouncetime=200)

class Button(Switch):
    def __init__(self,pin_id, button_callback):
        super().__init__(pin_id, button_callback)

class Vibration(Switch):
    def __init__(self,pin_id, button_callback):
        super().__init__(pin_id, button_callback)

class UInterrupter(Switch):
    def __init__(self,pin_id, button_callback):
        super().__init__(pin_id, button_callback)

class Reed(Switch):
    def __init__(self,pin_id, button_callback):
        super().__init__(pin_id, button_callback)

class ColorButton(Switch):
    def __init__(self,pin_id, button_callback):
        super().__init__(pin_id, button_callback, pull_up_down = GPIO.PUD_DOWN)

def smarket_switch_callback(chn):
    print(chn)

if __name__ == '__main__': 
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(11, GPIO.IN, pull_up_down= GPIO.PUD_UP)
    while True:
        print(GPIO.input(11))
        time.sleep(0.5)
        pass

