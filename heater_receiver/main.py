import machine
import socket
import time

import config
from oled_display import OledDisplay
from udp_receiver import UdpReceiver
from wifi_connection import WifiConnection
    
try:
    oled = OledDisplay()
    conn = WifiConnection()
    udp = UdpReceiver()

    oled.update(None, None, conn.hint)
    
    while True:
        conn.loop()
        
        if conn.connected:
            udp.loop()
            
        if conn.status_changed or udp.new_data:
            oled.update(udp.temperature_top, udp.temperature_bottom, conn.hint)

            if conn.error:
                machine.WDT(timeout=3000)

except(KeyboardInterrupt):
    udp.stop()
    conn.stop()