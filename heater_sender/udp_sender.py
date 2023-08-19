import socket
import struct

import config

class UdpSender:
    
    def __init__(self):        
        self.broadcast_ip = None
        
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__buffer = bytearray(8)
        
    def update(self, top, bottom):
        if top == None:
            top = -1000
            
        if bottom == None:
            bottom = -1000
        
        struct.pack_into('@ff', self.__buffer, 0, top, bottom)
        
        try:
            if self.broadcast_ip:
                self.__socket.sendto(self.__buffer, (self.broadcast_ip, config.udp_port))
        except:
            pass
    
    def stop(self):
        self.__socket.close()
            
