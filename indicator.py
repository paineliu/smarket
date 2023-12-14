import RPi.GPIO as GPIO

class Indicator:
    def __init__(self, pin_id, on_val = 1, off_val = 0):
        self.on_val = on_val
        self.off_val = off_val
        self.pin_id = pin_id
        self.is_on = False
        GPIO.setup(self.pin_id, GPIO.OUT)
        self.off()

    def on(self):
        self.is_on = True
        GPIO.output(self.pin_id, self.on_val)
    
    def off(self):
        self.is_on = False
        GPIO.output(self.pin_id, self.off_val)

    def turn(self):
        if (self.is_on):
            self.off()
        else:
            self.on()

class Led(Indicator):
    def __init__(self,pin_id):
        super().__init__(pin_id)

class Beep(Indicator):
    def __init__(self,pin_id):
        super().__init__(pin_id, on_val=0, off_val=1)
    

# G (S)
# R 
# GND
 
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
            self.red()
