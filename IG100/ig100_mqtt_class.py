import ig100_response_message_parser
import ig100_trigger
import os
import paho.mqtt.client as mqtt
import json, ast
import commands
import ig100_callback_queue
import ig100_logger
from threading import Thread

mac_id = commands.getstatusoutput('cat /sys/class/net/eth0/address')[1].replace(':','')
request_topic = "/ig100/{0}/request".format(str(mac_id))
response_topic = "/ig100/{0}/response".format(str(mac_id))
response_topic_trigger = "/ig100/{0}/trigger".format(str(mac_id))

print ("========== " + str(mac_id) + " ==========")

trigger = ig100_trigger.Trigger()

#MQTT server
mqtt_server_host = "localhost"
#mqtt_server_host = "13.59.190.62"
#mqtt_server_host = "broker.mqttdashboard.com"
mqtt_server_port = 1883
#mqtt_server_port = 8000
mqtt_keepalive   = 60

message_topic = ''
request_message_dictionary = {}
serial_data_queue = []
formatted_interrupt_response = ''

class IG100CommandProcessor:
    commands_topic = ""
    processed_commands_topic = ""
    active_instance = None

    def __init__(self, name):
        self.name  = name
        IG100CommandProcessor.commands_topic = request_topic
        IG100CommandProcessor.processed_commands_topic = response_topic
        IG100CommandProcessor.processed_commands_topic_trigger = response_topic_trigger
        self.client = mqtt.Client(protocol=mqtt.MQTTv311)
        IG100CommandProcessor.active_instance = self
        self.client.on_connect = IG100CommandProcessor.on_connect
        self.client.on_message = IG100CommandProcessor.on_message
        self.client.connect(host = mqtt_server_host, port = mqtt_server_port, keepalive = mqtt_keepalive)
        self.client.loop_start()

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        print("========== Connected to MQTT Server ==========")
        client.subscribe(IG100CommandProcessor.commands_topic, qos= 0)

    @staticmethod
    def on_message(client, userdata, msg):
        #if msg.topic == IG100CommandProcessor.commands_topic:
        print ("========== In Callback ==========")
        global request_message_dictionary
        global trigger
        try:
            request_message_dictionary = ast.literal_eval(msg.payload)
            
            if request_message_dictionary["payload"]["command"] == "TRIGGER_RELOAD":
                trigger = ig100_trigger.Trigger()
                print ("========== Trigger Reload ==========")
                #print ("========== ", trigger)
            else:
                s = ig100_callback_queue.WriteToSerial()
                t = Thread(target = s.run, args =(request_message_dictionary, )) 
                t.start()
        except:
            error_message = "json load exception in callback"
            event = "ig100_initialize_all"
            ig100_logger.createErrorLog(error_message, event)

    def publish_response_message(self, message):
        #print ('publish_response_message in parse_class.py')
        formatted_response = ''
        try: 
            formatted_response = ig100_response_message_parser.response_parser(message, request_message_dictionary)
            self.client.publish(topic = self.__class__.processed_commands_topic, payload = formatted_response)
        except:
            error_message = "publish response message exception"
            event = "ig100_mqtt_class"
            ig100_logger.createErrorLog(error_message, event)
            #with open('/root/IG100_Microprocessor_Script_1/log.json', 'a') as log:
                #json.dump('response paser error', log)
        '''if (request_message_dictionary['message_uid'] == 'TID'):
            self.client.publish(topic = self.__class__.processed_commands_topic_trigger, payload = formatted_response)
            # publish to trigger topoic
        else:
            self.client.publish(topic = self.__class__.processed_commands_topic, payload = formatted_response)
            # publish to response topic'''

    def publish_interrupt_message(self, value_list):
        print ("========== Interrupt Call ==========")
        formatted_interrupt_response = ''
        formatted_interrupt_response = ig100_response_message_parser.interrupt_parser(value_list)
        #print (formatted_interrupt_response)
        #print (value_list[0])
        trigger.checkInterruptTrigger(value_list[0])
        self.client.publish(topic = self.__class__.processed_commands_topic, payload = formatted_interrupt_response)

    def publish_interval_message(self, value_list):
        print ('========== Interval Call ==========')
        formatted_all_response = ig100_response_message_parser.all_pin_value(value_list)
        print ("========== Trigger in Interval ==========")
        #print ("========== ", trigger)
        trigger.checkCondition(formatted_all_response)
        self.client.publish(topic = self.__class__.processed_commands_topic, payload = formatted_all_response)

    def process_commands(self):
        self.client.loop()
