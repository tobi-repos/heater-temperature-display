import machine
import onewire
import ds18x20
import time

import config

class TemperatureSensors:
    
    def __init__(self):
        self.temperature_top = None
        self.temperature_bottom = None
        self.new_data = False
        
        self.__pin = machine.Pin(config.sensor_pin)
        self.__one_wire = onewire.OneWire(self.__pin)
        self.__sensor = ds18x20.DS18X20(self.__one_wire)
        self.__next_action = 0
        self.__perform_readout = False
        
    def loop(self):
        
        t = time.ticks_ms()
        
        self.new_data = False
        
        if time.ticks_diff(t, self.__next_action) >= 0:
            if self.__perform_readout:
                try:
                    self.temperature_top = self.__sensor.read_temp(config.sensor_top)
                except:
                    self.temperture_top = None
                    
                try:
                    self.temperature_bottom = self.__sensor.read_temp(config.sensor_bottom)
                except:
                    self.temperature_bottom = None
                    
                self.new_data = True
                
                self.__next_action = time.ticks_add(t, 4000)
                self.__perform_readout = False
                
            else:
                try:
                    self.__sensor.convert_temp()
                except:
                    pass
                
                self.__next_action = time.ticks_add(t, 1000)
                self.__perform_readout = True
