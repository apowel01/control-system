import time;

startTime = time.time()
'''
I ASSUME THE ARDUINOS WILL CLEARS THE DATA THEY SEND. THEREFORE SENDING ONLY THE DATA
COLLECTED DURING PERIODS BETWEEN EVERY CAN MESSAGE TO THE PI. THIS WILL STOP THE ACCUMULATION 
OF ERRORS IN THE READINGS OF THE SENSOR (LIDAR IS AN EXCEPTION)
'''
#Lidar - Distance
#HallSensors - RPM (SINCE LAST MESSAGE)
#Laser Sensor - Number of bands (SINCE LAST MESSAGE)


#lists cotaining data and the time of that data
positions = [] #2D list containing [position, time stamp]
velocities = [] #2D list containing [velocity, time stamp]
accelerations = [] #2D list containing [acceleration, time stamp]

#TotalDistance
CurrentDistance = 0

#Used to error proof lidar
#Allow up to 5 errors, then completely ignore the lidar
#Errors are counted when acceleration spikes unnaturally due to lidar
lidarErrorCounter = 0

#Indicates wheather or not position is determined by lidar for error countering reasons
lidarInUse = False

#LOOP FROM HERE
circumfrence_of_wheels = #####
lidarReading = #Get from Arduino
rpmCount_1 = #Get from Arduino
rpmCount_2 = #Get from Arduino
rpmCount_3 = #Get from Arduino
rpmCount_4 = #Get from Arduino
Number_of_bands_1 = #Get from Arduino
Number_of_bands_2 = #Get from Arduino

#Get readings from arduinos
#convert readings to cm
Lidar = (1250 - lidarReading)*100

HallSensors_1 = rpmCount_1*circumfrence_of_wheels
HallSensors_2 = rpmCount_2*circumfrence_of_wheels
HallSensors_3 = rpmCount_3*circumfrence_of_wheels
HallSensors_4 = rpmCount_4*circumfrence_of_wheels
HallSensors = [HallSensors_1, HallSensors_2, HallSensors_3, HallSensors_4]

LaserSensor_1 = Number_of_bands_1*3048 #100ft = 3048cm
LaserSensor_2 = Number_of_bands_2*3048 #100ft = 3048cm

'''PREPARE LIDAR DATA DATA'''
#If lidar within last 100 meters and the pod has crossed 1000 meters and less than 5 errors from lidar occured
if Lidar < 10000 and CurrentDistance > 100000 and lidarErrorCounter <5:
    CurrentDistance = 125000-Lidar 
    lidarInUse = True
else:
    '''PREPARE LASERSENSOR DATA'''
    if LaserSensor_2 != 0 and LaserSensor_1/LaserSensor_2 > 1.10:
        LaserSensor_distance =  LaserSensor_1 #Take sensor_1 if its higher and difference > 10%
    elif LaserSensor_1 != 0 and LaserSensor_2/LaserSensor_1 > 1.10:
        LaserSensor_distance =  LaserSensor_2 #Take sensor_2 if its higher and difference > 10%
    else:
        LaserSensor_distance = (LaserSensor_1+LaserSensor_2)/2 #Take average if two sensors are close within each other

    '''PREPARE HALLSENSOR DATA'''
    def median(lst):
        n = len(lst)
        s = sorted(lst)
        return (sum(s[n//2-1:n//2+1])/2.0, s[n//2])[n % 2] if n else None

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
        if (time.time() - startTime) > 2: #Wait until we have position data history
            previousPosition = positions[-1][0]
            previousVelocity = velocities[-1][0]
            estimatedCurrentPosition = previousPosition+previousVelocity*t(ime.time()-positions[-1][1]) #previousPosition+previousVelocity*time
            currentPosition = HallSensor_distance+previousPosition
            if currentPosition/estimatedCurrentPosition < 1.05: #if estimated position and position from hall sensor are within 5% of each other, go with hallsensor
                CurrentDistance += HallSensor_distance
    elif (HallSensor_distance/LaserSensor_distance-1) < .1: #Take the Hall Sensor data as distance ONLY when its within a 10% range and greater than the laser sensor readings
        CurrentDistance += HallSensor_distance
    else:
        CurrentDistance += LaserSensor_distance

position = CurrentDistance

#Get the current time since start
currentTime = time.time() - startTime
startTime = time.time()

positions.append([position, currentTime])

#calculate velocity (CM/Sec)
velocity = float(position/currentTime)
velocities.append([velocity, currentTime])

#calculate acceleration
acceleration = float(velocity/currentTime)
if acceleration > 200: #If acceleration recorded is over 200cm/s/s. There is an error
    if lidarInUse:
        lidarErrorCounter += 1
    acceleration = accelerations[-1][0] #update acceleration with last acceleration value
    velocities[-1][0] = velocities[-2][0] #update velocity with last velocity value
    velocity = velocities[-1][0]
    positions[-1][0] = positions[-2][0]+velocity*(positions[-1][1]-positions[-2][1])  #update positions with: lastPosition+lastVelocity*timeInterval
    position = positions[-1][0]
accelerations.append([acceleration, currentTime])

#position
#velocity
#acceleration
