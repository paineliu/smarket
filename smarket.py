import RPi.GPIO as GPIO
from switch import *
from indicator import *
from audio import play_sound

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

PIN_BUTTON_ID = 11
PIN_LED_RED_ID = 12
PIN_LED_GREEN_ID = 13
	
def smarket_setup():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)

def smarket_switch_callback(chn):
    print(chn)
    if chn == PIN_BUTTON_ID:
        g_led_rg.turn()
        g_beep.turn()
        g_led_la.turn()
        # play_sound("./wav/alert_fire.wav")

def smarket_main():
	global g_led_rg
	global g_led_la
	global g_beep 
	
	g_led_la = Led(GPIO_5)
	g_beep = Beep(GPIO_12)
	g_led_rg = LedRG(PIN_LED_RED_ID, PIN_LED_GREEN_ID)

	Vibration(GPIO_20, smarket_switch_callback)
	UInterrupter(GPIO_20, smarket_switch_callback)
	Switch(PIN_BUTTON_ID, smarket_switch_callback)
	
	while True:
		pass
	
def smarket_clean():
	g_led_la.off()
	g_led_rg.off()
	GPIO.cleanup()


if __name__ == '__main__': 
	smarket_setup()
	try:
		smarket_main()
	except KeyboardInterrupt:
		smarket_clean() 
