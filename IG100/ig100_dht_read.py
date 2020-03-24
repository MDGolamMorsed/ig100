'''this function reads dht pin and dht values'''
import ig100_serial_configuration
import ig100_trigger
import ig100_logger
import json

load = ig100_trigger.LoadConfigurationAndInit()

def get_dht_temperature_humidity():
    dht_pin_list = []
    dht_temperature_humidity_value_list = []
    print ("========== DHT Read ==========")
    try:
        for digital_sensor in load.digitals:
            #print (digital_sensor['isConfigured'])
            if digital_sensor['isConfigured'] == True:
                if digital_sensor['configuration']['sensor_uid'] == 'DHT_11':
                    dht_pin_list.append(digital_sensor['pin'])
                    try:
                        #print ("-----------------")
                        ig100_serial_configuration.ser.write('GDT0' + str(digital_sensor['pin']) + '\n')
                        while True:
                                if (ig100_serial_configuration.ser.inWaiting() > 0):
                                    value = ig100_serial_configuration.ser.read()
                                    if value == '\t':
                                        break
                                    else:
                                        dht_temperature_humidity_value_list.append(ord(value))
                                        #print (dht_temperature_humidity_value_list)
                        ig100_serial_configuration.ser.write('GDH0' + str(digital_sensor['pin']) + '\n')
                        while True:
                                if (ig100_serial_configuration.ser.inWaiting() > 0):
                                    value = ig100_serial_configuration.ser.read()
                                    if value == '\t':
                                        break
                                    else:
                                        dht_temperature_humidity_value_list.append(ord(value))
                                        #print (dht_temperature_humidity_value_list)
                    except:
                        message = "serial exception"
                        event = "ig100_dht_read"
                        ig100_logger.createErrorLog(message, event)
                        #print ("serial exception")
                        #with open('/root/IG100/log.json', 'a') as log:
                            #json.dump("serial exception in dht", log)
    except:
        message = "json load exception"
        event = "ig100_dht_read"
        ig100_logger.createErrorLog(message, event)
        #print ("json load exception in dht")
        #with open('/root/IG100/log.json', 'a') as log:
            #json.dump("json load exception in dht", log)
            
    
    return dht_pin_list, dht_temperature_humidity_value_list
