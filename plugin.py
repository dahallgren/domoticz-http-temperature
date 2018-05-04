# Domoticz plugin for reading temperature from http json data
#
# Author: Dan Hallgren
#
"""
<plugin key="httpjsontemperature" name="HTTP json temperature" version="0.1.0">
    <description>
        <h2>Temperature reading from json over HTTP</h2>
   </description>
    <params>
        <param field="Address" label="URL" width="200px" required="true"/>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal"  default="true" />
            </options>
        </param>
    </params>
</plugin>
"""
import json
import re
import urllib.request

import Domoticz


class HttpJsonTemperature:
    def __init__(self):
        self.interval = 30  # 5*6*10 seconds
        self.heartbeatcounter = 0

    def onStart(self):
        if Parameters["Mode6"] == "Debug":
            Domoticz.Debugging(1)
            DumpConfigToLog()

        temp_sensors = self.get_temperature_reading()

        if len(Devices) == 0 and temp_sensors:
            for i, sensor in enumerate(sorted(temp_sensors), start=1):
                # d_temp = Domoticz.Device(Name="temp_{}".format(sensor), Unit=i, Type=0xF3, Subtype=0x11, Used=1)
                d_temp = Domoticz.Device(Name="temp_{}".format(sensor), Unit=i, TypeName='Temperature', Used=0)
                d_temp.Create()
                d_temp.Update(int(temp_sensors[sensor]), str(temp_sensors[sensor]))
                Domoticz.Log("Temperature sensor {} created".format(sensor))

    def onStop(self):
        # Domoticz.Log("onStop called")
        pass

    def onConnect(self, Connection, Status, Description):
        # Domoticz.Log("onConnect called")
        pass

    def onMessage(self, Connection, Data, Status, Extra):
        # Domoticz.Log("onMessage called")
        pass

    def onCommand(self, unit, command, level, hue):
        # Domoticz.Log("onCommand called for Unit " +
        #              str(unit) + ": Parameter '" + str(command) + "', Level: " + str(level))
        pass

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        # Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status +
        #              "," + str(Priority) + "," + Sound + "," + ImageFile)
        pass

    def onDisconnect(self, Connection):
        # Domoticz.Log("onDisconnect called")
        pass

    def onHeartbeat(self):
        if self.heartbeatcounter % self.interval == 0:
            self.heartbeatcounter = 0
            temp_sensors = self.get_temperature_reading()

            for i in Devices:
                id = re.match('.*temp_(.*)', Devices[i].Name).groups()[0]
                if id in temp_sensors:
                    Devices[i].Update(int(temp_sensors[id]), str(temp_sensors[id]))
                    Domoticz.Debug('Updating temp id {}, value={}'.format(id, temp_sensors[id]))

        self.heartbeatcounter += 1

    def get_temperature_reading(self):
        data = {}

        with urllib.request.urlopen(Parameters["Address"]) as f:
            data = json.loads(f.read().decode('utf-8'))

        return data


global _plugin
_plugin = HttpJsonTemperature()


def onStart():
    global _plugin
    _plugin.onStart()


def onStop():
    global _plugin
    _plugin.onStop()


def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)


def onMessage(Connection, Data, Status, Extra):
    global _plugin
    _plugin.onMessage(Connection, Data, Status, Extra)


def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)


def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)


def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)


def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()


# Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug("'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return
