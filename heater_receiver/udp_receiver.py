import socket
import struct

import config

class UdpReceiver:
    
    def __init__(self):
        self.__timeout_count = 0
        self.temperature_top = None
        self.temperature_bottom = None
        self.new_data = True
        
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.settimeout(0.5)
        self.__socket.bind(('', config.udp_port))
        
    def loop(self):
        self.new_data = False
        
        try:
            data, addr = self.__socket.recvfrom(16)
            top, bottom = struct.unpack('@ff', data)
            
            if top == -1000:
                self.temperature_top = None
            else:
                self.temperature_top = top;
                
            if bottom == -1000:
                self.temperature_bottom = None
            else:
                self.temperature_bottom = bottom;
            
            self.__timeout_count = 0
            self.new_data = True
            
        except(KeyboardInterrupt):
            raise
        
        except:
            self.__timeout_count += 1
            
            if self.__timeout_count >= 30:
                self.temperature_top = None
                self.temperature_bottom = None
                self.new_data = True
                
    def stop(self):
        self.__socket.close()
            