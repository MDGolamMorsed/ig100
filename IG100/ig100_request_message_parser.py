"""parser for parsing command from mqtt and generate command for microcontroller """
import ig100_relay_pwm_value_store
#import ig100_logger

command_mapping_dictionary = {
                             "ALL_PIN_VALUE" : "CVA",
                             "ALL_PIN_STATUS" : "CPA",
                             "CONFIGURE_ALL_PIN" : "CSR",                    # CSRx
                             "CONFIGURE_DIGITAL_ALL" : "SDA",                # SDAx
                             "GET_DIGITAL_ALL_PIN_STATUS" : "GDA",
                             "GET_DIGITAL_ALL_PIN_VALUE" : "GDVA",
                             "CONFIGURE_ANALOG_ALL" : "SAA",                 # SAAx
                             "GET_ANALOG_ALL_PIN_STATUS" : "GAA",
                             "GET_ANALOG_ALL_PIN_VALUE" : "GAVA",
                             "CONFIGURE_RELAY_ALL_PIN" : "SRA",              # SRAx
                             "SET_RELAY_ALL_PIN_VALUE" : "SRVA",             # SRVAx
                             "GET_RELAY_ALL_PIN_STATUS" : "GRA",
                             "GET_RELAY_ALL_PIN_VALUE" : "GRVA",
                             "CONFIGURE_PWM_ALL_PIN" : "SPA",                # SPAx
                             "SET_PWM_ALL_PIN_VALUE" : "SPVA",               # SPVAx
                             "GET_PWM_ALL_PIN_STATUS" : "GPA",
                             "GET_PWM_ALL_PIN_VALUE" : "GPVA",
                             "CONFIGURE_INTERRUPT_ALL_PIN" : "SIA",          # SIAx
                             "GET_INTERRUPT_ALL_PIN_STATUS" : "GIA",
                             "CONFIGURE_DIGTIAL_PIN" : "SD",                 # SDnnx
                             "GET_DIGTIAL_PIN_STATUS" : "GD",                # GDnn
                             "GET_DIGTIAL_PIN_VALUE" : "GDV",                # GDVnn
                             "GET_DIGTIAL_PIN_TEMPERATURE_VALUE" : "GDT",    # GDTnn
                             "GET_DIGTIAL_PIN_HUMIDITY_VALUE" : "GDH",       # GDHnn
                             "CONFIGURE_ANALOG_PIN" : "SA",                  # SAnx
                             "GET_ANALOG_PIN_STATUS" : "GA",                 # GAn
                             "GET_ANALOG_PIN_VALUE" : "GAV",                 # GAVn
                             "CONFIGURE_RELAY_PIN" : "SR",                   # SRnx
                             "SET_RELAY_PIN_VALUE" : "SRV",                  # SRVnx
                             "GET_RELAY_PIN_STATUS" : "GR",                  # GRn
                             "GET_RELAY_PIN_VALUE" : "GRV",                  # GRVn
                             "CONFIGURE_PWM_PIN" : "SP",                     # SPnx
                             "SET_PWM_PIN_VALUE" : "SPV",                    # SPVnx
                             "GET_PWM_PIN_STATUS" : "GP",                    # GPn
                             "GET_PWM_PIN_VALUE" : "GPV",                    # GPVn
                             "CONFIGURE_INTERRUPT_PIN" : "SI",               # SInx
                             "GET_INTERRUPT_PIN_STATUS" : "GI",              # GIn
                             "GET_MODBUS_MESSAGE" : "GM",
                             "GET_CANBUS_MESSAGE" : "GC",
                             "INTERRUPT_RESPONSE" : "I",                     # In
                     }

microcontroller_command_mapping_list_one = ["CSR", "SDA", "SAA", "SRA", "SRVA", "SPA", "SPVA", "SIA"] #value
microcontroller_command_mapping_list_two = ["GD", "GDV", "GDT", "GDH", "GA", "GAV", "GR", "GRV", "GP", "GPV", "GI", "I"] # pin
microcontroller_command_mapping_list_three = ["SD", "SA", "SR", "SRV", "SP", "SPV", "SI"] # pin + value

def parser_command(command):
    print ("========== In Request Parser Command ==========")
    #print (command)
    try:
        type = command ['command']
        microcontrolller_command = command_mapping_dictionary[type]
        if microcontrolller_command in microcontroller_command_mapping_list_one:
            value = command ["value"]
            if (microcontrolller_command == 'SRVA' or microcontrolller_command == 'SPVA'):
                ig100_relay_pwm_value_store.all_relay_pwm_value_store(microcontrolller_command, value)
            return microcontrolller_command + value
        elif microcontrolller_command in microcontroller_command_mapping_list_two:
            pin = command ["pin"]
            #print (pin)
            return microcontrolller_command + pin
        elif microcontrolller_command in microcontroller_command_mapping_list_three:
            pin = command ["pin"]
            value = command ["value"]
            if (microcontrolller_command == 'SRV' or microcontrolller_command == 'SPV'):
                ig100_relay_pwm_value_store.single_relay_pwm_value_store(microcontrolller_command, pin, value)
            return microcontrolller_command + pin + value
        else:
            return microcontrolller_command
    except:
        message = "request command exception"
        event = "ig100_request_message_parser"
        ig100_logger.createErrorLog(message, event)

