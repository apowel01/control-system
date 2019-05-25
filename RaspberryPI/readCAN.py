#	read_CAN
#	Brandon Nowak
#	
# Function:
# read CAN bus messages and parse data
# 
import can

def read_CAN(bus):
    #bus = can.interface.Bus(channel = 'can0', bustype = 'socketcan_native')
    listener = can.BufferedReader()
    notifier = can.Notifier(bus, [listener])
    ids = {msgID : variable}
    vals = {variable : data}

    for i in range(10):
        msg = listener.get_message()
        #check msg id and stop code if not useful
        if msg = None:
            break
        variable = ids[msg.arbitration_id]
        #Todo 
        #Add a data parser based on variable
        #Assign data to the variable in vals id

    	
