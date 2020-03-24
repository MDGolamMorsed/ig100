'''this file read feedback from the initialization of relay and pwm '''
import ig100_serial_configuration
import ig100_logger
import json

def ir_initialization():
    while True:
        try:
            if (ig100_serial_configuration.ser.inWaiting() > 0):
                value = ig100_serial_configuration.ser.read()
                if value == '\t':
                    break
                elif ord(value) == 1:
                    print("========== All Relay Values Initialized ==========")
                else:
                    pass
        except:
            #with open('/root/IG100_Microprocessor_Script_1/log.json', 'a') as log:
            message = "ir initialization error"
            event = "ig100_write_ir_ip_in_serial"
            ig100_logger.createErrorLog(message, event)
            #with open('/root/IG100/log.json', 'a') as log:
                #json.dump('pwm initialization error', log)

def ip_initialization():
    while True:
        try:
            if (ig100_serial_configuration.ser.inWaiting() > 0):
                value = ig100_serial_configuration.ser.read()
                if value == '\t':
                    break
                elif ord(value) == 1:
                    print("========== All PWM Values Initialized ==========")
                else:
                    pass
        except:
            #with open('/root/IG100_Microprocessor_Script_1/log.json', 'a') as log:
            message = "ip initialization error"
            event = "ig100_write_ir_ip_in_serial"
            ig100_logger.createErrorLog(message, event)
            #with open('/root/IG100/log.json', 'a') as log:
                #json.dump('pwm initialization error', log)