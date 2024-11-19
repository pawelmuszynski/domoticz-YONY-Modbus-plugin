# domoticz-YONY-Modbus
## Description
YONY heat meter with RS485 Port modbus RTU for Domoticz plugin.

Based on https://github.com/MFxMF/SDM630-Modbus sceleton, I prepared Modbus plugin for YONY heat meter.
For now it supports Flow rate and Heat power values only.

## Hardware and wiring
Tested with chinese RS485 to serial UART module. It didn't work with low voltage RS485 logic on other devices.

## Installation
```
cd ~/domoticz/plugins
pip install minimalmodbus
git clone https://github.com/pawelmuszynski/domoticz-YONY-Modbus-plugin
```
Restart your Domoticz server.

## Used modules
- minimalmodbus 2.0.1

Tested with Domoticz 2022.2.
