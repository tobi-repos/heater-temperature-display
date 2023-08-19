import network
import rp2
import time

import config

class WifiConnection:
    
    def __ip_to_int(self, ip):
        result = 0
        
        for b in ip.split('.'):
            result = (result << 8) | int(b)
            
        return result
    
    def __int_to_ip(self, value):
        result = str((value >> 24) & 255)
        result = result + '.' + str((value >> 16) & 255)
        result = result + '.' + str((value >> 8) & 255)
        result = result + '.' + str(value & 255)
        
        return result
    
    def __init__(self):
        self.__fail_count = 0
        self.__connection_restart = time.ticks_ms()
        self.__connecting = False
        
        self.connected = False
        self.error = False
        self.status_changed = True
        self.hint = 'I'
        self.ip = None
        self.mask = None
        self.gateway = None
        self.dns = None
        self.broadcast_ip = None
        
        rp2.country('DE')
        self.__wlan = network.WLAN(network.STA_IF)
        self.__wlan.active(True)
            
    def stop(self):
        self.__wlan.disconnect()
        self.__wlan.active(False)
        
        self.__connecting = False
        self.connected = False
        self.ip = None
        self.mask = None
        self.gateway = None
        self.dns = None
        self.broadcast_ip = None
        
    def loop(self):
        
        self.status_changed = False
        
        if self.__connecting:
                s = self.__wlan.status()
                
                if s == network.STAT_CONNECT_FAIL:
                    self.__fail_count += 1
                    self.__connection_restart = time.ticks_add(time.ticks_ms(), 1000)
                    self.__connecting = False
                    self.connected = False
                    self.error = self.__fail_count >= 5
                    self.status_changed = True
                    self.hint = 'F'
                    print('WIFI connection: Connect failed.')
                    
                elif s == network.STAT_NO_AP_FOUND:
                    self.__connection_restart = time.ticks_add(time.ticks_ms(), 30000)
                    self.__connecting = False
                    self.connected = False
                    self.status_changed = True
                    self.hint = 'A'
                    print('WIFI connection: Not access point found.')
                    
                elif s == network.STAT_WRONG_PASSWORD:
                    self.__connection_restart = time.ticks_add(time.ticks_ms(), 30000)
                    self.__connecting = False
                    self.connected = False
                    self.status_changed = True
                    self.hint = 'P'
                    print('WIFI connection: Wrong password.')
                    
                elif s == network.STAT_GOT_IP:                    
                    conf = self.__wlan.ifconfig()
                    self.ip = conf[0]
                    self.mask = conf[1]
                    self.gateway = conf[2]
                    self.dns = conf[3]
                    
                    ip = self.__ip_to_int(self.ip)
                    mask = self.__ip_to_int(self.mask)
                    ip = (ip & mask) | (0xffffffff & (~mask))
                    
                    self.broadcast_ip = self.__int_to_ip(ip)
                    self.__fail_count = 0
                    self.__connecting = False
                    self.connected = True
                    self.status_changed = True
                    self.hint = None
                    print(f'WIFI connection: Got IP address. ({self.ip})')
     
        elif self.connected:
            if not self.__wlan.isconnected():
                self.__wlan.disconnect()
                self.__connection_restart = time.ticks_add(time.ticks_ms(), 1000)
                self.__connecting = False
                self.connected = False
                self.hint = 'W'
                self.status_changed = True
                self.ip = None
                self.mask = None
                self.gateway = None
                self.dns = None
                self.broadcast_ip = None
                print('WIFI connection: Connection lost.')
                
        elif not self.error:
            if time.ticks_diff(time.ticks_ms(), self.__connection_restart) >= 0:
                self.__wlan.connect(config.wlan_ssid, config.wlan_password)
                self.__connecting = True
                self.connected = False
                self.error = False
                self.hint = 'V'
                self.status_changed = True
                print('WIFI connection: Starting connection.')
                