import framebuf

class FontRenderer:
    def __init__(self, font):
        
        with open(font, 'rb') as fin:
            self.__char_width = ord(fin.read(1))
            self.__char_height = ord(fin.read(1))
            self.__fb_bytes = ord(fin.read(1)) + 256 * ord(fin.read(1))
            self.__font_data = fin.read()
                    
        self.__fb_data = bytearray(self.__fb_bytes)
        self.__fb = framebuf.FrameBuffer(self.__fb_data, self.__char_width, self.__char_height, framebuf.MONO_HLSB)
        
    def print_text(self, oled, text, x, y):
        offset = x

        for c in text:
            try:
                position = ord(c) * self.__fb_bytes
                self.__fb_data[:] = self.__font_data[position: position + self.__fb_bytes]
                oled.blit(self.__fb, offset, y)
            except:
                pass
            
            offset = offset + self.__char_width