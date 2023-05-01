import sys
import RPi.GPIO as GPIO
import time
from termcolor import colored

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# set pins for switching screens
usb_switch = 2
left_switch = 3
right_switch = 4

GPIO.setup(usb_switch, GPIO.OUT)
GPIO.setup(left_switch, GPIO.OUT)
GPIO.setup(right_switch, GPIO.OUT)

# set pins for checking which screens are currently active
usb_check_mac = 27
usb_check_desktop = 17
left_check_mac = 10
left_check_desktop = 22
right_check_mac = 11
right_check_desktop = 9

# class to store and initialize GPIO pins for a switch
class Switch:
    def __init__(self, name, switching_pin, mac_status_pin, desktop_status_pin):
        self.name = name
        self.switching_pin = switching_pin
        self.mac_status_pin = mac_status_pin
        self.desktop_status_pin = desktop_status_pin
        self.init_GPIO()

    def init_GPIO(self):
        GPIO.setup(self.switching_pin, GPIO.OUT)
        GPIO.setup(self.mac_status_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.desktop_status_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def switch(self):
        GPIO.output(self.switching_pin,True)
        # GPIO readout seems to not work unless this delay is added
        time.sleep(0.1)
        self.reset()
    
    def reset(self):
        GPIO.output(self.switching_pin,False)

    def is_mac(self):
        return GPIO.input(self.mac_status_pin)
    
    def is_desktop(self):
        return GPIO.input(self.desktop_status_pin)

    def set_mac(self):
        if not self.is_mac(): self.switch()

    def set_desktop(self):
        if not self.is_desktop(): self.switch()
    
    def __str__(self):
        return self.name + ": mac status: " + str(self.is_mac()) + " desktop status: " + str(self.is_desktop())


# container to store all the switches
class Switches:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.switches = [self.usb,self.left,self.right]

    def switch_all(self):
        for switch in self.switches:
            switch.switch()   

    def set_mac(self):
        for switch in self.switches:
            switch.set_mac()
    
    def set_desktop(self):
        for switch in self.switches:
            switch.set_desktop()

# define switches
usb = Switch('usb', usb_switch, usb_check_mac, usb_check_desktop)
left = Switch('left', left_switch, left_check_mac, left_check_desktop)
right = Switch('right', right_switch, right_check_mac, right_check_desktop)
switches = Switches(usb=usb,left=left,right=right)

def print_status(status):
    print(colored('Screen Switcher:', 'light_blue', attrs=['bold']), status)

def command_not_recognized():
    print_status(colored('Command not recognized.', 'red'))

# check for input parameters
if len(sys.argv)==1: switches.switch_all()

elif len(sys.argv) == 2:
    if sys.argv[1] == 'mac': switches.set_mac()
    elif sys.argv[1] == 'desktop': switches.set_desktop() 
    else: command_not_recognized()

elif len(sys.argv) == 3:
    if sys.argv[1] == 'usb':
        if sys.argv[2] == 'mac': switches.usb.set_mac()
        elif sys.argv[2] == 'desktop': switches.usb.set_desktop()
        else: command_not_recognized()

    elif sys.argv[1] == 'left':
        if sys.argv[2] == 'mac': switches.left.set_mac()
        elif sys.argv[2] == 'desktop': switches.left.set_desktop()
        else: command_not_recognized()

    elif sys.argv[1] == 'right':
        if sys.argv[2] == 'mac': switches.right.set_mac()
        elif sys.argv[2] == 'desktop': switches.right.set_desktop()
        else: command_not_recognized() 
    else: command_not_recognized()
else: command_not_recognized()