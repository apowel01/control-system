import asyncio
import time

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

async def updatePosition(lidarReading, rpms_list, bands_list):
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
    currentTimestep = time.time()-currentTime

    #TotalDistance (gets last recorded position)
    CurrentDistance = positions[-1][0]

    #Used to calculate distance from revolutions
    circumfrence_of_wheels = #####

    #Get readings from arduinos
    #convert readings to cm
    Lidar = (1250 - lidarReading)*100

    HallSensors = [rpm*circumfrence_of_wheels*currentTimestep for rpm in rpms_list]

    LaserSensor_1 = bands_list[0]*3048 #100ft = 3048cm
    LaserSensor_2 = bands_list[1]*3048 #100ft = 3048cm

    '''PREPARE LIDAR DATA DATA'''
    #If lidar within last 100 meters and the pod has crossed 1000 meters and less than 5 errors from lidar occured
    if Lidar < 10000 and CurrentDistance > 100000 and lidarErrorCounter <5:
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

        if LaserSensor_1 != lastBand_1 or LaserSensor_2 != lastBand_2:
            hallSensor_total += HallSensor_distance #Keeps track of how long we have traveled with Hall Sensor
        else:
            hallSensor_total = 0 #Clear hall sensor distance if we just detected a band


        '''PREPARE LASERSENSOR DATA''' #GET BACK TO THIS
        if LaserSensor_1 > LaserSensor_2:
            LaserSensor_distance =  LaserSensor_1
            lastBand_1 = LaserSensor_1
            hallSensor_total = 0 #Reset hall sensor distance to 0 when a band is sensed
        else:
            LaserSensor_distance =  LaserSensor_2
            LaserSensor_2 = LaserSensor_2
            hallSensor_total = 0 #Reset hall sensor distance to 0 when a band is sensed



    position = LaserSensor_distance + hallSensor_total

    #Insert position
    positions.append([position, currentTime])

    #calculate velocity (CM/Sec)
    velocity = float(position/currentTime)
    velocities.append([velocity, currentTime])


    #calculate acceleration
    acceleration = float(velocity/currentTime)
    accelerations.append([acceleration, currentTime])

    if Lidar < 10000 and CurrentDistance < 100000 and lidarErrorCounter < 5:
        lidarErrorCounter += 1

    #Returns current data
    #history of data can be accessed via the global lists (positions, velocities, accelerations)
    return [position, velocity, acceleration]
