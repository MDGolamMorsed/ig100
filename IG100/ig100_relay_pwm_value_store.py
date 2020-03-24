'''This file store permanently relay and pwm last value to a file'''
import ig100_read_write_relay_pwm_file

def all_relay_pwm_value_store(message_command, value):
    print ('all_relay_pwm_value_store in ig100_relay_pwm_value_store')
    if (message_command == 'SRVA'):
        all_relay_value_store(value)
    else:
        all_pwm_value_store(value)

def single_relay_pwm_value_store(message_command, pin, value):
    print ('all_relay_pwm_value_store in ig100_relay_pwm_value_store')
    data = ig100_read_write_relay_pwm_file.read_relay_pwm_value_from_file()
    relay_value_list = data['relay_value_list']
    pwm_value_list = data ['pwm_value_list']
    if (message_command == 'SRV'):
        single_relay_value_store(pin, value)
    else:
        single_pwm_value_store(pin, value)

def pwm_value_mapping(value):
    if (int(value)<10):
        value = '00' + str(value)
    elif (int(value)<100):
        value = '0' + str(value)
    else:
        value = str(value)
    return value
    
def all_relay_value_store(value):
    data = ig100_read_write_relay_pwm_file.read_relay_pwm_value_from_file()
    relay_value_list = data['relay_value_list']
    for i in range(0, 4):
        relay_value_list[i] = value
    data ['relay_value_list'] = relay_value_list
    ig100_read_write_relay_pwm_file.write_relay_pwm_value_to_file(data)

def all_pwm_value_store(value):
    value = pwm_value_mapping(value)
    data = ig100_read_write_relay_pwm_file.read_relay_pwm_value_from_file()
    pwm_value_list = data ['pwm_value_list']
    for i in range(0, 4):
        pwm_value_list[i] = value
    data ['pwm_value_list'] = pwm_value_list
    ig100_read_write_relay_pwm_file.write_relay_pwm_value_to_file(data)
    
def single_relay_value_store(pin, value):
    data = ig100_read_write_relay_pwm_file.read_relay_pwm_value_from_file()
    relay_value_list = data['relay_value_list']
    pin = int(pin)
    for i in range(0, 4):
        if (i == pin):
            relay_value_list[i] = value
    data ['relay_value_list'] = relay_value_list
    ig100_read_write_relay_pwm_file.write_relay_pwm_value_to_file(data)
    
def single_pwm_value_store(pin, value):
    value = pwm_value_mapping(value)
    data = ig100_read_write_relay_pwm_file.read_relay_pwm_value_from_file()
    pwm_value_list = data ['pwm_value_list']
    pin = int(pin)
    for i in range(0, 4):
        if (i == pin):
            pwm_value_list[i] = value
    data ['pwm_value_list'] = pwm_value_list
    ig100_read_write_relay_pwm_file.write_relay_pwm_value_to_file(data)