import RPi.GPIO as GPIO

class Switch:
    def __init__(self, pin_id, button_callback):
        self.pin_id = pin_id
        GPIO.setup(self.pin_id, GPIO.IN, pull_up_down=GPIO.PUD_UP)
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
