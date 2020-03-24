'''this function parse the response from the microcontroller for sending to the broker'''
import ig100_dht_read
import ig100_logger
import json

single_relay_value_list = ['CONFIGURE_RELAY_PIN', 'CONFIGURE_RELAY_ALL_PIN', 'SET_RELAY_ALL_PIN_VALUE', 'SET_RELAY_PIN_VALUE', 'GET_RELAY_PIN_STATUS', 'GET_RELAY_PIN_VALUE']
single_pwm_value_list = ['CONFIGURE_PWM_ALL_PIN', 'SET_PWM_ALL_PIN_VALUE', 'CONFIGURE_PWM_PIN', 'SET_PWM_PIN_VALUE', 'GET_PWM_PIN_STATUS']
single_digital_value_list = ['CONFIGURE_DIGITAL_ALL', 'CONFIGURE_DIGTIAL_PIN', 'GET_DIGTIAL_PIN_STATUS', 'GET_DIGTIAL_PIN_VALUE']
single_analog_value_list = ['CONFIGURE_ANALOG_ALL', 'CONFIGURE_ANALOG_PIN', 'GET_ANALOG_PIN_STATUS', 'GET_ANALOG_PIN_VALUE']
single_interrupt_value_list = ['CONFIGURE_INTERRUPT_ALL_PIN', 'CONFIGURE_INTERRUPT_PIN', 'GET_INTERRUPT_PIN_STATUS']
single_dht_value_list = ['GET_DIGTIAL_PIN_TEMPERATURE_VALUE', 'GET_DIGTIAL_PIN_HUMIDITY_VALUE']


def response_parser(message_list, request_message_dictionary):
    #print ('In response message parser in response_message_parser.py')
    print ("========== Response Message Parser ==========")
    message_command = request_message_dictionary['payload']['command']
    message_uid = request_message_dictionary ['message_uid']
    print (message_command)
    print (message_uid)
    if (message_command == 'ALL_PIN_VALUE' or message_command == 'ALL_PIN_STATUS'):
        return all_pin_status_value(message_command, message_uid, message_list)
    if (message_command == 'GET_DIGITAL_ALL_PIN_STATUS' or message_command == 'GET_DIGITAL_ALL_PIN_VALUE' or message_command == 'GET_INTERRUPT_ALL_PIN_STATUS'):
        return all_digital_pin_status_value(message_command, message_uid, message_list)
    if (message_command == 'GET_ANALOG_ALL_PIN_STATUS' or message_command == 'GET_ANALOG_ALL_PIN_VALUE' or message_command == 'GET_RELAY_ALL_PIN_STATUS' or message_command == 'GET_RELAY_ALL_PIN_VALUE' or message_command == 'GET_PWM_ALL_PIN_STATUS' or message_command == 'GET_PWM_ALL_PIN_VALUE'):
        return all_analog_relay_pwm_interrupt_pin_status_value(message_command, message_uid, message_list)
    if message_command in single_relay_value_list:
        return single_relay_value(message_command, message_uid, message_list)
    if message_command in single_pwm_value_list:
        return single_pwm_value(message_command, message_uid, message_list)
    if message_command in single_digital_value_list:
        return single_digital_value(message_command, message_uid, message_list)
    if message_command in single_analog_value_list:
        return single_analog_value(message_command, message_uid, message_list)
    if message_command in single_interrupt_value_list:
        return single_interrupt_value(message_command, message_uid, message_list)
    if message_command in single_dht_value_list:
        #return single_temperature_value(message_command, message_uid, message_list)
        return single_dht_value(message_command, message_uid, message_list)


def response_message_dictionary_initialization():
    #print ('response_message_dictionary_initialization in response_message_parser.py')
    print ("========== Response Message Dictionary Initailazation ==========")
    response_message_dictionary = {
        "message_uid": "",
        "payload": {
            "command": "", 
            "response_code": "200",  
            "response_message": "successful",
            #'digitals': [[0],[0],[0],[0],[0],[0],[0],[1],[0],[0],[0],[0]],
            "digitals": [[],[],[],[],[],[],[],[],[],[],[],[]],
            #'digitals': [],
            "analog": [],
            "relay": [], 
            "pwm": [],
            "interrupt": [] 
        }
    }
    return response_message_dictionary


def response_message_dictionary_initialization_error():
    #print ('response_message_dictionary_initialization in response_message_parser.py')
    print ("========== Response Message Dictionary Initailazation ==========")
    response_message_dictionary_error = {
        "message_uid": "",
        "payload": {
            "command": "", 
            "response_code": "404",  
            "response_message": "unsuccessful",
            #'digitals': [[0],[0],[0],[0],[0],[0],[0],[1],[0],[0],[0],[0]],
            "digitals": [[],[],[],[],[],[],[],[],[],[],[],[]],
            #'digitals': [],
            "analog": [],
            "relay": [], 
            "pwm": [],
            "interrupt": [] 
        }
    }
    return response_message_dictionary_error


def all_pin_status_value(message_command, message_uid, message_list):
    print ('all_pin_status_value in response_message_parser.py')
    response_message_dictionary = response_message_dictionary_initialization()
    
    response_message_dictionary ["message_uid"] = message_uid
    response_message_dictionary["payload"]["command"] = message_command
    
    dht_pin_list, dht_temperature_humidity_value_list = ig100_dht_read.get_dht_temperature_humidity() # DHT function call
    
    try:
        z = 0
        for i in range(0,12):
            if i in dht_pin_list:
                response_message_dictionary["payload"]["digitals"][i].append(int(dht_temperature_humidity_value_list[ z + 0]))
                response_message_dictionary["payload"]["digitals"][i].append(int(dht_temperature_humidity_value_list[z + 1]))
                z = z + 2
            else:
                response_message_dictionary["payload"]["digitals"][i].append(message_list[i])

        #for i in range(0,12):
            #response_message_dictionary['payload']['digital'].append(message_list[i])
            #response_message_dictionary['payload']['digitals'][i][0] = message_list[i]
        for i in range(12,16):
            response_message_dictionary["payload"]["analog"].append(message_list[i])
        for i in range(16,20):
            response_message_dictionary["payload"]["relay"].append(message_list[i])
        for i in range(20,24):
            response_message_dictionary["payload"]["pwm"].append(message_list[i])

        #return str(response_message_dictionary)
        response_message_dictionary = json.dumps(response_message_dictionary)
        return response_message_dictionary
        
    except IndexError as error:
        print (error)
        error_message = error
        event = "ig100_response_message_parser"
        ig100_logger.createErrorLog(error_message, event)
        
        response_message_dictionary_error = json.dumps(response_message_dictionary_initialization_error())
        return response_message_dictionary_error
    
def all_digital_pin_status_value(message_command, message_uid, message_list):
    print ('all_pin_status_value in response_message_parser.py')
    response_message_dictionary = response_message_dictionary_initialization()
    response_message_dictionary ["message_uid"] = message_uid
    response_message_dictionary["payload"]["command"] = message_command
    
    try:
        if (message_command == 'GET_INTERRUPT_ALL_PIN_STATUS'):
            try:
                for i in range(0,12):
                    response_message_dictionary["payload"]["interrupt"].append(message_list[i])
            except IndexError as error:
                print (error)
        elif (message_command == 'GET_DIGITAL_ALL_PIN_VALUE'):
            #for i in range(0,12):
                #response_message_dictionary['payload']['digitals'][i][0] = message_list[i]
            dht_pin_list, dht_temperature_humidity_value_list = ig100_dht_read.get_dht_temperature_humidity() # DHT function call
            
            try:
                z = 0
                for i in range(0,12):
                    if i in dht_pin_list:
                        response_message_dictionary["payload"]["digitals"][i].append(int(dht_temperature_humidity_value_list[ z + 0]))
                        response_message_dictionary["payload"]["digitals"][i].append(int(dht_temperature_humidity_value_list[z + 1]))
                        z = z + 2
                    else:
                        response_message_dictionary["payload"]["digitals"][i].append(message_list[i])
            except IndexError as error:
                print (error)
        else:
            try:
                for i in range(0,12):
                    response_message_dictionary["payload"]["digitals"][i].append(message_list[i])
            except IndexError as error:
                print (error)
                #response_message_dictionary['payload']['digitals'][i][0] = message_list[i]
        #return str(response_message_dictionary)
        response_message_dictionary = json.dumps(response_message_dictionary)
        return response_message_dictionary
    
    except IndexError as error:
        print (error)
        error_message = error
        event = "ig100_response_message_parser"
        ig100_logger.createErrorLog(error_message, event)
        
        response_message_dictionary_error = json.dumps(response_message_dictionary_initialization_error())
        return response_message_dictionary_error

def all_analog_relay_pwm_interrupt_pin_status_value(message_command, message_uid, message_list):
    print ('all_analog_relay_pwm_interrupt_pin_status_value in response_message_parser.py')
    response_message_dictionary = response_message_dictionary_initialization()
    response_message_dictionary ["message_uid"] = message_uid
    response_message_dictionary["payload"]["command"] = message_command
    
    try:
        if (message_command == 'GET_ANALOG_ALL_PIN_STATUS' or message_command == 'GET_ANALOG_ALL_PIN_VALUE'):
            for i in range(0,4):
                response_message_dictionary["payload"]["analog"].append(message_list[i])
        if (message_command == 'GET_RELAY_ALL_PIN_STATUS' or message_command == 'GET_RELAY_ALL_PIN_VALUE'):
            for i in range(0,4):
                response_message_dictionary["payload"]["relay"].append(message_list[i])
        if (message_command == 'GET_PWM_ALL_PIN_STATUS' or message_command == 'GET_PWM_ALL_PIN_VALUE'):
            for i in range(0,4):
                response_message_dictionary["payload"]["pwm"].append(message_list[i])
                
        #return str(response_message_dictionary)
        response_message_dictionary = json.dumps(response_message_dictionary)
        return response_message_dictionary
        
    except IndexError as error:
        print (error)
        error_message = error
        event = "ig100_response_message_parser"
        ig100_logger.createErrorLog(error_message, event)
        
        response_message_dictionary_error = json.dumps(response_message_dictionary_initialization_error())
        return response_message_dictionary_error
    
    
def single_digital_value(message_command, message_uid, message_list):
    print ('all_pin_status_value in response_message_parser.py')
    response_message_dictionary = response_message_dictionary_initialization()
    response_message_dictionary ["message_uid"] = message_uid
    response_message_dictionary["payload"]["command"] = message_command
    
    #response_message_dictionary['payload']['digitals'] = message_list
    #response_message_dictionary['payload']['digitals'][0][0] = message_list[0]
    
    try:
        response_message_dictionary["payload"]["digitals"][0].append(message_list[0])
        response_message_dictionary = json.dumps(response_message_dictionary)
        return str(response_message_dictionary)
        
    except IndexError as error:
        print (error)
        error_message = error
        event = "ig100_response_message_parser"
        ig100_logger.createErrorLog(error_message, event)
        
        response_message_dictionary_error = json.dumps(response_message_dictionary_initialization_error())
        return response_message_dictionary_error
    
    
def single_dht_value(message_command, message_uid, message_list):
    if message_command == 'GET_DIGTIAL_PIN_TEMPERATURE_VALUE':
        return single_temperature_value(message_command, message_uid, message_list)
    else:
        return single_humidity_value(message_command, message_uid, message_list)
    
def single_temperature_value(message_command, message_uid, message_list):
    print ('all_pin_status_value in response_message_parser.py')

    response_message_dictionary = response_message_dictionary_initialization()
    response_message_dictionary ["message_uid"] = message_uid
    response_message_dictionary["payload"]["command"] = message_command
    
    #response_message_dictionary['payload']['digitals'] = message_list
    #response_message_dictionary['payload']['digitals'][0][0] = message_list[0]
    
    try:
        response_message_dictionary["payload"]["digitals"][0].append(message_list[0])
        #print (response_message_dictionary)
        
        #return str(response_message_dictionary)
        response_message_dictionary = json.dumps(response_message_dictionary)
        return response_message_dictionary
        
    except IndexError as error:
        print (error)
        error_message = error
        event = "ig100_response_message_parser"
        ig100_logger.createErrorLog(error_message, event)
        
        response_message_dictionary_error = json.dumps(response_message_dictionary_initialization_error())
        return response_message_dictionary_error
    
    
def single_humidity_value(message_command, message_uid, message_list):
    print ('all_pin_status_value in response_message_parser.py')
    print ('single_humidity_value')

    response_message_dictionary = response_message_dictionary_initialization()
    response_message_dictionary ["message_uid"] = message_uid
    response_message_dictionary["payload"]["command"] = message_command
    
    #response_message_dictionary['payload']['digitals'] = message_list
    #response_message_dictionary['payload']['digitals'][0][0] = message_list[0]
    
    try:
        response_message_dictionary["payload"]["digitals"][0].append(message_list[0])
        #return str(response_message_dictionary)
        response_message_dictionary = json.dumps(response_message_dictionary)
        return response_message_dictionary
        
    except IndexError as error:
        print (error)
        error_message = error
        event = "ig100_response_message_parser"
        ig100_logger.createErrorLog(error_message, event)
        
        response_message_dictionary_error = json.dumps(response_message_dictionary_initialization_error())
        return response_message_dictionary_error
    
def single_analog_value(message_command, message_uid, message_list):
    print ('all_pin_status_value in response_message_parser.py')
    response_message_dictionary = response_message_dictionary_initialization()
    response_message_dictionary ["message_uid"] = message_uid
    response_message_dictionary["payload"]["command"] = message_command
    
    try:
        #response_message_dictionary["payload"]["analog"] = message_list
        response_message_dictionary["payload"]["analog"].append(message_list[0])
        
        #return str(response_message_dictionary)
        response_message_dictionary = json.dumps(response_message_dictionary)
        return response_message_dictionary
    except IndexError as error:
        print (error)
        error_message = error
        event = "ig100_response_message_parser"
        ig100_logger.createErrorLog(error_message, event)
        
        response_message_dictionary_error = json.dumps(response_message_dictionary_initialization_error())
        return response_message_dictionary_error
    
def single_relay_value(message_command, message_uid, message_list):
    print ('single_relay_value in response_message_parser.py')
    response_message_dictionary = response_message_dictionary_initialization()
    response_message_dictionary ["message_uid"] = message_uid
    response_message_dictionary["payload"]["command"] = message_command
    
    try:
        #response_message_dictionary["payload"]["relay"] = message_list
        response_message_dictionary["payload"]["relay"].append(message_list[0])
        
        #return str(response_message_dictionary)
        response_message_dictionary = json.dumps(response_message_dictionary)
        return response_message_dictionary
        
    except IndexError as error:
        print (error)
        error_message = error
        event = "ig100_response_message_parser"
        ig100_logger.createErrorLog(error_message, event)
        
        response_message_dictionary_error = json.dumps(response_message_dictionary_initialization_error())
        return response_message_dictionary_error
    
    
def single_pwm_value(message_command, message_uid, message_list):
    print ('all_pin_status_value in response_message_parser.py')
    response_message_dictionary = response_message_dictionary_initialization()
    response_message_dictionary ["message_uid"] = message_uid
    response_message_dictionary["payload"]['command'] = message_command
    
    try:
        #response_message_dictionary["payload"]["pwm"] = message_list
        response_message_dictionary["payload"]["pwm"].append(message_list[0])
        
        #return str(response_message_dictionary)
        response_message_dictionary = json.dumps(response_message_dictionary)
        return response_message_dictionary
    except IndexError as error:
        print (error)
        error_message = error
        event = "ig100_response_message_parser"
        ig100_logger.createErrorLog(error_message, event)
        
        response_message_dictionary_error = json.dumps(response_message_dictionary_initialization_error())
        return response_message_dictionary_error
    
def single_interrupt_value(message_command, message_uid, message_list):
    print ('all_pin_status_value in response_message_parser.py')
    response_message_dictionary = response_message_dictionary_initialization()
    response_message_dictionary ["message_uid"] = message_uid
    response_message_dictionary["payload"]["command"] = message_command
    
    try:
        #response_message_dictionary["payload"]["interrupt"] = message_list
        response_message_dictionary["payload"]["interrupt"].append(message_list[0])
        
        #return str(response_message_dictionary)
        response_message_dictionary = json.dumps(response_message_dictionary)
        return response_message_dictionary
    except IndexError as error:
        print (error)
        error_message = error
        event = "ig100_response_message_parser"
        ig100_logger.createErrorLog(error_message, event)
        
        response_message_dictionary_error = json.dumps(response_message_dictionary_initialization_error())
        return response_message_dictionary_error
    
def interrupt_parser(value_list):
    print ('interrupt_parser in response_message_parser.py')
    response_message_dictionary = response_message_dictionary_initialization()
    
    response_message_dictionary["payload"]["command"] = 'INTERRUPT_RESPONSE'
    
    try:
        response_message_dictionary["payload"]["interrupt"].append(value_list[0])
        
        #print (response_message_dictionary)
        #return str(response_message_dictionary)
        response_message_dictionary = json.dumps(response_message_dictionary)
        return response_message_dictionary
        
    except IndexError as error:
        print (error)
        error_message = error
        event = "ig100_response_message_parser"
        ig100_logger.createErrorLog(error_message, event)
        
        response_message_dictionary_error = json.dumps(response_message_dictionary_initialization_error())
        return response_message_dictionary_error
    
    
def all_pin_value( message_list):
    #print ('all_pin_status_value in response_message_parser.py')
    print ("========== All Pin Value in Response Message Parser ==========")
    response_message_dictionary = response_message_dictionary_initialization()
    
    response_message_dictionary ["message_uid"] = "1010"
    response_message_dictionary["payload"]["command"] = "ALL_PIN_VALUE"
    
    dht_pin_list, dht_temperature_humidity_value_list = ig100_dht_read.get_dht_temperature_humidity() # DHT function call
    
    
    try:
        z = 0
        for i in range(0,12):
            if i in dht_pin_list:
                response_message_dictionary["payload"]["digitals"][i].append(int(dht_temperature_humidity_value_list[ z + 0]))
                response_message_dictionary["payload"]["digitals"][i].append(int(dht_temperature_humidity_value_list[z + 1]))
                z = z + 2
            else:
                response_message_dictionary["payload"]["digitals"][i].append(message_list[i])
        for i in range(12,16):
            response_message_dictionary["payload"]["analog"].append(message_list[i])
        for i in range(16,20):
            response_message_dictionary["payload"]["relay"].append(message_list[i])
        for i in range(20,24):
            response_message_dictionary["payload"]["pwm"].append(message_list[i])
            
        #return str(response_message_dictionary)
        response_message_dictionary = json.dumps(response_message_dictionary)
        return response_message_dictionary
        
    except IndexError as error:
    #except:
        print (error)
        error_message = error
        event = "ig100_response_message_parser"
        ig100_logger.createErrorLog(error_message, event)
        
        response_message_dictionary_error = json.dumps(response_message_dictionary_initialization_error())
        return response_message_dictionary_error
