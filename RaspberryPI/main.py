import FSMClasses
from FSMConfig import config
from time import sleep
import sys
sys.path.append('../')
import interupt_test.ino
import HealthMCU
#### The FSM for the Raspberry Pi Control System ####
    # Author: Amberley Powell
    # Last edited by: Amberley Powell
    # Date created: ???
    # Date last edited: 4/27/2019

# power on the pod systems into start up state
def initialize():
    # check communication with VITAL sensors // MCUs
    print("I have initalized")
    return

# power off protocol
def power_off():
    print("I am powering off")

# determine if pod is safe to approach
def safe_to_approach_check():
    print("I am checking if I am safe to apprach")
    velocity = 0
    print("velocity = " + str(velocity))
    # velocity test
    if velocity == 0:
        return True
    else:
        fault = True
        state = state_dict["fault"]
        return False
    # power to motor test
#    for motor in motors:
###        else:
    #        return False

    # power to brakes test

# power off the motors
def motors_off():
    print("I am turning off power to the motors")
    motor1.off()
    motor2.off()
    motor3.off()
    motor4.off()
    motor5.off()
    motor6.off()

# disengage all brakes
def brakes_off():
    print("I am disengaging the brakes")
    brake1.disengage()
    brake2.disengage()
    brake3.disengage()
    brake4.disengage()
    brake5.disengage()
    brake6.disengage()


def main():
    state = state_dict["start_up"] # start in start_up state (1)
    previousState = -1
    fault = False

    while state != state_dict["fault"]: # check for fault condition
        # START UP STATE
        if state == state_dict["start_up"]:
            print("****START UP****")
            previousState = state
            initialize() # power on sequence
            state = state_dict["system_diagnostic"] # always move to system diagnositc state from start up

        # SYSTEM DIAGNOSTIC
        elif state == state_dict["system_diagnostic"]:
            print("****SYSTEM DIAGNOSTIC****")
            # print("I am in the System Diagnostic State")
            # if previousState == 0:
            #     print("WARNING: I came from the FAULT state")
            # else:
            #     print("I am just starting up")

            # determine if the pod is safe to approach
            safeToApproach = safe_to_approach_check() # is it safe??
            if safeToApproach == True:
                state = state_dict["safe_to_approach"]
            else: # if not safe to approach, move to fault state
                fault = True
                state = state_dict["Fault"]

        # SAFE TO APPROACH
        elif state == state_dict["safe_to_approach"]:
            print("****SAFE TO APPROACH****")
            launch = input("Prepare to launch? (True/False) ")
            if launch == "True":
                state = state_dict["prepare_to_launch"]
            else:
                sleep(5) # wait 5s before looping
                state = state_dict["safe_to_approach"]

        # PREPARE TO LAUNCH
        elif state == state_dict["prepare_to_launch"]:
            print("****PREPARE TO LAUNCH****")
            # print("WARNING: I am preparing to launch!")

            state = state_dict["ready_to_launch"]
        #    sys.exit()

        elif state == state_dict["ready_to_launch"]:
            print("****READY TO LAUNCH****")
            ready_to_launch = input("Are you sure you want to launch? (True/False) ")
            if ready_to_launch == "True":
                # print("I am launching")
                state = state_dict["launching"]
            else:
                state = state_dict["safe_to_approach"]

        elif state == state_dict["launching"]:
            print("****LAUNCHING****")
            while distance < stop_distance:
                accelerate()
            state = state_dict["coasting"] # once we are done accelerating


        elif state == state_dict["coasting"]:
            print("****COASTING****")
            # let momentum travel us forwards
            motors_off() # make sure to cut power to motors
            brakes_off() # disengage breaks
            while distance <= coast_distance:
                print(velocity)

        elif state == state_dict["braking"]:
            print("****BRAKING****")
            brakes_full_stop()
            if velocity == 0:
                state = state_dict["safe_to_approach"]
            else:
                fault = True
                state = state_dict["fault"]

        elif state == state_dict["crawling"]:
            print("****CRAWLING****")
            pass

        elif state == state_dict["power_off"]:
            print("****POWER OFF****")
            power_off()
            pass

        else:
            state = state_dict["fault"] # should never reach this state

    else:
        while fault == True:
            if state == state_dict["fault_braking"]:
                # if fault_braking_done ==
                brakes_full_stop()
                if velocity == 0:
                    state = state_dict["fault_stop"]
                else:
                    state = state_dict["fault_braking"]

            elif state == state_dict["fault_stop"]:
                pass

            elif state == state_dict["fault_diagnostic"]:
                print("FAULT: I have entered a FAULT state")

            elif state == state_dict["fault_diagnostic"]:
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
            state = state_dict["fault_diagnostic"]
    # end eventually, please
    loop += 1
    if loop >= 100:
        sys.exit()
main()
