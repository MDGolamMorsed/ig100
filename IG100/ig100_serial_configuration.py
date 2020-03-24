import serial
import time
import ig100_logger
import json

port = "/dev/ttyATH0"

try: 
    ser = serial.Serial( port, 115200, timeout = 5)
    ser.flushInput()
    time.sleep(0.1)
    
except:
    #with open('/root/IG100_Microprocessor_Script_1/log.json', 'a') as log:
    message = "serial initialization error"
    event = "ig100_serial_configuration"
    ig100_logger.createErrorLog(message, event)
    #with open('/root/IG100/log.json', 'a') as log:
        #json.dump('serial initialization error', log)
