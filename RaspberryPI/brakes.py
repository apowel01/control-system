# for FSM interactions with brakes

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
