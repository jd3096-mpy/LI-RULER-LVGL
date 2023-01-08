#CST816S lvgl driver by jd3096 20230107
from machine import SoftI2C,Pin
import time
import lvgl as lv

class CST816S:
    I2CADDR  = const(21)
    GET_POINT = const(1)
    def __init__(self,rst=10,sda=11,scl=12):
        self.x=0
        self.y=0
        #reset first
        self.rstpin=Pin(rst)
        self.rstpin.value(1)
        time.sleep_ms(50)
        self.rstpin.value(0)
        time.sleep_ms(5)
        self.rstpin.value(1)
        time.sleep_ms(50)
        #init I2C
        self.i2c=SoftI2C(sda=Pin(sda),scl=Pin(scl), freq=400000)
        #init lvgl device
        indev_drv = lv.indev_drv_t()
        indev_drv.init()
        indev_drv.type = lv.INDEV_TYPE.POINTER
        indev_drv.read_cb = self.read
        indev_drv.register()
   
    # @micropython.native
    def read(self, indev_drv, data) -> int:
        try:
            xraw=self.i2c.readfrom_mem(21,3,2)
            yraw=self.i2c.readfrom_mem(21,5,2)
            self.y=abs(240-xraw[1])
            self.x=yraw[0]*256+yraw[1]
            finger=self.i2c.readfrom_mem(21,2,1)
        except:
            self.x=0
            self.y=0
            finger=b'\x00'

        if finger==b'\x00':
            data.state = lv.INDEV_STATE.RELEASED
            return False
        if (self.x,self.y)!=(0,0):
            data.point.x ,data.point.y = self.x,self.y
            data.state = lv.INDEV_STATE.PRESSED
            return False
        return False


