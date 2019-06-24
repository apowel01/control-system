#### The FSM for the Raspberry Pi Control System ####
import FSMClasses as FSM
from FSMConfig import config
from time import sleep
import can
import health
# import brakes
# import motors

# let the pod coast
def coast():
    pass

# power on the pod systems into start up state
def initialize_pod():
    # check communication with vital sensors and MCUs
    print("TODO: Check sensor readings")
    print("TODO: Check MCU statuses")
    print("TODO: Initialize & create motor objects")
    print("TODO: Initialize & create brake objects")
    # motors.create_motors()     # create motors
    # brakes.create_brakes()     # create brake objects
    # TODO: initialize other peripherals
    print("I have initalized")

# power off protocol
def power_off():
    print("I am powering off")
    # power off stuff
    # CAN bus ID 0x000 should kill power to all nodes??
    motors.motors_off()

# determines if pod is safe to approach
def safe_to_approach_check():
    print("I am checking if I am safe to apprach")
    # by default, safe to approach is false
    SAFE_TO_APPROACH = False
    # TODO: velocity test

    # TODO: power to motor test

    # TODO: power to brakes test

    return SAFE_TO_APPROACH

# Main state machine
def main():
    state = FSM.states["start_up"] # start in start_up state
    fault = False # initally not in a fault state

    while state != FSM.states["fault"]: # check for fault state transition
        # START UP STATE
        if state == FSM.states["start_up"]:
            print("****START UP****")
            initialize_pod() # power on sequence
            state = FSM.states["system_diagnostic"] # always move to system diagnositc state from start up

        # SYSTEM DIAGNOSTIC
        elif state == FSM.states["system_diagnostic"]:
            print("****SYSTEM DIAGNOSTIC****")
            if health.safe_to_approach_check() == True:
                state = FSM.states["safe_to_approach"]
            else: # if not safe to approach, move to fault state
                fault = True
                state = FSM.states["fault"]

        # SAFE TO APPROACH
        elif state == FSM.states["safe_to_approach"]:
            print("****SAFE TO APPROACH****")
            launch = input("Prepare to launch? (True/False) ") #TODO: connect to GUI
            if launch == "True":
                state = FSM.states["prepare_to_launch"]
            else:
                sleep(5) # wait 5s before looping
                state = FSM.states["safe_to_approach"]

        # PREPARE TO LAUNCH
        elif state == FSM.states["prepare_to_launch"]:
            print("****PREPARE TO LAUNCH****")
            # what do we do here?
            state = FSM.states["ready_to_launch"]

        elif state == FSM.states["ready_to_launch"]:
            print("****READY TO LAUNCH****")
            ready_to_launch = input("Are you sure you want to launch? (True/False) ")
            if ready_to_launch == "True":
                state = FSM.states["launching"]
            else:
                state = FSM.states["system_diagnostic"]

        elif state == FSM.states["launching"]:
            print("****LAUNCHING****")
            while distance < FSMConfig.stop_distance: #TODO: add stop distance threshold
                accelerate()
            state = FSM.states["coasting"] # once we are done accelerating

        elif state == FSM.states["coasting"]:
            print("****COASTING****")
            motors_off() # cut power to motors
            brakes_off() # disengage brakes
            while distance <= coast_distance:
                # keep coasting
                coast()

        elif state == FSM.states["braking"]:
            print("****BRAKING****")
            brakes_full_stop()
            if velocity == 0:
                state = FSM.states["safe_to_approach"]
            else:
                fault = True
                state = FSM.states["fault"]

        elif state == FSM.states["crawling"]:
            print("****CRAWLING****")
            pass

        elif state == FSM.states["power_off"]:
            print("****POWER OFF****")
            power_off()
            pass

        else:
            state = FSM.states["fault"] # should never reach this state

    else:
        while fault == True:
            if state == FSM.states["fault_braking"]:
                # if fault_braking_done ==
                brakes_full_stop()
                if velocity == 0:
                    state = FSM.states["fault_stop"]
                else:
                    state = FSM.states["fault_braking"]

            elif state == FSM.states["fault_stop"]:
                pass

            elif state == FSM.states["fault_diagnostic"]:
                print("FAULT: I have entered a FAULT state")

            elif state == FSM.states["fault_diagnostic"]:
                print("FAULT: I have entered a FAULT state")

        if velocity != 0:
            #is it safe to stop
            # if moving, determine whether to stop or not
            # if not moving, try to reach safe to approach conditions
            #   determing whether problem is with brakes
            #   if problem is not brakes, apply brakes
            print("I think I am moving")
        elif config["velocity"] == 0:
            # attempt to reach safe to approach conditions
            print("FAULT: but at least I'm not moving")
        else:
            state = FSM.states["fault_diagnostic"]
    # end eventually, please
    loop += 1
    print("Loop count: {}".format(loop))
    if loop >= 100:
        sys.exit()

# main()