'''this function parse the regular request command and write the microcontroller command to the serial'''
import ig100_request_message_parser
import ig100_serial_configuration
import ig100_logger
import json

class WriteToSerial: 
    def __init__(self): 
        self._running = True
      
    def terminate(self): 
        self._running = False
          
    def run(self, request_message_dictionary): 
        try:
            #while request_message_dictionary in serial_data_queue:
            #print (request_message_dictionary)
            command = request_message_dictionary['payload']
            microcontroller_command_from_parser = ig100_request_message_parser.parser_command(command)
            print ('========== In Callback Serial Write ==========')
            print (microcontroller_command_from_parser)
            ig100_serial_configuration.ser.write(microcontroller_command_from_parser + '\n')
            self.terminate()
        except:
            #with open('/root/IG100_Microprocessor_Script_1/log.json', 'a') as log:
            message = "request parser or serial write error"
            event = "ig100_callback_queue"
            ig100_logger.createErrorLog(message, event)
            #with open('/root/IG100/log.json', 'a') as log:
                #json.dump('request parser or serial write error', log)
            self.terminate()
