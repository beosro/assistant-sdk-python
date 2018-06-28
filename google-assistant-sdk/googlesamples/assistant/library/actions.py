import os

class Actions:
        def __init__(self, assistant):
                self.commands ={
                        "turn":self.toggleDevice
                    }
                self.assistant = assistant
                
        def checkCommand(self, c, source):
                for key in self.commands.iteritems():
                        if str(key[0]) in c:
                            if source == "goog":
                                    self.assistant.stop_conversation()
                            self.commands[key[0]](c)
                            break
                
        def toggleDevice(self, voice_command):
                devices = ["light","tv","television","xbox","piano"]
                modes = ["on","off"]
                c = voice_command.lower() 
                for mode in modes:
                    for device in devices:
                            if device in c and mode in c:
                                    #self.say("okay, turning " + device + " " + mode)
                                    os.system("sudo python /var/www/html/433.py " + mode + " " + device)
                                    print(device,mode)
