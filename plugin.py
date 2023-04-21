#!/usr/bin/env python

"""
YONY Heat meter. The Python plugin for Domoticz
Author: MFxMF / pawelmuszynski
Requirements:
    1.python module minimalmodbus -> http://minimalmodbus.readthedocs.io/en/master/
        (pi@raspberrypi:~$ sudo pip3 install minimalmodbus)
    2.Communication module Modbus USB to RS485 converter module
"""
"""
<plugin key="YONY" name="YONY-Modbus" version="1.0.1" author="MFxMF / pawelmuszynski">
    <params>
        <param field="SerialPort" label="Modbus Port" width="200px" required="true" default="/dev/ttyUSB0" />
        <param field="Mode1" label="Baud rate" width="40px" required="true" default="9600"  />
        <param field="Mode2" label="Device ID" width="40px" required="true" default="200" />
        <param field="Mode3" label="Reading Interval sec." width="40px" required="true" default="60" />
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal"  default="true" />
            </options>
        </param>
    </params>
</plugin>
"""

import minimalmodbus
import Domoticz
import time


class BasePlugin:
    def __init__(self):
        self.runInterval = 1
        self.rs485 = ""
        return

    def onStart(self):
        self.rs485 = minimalmodbus.Instrument(Parameters["SerialPort"], int(Parameters["Mode2"]))
        self.rs485.serial.baudrate = Parameters["Mode1"]
        self.rs485.serial.bytesize = 8
        self.rs485.serial.parity = minimalmodbus.serial.PARITY_NONE
        self.rs485.serial.stopbits = 1
        self.rs485.serial.timeout = 1
        self.rs485.debug = False


        self.rs485.mode = minimalmodbus.MODE_RTU
        devicecreated = []
        Domoticz.Log("YONY Modbus plugin start")
        self.runInterval = int(Parameters["Mode3"]) / 60
        if 1 not in Devices:
            Domoticz.Device(Name="Flow rate", Unit=1, TypeName="Custom", Used=0, Options={ "Custom": "1;L/h" }).Create()
        if 2 not in Devices:
            Domoticz.Device(Name="Heat power", Unit=2, TypeName="Usage", Used=0).Create()


    def onStop(self):
        Domoticz.Log("YONY Modbus plugin stop")

    def onHeartbeat(self):
        self.runInterval -=1;
        if self.runInterval <= 0:
            # Get data from YONY
            try:
                time.sleep(1)
                flowRate = self.rs485.read_long(registeraddress=1, functioncode=3, signed=True, byteorder=minimalmodbus.BYTEORDER_LITTLE_SWAP)
                time.sleep(1)
                heatPower = self.rs485.read_long(registeraddress=4, functioncode=3, signed=True, byteorder=minimalmodbus.BYTEORDER_LITTLE_SWAP)
            except:
                Domoticz.Log("Connection problem");
            else:
                #Update devices
                Devices[1].Update(0,str(flowRate))
                Devices[2].Update(0,str(heatPower))


            if Parameters["Mode6"] == 'Debug':
                Domoticz.Log("YONY Modbus Data")
                Domoticz.Log('Flow Rate: {0:.3f} L/h'.format(flowRate))
                Domoticz.Log('Heat Power: {0:.3f} W'.format(heatPower))

        self.runInterval = int(Parameters["Mode3"]) * 0.1

global _plugin
_plugin = BasePlugin()


def onStart():
    global _plugin
    _plugin.onStart()


def onStop():
    global _plugin
    _plugin.onStop()


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
