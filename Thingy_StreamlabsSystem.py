# ---------------------------
#   Import Libraries
# ---------------------------

import json
import os
import sys
from time import time
# point at lib folder for classes / references
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))


from Settings_Module import MySettings
import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#   Import your Settings class

# ---------------------------
#   Define Global Variables
# ---------------------------
global SettingsFile
SettingsFile = ""
global ScriptSettings
ScriptSettings = MySettings()

global Attending
Attendind = []

isTakingAttendence = False

# ---------------------------
#   [Required] Script Information
# ---------------------------
ScriptName = "Thingy Script"
Website = "https://www.twitch.tv/brodytheginger"
Description = ""
Creator = "bezalel6"
Version = "1.0.0.0"

# ---------------------------
#   [Required] Initialize Data (Only called on load)
# ---------------------------


def Init():
    global ScriptSettings
    #   Create Settings Directory
    directory = os.path.join(os.path.dirname(__file__), "Settings")
    if not os.path.exists(directory):
        os.makedirs(directory)

    #   Load settings
    SettingsFile = os.path.join(os.path.dirname(
        __file__), "Settings\settings.json")
    ScriptSettings = MySettings(SettingsFile)
    # ScriptSettings.Response = "Overwritten pong! ^_^"
    return

def StartTaking():
    global isTakingAttendence, Attendind, MillisStart, MillisLeft
    isTakingAttendence = True
    Attendind = []
    MillisStart = time()
    MillisLeft = ScriptSettings.Time
    return ScriptSettings.StartMessage

def StopTaking():
    global isTakingAttendence, Attendind, MillisStart, MillisLeft
    # if not isTakingAttendence:
        # return ""
    MillisLeft = MillisStart = 0
    isTakingAttendence = False
    if ScriptSettings.ExportPath != "":
        path = ""+ScriptSettings.ExportPath
        if not path.endswith('.txt'):
            path += '.txt'
        with open(path, 'w') as f:
            f.write('\n'.join(Attendind))

    return ScriptSettings.StopMessage



# ---------------------------
#   [Required] Execute Data / Process messages
# ---------------------------
def Execute(data):
    global isTakingAttendence, Attendind

    if data.IsChatMessage():
        cmd = data.Message.lower()
        res = ""
        if cmd in ScriptSettings.AttendCmds:
            if isTakingAttendence:
                res = ScriptSettings.AttendMessage
                if not data.User in Attendind:
                    Attendind.append(data.User)
                if res != "":
                    res += " attending: "+", ".join(Attendind)
            # else:
                # res=NOT_ATTENDING_MSG

        elif cmd == ScriptSettings.ListAttending:

            res = "attending: "+" ".join(Attendind)
        elif cmd == ScriptSettings.HelpCmd:
            res = ScriptSettings.HelpMessage

        elif Parent.HasPermission(data.User, ScriptSettings.Permission, ScriptSettings.UserSpecific):
            if cmd == ScriptSettings.StartCmd:
                res = StartTaking()
                
            elif cmd == ScriptSettings.StopCmd:
              res=StopTaking()
              
        if res != "":
            Parent.SendStreamMessage(res)    # Send your message to chat

    return

# ---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
# ---------------------------


global MillisLeft
MillisLeft=0
global MillisStart
MillisStart=0

def Tick():
    if isTakingAttendence and MillisLeft>0 and ScriptSettings.Time>0:
        elapsed = time()-MillisStart
        if elapsed>=MillisLeft:
            Parent.SendStreamMessage(StopTaking())

    return


# ---------------------------
#   [Optional] Parse method (Allows you to create your own custom $parameters)
# ---------------------------


def Parse(parseString, userid, username, targetid, targetname, message):
    return parseString

# ---------------------------
#   [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
# ---------------------------


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
    SettingsFile = os.path.join(os.path.dirname(
        __file__), "Settings\settings.json")
    ScriptSettings = MySettings(SettingsFile)
    return

# ---------------------------
#   [Optional] Unload (Called when a user reloads their scripts or closes the bot / cleanup stuff)
# ---------------------------


def Unload():

    return

# ---------------------------
#   [Optional] ScriptToggled (Notifies you when a user disables your script or enables it)
# ---------------------------


def ScriptToggled(state):
    return
