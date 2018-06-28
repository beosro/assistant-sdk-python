import os
            
def toggleDevice(voice_command):
        devices = ["light","television","xbox","piano"]
        modes = ["on","off"]
        for mode in modes:
            for device in devices:
                    if device in voice_command and mode in voice_command:
                            #self.say("okay, turning " + device + " " + mode)
                            os.system("sudo python /var/www/html/433.py " + mode + " " + device)
                            print(device,mode)
