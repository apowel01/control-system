import time;

startTimer = time.time()
'''
I ASSUME THE ARDUINOS WILL CLEARS THE DATA THEY SEND. THEREFORE SENDING ONLY THE DATA
COLLECTED DURING PERIODS BETWEEN EVERY CAN MESSAGE TO THE PI. THIS WILL STOP THE ACCUMULATION 
OF ERRORS IN THE READINGS OF THE SENSOR (LIDAR IS AN EXCEPTION)
'''
#Lidar - Distance
#HallSensors - RPM (SINCE LAST MESSAGE)
#Laser Sensor - Number of bands (SINCE LAST MESSAGE)

#TotalDistance

#Get readings from arduinos
#convert readings to cm
Lidar = (1250 - reading_from_arduino)*100

HallSensors_1 = Revolutions_from_arduino_1*circumfrence_of_wheels
HallSensors_2 = Revolutions_from_arduino_2*circumfrence_of_wheels
HallSensors_3 = Revolutions_from_arduino_3*circumfrence_of_wheels
HallSensors_4 = Revolutions_from_arduino_4*circumfrence_of_wheels
HallSensors = [HallSensors_1, HallSensors_2, HallSensors_3, HallSensors_4]

LaserSensor_1 = Number_of_bands_1*3048 #100ft = 3048cm
LaserSensor_2 = Number_of_bands_2*3048 #100ft = 3048cm

#Logic of 
if Lidar < 10000: #If lidar within last 100 meters
    CurrentDistance = 125000-Lidar 

if LaserSensor_1/LaserSensor_2 > 1.10:
    LaserSensor_distance =  LaserSensor_1 #Take sensor_1 if its higher and difference > 10%
elif LaserSensor_2/LaserSensor_1 > 1.10:
    LaserSensor_distance =  LaserSensor_2 #Take sensor_2 if its higher and difference > 10%
else:
    LaserSensor_distance = (LaserSensor_1+LaserSensor_2)/2 #Take average if two sensors are close within each other


def median(lst):
    n = len(lst)
    s = sorted(lst)
    return (sum(s[n//2-1:n//2+1])/2.0, s[n//2])[n % 2] if n else None

HallSensor_median = median(HallSensors)
HallSensors_withinRange = []
for HallSensor in HallSensors: #Filter out hall sensors that are not within range
    if abs(HallSensor/HallSensor_median-1) >.1:
        HallSensors_withinRange.append(HallSensor)

HallSensor_distance = 0
for HallSensor in HallSensors_withinRange: #Take the average of hall sensors within range
    HallSensor_distance += HallSensor
HallSensor_distance = HallSensor_distance/len(HallSensors_withinRange)

if (HallSensor_distance/LaserSensor_distance-1) > .1: #Take the Hall Sensor data as distance ONLY when its within a 10% range and greater than the laser sensor readings
    CurrentDistance += HallSensor_distance
else:
    CurrentDistance += LaserSensor_distance




#calculate velocity




#calculate acceleration