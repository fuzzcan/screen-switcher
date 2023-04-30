print('switching screens')

import sys
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# set pins for switching screens
usb_switch = 2
dp_left_switch = 3
dp_right_switch = 4

GPIO.setup(usb_switch, GPIO.OUT)
GPIO.setup(dp_left_switch, GPIO.OUT)
GPIO.setup(dp_right_switch, GPIO.OUT)

# set pins for checking which screens are currently active
usb_check_desktop = 17
usb_check_mac = 27
dp_left_check_desktop = 22
dp_left_check_mac = 10
dp_right_check_desktop = 9
dp_right_check_mac = 11

GPIO.setup(usb_check_desktop, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(usb_check_mac, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dp_left_check_desktop, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dp_left_check_mac, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dp_right_check_desktop, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dp_right_check_mac, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# check for input parameters
if len(sys.argv)==0:
    switch_all()

elif len(sys.argv) == 1:
    elif sys.argv[0] == 'mac':
        if not usb_check_mac:
            GPIO.output(usb_switch,True)
        if not dp_left_check_mac:
            GPIO.output(dp_left_switch,True)
        if not dp_right_check_mac:
            GPIO.output(dp_right_switch,True)
            
    elif sys.argv[0] == 'desktop':
        if not usb_check_desktop:
            GPIO.output(usb_switch,True)
        if not dp_left_check_desktop:
            GPIO.output(dp_left_switch,True)
        if not dp_right_check_desktop:
            GPIO.output(dp_right_switch,True)

elif len(sys.argv) == 2:
    if sys.argv[0] == 'usb':
        if sys.argv[1] == 'mac':
            if not usb_check_mac:
            GPIO.output(usb_switch,True)
        elif sys.argv[1] == 'desktop':
            if not usb_check_desktop:
            GPIO.output(usb_switch,True)
        else:
            command_not_recognized()

    elif sys.argv[0] == 'left':
        if sys.argv[1] == 'mac':
            if not dp_left_check_mac:
                GPIO.output(dp_left_switch,True)
        elif sys.argv[1] == 'desktop':
            if not dp_left_check_desktop:
                GPIO.output(dp_right_switch,True)
        else:
            command_not_recognized()

    elif sys.argv[0] == 'right':
        if sys.argv[1] == 'mac':
            if not dp_right_check_mac:
                GPIO.output(dp_left_switch,True)
        elif sys.argv[1] == 'desktop':
            if not dp_right_check_desktop:
                GPIO.output(dp_right_switch,True)
        else:
            command_not_recognized()

    elif sys.argv[0] == 'mac' and sys.argv[1] == 'desktop':
        if not dp_left_check_mac:
            GPIO.output(dp_left_switch,True)
        if not dp_right_check_desktop:
                GPIO.output(dp_right_switch,True)
    
    elif sys.argv[0] == 'desktop' and sys.argv[1] == 'mac':
        if not dp_right_check_mac:
                GPIO.output(dp_left_switch,True)
        if not dp_left_check_desktop:
                GPIO.output(dp_right_switch,True)

time.sleep(.1)
reset_pins()

if GPIO.input(usb_check_desktop):
        print('usb is connected to desktop')

if GPIO.input(usb_check_mac):
        print('usb is connected to mac')

if GPIO.input(dp_left_check_desktop):
        print('dp_left is connected to desktop')

if GPIO.input(dp_left_check_mac):
        print('dp_left is connected to mac')

if GPIO.input(dp_right_check_desktop):
        print('dp_right is connected to desktop')

if GPIO.input(dp_right_check_mac):
        print('dp_right is connected to mac')

def switch_all():
    GPIO.output(usb_switch,True)
    GPIO.output(dp_left_switch,True)
    GPIO.output(dp_right_switch,True)
    

def reset_pins():
    GPIO.output(usb_switch,False)
    GPIO.output(dp_left_switch,False)
    GPIO.output(dp_right_switch,False)
    time.sleep(.5)

def command_not_recognized():
    print('Screen Switcher: Command not recognized.')