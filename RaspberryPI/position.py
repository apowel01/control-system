import asyncio
import time

import threading

'''
I ASSUME THE ARDUINOS WILL CLEARS THE DATA THEY SEND. THEREFORE SENDING ONLY THE DATA
COLLECTED DURING PERIODS BETWEEN EVERY CAN MESSAGE TO THE PI. THIS WILL STOP THE ACCUMULATION 
OF ERRORS IN THE READINGS OF THE SENSOR (LIDAR IS AN EXCEPTION)
'''
#Lidar - Distance
#HallSensors - revoloution (SINCE LAST MESSAGE)
#Laser Sensor - Number of bands (SINCE LAST MESSAGE)

startTime = time.time()

#lists cotaining data and the time of that data
positions = [[0,0]] #2D list containing [position, time stamp]
velocities = [[0,0]] #2D list containing [velocity, time stamp]
accelerations = [[0,0]] #2D list containing [acceleration, time stamp]

#Used to error proof lidar
#Allow up to 5 errors, then completely ignore the lidar
#Errors are counted when acceleration spikes unnaturally due to lidar
lidarErrorCounter = 0

#Indicates wheather or not position is determined by lidar for error countering reasons
lidarInUse = False

# async def updatePosition(lidarReading, revoloutions_list, bands_list):
def updatePosition(lidarReading, revoloutions_list, bands_list):
    global startTime
    global positions
    global velocities
    global accelerations
    global lidarErrorCounter
    global lidarInUse

    #Get the current time since start
    currentTimestep = time.time()-currentTime
    currentTime = time.time() - startTime

    #TotalDistance (gets last recorded position)
    CurrentDistance = positions[-1][0]

    #Used to calculate distance from revolutions
    circumfrence_of_wheels = #####

    #Get readings from arduinos
    #convert readings to cm
    Lidar = (1250 - lidarReading)*100

    HallSensors = [revoloution*circumfrence_of_wheels for revoloution in revoloutions_list]

    LaserSensor_1 = bands_list[0]*3048 #100ft = 3048cm
    LaserSensor_2 = bands_list[1]*3048 #100ft = 3048cm

    '''PREPARE LIDAR DATA DATA'''
    #If lidar within last 100 meters and the pod has crossed 1000 meters and less than 5 errors from lidar occured
    if Lidar < 10000 and CurrentDistance > 100000 and lidarErrorCounter <5:
        CurrentDistance = Lidar 
        lidarInUse = True
    else:
        '''PREPARE LASERSENSOR DATA''' #GET BACK TO THIS
        if LaserSensor_2 != 0 and LaserSensor_1/LaserSensor_2 > 1.10:
            LaserSensor_distance =  LaserSensor_1 #Take sensor_1 if its higher and difference > 10%
        elif LaserSensor_1 != 0 and LaserSensor_2/LaserSensor_1 > 1.10:
            LaserSensor_distance =  LaserSensor_2 #Take sensor_2 if its higher and difference > 10%
        else:
            LaserSensor_distance = (LaserSensor_1+LaserSensor_2)/2 #Take average if two sensors are close within each other

        '''PREPARE HALLSENSOR DATA'''
        HallSensor_median = median(HallSensors)
        HallSensors_withinRange = []
        for HallSensor in HallSensors: #Filter out hall sensors that are not within range
            if abs(HallSensor/HallSensor_median-1) <.1:
                HallSensors_withinRange.append(HallSensor)

        HallSensor_distance = 0
        for HallSensor in HallSensors_withinRange: #Take the average of hall sensors within range
            HallSensor_distance += HallSensor
        HallSensor_distance = HallSensor_distance/len(HallSensors_withinRange)

        '''DECIDE WHEATHER TO GO WITH HALLSENSOR OR LASERSENSOR '''
        if LaserSensor_distance == 0: #if laser sensor reading is zero
            # if (time.time() - startTime) > 2: #Wait until we have position data history
            previousPosition = positions[-1][0]
            previousVelocity = velocities[-1][0]
            previousAcceleration = accelerations[-1][0]
            estimatedCurrentPosition = previousPosition+(previousVelocity+(previousVelocity+previousAcceleration*currentTimestep))/2*currentTimestep #previousPosition+previousVelocity*time
            currentPosition = HallSensor_distance+previousPosition
            if HallSensor_distance/estimatedCurrentPosition < 1.05: #if estimated position and position from hall sensor are within 5% of each other, go with hallsensor
                CurrentDistance += HallSensor_distance
        elif LaserSensor_distance != 0 and (HallSensor_distance/LaserSensor_distance-1) < .1: #Take the Hall Sensor data as distance ONLY when its within a 10% range and greater than the laser sensor readings
            CurrentDistance += HallSensor_distance
        else:
            CurrentDistance += LaserSensor_distance

    position = CurrentDistance


    #Insert position
    positions.append([position, currentTime])

    #calculate velocity (CM/Sec)
    velocity = float(position/currentTime)
    velocities.append([velocity, currentTime])


    #calculate acceleration
    acceleration = float(velocity/currentTime)
    if acceleration > 10000: #If acceleration recorded is over 200cm/s/s. There is an error
        if lidarInUse:
            lidarErrorCounter += 1
        acceleration = accelerations[-1][0] #update acceleration with last acceleration value
        velocities[-1][0] = velocities[-2][0] + accelerations[-2][0]*currentTimestep #update velocity with last velocity value
        avgvelocity = (velocities[-2][0] + velocities[-1][0])/2

        positions[-1][0] = positions[-2][0]+avgvelocity*currentTimestep  #update positions with: lastPosition+lastVelocity*timeInterval
        position = positions[-1][0]
    accelerations.append([acceleration, currentTime])

    #Returns current data
    #history of data can be accessed via the global lists (positions, velocities, accelerations)
    return [position, velocity, acceleration]


async def main():
def main():
    lidarReading = #Get from Arduino

    revoloutionCount_1 = #Get from Arduino
    revoloutionCount_2 = #Get from Arduino
    revoloutionCount_3 = #Get from Arduino
    revoloutionCount_4 = #Get from Arduino
    revoloutions_list = [revoloutionCount_1,revoloutionCount_2,revoloutionCount_3,revoloutionCount_4]
    
    Number_of_bands_1 = #Get from Arduino
    Number_of_bands_2 = #Get from Arduino
    bands_list = [Number_of_bands_1, Number_of_bands_2]

    currentData = updatePosition(lidarReading, revoloutions_list, bands_list)
    # await asyncio.wait(currentData)


timer = QTimer()
timer.timeout.connect(update_labels)
timer.start(20)
