# Hold variable classes for FSM
# Created by: Amberley Powell
# Date Created: 3/28/2019
# Last modified by:
# Date last modified:
# Notes:

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

class motor(object):
    # Holds attribute information for all motor objects

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
    # All brake pads on pod

    def __init__(self, addr, temp=0):
        self.i = i
        self.v = v
        self.temp = temp

    def get_temp(self):
        pass

class wheel(object):
    # just for tracking RPM

    def __init__(self,addr,rpm=0):
        self.rpm = rpm

class contractor(object):
    # need more info on this
    def __init__(self, addr, placeholder=0):
        self.placeholder = placeholder
