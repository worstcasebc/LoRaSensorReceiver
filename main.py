import time
import pycom
import socket
import struct
import adafruit_sharpmemorydisplay
from machine import SPI, Pin, RTC
from network import LoRa, WLAN

# initialize with empty values
dataArray = ["","","","","","","",float(0.0), float(0.0)]

# get the wlan-config for IP-address
wlan = WLAN()
strWLAN = str(wlan.ifconfig())
strWLAN = strWLAN[2:strWLAN.find(',',2)-1]

# synchronize with time-server
rtc = RTC()
rtc.ntp_sync('pool.ntp.org')
time.sleep(2)

# create LoRa-socket
lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# the display is a SHARP Memory Display Breakout - 1.3" 96x96 Silver Monochrome
# https://www.exp-tech.de/displays/lcd/5090/sharp-memory-display-breakout-1.3-96x96-silver-monochrome
# this uses the Lopys SPI default pins for CLK, MOSI and MISO (``P10``, ``P11`` and ``P14``)
spi = SPI(0, mode=SPI.MASTER, baudrate=2000000, polarity=0, phase=0)
# define a dedicated pin for CS
scs = Pin('P9', mode=Pin.OUT)

# pass in the display size, width and height, as well
display = adafruit_sharpmemorydisplay.SharpMemoryDisplay(spi, scs, 96, 96)

# set the display rotation (possible values: 0, 1, 2, 3)
display.rotation = 0

def recLoRa(delay, id, dataArray):
    print("now listening ...")
    # check lora-interface for sensor-data
    s.setblocking(False)
    data = ""
    # listen as long as the received data-length is lower 8 byte
    while len(data) < 8:
        data = s.recv(64)
        time.sleep_ms(delay)
    # if received data larger than 8 byte continue
    if len(data) >= 8:
        # get localtime (see boot.py for setting of the timezone)
        d = time.localtime()
        dataArray[1] = d[0]
        dataArray[2] = d[1]
        dataArray[3] = d[2]
        dataArray[4] = d[3]
        dataArray[5] = d[4]
        dataArray[6] = d[5]
        dataArray[7] = float(0.0)
        dataArray[8] = float(0.0)
        # fill a leading "0" to month, day, hour, minute and second < 10
        if dataArray[2] < 10:
            dataArray[2] = "0"+str(dataArray[2])
        if dataArray[3] < 10:
            dataArray[3] = "0"+str(dataArray[3])
        if dataArray[4] < 10:
            dataArray[4] = "0"+str(dataArray[4])
        if dataArray[5] < 10:
            dataArray[5] = "0"+str(dataArray[5])
        if dataArray[6] < 10:
            dataArray[6] = "0"+str(dataArray[6])
        # unpack the received structur containing a deviceID, temperature and humidity
        dataArray[0], datatemp, datahum = struct.unpack('<4shh', data)
        dataArray[7] = float(datatemp / 100)
        dataArray[8] = float(datahum / 100)
        print('data received from {} and decoded @{}.{}.{} {}:{}:{} to: {} / {}'.format(dataArray[0], dataArray[3], dataArray[2], dataArray[1], dataArray[4], dataArray[5], dataArray[6], dataArray[7], dataArray[8]))

def displayData():
    # displays the received data with timestamp and actual ip-address
    print("display data on screen ...")
    display.fill(1)
    display.text(' Temp:' + str(dataArray[7]) + "'C", 0, 8, 0)
    display.text(' Hum :' + str(dataArray[8]) + "%", 0, 16,0)
    display.text(' Last refresh:',0, 32, 0)
    display.text(' {}.{}.{} '.format(dataArray[3], dataArray[2], dataArray[1]), 0, 40, 0)
    display.text(' {}:{}:{}'.format(dataArray[4], dataArray[5], dataArray[6]), 0, 48, 0)
    display.text(' Actual IP:', 0, 64,0)
    display.text(" "+strWLAN,0,72,0)
    display.show()

def displaySplashScreen():
    print("display splashscreen ...")
    display.fill(1)
    display.text(' presented by', 0, 40, 0)
    display.text(' worstcase_ffm', 0, 48, 0)
    display.show()
    time.sleep(2)
    display.fill(1)
    display.text(' now listening', 0, 40, 0)
    display.text(' to LoRa @868MHz', 0, 48, 0)
    display.show()

displaySplashScreen()
    
while True:
    recLoRa(10, 1, dataArray)
    displayData()