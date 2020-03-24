import ig100_serial_configuration
import ig100_trigger
import ig100_logger
import time
import json

load_init = ig100_trigger.LoadConfigurationAndInit()
#print (load_init.mac)
l = []
k = []

def init_all_config(init_command):
    #print ('init_all_config')
    #print (init_command)
    #ser.write(init_command + '\n')
    ig100_serial_configuration.ser.write(init_command + '\n')
    #print ("Import")
    time.sleep(0.1)
    while True:
        if (ig100_serial_configuration.ser.inWaiting() > 0):
            value = ig100_serial_configuration.ser.read()
            if value == '\t':
                break
            elif ord(value) == 1:
                #print("initialized")
                l.append(ord(value))
                #print (l)
                #pass
            else:
                k.append(ord(value))
                #print (k)
                #print ('value')
                
                
def reset_intt():
    print ('========== Reset Intt ==========')
    init_all_config('SI040')
    init_all_config('SI050')
    init_all_config('SI100')
    init_all_config('SI110')
    
    
def reset_digital():
    print ('========== Reset Digital ==========')
    for i in range(12):
        if i < 10:
            init_command = 'SD0' + str(i) + '0'
            init_all_config (init_command )
        else:
            init_command = 'SD' + str(i) + '0'
            init_all_config (init_command )
                
                
def reset_analog():
    print ('========== Reset Analog ==========')
    for i in range(4):
        init_command = 'SA0' + str(i) + '0'
        init_all_config (init_command )
                
                
def reset_relay():
    print ('========== Reset Relay ==========')
    for i in range(4):
        init_command = 'SR0' + str(i) + '0'
        init_all_config (init_command )
                
                
def reset_pwm():
    print ('========== Reset PWM ==========')
    for i in range(4):
        init_command = 'SP0' + str(i) + '0'
        init_all_config (init_command )
                
                
def digital_initialized():
    print ("========== Initialize Digital ==========")
    try: 
        for digitals in load_init.digitals:
            #print (digitals['isConfigured'])
            if digitals['isConfigured'] == True:
                if digitals['isInterruptPin'] ==  True:
                    if digitals['setAsInterrupt'] == False:
                        if digitals['pin'] < 10:
                            #print ('SD0' + str(digitals['pin']) + '1')
                            init_command = 'SD0' + str(digitals['pin']) + '1'
                            init_all_config (init_command)
                        else:
                            #print ('SD' + str(digitals['pin']) + '1')
                            init_command = 'SD' + str(digitals['pin']) + '1'
                            init_all_config (init_command)
                else:
                    if digitals['pin'] < 10:
                        #print ('SD0' + str(digitals['pin']) + '1')
                        init_command = 'SD0' + str(digitals['pin']) + '1'
                        init_all_config (init_command)
                    else:
                        #print ('SD' + str(digitals['pin']) + '1')
                        init_command = 'SD' + str(digitals['pin']) + '1'
                        init_all_config (init_command)
            else:
                if digitals['pin'] < 10:
                    #print ('SD0' + str(digitals['pin']) + '0')
                    init_command = 'SD0' + str(digitals['pin']) + '0'
                    init_all_config (init_command)
                else:
                    #print ('SD' + str(digitals['pin']) + '0')
                    #print ('=================================10/11==========================')
                    init_command = 'SD' + str(digitals['pin']) + '0'
                    init_all_config (init_command)
                    
    except:
        message = "json load exception"
        event = "ig100_initialize_all"
        ig100_logger.createErrorLog(message, event)
        
        
def analog_initialized():
    print ("========== Initialize Analog ==========")
    for analog in load_init.analog:
        #print (analog['isConfigured'])
        #print (type(analog['isConfigured']))
        if analog['isConfigured'] == True:
            #print ('SA' + str(analog['pin']) + '1')
            init_command = 'SA' + str(analog['pin']) + '1'
            init_all_config (init_command)
        else:
            #print ('SA' + str(analog['pin']) + '0')
            init_command = 'SA' + str(analog['pin']) + '0'
            init_all_config (init_command)
            
            
def pwn_initialized():
    print ("========== Initialize PWM ==========")
    for pwm in load_init.pwm:
        #print (pwm['isConfigured'])
        if pwm['isConfigured'] == True:
            #print ('SP' + str(pwm['pin']) + '1')
            init_command = 'SP' + str(pwm['pin']) + '1'
            init_all_config (init_command)
        else:
            #print ('SP' + str(pwm['pin']) + '0')
            init_command = 'SP' + str(pwm['pin']) + '0'
            init_all_config (init_command)
            
            
def relay_initialized():
    print ("========== Initialize Relay ==========")
    for relay in load_init.relay:
        #print (relay['isConfigured'])
        if relay['isConfigured'] == True:
            #print ('SR' + str(relay['pin']) + '1')
            init_command = 'SR' + str(relay['pin']) + '1'
            init_all_config (init_command)
        else:
            #print ('SR' + str(relay['pin']) + '0')
            init_command = 'SR' + str(relay['pin']) + '0'
            init_all_config (init_command)
        
        
def interrupt_initialized():
    print ("========== Initialize Interrupt ==========")
    try:
        for digitals in load_init.digitals:
            #print (digitals['isInterruptPin'])
            if digitals['isConfigured'] == True:
                if digitals['isInterruptPin'] == True:
                    if digitals['pin'] < 10:
                        if (digitals['pin'] == 4 or digitals['pin'] == 5):
                            #print (digitals['setAsInterrupt'])
                            if digitals['setAsInterrupt'] == True:
                                #print (digitals['pin'])
                                #print ('SI0' + str(digitals['pin']) + '1')
                                init_command = 'SI0' + str(digitals['pin']) + '1'
                                init_all_config(init_command)
                                #print ("===================Interrupt4/5=============================")
                            else:
                                #print ('SI0' + str(digitals['pin']) + '0')
                                init_command = 'SI0' + str(digitals['pin']) + '0'
                                init_all_config (init_command)
                    else:
                        #print (digitals['setAsInterrupt'])
                        if digitals['setAsInterrupt'] == True:
                            #print ('SI' + str(digitals['pin']) + '1')
                            init_command = 'SI' + str(digitals['pin']) + '1'
                            init_all_config (init_command)
                        else:
                            #print ('SI' + str(digitals['pin']) + '0')
                            init_command = 'SI' + str(digitals['pin']) + '0'
                            init_all_config (init_command)
                    
    except:
        message = "json load exception"
        event = "ig100_initialize_all"
        ig100_logger.createErrorLog(message, event)
        
        
#if __name__ == "__main__":

#digital_initialized()
#analog_initialized()
#pwn_initialized()
#relay_initialized()
#interrupt_initialized()