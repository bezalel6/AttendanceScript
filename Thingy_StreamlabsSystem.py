#---------------------------
#   Import Libraries
#---------------------------
import os
import sys
import json
sys.path.append(os.path.join(os.path.dirname(__file__), "lib")) #point at lib folder for classes / references


import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#   Import your Settings class
from Settings_Module import MySettings



# PERMISSION = "moderator"

# START_CMD = "!attend-start"
# HELP_CMD = "!attend"
# STOP_CMD = "!attend-stop"
# LIST_ATTENDING = "!attend-list"
# ATTEND_CMD = ["o7","brodyt1hey"]

# ATTENDED_MSG = "thank you for attending!"
# NOT_ATTENDING_MSG = "the streamer is not taking attendence at the moment"

# START_MSG = "attendence started! type "
# for c in ATTEND_CMD:
#     START_MSG+= c+" "
# START_MSG += "to attend"

# STOP_MSG = "attendence stopped"

# HELP ="""
# once attendence has started, you can type {0} to attend.
# type {1} to see currently attending users.
# {2}s can control attendence by {3} to start taking attendence, and {4} to stop.
# """.format(' '.join(ATTEND_CMD),LIST_ATTENDING,PERMISSION,START_CMD,STOP_CMD).replace('\n',' ')

#---------------------------
#   Define Global Variables
#---------------------------
global SettingsFile
SettingsFile = ""
global ScriptSettings
ScriptSettings = MySettings()

global Attending
Attendind = []

isTakingAttendence = False

#---------------------------
#   [Required] Script Information
#---------------------------
ScriptName = "Thingy Script"
Website = "https://www.twitch.tv/brodytheginger"
Description = ""
Creator = "bezalel6"
Version = "1.0.0.0"

#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
def Init():
    global ScriptSettings
    #   Create Settings Directory
    directory = os.path.join(os.path.dirname(__file__), "Settings")
    if not os.path.exists(directory):
        os.makedirs(directory)

    #   Load settings
    SettingsFile = os.path.join(os.path.dirname(__file__), "Settings\settings.json")
    ScriptSettings = MySettings(SettingsFile)

    # ScriptSettings.Response = "Overwritten pong! ^_^"
    return


#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------
def Execute(data):
    global isTakingAttendence, Attendind


    if data.IsChatMessage():
        cmd=data.Message.lower()
        res=""
        if cmd in ScriptSettings.AttendCmds:
            if isTakingAttendence:
                res=ScriptSettings.AttendMessage
                if not data.User in Attendind:
                    Attendind.append(data.User)
                if res!="":
                    res+=" attending: "+", ".join(Attendind)
            # else:
                # res=NOT_ATTENDING_MSG

        elif cmd==ScriptSettings.ListAttending:
            
            res="attending: "+" ".join(Attendind)
        elif cmd==ScriptSettings.HelpCmd:
            res=ScriptSettings.HelpMessage

        elif Parent.HasPermission(data.User, ScriptSettings.Permission, ScriptSettings.UserSpecific):
            if cmd==ScriptSettings.StartCmd:
                isTakingAttendence = True
                Attendind = []
                res = ScriptSettings.StartMessage
            elif cmd==ScriptSettings.StopCmd:
                isTakingAttendence = False
                res=ScriptSettings.StopMessage
                
       
        if res!="":
            Parent.SendStreamMessage(res)    # Send your message to chat 
    
    return

#---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
#---------------------------
def Tick():
    return

#---------------------------
#   [Optional] Parse method (Allows you to create your own custom $parameters) 
#---------------------------
def Parse(parseString, userid, username, targetid, targetname, message):
    return parseString

#---------------------------
#   [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
#---------------------------
def ReloadSettings(jsonData):
    global ScriptSettings
    # raise RuntimeError(' '.join(dir(jsonData)))
    # Execute json reloading here
    ScriptSettings.__dict__ = json.loads(jsonData)
    ScriptSettings.Save(SettingsFile)
    #   Create Settings Directory
    directory = os.path.join(os.path.dirname(__file__), "Settings")
    if not os.path.exists(directory):
        os.makedirs(directory)

    #   Load settings
    SettingsFile = os.path.join(os.path.dirname(__file__), "Settings\settings.json")
    ScriptSettings = MySettings(SettingsFile)

    return

#---------------------------
#   [Optional] Unload (Called when a user reloads their scripts or closes the bot / cleanup stuff)
#---------------------------
def Unload():

    return

#---------------------------
#   [Optional] ScriptToggled (Notifies you when a user disables your script or enables it)
#---------------------------
def ScriptToggled(state):
    return
