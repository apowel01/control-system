state = None

while true:
  if state == 0: #fault
    #break on
    #motor off
    #main battery output off
    #master diagnostic
    if masterDiagnostics: #Master Diagnostics called and verifies system stability
    	state = 1;
      
  elif state == 1:  #safe to approach
    #Brakes On
    #Motor Off
    #Main Battery Output Off
    if CrawlSignal:#Crawl Signal Recieved
    	state = 6
    
  elif state == 2: #ready to launch
  	#Brakes On
    #Motor Off
    #Main Battery Output On
    if LaunchSignal: #When the Launch Signal returns True, change the state to 3
    	state = 3
      
  elif state == 3: #launching
  	#Brakes Off
    #Motor Max Acceleration
    #Main Battery Output
    if position < FinalPosThreshold: #When the final position approaching, change the state to 5(Braking)
    	state = 5
    if MaximumSpeedReached: #When the pod reaches maximum speed, change the state to 4 (Coasting)
    	state = 4
    
  elif state == 4:  #Coasting
  	#Brakes Off
    #Motor Off
    #Main Battery Output Off
    if FinalPosition<FinalPosThreshold: #Final Position Approaching
    	state = 5
      
  elif state == 5:   #Braking
  	#Brakes On
    #Motor Off
    #Main Battery Output On
    if finalPosition>FinalPosThreshold and velocity == 0: #If final Position Not Reached and Velocity is 0
    	state = 6
    
  elif state == 6: #Crawling
  	#Brakes Off
    #Motor Low Speed
    #Main Battery Output On
    if positon < FinalPosThreshold: #When the final position is approaching and current state is in crawling mode, change the state to 5 (Braking)
    	state = 5
    
  elif state == 7: #Startup
  	#Brakes On
    #Motor Off
    #Main Battery Off
    if launchSignalReady: #prepare to launch signal
    	state = 2
   
  #External Messgaes
  if (startup):  # when startup signal recieved
  	state=7
  
  if (ExternalReset):  # when the external reset is true moves to state 7 for startup
  	state=7
    
  if not(Communication): #If communication is lost
  	state = 4
    
	if not(healthSystemCheck): #If Health System Abnormality Identified
  	state = 0


  #Constantly Read Date From MCUs
  #getVelocity
  #getPosition
  #getHealth
  #etc
  

    