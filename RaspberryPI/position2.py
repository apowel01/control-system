import asyncio
import time

import threading

def median(lst):
    n = len(lst)
    s = sorted(lst)
    return (sum(s[n//2-1:n//2+1])/2.0, s[n//2])[n % 2] if n else None


#LASER SENSOR sends total number of bands

startTime = time.time()

#lists cotaining data and the time of that data
positions = [[0,0]] #2D list containing [position, time stamp]
velocities = [[0,0]] #2D list containing [velocity, time stamp]
accelerations = [[0,0]] #2D list containing [acceleration, time stamp]

#Used to error proof lidar
#Allow up to 5 errors, then completely ignore the lidar
#Errors are counted when acceleration spikes unnaturally due to lidar
lidarErrorCounter = 0

hallSensor_total = 0
lastBand_1 = 0
lastBand_2 = 0

# async def updatePosition(lidarReading, rpms_list, bands_list):
def updatePosition(lidarReading, rpms_list, bands_list):
    global startTime

    global positions
    global velocities
    global accelerations
    
    global lidarErrorCounter
    global hallSensor_total
    global lastBand_1
    global lastBand_2
    global firstCanMessage

    #Get the current time since start
    currentTime = time.time() - startTime
    currentTimestep = time.time()-positions[-1][1]-startTime
    # currentTimestep = time.time()-currentTime 

    #TotalDistance (gets last recorded position)
    CurrentDistance = positions[-1][0]
    print("current distance, ", CurrentDistance)

    #Used to calculate distance from revolutions
    circumfrence_of_wheels = 3048#####

    #Get readings from arduinos
    #convert readings to cm
    Lidar = (1250 - lidarReading)*100
    print(currentTimestep)
    HallSensors = [rpm*circumfrence_of_wheels*currentTimestep*(1/60) for rpm in rpms_list]

    LaserSensor_1 = bands_list[0]*3048 #100ft = 3048cm
    LaserSensor_2 = bands_list[1]*3048 #100ft = 3048cm

    '''PREPARE LIDAR DATA DATA'''
    #If lidar within last 100 meters and the pod has crossed 1000 meters and less than 5 errors from lidar occured
    if lidarReading < 10000 and CurrentDistance > 100000 and lidarErrorCounter <5:
        CurrentDistance = Lidar 
    else:
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

        '''PREPARE LASERSENSOR DATA''' #GET BACK TO THIS
        if LaserSensor_1 != lastBand_1 or LaserSensor_2 != lastBand_2:
            hallSensor_total = 0  #Clear hall sensor distance if we just detected a band
            if LaserSensor_1 > LaserSensor_2:
                LaserSensor_distance =  LaserSensor_1
                lastBand_1 = LaserSensor_1
            else:
                LaserSensor_distance =  LaserSensor_2
                lastBand_2 = LaserSensor_2
        else:
            if HallSensor_distance >= 3048: #if hallsensor distance calculated is over 100ft, then block it at 100ft
                hallSensor_total = 3048
            else:
                hallSensor_total += HallSensor_distance #Keeps track of how long we have traveled with Hall Sensor
        CurrentDistance = LaserSensor_distance + hallSensor_total
    position = CurrentDistance

    #Insert position
    positions.append([position, currentTime])

    #calculate velocity (CM/Sec)
    velocity = float(positions[-1][0]-positions[-2][0]/currentTimestep)
    velocities.append([velocity, currentTime])


    #calculate acceleration
    acceleration = float(velocity/currentTimestep)
    accelerations.append([acceleration, currentTime])

    #Check if an error occured with the lidar
    #Allow up to 5 errors
    if lidarReading < 10000 and CurrentDistance < 100000 and lidarErrorCounter < 5:
        lidarErrorCounter += 1

    #Returns current data
    #history of data can be accessed via the global lists (positions, velocities, accelerations)
    return [position, velocity, acceleration]





'''SIMULATION'''

rpmCount_1 = 0#Get from Arduino
rpmCount_2 = 0#Get from Arduino
rpmCount_3 = 0#Get from Arduino
rpmCount_4 = 0#Get from Arduino
bandsTotal_1=0
bandsTotal_2=0
def main():
    threading.Timer(1, main).start()

    global rpmCount_1
    global rpmCount_2
    global rpmCount_3
    global rpmCount_4
    global bandsTotal_1
    global bandsTotal_2


    lidarReading = 90

    rpmCount_1 = 60
    rpmCount_2 = 60
    rpmCount_3 = 60
    rpmCount_4 = 60
    revoloutions_list = [rpmCount_1,rpmCount_2,rpmCount_3,rpmCount_4]
    
    bandsTotal_1 += 1
    bandsTotal_2 += 1

    bands_list = [bandsTotal_1, bandsTotal_2]

    currentData = updatePosition(lidarReading, revoloutions_list, bands_list)
    print(currentData)
    # await asyncio.wait(currentData)

main()
