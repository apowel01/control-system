import piplates.RELAYplate as RELAY
import can

state = None
# Used for the relay
relayAddr = 0
# The relay code assumes our motors are on relays 1-6, 7 unused

bus = can.interface.Bus(channel='can0', bustype='socketcan_native')

while true:
  if state == 0: #fault
    msg = can.Message(arbitration_id=0x000, data=[0], extended_id=False)
    bus.send(msg) #break on / everything off
    
    relayALL(realyAddr, 0) #main battery output off
    #master diagnostic
    if masterDiagnostics: #Master Diagnostics called and verifies system stability
    	state = 1;
      
  elif state == 1:  #safe to approach

    msg1 = can.Message(arbitration_id=0x200, data=[0], extended_id=False)
    msg2 = can.Message(arbitration_id=0x100, data=[0], extended_id=False)
    bus.send(msg1) #breaks on
    bus.send(msg2) #Motors Off
    
    relayALL(relayAddr, 0) #Main Battery Output Off
    if CrawlSignal:#Crawl Signal Recieved
    	state = 6
    
  elif state == 2: #ready to launch
    msg1 = can.Message(arbitration_id=0x200, data=[0], extended_id=False)
    msg2 = can.Message(arbitration_id=0x100, data=[0], extended_id=False)
    bus.send(msg1) #breaks on
    bus.send(msg2) #Motors Off
    
    relayALL(relayAddr, 63) #Main Battery Output On
    if LaunchSignal: #When the Launch Signal returns True, change the state to 3
    	state = 3
      
  elif state == 3: #launching
    msg1 = can.Message(arbitration_id=0x201, data=[0], extended_id=False)
    msg2 = can.Message(arbitration_id=0x101, data=[0], extended_id=False)
    
    bus.send(msg1) #Brakes Off
    bus.send(msg2) #Motor Max Acceleration

    relayALL(relayAddr, 63) #Main Battery Output
    if position < FinalPosThreshold: #When the final position approaching, change the state to 5(Braking)
    	state = 5
    if MaximumSpeedReached: #When the pod reaches maximum speed, change the state to 4 (Coasting)
    	state = 4
    
  elif state == 4:  #Coasting
    msg1 = can.Message(arbitration_id=0x201, data=[0], extended_id=False)
    msg2 = can.Message(arbitration_id=0x100, data=[0], extended_id=False)
    
    bus.send(msg1) #Brakes Off
    bus.send(msg2) #Motor Off

    relayALL(relayAddr, 0) #Main Battery Output Off
    if FinalPosition<FinalPosThreshold: #Final Position Approaching
    	state = 5
      
  elif state == 5:   #Braking
    msg1 = can.Message(arbitration_id=0x200, data=[0], extended_id=False)
    msg2 = can.Message(arbitration_id=0x100, data=[0], extended_id=False)
    bus.send(msg1) #Brakes on
    bus.send(msg2) #Motor Off

    relayALL(relayAddr, 63) #Main Battery Output On
    if finalPosition>FinalPosThreshold and velocity == 0: #If final Position Not Reached and Velocity is 0
    	state = 6
    
  elif state == 6: #Crawling
    msg1 = can.Message(arbitration_id=0x201, data=[0], extended_id=False)
    msg2 = can.Message(arbitration_id=0x100, data=[0], extended_id=False)
    bus.send(msg1) #Brakes Off
    bus.send(msg2) #Motor Low Speed

    relayALL(relayAddr, 63) #Main Battery Output On
    if positon < FinalPosThreshold: #When the final position is approaching and current state is in crawling mode, change the state to 5 (Braking)
    	state = 5
    
  elif state == 7: #Startup
    #Brakes On
    #Motor Off
    msg1 = can.Message(arbitration_id = 0x200,data = [0], extended_id=False)
    msg2 = can.Message(arbitration_id = 0x100,data = [0], extended_id = False)
    relayALL(relayAddr, 0) #Main Battery Off
    if launchSignalReady: #prepare to launch signal
    	state = 2
   
  #External Message
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
  

    
