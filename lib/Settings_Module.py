import os
import codecs
import json

class MySettings(object):
	def __init__(self, settingsfile=None):
		try:
			with codecs.open(settingsfile, encoding="utf-8-sig", mode="r") as f:
				self.__dict__ = json.load(f, encoding="utf-8")
		except Exception as e:
			if(settingsfile):raise e
			self.Permission = "moderator"
			self.UserSpecific = ""
			self.AttendCmds="o7 brodyt1hey".split(' ')
			self.AttendMessage='Thank you for attending!'
			self.HelpMessage =  "once attendence has started, you can type o7 brodyt1hey to attend. type !attend-list to see currently attending users. moderators can control attendence by !attend-start to start taking attendence, and !attend-stop to stop.sss"
			self.HelpCmd="!attend"
			self.ListAttending='!attend-list'
			self.StartCmd='!attend-start'
			self.StartMessage='attendance started!'
			self.StopCmd='!attend-stop'
			self.StopMessage='attendance stopped!'
			self.ExportPath=''
			



	def Reload(self, jsondata):
		self.__dict__ = json.loads(jsondata, encoding="utf-8")
		return

	def Save(self, settingsfile):
		# raise RuntimeError(" ".join(dir(settingsfile)))
		try:
			with codecs.open(settingsfile, encoding="utf-8-sig", mode="w+") as f:
				json.dump(self.__dict__, f, encoding="utf-8")
			with codecs.open(settingsfile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
				f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8')))
		except Exception as e:
			# Parent.Log(ScriptName, "Failed to save settings to file.")
			raise e
		return