#!/usr/bin/env python

# Copyright (C) 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import os
from modes import Mode
from actions import *
import sys
import time
import argparse
import json
import os.path
import pathlib2 as pathlib
from datetime import datetime
import google.oauth2.credentials

from google.assistant.library import Assistant
from google.assistant.library.event import EventType
from google.assistant.library.file_helpers import existing_file
from google.assistant.library.device_helpers import register_device
from google.assistant.embedded.v1alpha2 import *

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


WARNING_NOT_REGISTERED = """
    This device is not registered. This means you will not be able to use
    Device Actions or see your device in Assistant Settings. In order to
    register this device follow instructions at:

    https://developers.google.com/assistant/sdk/guides/library/python/embed/register-device
"""

class VoiceAssistant:
    def __init__(self):
        print("Initialising")
	if len(sys.argv) > 1:
		os.system("sudo /home/pi/PiBits/ServoBlaster/user/./servod")
		os.system("sudo pigpiod")

    def speak(self,m):
	os.system("espeak -s 135 -v en -p 50 '" + str(m) + "'  --stdout | aplay -c1 -D plughw:1,0")
	#os.system("espeak -s 135 -v en -p 50 '" + str('hi') + "'") 
    def welcome(self):
	hour = datetime.now().hour

        if(hour < 12):
           self.speak("Good morning, how can I help?")

        if(hour < 16 & hour > 12):
           self.speak("Good afternoon, how can I help?")

        if (hour >= 16):
           self.speak("Good evening, how can I help?")

    def process_event(self,event):
        """Pretty prints events.

        Prints all events that occur with two spaces between each new
        conversation and a single space between turns of a conversation.

        Args:
            event(event.Event): The current event to process.
        """
        if event.type == EventType.ON_CONVERSATION_TURN_STARTED:
            print()
	if event.type == EventType.ON_RESPONDING_STARTED or EventType.ON_RESPONDING_FINISHED:
	    print(event.type)	
        if (event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and
                event.args):
            c = event.args['text']
            self.actions.checkCommand(c, "goog")

	if (event.type == EventType.ON_RENDER_RESPONSE and event.args):
	    resp = event.args['text']
	    #try:
		#self.speak(resp)
	    #except:
		#self.speak('Sorry, there was an error')
	           
        if (event.type == EventType.ON_CONVERSATION_TURN_FINISHED and
                event.args and not event.args['with_follow_on_turn']):
            print()
        if event.type == EventType.ON_DEVICE_ACTION:
            for command, params in event.actions:
                print('Do command', command, 'with params', str(params))

    def main(self):
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('--device-model-id', '--device_model_id', type=str,
                            metavar='DEVICE_MODEL_ID',default="abcdefghi", required=False,
                            help='the device model ID registered with Google')
        parser.add_argument('--project-id', '--project_id', type=str,
                            metavar='PROJECT_ID',default="finalassistant", required=False,
                            help='the project ID used to register this device')
        parser.add_argument('--device-config', type=str,
                            metavar='DEVICE_CONFIG_FILE',
                            default=os.path.join(
                                os.path.expanduser('~/.config'),
                                'googlesamples-assistant',
                                'device_config_library.json'
                            ),
                            help='path to store and read device configuration')
        parser.add_argument('--credentials', type=existing_file,
                            metavar='OAUTH2_CREDENTIALS_FILE',
                            default=os.path.join(
                                os.path.expanduser('~/.config'),
                                'google-oauthlib-tool',
                                'credentials.json'
                            ),
                            help='path to store and read OAuth2 credentials')
        parser.add_argument('-v', '--version', action='version',
                            version='%(prog)s ' + Assistant.__version_str__())
	parser.add_argument('-x','--abcd')

        args = parser.parse_args()
        with open(args.credentials, 'r') as f:
            credentials = google.oauth2.credentials.Credentials(token=None,
                                                                **json.load(f))

        device_model_id = None
        last_device_id = None
        try:
            with open(args.device_config) as f:
                device_config = json.load(f)
                device_model_id = device_config['model_id']
                last_device_id = device_config.get('last_device_id', None)
        except FileNotFoundError:
            pass

        if not args.device_model_id and not device_model_id:
            raise Exception('Missing --device-model-id option')

        # Re-register if "device_model_id" is given by the user and it differs
        # from what we previously registered with.
        should_register = (
            args.device_model_id and args.device_model_id != device_model_id)

        device_model_id = args.device_model_id or device_model_id
        with Assistant(credentials, device_model_id) as assistant:
            self.assistant = assistant
            self.actions = Actions(self.assistant)
            events = self.assistant.start()
            

            device_id = assistant.device_id
            print('device_model_id:', device_model_id)
            print('device_id:', device_id + '\n')

            # Re-register if "device_id" is different from the last "device_id":
            if should_register or (device_id != last_device_id):
                if args.project_id:
                    register_device(args.project_id, credentials,
                                    device_model_id, device_id)
                    pathlib.Path(os.path.dirname(args.device_config)).mkdir(
                        exist_ok=True)
                    with open(args.device_config, 'w') as f:
                        json.dump({
                            'last_device_id': device_id,
                            'model_id': device_model_id,
                        }, f)
                else:
                    print(WARNING_NOT_REGISTERED)
            self.m = Mode(self)
                    
            #x = threading.Thread(target=m.start)
            #x.daemon = True
            #x.start()
            
            for event in events:
                self.process_event(event)
                self.m.changeVoiceMode(event)


if __name__ == '__main__':
    va = VoiceAssistant()
    va.main()
