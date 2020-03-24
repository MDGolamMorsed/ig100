import json
import os
import ig100_logger

def read_relay_pwm_value_from_file():
    print ("===================\============================")
    try:
        #with open('/root/IG100_Microprocessor_Script_1/relay_pwm_value.json') as f:
        with open('/root/IG100/relay_pwm_value.json') as f:
            data = json.load(f)
        return data
    #except FileNotFoundError as fnf_error:
    except:
        message = "file not found exception"
        event = "ig100_read_write_relay_pwm_file"
        ig100_logger.createErrorLog(message, event)
        #with open('/root/IG100_Microprocessor_Script_1/log.json', 'a') as log:
        #with open('/root/IG100/log.json', 'a') as log:
            #json.dump(fnf_error, log)

def write_relay_pwm_value_to_file(data):
    try:
        #with open('/root/IG100_Microprocessor_Script_1/relay_pwm_value.json', 'w') as f:
        with open('/root/IG100/relay_pwm_value.json', 'w') as f:
            json.dump(data, f)
    #except FileNotFoundError as fnf_error:
    except:
        message = "file not found exception"
        event = "ig100_read_write_relay_pwm_file"
        ig100_logger.createErrorLog(message, event)
        #with open('/root/IG100_Microprocessor_Script_1/log.json', 'a') as log:
        #with open('/root/IG100/log.json', 'a') as log:
            #json.dump(fnf_error, log)
