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

import time

from mycroft.messagebus.message import Message
from mycroft.skills.core import MycroftSkill, intent_handler
from adapt.intent import IntentBuilder
from mycroft.util.log import LOG
from mycroft import intent_file_handler



class TvConnector(MycroftSkill):

	def __init__(self):
		super(TvConnector, self).__init__(name="TvConnector")

	def initialize(self):
		self.log.info("Tv Connector: Initializing")

	def startTv(self):
		self.log.info("Tv Connector: startTv")

	def stopTv(self):
		self.log.info("Tv Connector: stopTv")


	@intent_handler(IntentBuilder("").require("device").require("start_tv"))
	def handle_start_tv_intent(self, message):
		self.startTv()
		self.speak_dialog("default")

	@intent_handler(IntentBuilder("").require("device").require("stop_tv"))
	def handle_stop_tv_intent(self, message):
		self.stopTv()
		self.speak_dialog("default")

def create_skill():
	return TvConnector()
