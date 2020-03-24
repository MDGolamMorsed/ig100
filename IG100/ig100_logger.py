# Logger to log error, warning, and success action
# of ig100
import time
import json 


class Logger():
    def __init__(self, log_type, message, event):
        fileUrl = "/usr/lib/lua/luci/log/syslog.json"
        try: 
            with open(fileUrl, 'r') as myfile:
                data = myfile.read()
            self.logs = json.loads(data)
            currentLog = {
                'logType': log_type,
                'message': message,
                'event': event,
                'time': time.time(),
            }
            
            self.logs.insert(0, currentLog)

            if(len(self.logs) >= 100): 
                del self.logs[-1]
            
            with open(fileUrl, 'w') as outfile:
                json.dump(self.logs, outfile)
        except: 
            print("Json load error, create new json file") 
            with open(fileUrl, 'w') as outfile:
                json.dump([], outfile)


def createErrorLog(message, event):
    Logger('error', message, event)

def createWarningLog(message, event):
    Logger('warning', message, event)

def createSuccessLog(message, event):
    Logger('success', message, event)



## Test 

if __name__ == "__main__": 
    for i in range(10): 
        print("running in loop --- " + str(i))    
        createErrorLog('new error log for test' + str(i), 'test')