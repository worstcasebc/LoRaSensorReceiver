import machine
import time
from network import WLAN
import config

wlan = WLAN(mode=WLAN.STA) # get current object, without changing the mode

if not wlan.isconnected():
    # change the line below to match your network ssid, security and password
    wlan.connect(config.WiFiSSID, auth=(WLAN.WPA2, config.WiFiKey))
    while not wlan.isconnected():
        machine.idle() # save power while waiting
    print("WiFi connected ...")
    print(wlan.ifconfig())

rtc = machine.RTC()
rtc.init((2019, 11, 21, 20, 00, 0, 0, 0))
rtc.ntp_sync('pool.ntp.org')
while not rtc.synced():
    time.sleep_ms(100)

time.timezone(3600)
print('Time synced: {}'.format(time.localtime()))