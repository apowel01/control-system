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
    motor1.power_off()
    motor2.power_off()
    motor3.power_off()
    motor4.power_off()
    motor5.power_off()
    motor6.power_off()
