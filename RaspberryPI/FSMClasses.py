# Hold variable classes for FSM
# Created by: Amberley Powell
# Date Created: 3/28/2019
# Last modified by:
# Date last modified:
# Notes:
import sys
sys.path.append('../')
import HealthMCU

state_dict = {"start_up" : 1,
              "system_diagnostic" : 2,
              "safe_to_approach" : 3,
              "prepare_to_launch" : 4,
              "ready_to_launch" : 5,
              "launching" : 6,
              "coasting" : 7,
              "braking" : 8,
              "full_stop" : 9,
              "crawling" : 10,
              "power_off" : 11,
              "fault" : 0,
              "fault_braking" : 12,
              "fault_stop" : 13,
              "fault_diagnostic" : 14,
              "purgatory" : 15}

# Used for the relay
relayAddr = 0
# The relay code assumes our motors are on relays 1-6, 7 unused
bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
msg = can.Messages(arbitration_id=0x000, data=[0], extended_id=False)
bus.send(msg)

class motor(object):
    # Holds attribute information for all motor objects

    def __init__(self, addr, i=0, v=0, temp=0):
        self.i = i
        self.v = HealthMCU.get_motor_voltage()
        self.temp = temp

    def power_on(self):

        pass

    def get_current(self):
        pass

    def get_voltage(self):
        pass

    def get_temp(self):
        pass

    def power_on_check(self):
        pass

    def power_off(self):
        pass

class battery(object):
    # Holds attribute information for all battery objects

    def __init__(self, addr, i=0, v=0, temp=0):
        self.i = i
        self.v = v
        self.temp = temp

    def get_current(self):
        pass

    def get_voltage(self):
        pass

    def get_temp(self):
        pass

class brake(object):
    # All brake pads on pod (12?)

    def __init__(self, addr, temp=0):
        self.i = i
        self.v = v
        self.temp = self.get_temp()

    def get_temp(self):
        interupt_test.get_break_tempurature()
        return

class wheel(object):
    # just for tracking RPM

    def __init__(self,addr,rpm=0):
        self.rpm = self.get_rpm()

    def get_rpm(self):
        return get_rpm() # placeholder function

class contractor(object):
    # need more info on this
    def __init__(self, addr, placeholder=0):
        self.placeholder = placeholder
