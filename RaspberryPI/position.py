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
if Lidar < 10000 and CurrentDistance > 100000: #If lidar within last 100 meters and has crossed 1000 meters
    CurrentDistance = 125000-Lidar 
else:
    '''PREPARE LASERSENSOR DATA'''
    if LaserSensor_1/LaserSensor_2 > 1.10:
        LaserSensor_distance =  LaserSensor_1 #Take sensor_1 if its higher and difference > 10%
    elif LaserSensor_2/LaserSensor_1 > 1.10:
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
    if (HallSensor_distance/LaserSensor_distance-1) < .1: #Take the Hall Sensor data as distance ONLY when its within a 10% range and greater than the laser sensor readings
        CurrentDistance += HallSensor_distance
    else:
        CurrentDistance += LaserSensor_distance


#Get the current time since start
currentTime = time.time() - startTime

#calculate velocity (CM/Sec)
positions.append([CurrentDistance, currentTime])
for pos, time in positions:
    velocity = float(pos/time)
    if velocity > 8940: #If velocity recorded is over 8940cm/s (200mph). There is an error
        velocities.append([velocity, time])
    else:
        velocities.append([velocity, time])

#calculate acceleration
for vel, time in velocities:
    acceleration = float(vel/time)
    accelerations.append([acceleration, time])
