import sys
import pigpio
import time
from termcolor import colored
from enum import Enum

# pins for switching screens
usb_switch = 11
left_switch = 4
right_switch = 22

# pins for readout leds
readout_usb_mac = 13
readout_usb_desktop = 6
readout_left_mac = 20
readout_left_desktop = 16
readout_right_mac = 26
readout_right_desktop = 19
readout_status = 12

# pins for checking which screens are currently active
usb_check_mac = 9
usb_check_desktop = 10
left_check_mac = 2
left_check_desktop = 3
right_check_mac = 17
right_check_desktop = 27

class Mode(Enum):
    any = 0
    mac = 1
    desktop = 2

def print_status(status):
    print(colored('Screen Switcher:', 'light_blue', attrs=['bold']), status)

def command_not_recognized():
    print_status(colored('Command not recognized.', 'red'))

# init pigpio
pi = pigpio.pi()

# class to store and initialize GPIO pins for a switch
class Switch:
    def __init__(self, name, switching_pin, mac_status_pin, desktop_status_pin, readout_mac, readout_desktop):
        self.name = name
        self.mode = Mode.desktop
        self.switching_pin = switching_pin
        self.mac_status_pin = mac_status_pin
        self.desktop_status_pin = desktop_status_pin
        self.readout_mac = readout_mac
        self.readout_desktop = readout_desktop
        self.init_GPIO()

    def init_GPIO(self):
        pi.set_mode(self.switching_pin, pigpio.OUTPUT)
        pi.set_mode(self.mac_status_pin, pigpio.INPUT)
        pi.set_pull_up_down(self.mac_status_pin,pigpio.PUD_DOWN)
        pi.set_mode(self.desktop_status_pin, pigpio.INPUT)
        pi.set_pull_up_down(self.desktop_status_pin,pigpio.PUD_DOWN)
        pi.set_mode(self.readout_mac, pigpio.OUTPUT)
        pi.set_mode(self.readout_desktop, pigpio.OUTPUT)

    def switch(self, mode):
        self.get_current_pin_statuses()
        time.sleep(0.5)
        if mode == mode.mac:
            if self.mode != Mode.mac:
                print_status(self.name + " to mac")
                self.set_switching_pin()
                self.mode = Mode.mac
        elif mode == mode.desktop:
            if self.mode != Mode.desktop:
                print_status(self.name + " to desktop")
                self.set_switching_pin()
                self.mode = Mode.desktop
        elif mode == Mode.any:
            print_status(self.name + " switching")
            if self.mode == Mode.mac: self.mode = Mode.desktop
            elif self.mode == Mode.desktop: self.mode = Mode.mac
            self.set_switching_pin()
            time.sleep(0.1)

    def set_switching_pin(self):
        pi.write(self.switching_pin,1)
        time.sleep(0.1)
        pi.write(self.switching_pin,0)

    def get_current_pin_statuses(self):
        if(pi.read(self.mac_status_pin)):
            self.mode = Mode.mac
        elif(pi.read(self.desktop_status_pin)):
            self.mode = Mode.desktop

    def print_status(self):
        if(self.mode == Mode.mac):
            print_status(self.name + ": " + "mac")
        else:
            print_status(self.name + ": " + "desktop")

    def blank_readout(self):
        pi.write(self.readout_desktop,0) 
        pi.write(self.readout_mac,0)

    def set_readout(self):
        pi.write(self.readout_mac,self.mode == Mode.mac)
        pi.write(self.readout_desktop,self.mode == Mode.desktop) 

    def __str__(self):
        return self.name + ": mac status: " + str(self.mode == Mode.mac) + " desktop status: " + str(self.mode == Mode.desktop)

# container to store all the switches
class Switches:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.switches = [self.usb,self.left,self.right]

    def switch_all(self):
        print_status("Switching screens.")
        for switch in self.switches:
            switch.switch(Mode.any)

    def set_mac(self):
        print_status("Switching to mac.")
        for switch in self.switches:
            switch.switch(Mode.mac)

    def set_desktop(self):
        print_status("Switching to desktop.")
        for switch in self.switches:
            switch.switch(Mode.desktop)

    def get_pin_status(self):
        for switch in self.switches:
            switch.print_status()

# define switches
usb = Switch('usb', usb_switch, usb_check_mac, usb_check_desktop, readout_usb_mac, readout_usb_desktop)
left = Switch('left', left_switch, left_check_mac, left_check_desktop, readout_left_mac, readout_left_desktop)
right = Switch('right', right_switch, right_check_mac, right_check_desktop, readout_right_mac, readout_right_desktop)
switches = Switches(usb=usb,left=left,right=right)

for switch in switches.switches:
    switch.get_current_pin_statuses()

# check for input parameters
if len(sys.argv)==1:
    switches.switch_all()
    for switch in switches.switches:
        switch.blank_readout()
        switch.set_readout()

elif len(sys.argv) == 2:
    if sys.argv[1] == 'mac': switches.set_mac()
    elif sys.argv[1] == 'desktop': switches.set_desktop() 
    elif sys.argv[1] == 'status': switches.get_pin_status()
    else: command_not_recognized()
    for switch in switches.switches:
        switch.blank_readout()
        switch.set_readout()

elif len(sys.argv) == 3:
    if sys.argv[1] == 'usb':
        if sys.argv[2] == 'mac': switches.usb.switch(Mode.mac)
        elif sys.argv[2] == 'desktop': switches.usb.switch(Mode.desktop)
        else: command_not_recognized()
        switches.usb.blank_readout()
        switches.usb.set_readout()

    elif sys.argv[1] == 'left':
        if sys.argv[2] == 'mac': switches.left.switch(Mode.mac)
        elif sys.argv[2] == 'desktop': switches.left.switch(Mode.desktop)
        else: command_not_recognized()
        switches.left.blank_readout()
        switches.left.set_readout()

    elif sys.argv[1] == 'right':
        if sys.argv[2] == 'mac': switches.right.switch(Mode.mac)
        elif sys.argv[2] == 'desktop': switches.right.switch(Mode.desktop)
        else: command_not_recognized() 
        switches.right.blank_readout()
        switches.right.set_readout()
    else: command_not_recognized()
else: command_not_recognized()



pi.write(readout_status,1)
