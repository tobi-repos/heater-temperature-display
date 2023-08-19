import machine
import ssd1306

import config
import font_renderer

class OledDisplay:
    
    def __init__(self):
        self.__scl = machine.Pin(config.oled_scl_pin)
        self.__sda = machine.Pin(config.oled_sda_pin)
        self.__i2c = machine.I2C(config.oled_i2c_index, sda=self.__sda, scl=self.__scl, freq=400000)
        self.__oled = ssd1306.SSD1306_I2C(128, 64, self.__i2c, config.oled_id)
        self.__font_renderer = font_renderer.FontRenderer('dejavu_sans_mono_14x25.bin')
        
    def update(self, temperature_top, temperature_bottom, indicator = None):        
        self.__oled.fill(0)
        
        self.__oled.text('OBEN:', 0, 0, 1)
        self.__oled.rect(48, 1, 80, 6, 1)
        
        if temperature_top:
            width = int((temperature_top * 80) / 100)
            self.__oled.hline(48, 2, width, 1)
            self.__oled.hline(48, 3, width, 1)
            self.__oled.hline(48, 4, width, 1)
            self.__oled.hline(48, 5, width, 1)
            self.__font_renderer.print_text(self.__oled, f'{temperature_top:.1f}°C', 22, 7)
        else:
            self.__font_renderer.print_text(self.__oled, '---', 22, 7)

        self.__oled.text('UNTEN:', 0, 32, 1)
        self.__oled.rect(48, 33, 80, 6, 1)
        
        if temperature_bottom:
            width = int((temperature_bottom * 80) / 100)
            self.__oled.hline(48, 34, width, 1)
            self.__oled.hline(48, 35, width, 1)
            self.__oled.hline(48, 36, width, 1)
            self.__oled.hline(48, 37, width, 1)
            self.__font_renderer.print_text(self.__oled, f'{temperature_bottom:.1f}°C', 22, 39)
        else:
            self.__font_renderer.print_text(self.__oled, '---', 22, 39)
            
        if indicator:
            self.__oled.text(indicator, 120, 48, 1)
        
        self.__oled.show()
        
