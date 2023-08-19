import machine
import socket
import time
import urequests

import config
from oled_display import OledDisplay
from temperature_sensors import TemperatureSensors
from udp_sender import UdpSender
from wifi_connection import WifiConnection

try:
    ts = TemperatureSensors()
    oled = OledDisplay()
    conn = WifiConnection()
    udp = UdpSender()

    while True:
        conn.loop()
        ts.loop()
        
        if conn.status_changed or ts.new_data:
            oled.update(ts.temperature_top, ts.temperature_bottom, conn.hint)
            
            if conn.connected:
                udp.broadcast_ip = conn.broadcast_ip
                udp.update(ts.temperature_top, ts.temperature_bottom)
                
            elif conn.error:
                machine.WDT(timeout=3000)

except(KeyboardInterrupt):
    udp.stop()
    conn.stop()