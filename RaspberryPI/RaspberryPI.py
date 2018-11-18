import smbus2
import time

# This is the address we setup in the Arduino Program
#This address is determined by which pins the I2C Connection is
#plugged into on the Raspberry PI
address = None

#list of Strings used to denote request types
#could use enum in the future, but this seems to work ok
#add other types to the list, index reperesents the 
#I2C code
requestType = ["HALL_POSITION", "LASER_POSITION", "PERCENT_ERROR", "RESET"]


def writeRequest(request):
    #this is another way to write to bus using smbus2
    with smbus2.SMBusWrapper(1) as bus:
        # Write a byte to address, offset 0
        #not sure what offset means, but will look into it
        bus.write_byte_data(address, 0, request)

def readNumber():
    #this is another way to read from I2C using smbus2
    with smbus2.SMBusWrapper(1) as bus:
        #reads a byte from given address, offset 0
        #not sure what offset means, but will look into it
        number = bus.read_byte_data(address, 0)
        return int(number)

while True:
    
    #This is just for testing purposes if we want to test with a second arduino
    if (input("Enter 1 for  address (0x04) and  2 for address (0x05): ") == "1"):
        address = 0x04
    else:
        address = 0x05

    #get request Type from console input
    request = int(input("Select 0 for hall position, 1 for laser position, 2 for error, 3 to reset position MCU: "))
    
    #sends a request to the RPI
    writeRequest(request)
    print( "RPI: Hi Arduino, I sent you a " + requestType[request] + " request")

    #reads data sent from Arduino (arduino will reset the Hall Count after a request)
    number = readNumber()
    print ("Data recieved from adrduino "+ str(number))