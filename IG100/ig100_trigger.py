import json
import os
import time
#import Logger
import ig100_logger
import commands

class LoadConfigurationAndInit():
    def __init__(self):
        print("loading initial configuration")
        fileUrl = "/usr/lib/lua/luci/config/config.json"
        with open(fileUrl, 'r') as myfile:
            data = myfile.read()
        self.config = json.loads(data)
        mac_id = commands.getstatusoutput('cat /sys/class/net/eth0/address')[1].replace(':','')
        self.config['mac'] = mac_id
        
        with open(fileUrl, 'w') as myfile:
            json.dump(self.config, myfile)
        
        with open(fileUrl, 'r') as myfile:
            data = myfile.read()
        self.config = json.loads(data)
        
        self.prevOutputState = {
            'pwm': [0, 0, 0, 0],
            'relay': [0, 0, 0, 0], 
        }
        
        self.mac = self.config['mac']
        self.inputs = self.config['inputs']
        self.outputs = self.config['outputs']
        self.digitals = self.inputs['digitals']
        self.analog = self.inputs['analog']
        self.pwm = self.outputs['pwm']
        self.relay = self.outputs['relay']
        self.triggers = self.config['triggers']
        self.notifications = self.config['notifications']
        self.input_map = {}
        self.output_map = {}
        self.sensordata = {}

        self.trigger_prev_times_map = {}
        self.notification_prev_times_map = {}
        self.isFirstTime = True 
        
        for k in self.digitals:
            self.input_map[k['uid']] = k
        for k in self.analog:
            self.input_map[k['uid']] = k 
        for k in self.pwm:
            self.output_map[k['uid']] = k 
        for k in self.relay:
            self.output_map[k['uid']] = k 
        for t in self.triggers:
            self.trigger_prev_times_map[t] = time.time()
        
        




class Trigger(LoadConfigurationAndInit):
    
    def checkCondition(self, sensordata):
        self.sensordata = json.loads(sensordata.replace("'", "\""))
        self.sensordata = self.sensordata['payload']
        if(len(self.triggers) > 0): 
            for k in self.triggers: 
                triggerTime = int( self.triggers[k]['triggertime'] )
                isPause = self.triggers[k]['isPause']
                if not isPause: 
                    passed_time = time.time() - self.trigger_prev_times_map[k]
                    print("trigger id", k, "trigger time", triggerTime, "passed time", passed_time)
                    if self.isFirstTime or ((passed_time >= triggerTime) or ((passed_time + 3) >= triggerTime)): 
                        self.isFirstTime = False
                        self.trigger_prev_times_map[k] = time.time()
                        print("time true is for check condition")
                        self.__checkATriggerInputData(k)
                        


    def checkInterruptTrigger(self, pin): 
        print ("======================================= CheckInterruptTrigger ======================================")
        interrupt_pin_uid = ['digital5', 'digital6', 'digital11', 'digital12'][pin]
        if(len(self.triggers) > 0): 
            for k in self.triggers: 
                condition_inputs = self.triggers[k]['inputs']
                inputs_len = len(condition_inputs)
                if ((inputs_len == 1) and (interrupt_pin_uid == condition_inputs[0])) :
                    print("--------------- Calling Trigger for Interrupt ------------")
                    outputs = self.triggers[k]['outputs']
                    for index in range(len(outputs)): 
                        self.__checkOutputState(outputs[index])


    def __checkATriggerInputData(self, triggerUID): 
        print('Trigger ID: ',triggerUID)
        conditionStatus = []
        inputs = self.triggers[triggerUID]['inputs']
        outputs = self.triggers[triggerUID]['outputs']
        joins = self.triggers[triggerUID]['join_by']
        input_len = len(inputs)
        join_len = len(joins)
        if(input_len > 0):
            isConditionTrue = True
            for index in range(input_len):
                conditionStatus.append(self.__checkSingleTriggerCondition(triggerUID, inputs[index], index, input_len))
                
            andIndexes = [i for i,x in enumerate(joins) if x == 'and']
            andIndexLen = len(andIndexes)

            for index in andIndexes:
                andResult = (self.__checkJoinCondition(joins[index], conditionStatus[index], conditionStatus[index+1]))
                print ('AND' + 'RESULT' + str(andResult))
                conditionStatus[index] = andResult
                del conditionStatus[index+1]

                for i in range(andIndexLen):
                    andIndexes[i] = andIndexes[i] - 1
            
            if True in conditionStatus:
                print('Conditions have met!')
                isConditionTrue = True
            else:
                print('Conditions have not met!')
                isConditionTrue = False

            if isConditionTrue: 
                for index in range(len(outputs)): 
                    if outputs[index]['type'] == "output":
                        self.__checkOutputState(outputs[index])
                    elif outputs[index]['type'] == "notification":
                        self._checkNotification(outputs[index]['uid'])

    def _checkNotification(self, not_uid):
        notification = self.notifications[not_uid]
        interval = int(self.notifications[not_uid])
        current_time = 0

        if self.notification_prev_times_map[not_uid] == None: 
            current_time = time.time() - self.notification_prev_times_map[not_uid]['time'] 
        else: 
            self.notification_prev_times_map[not_uid] = {
                time: time.time(), 
                isFirstTime: True,
            }
        isFirstTime = self.notification_prev_times_map[not_uid]['isFirstTime']
        if current_time >= interval or isFirstTime: 
            self.notification_prev_times_map[not_uid]['time'] = time.time()
            self.notification_prev_times_map[not_uid]['isFirstTime'] = False
            print("current notification --------- ")
            print(notification)
            not_type = notification['type']
            if not_type == "sms": 
                self._sendSMS(notification)
            elif not_type == "mail":
                self._sendMail(notification)
            elif not_type == "broker":
                self._publishToBroker(notification)


    def _sendSMS(self, smsdata): 
        print("--------- Sending Sms ----------------")
        url = "http://66.45.237.70/api.php";
        number= smsdata['sms_no'];
        text= smsdata['text'] + "\n\n"
        payload = "username=01718109528&password=MZ4P8SRB&number="+number+"&message="+text

        r = 'curl -d "'+ payload +'" -X POST ' + url 
        os.system(r)
        ig100_logger.createSuccessLog('A New SMS ' + text + 'Sended to' + number, 'Trigger::SMS Send')
        

    def _sendMail(self, mailData): 
        print("--------- Sending MAIL ----------------")
        ig100_logger.createSuccessLog('A New Mail Sended', 'Trigger::Mail Sended')

    def _publishToBroker(self, brokerData): 
        print("--------- Publish To Broker ----------------")
        ig100_logger.createSuccessLog('A New Data Publish To Broker', 'Trigger::Broker Publish')


    def __checkSingleTriggerCondition(self, triggerUID, inpuid, index, input_len):
        _input = self.input_map[inpuid]
        _input_pin = _input['pin']
        condition = self.triggers[triggerUID]['condition'][index]
        condition_value = self.triggers[triggerUID]['condition_value'][index]
        condition_value = int(condition_value)
  
        if(_input['type'] == 'digital'):
            data = self.sensordata['digitals'][_input_pin][0]
            print ("DATA" + str(data))
            return self.__checkSingleCondition(condition, condition_value, data)
        elif (_input['type'] == 'analog'):
            data = self.sensordata['analog'][_input_pin]
            return self.__checkSingleCondition(condition, condition_value, data)
        return False

    def __checkJoinCondition(self, condition, data1, data2):
        if condition == 'and':
            return data1 and data2
        if condition == 'or':
            return data1 or data2
        return False
    
    def __checkSingleCondition(self, condition, condition_value, data):
        if condition == 'greater_than': 
            if(data > condition_value): 
                return True
        elif condition == 'less_than':
            if(data < condition_value): 
                return True
        elif condition == 'equal_to':
            if(data == condition_value): 
                return True
        elif condition == 'greater_or_equal':
            if(data >= condition_value): 
                return True
        elif condition == 'less_or_equal':
            if(data <= condition_value): 
                return True
        return False


    def __checkOutputState(self, output): 
        output_uid = output['uid']
        set_value = output['set_value']
        output = self.output_map[output_uid]
        pin = output['pin']
        print("check output state called: output", output);
        if output['type'] == 'relay':
            # data = self.sensordata['relay'][pin]
            self.__controlOutput('relay', pin, set_value)
            # self.prevOutputState['relay'][pin] = data
        elif output['type'] == 'pwm':
            # data = self.sensordata['pwm'][pin]
            self.__controlOutput('pwm', pin, set_value)
            # self.prevOutputState['pwm'][pin] = data
        

    def __controlOutput(self, name, pin, status):
        print("controlled output called", name, pin, status)
        message_json = {
            'payload': {
                'command': "SET_PWM_PIN_VALUE",
                'pin': str(pin), 
                'value': status   
            },
            'message_uid': '00001',
        }
        if name == 'pwm': 
            message = json.dumps(message_json)
            command = "mosquitto_pub -t '/ig100/"+ self.mac +"/request' -m '" + message + "'"
            print(command)
            os.system(command)
            ig100_logger.createSuccessLog('PWM Control '+ command, 'Trigger::PWM Control')
        elif name == 'relay': 
            message_json['payload']['command'] = "SET_RELAY_PIN_VALUE"
            message = json.dumps(message_json)
            command = "mosquitto_pub -t '/ig100/"+ self.mac +"/request' -m '" + message + "'"
            print(command)
            os.system(command)
            ig100_logger.createSuccessLog('Relay Control '+ command, 'Trigger::Relay Control')




## test   
'''
    if __name__ == "__main__":
        trigger = Trigger()
        trigger.checkCondition({
            'digitals': [110,0,0,0,0,0,1,1,1,0,0,1],
            'analog': [650,810,520,0],
            'pwm': [80,0,25,30],
            'relay': [0,0,0,0]
        })

        trigger.checkInterruptTrigger(0)

'''
