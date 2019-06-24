# health and safety functions

# determine if pod is safe to approach
def safe_to_approach_check():
    print("I am checking if I am safe to apprach")
    tmp_safe = False
    # velocity test
    print("TODO: Check that velocity == 0")
    # -- Old (usable?) code
    # if health.velocity != 0:
    #     return tmp_safe
    # --

    # power to motor test
    print("TODO: Ensure motor power is on")
    if motor_power_is_on == True:
        return

    # power to brakes test

    return tmp_safe

#### MOTOR HEALTH FUNCTIONS ####

# for all functions called by FSM pertaining to the motors (1-6)
def create_motors():
    motor1 = motor()
    motor2 = motor()
    motor3 = motor()
    motor4 = motor()
    motor5 = motor()
    motor6 = motor()

def motors_on():
    print("I am turning off power to the motors")
    motor1.power_on()
    motor2.power_on()
    motor3.power_on()
    motor4.power_on()
    motor5.power_on()
    mootr6.power_on()

# power off the motors
def motors_off():
    print("I am turning off power to the motors")
    # can_msg = 0x000
    # send msg
    motor1.power_off()
    motor2.power_off()
    motor3.power_off()
    motor4.power_off()
    motor5.power_off()
    motor6.power_off()

# check if power is applied to motors
def motor_power_is_on():
    pass
#### BRAKE HEALTH FUNCTIONS ####

def create_brakes():
    # create brake objects
    brake1 = brake()
    brake2 = brake()
    brake3 = brake()
    brake4 = brake()
    brake5 = brake()
    brake6 = brake()

# engage all brakes
def brakes_engage():
    print("I am engaging the brakes")
    brake1.engage()
    brake2.engage()
    brake3.engage()
    brake4.engage()
    brake5.engage()
    brake6.engage()

# disengage all brakes
def brakes_disengage():
    print("I am disengaging the brakes")
    brake1.disengage()
    brake2.disengage()
    brake3.disengage()
    brake4.disengage()
    brake5.disengage()
    brake6.disengage()
