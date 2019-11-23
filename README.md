# LoRaSensorReceiver
First project using micropython on Pycom LoPy4 to transmit sensor-data via LoRa

## Overview
That project consists of two components, the [sender](https://github.com/worstcasebc/LoRaSensorSender) and a receiver. Both are running on LoPy4 and communicate via Raw-LoRa. Both components can be found in my Git-repositories. I use VSCode, but feel free to use an IDE of your choice.

## Receiver
That component receives the sent temperature and humidity data via Raw-LoRa and displays the data together with the timestamp on a display.

<img src="https://user-images.githubusercontent.com/58089458/69477128-b2196480-0de2-11ea-8f79-3ef3ab7dd83d.jpg" width="600" height="400" />

### Hardware used
* [Pycom LoPy4](https://pycom.io/product/lopy4/) (LoRa-antenna is necessary to not destroy your board)
* [Pycom Expansion Board 2.0](https://pycom.io/product/expansion-board-3-0/)
* [Sharp Memory Display](https://www.exp-tech.de/displays/lcd/5090/sharp-memory-display-breakout-1.3-96x96-silver-monochrome)
* [DHT22 Temperature and Humidity sensor](https://www.exp-tech.de/sensoren/temperatur/7784/dht22-am2302-feuchtigkeits-und-temperatursensor)
* a few jumper cables and a breadboard

### Wiring
|LoPy4          |Display        |Description                            |
| ------------- | ------------- | ------------------------------------- |
| 3.3V          | VIN           | the display is working with 3.3V      |
| GND           | GND           |                                       |
| P9  (G16)     | CS            |                                       |
| P10 (G17)     | CLK           | SPI clock signal                      |
| P11 (G22)     | DI            | SPI MOSI                              |

### Used libraries
There is a very good [library from Adafruit](https://github.com/adafruit/Adafruit_CircuitPython_SharpMemoryDisplay) for the usage of Sharp memory displays with their CircuitPlayground-devices. I only made minor changes to adapt it to the specifics of Pycoms Micropython.

### Code
The Lopy4 board connects to a WiFi first. This happens in the boot.py, that is called first after a start/reboot. You need to provide a SSID and the key for that WiFi within boot.py in line 5 and 6. After WiFi is connected, the actual time is requested and stored to the RTC of the board.
Within the main.py the lora-connection is prepared, the display initiated and some other initialization stuff done. The function recLoRa() listen to the LoRa-socket until a data-packet is received, which is larger than 8 bytes. Then the received data are unpacked with
```python
dataArray[0], datatemp, datahum = struct.unpack('<4shh', data) 
```
After that dataArray[0] contains the deviceID of the sending device (I only transmit the last 4 chars for payload-reasons) and datatemp/datahum contains the received sensor-data (transmitted as int-values also for payload-reasons and need to be divided by 100 to get original values back).
