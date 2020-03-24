'''This file reads the relay and pwm pins values first and send these values to the microcontroller as command'''
import ig100_read_write_relay_pwm_file


def initialize_relay_value():
    IR = 'IR'
    data = ig100_read_write_relay_pwm_file.read_relay_pwm_value_from_file()
    for i in data['relay_value_list']:
        IR = IR + str(i)
        #print (i)
    #print (IR)
    return str(IR)

def initialize_pwm_value():
    data = ig100_read_write_relay_pwm_file.read_relay_pwm_value_from_file()
    IP = 'IP'
    for i in data['pwm_value_list']:
        IP = IP + i
        #print (i)
    #print (IP)
    return str(IP)
    