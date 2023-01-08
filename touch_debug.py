from machine import SoftI2C,Pin
import time
tprst=Pin(10,Pin.OUT)
tprst.value(1)
time.sleep_ms(50)
tprst.value(0)
time.sleep_ms(5)
tprst.value(1)
time.sleep_ms(50)
i2c=SoftI2C(sda=Pin(11),scl=Pin(12), freq=300000)
#it=Pin(9,Pin.IN,Pin.PULL_DOWN)
print(i2c.scan())
while 1:
    time.sleep_ms(100)
    try:
        xraw=i2c.readfrom_mem(21,3,2)
        yraw=i2c.readfrom_mem(21,5,2)
        finger=i2c.readfrom_mem(21,2,1)
        print(finger)
        y=abs(240-xraw[1])
        x=yraw[0]*256+yraw[1]
        print(x,y)
    except:
        pass
