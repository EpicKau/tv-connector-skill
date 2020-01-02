# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# 


from mycroft.messagebus.message import Message
from mycroft.skills.core import MycroftSkill, intent_handler
from adapt.intent import IntentBuilder
from mycroft.util.log import LOG
from mycroft import intent_file_handler
from wakeonlan import send_magic_packet

import samsungctl
import time
import socket
import websocket
import json

class TvConnector(MycroftSkill):

    def startTv(self):
        self.log.info("startTv")
        send_magic_packet(self.settings["tv_mac"])

    def stopTv(self):
        self.log.info("stopTv")

        try:
            with samsungctl.Remote(self.config) as remote:
                remote.control("KEY_POWER")
            return True

        except socket.error:
            return False
        except websocket._exceptions.WebSocketConnectionClosedException:
            self.log.info('Websocket error! Maybe try sending with legacy?')
            return False

    def getAppId(self, name):
        self.log.info("getAppId")
        apps = self.settings.get("tv_apps")

        apps = json.loads(apps)
        if(apps):
            for app in apps:
                print(app["name"])
                if(app["name"].lower() == name.lower()):
                    return app["appId"]
            return 0

    def startApp(self, name):
        self.log.info("startApp")

        appId = self.getAppId(name)
        if not (appId):
            self.log.info("no appId found")
        else:
            self.log.info(appId)

            try:
                with samsungctl.Remote(self.config) as remote:
                    remote.launch(appId)
                    return True

            except socket.error:
                return False
            except websocket._exceptions.WebSocketConnectionClosedException:
                self.log.info('Websocket error! Maybe try sending with legacy?')
                return False

    def getApps(self):
        self.log.info("getApps")

        try:
            with samsungctl.Remote(self.config) as remote:
                apps = remote.get_installed_apps()
                apps = json.loads(apps)

                if(apps):
                    installed_apps = []
                    for app in apps["data"]:
                        installed_apps += [{"appId": app["appId"], "name": app["name"]}]

                    self.settings["tv_apps"] = json.dumps(installed_apps)
                    #print(json.dumps(installed_apps))
            return True

        except socket.error:
            return False
        except websocket._exceptions.WebSocketConnectionClosedException:
            self.log.info('Websocket error! Maybe try sending with legacy?')
            return False

    def __init__(self):
        MycroftSkill.__init__(self)
        self.settings.get('tv_mac')
        self.settings.get('tv_ip')
        self.settings.get('tv_type')
        self.settings.get('tv_port')
        self.settings.get('tv_name')
        self.log.info("tv_mac: " + self.settings["tv_mac"])
        self.log.info("tv_ip: " + self.settings["tv_ip"])
        self.log.info("tv_type: " + self.settings["tv_type"])
        self.log.info("tv_port: " + self.settings["tv_port"])
        self.log.info("tv_name: " + self.settings["tv_name"])

        self.config = {
            "name": self.settings["tv_name"],
            "mac": self.settings["tv_mac"],
            "host": self.settings["tv_ip"],
            "port": self.settings["tv_port"],
            "method": self.settings["tv_type"],
            "timeout": 5
        }

    @intent_handler(IntentBuilder("StartIntent").require("device"))
    def handle_start_tv_intent(self, message):
        self.startTv()
        self.speak_dialog("default")

    @intent_handler(IntentBuilder("StopIntent").require("device"))
    def handle_stop_tv_intent(self, message):
        self.stopTv()
        self.speak_dialog("default")

    @intent_handler(IntentBuilder("").require("start").one_of("apps"))
    def handle_start_app_intent(self, message):
        app = message.data.get('apps')
        self.startApp(app)

def create_skill():
    return TvConnector()

