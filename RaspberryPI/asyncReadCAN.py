import asyncio
import can
import canDict

vals = {'Motor 1 Recieved' : False,
        'Motor 1 Voltage'  : None,
        'Motor 1 Temp'     : None,
        'Motor 1 Throttle' : None,
        'Motor 2 Recieved' : False,
        'Motor 2 Voltage'  : None,
        'Motor 2 Temp'     : None,
        'Motor 2 Throttle' : None,
        'Motor 3 Recieved' : False,
        'Motor 3 Voltage'  : None,
        'Motor 3 Temp'     : None,
        'Motor 3 Throttle' : None,
        'Motor 4 Recieved' : False,
        'Motor 4 Voltage'  : None,
        'Motor 4 Temp'     : None,
        'Motor 4 Throttle' : None,
        'Motor 5 Recieved' : False,
        'Motor 5 Voltage'  : None,
        'Motor 5 Temp'     : None,
        'Motor 5 Throttle' : None,
        'Motor 6 Recieved' : False,
        'Motor 6 Voltage'  : None,
        'Motor 6 Temp'     : None,
        'Motor 6 Throttle' : None,

        'FR Brake Recieved': False,
        'FR Brake Temp'    : None,
        'FR Brake Boolean' : False,
        'FL Brake Recieved': False,
        'FL Brake Temp'    : None,
        'FL Brake Boolean' : False,
        'MR Brake Recieved': False,
        'MR Brake Temp'    : None,
        'MR Brake Boolean' : False,
        'ML Brake Recieved': False,
        'ML Brake Temp'    : None,
        'ML Brake Boolean' : False,
        'RR Brake Recieved': False,
        'RR Brake Temp'    : None,
        'RR Brake Boolean' : False,
        'RL Brake Recieved': False,
        'RL Brake Temp'    : None,
        'RL Brake Boolean' : False,

        'FR Tensioner Recieved': False,
        'FR Tensioner Boolean' : False,
        'FL Tensioner Recieved': False,
        'FL Tensioner Boolean' : False,
        'MR Tensioner Recieved': False,
        'MR Tensioner Boolean' : False,
        'ML Tensioner Recieved': False,
        'ML Tensioner Boolean' : False,
        'RR Tensioner Recieved': False,
        'RR Tensioner Boolean' : False,
        'RL Tensioner Recieved': False,
        'RL Tensioner Boolean' : False,

        'F LIDAR Recieved' : False,
        'F LIDAR Distance' : None,
        'R LIDAR Recieved' : False,
        'R LIDAR Distance' : None
        }

def print_message(msg):
    """Regular callback function. Can also be a coroutine."""
    print(msg)

async def async_read_CAN(bus):
    can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan_native', receive_own_messages = True)
    reader = can.AsyncBufferedReader()

    listeners = [
            print_message,
            reader
    ]

    loop = asyncio.get_event_loop()
    notifier = can.Notifier(can0, listeners, loop = loop)

    for i in range(10):
        msg = await reader.get_message()
        if NOT (msg.arbitration_id in canDict.ids):
            break
        msgtype = canDict.ids[msg.arbitration_id]
        #parseData(msg, msgtype)

    notifier.stop()
    can0.shutdown()

# Get the default event loop
loop = asyncio.get_event_loop()
# Run until main coroutine finishes
loop.run_until_complete(async_read_CAN)
loop.close()
