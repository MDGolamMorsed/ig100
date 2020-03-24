'''this is the main functio for the ig100 '''
import ig100_mqtt_class
import ig100_initialize_relay_pwm_value
import ig100_write_ir_ip_in_serial
import ig100_serial_configuration
import ig100_initialize_all
import ig100_logger
import time

general_update_interval= 10 #in seconds
now_time = 0
prev_time = 0

#-------------------------------------------------------- Reset All before initialize from config file -----------------------------------------------------------------------

ig100_initialize_all.reset_intt()
ig100_initialize_all.reset_digital()
ig100_initialize_all.reset_analog()
ig100_initialize_all.reset_relay()
ig100_initialize_all.reset_pwm()

#-------------------------------------------------------- Digital, Analog, Relay and PWM pin initialize from config file-------------------

ig100_initialize_all.digital_initialized()
ig100_initialize_all.analog_initialized()
ig100_initialize_all.pwn_initialized()
ig100_initialize_all.relay_initialized()
ig100_initialize_all.interrupt_initialized()

print ('========== Digital_Analog_Relay_PWM_Interrupt_Initialized ==========')

#--------------------------------------------------------relay and pwm value initialize----------------------------------------------------

IR = ig100_initialize_relay_pwm_value.initialize_relay_value()
#print (IR)
IP = ig100_initialize_relay_pwm_value.initialize_pwm_value()
#print (IP)

#--------------------------------------------------------main loop-----------------------------------------------------------------------

if __name__ == "__main__":
    ig100_serial_configuration.ser.write(IR + '\n')
    ig100_write_ir_ip_in_serial.ir_initialization()
    ig100_serial_configuration.ser.write(IP + '\n')
    ig100_write_ir_ip_in_serial.ip_initialization()
    ig100_command_processor = ig100_mqtt_class.IG100CommandProcessor("ig100_01")
    time.sleep(2)
    print ('========== Loading ==========')
    print ('========== IR and IP Initialized ==========')
    interrupt_message = ''
    while True:
        flag = False
        interval_flag = False
        response_flag = False
        value_list = []
        while True:
            try:
                now_time = int(time.time())
                if((now_time-prev_time)>=general_update_interval):
                    prev_time = now_time
                    ig100_serial_configuration.ser.write('CVA' + '\n')
                    interval_flag = True
                if (ig100_serial_configuration.ser.inWaiting() > 0):
                    value = ig100_serial_configuration.ser.read()
                    #print(ord(value))
                    if value == '\t':
                        #print("breaking ...")
                        break
                    else:
                        if flag == False:
                            if value == 'i':
                                flag = True
                                print (value)
                            elif interval_flag == True:
                                value_list.append(ord(value)) # interval_all_value
                                #print (value_list)
                            else:
                                value_list.append(ord(value)) # response_value
                                #print (value_list)
                                response_flag = True
                        else:
                            value_list.append(ord(value))
                            interval_flag = False
                            response_flag = False
                            #print (value_list)
                            ig100_command_processor.publish_interrupt_message(value_list)
            except:
                message = "serial read exception"
                event = "ig100_main"
                ig100_logger.createErrorLog(message, event)
                
        #ig100_command_processor.publish_response_message(value_list) # response_value_publish
        if interval_flag == True:
            print ("\n")
            print ("========== INTERVAL CALL ==========")
            ig100_command_processor.publish_interval_message(value_list) # response_all_value_publish
        elif response_flag == True:
            print ("\n")
            print ("========== RESPONSE CALL ==========")
            ig100_command_processor.publish_response_message(value_list) # response_value_publish
            #print (value_list)

