import machine
import ili9XXX
import lvgl as lv
import espidf as esp
import time
from machine import Pin
import touch
import usocket
import network

bl=Pin(15,Pin.OUT)
bl.on()

def load_image(filename):
    filename='/ico/'+filename+'.png'
    with open(filename,'rb') as f:
        png_data = f.read()
    img=lv.img_dsc_t({
      'data_size': len(png_data),
      'data': png_data
    })
    return img
clockbg_png = load_image('clockbg')

import fs_driver
fs_drv = lv.fs_drv_t()
fs_driver.fs_register(fs_drv, 'S')
font_mc = lv.font_load("S:ui_font_mc.bin")

disp = ili9XXX.st7789(width=300, height=240,miso=41, mosi=14, clk=21, cs=47, dc=48, rst=13, mhz=40,spihost=esp.HSPI_HOST,rot=-2,colormode=ili9XXX.COLOR_MODE_RGB)
tp=touch.CST816S()
lv.init()

ui_Screen1 = lv.obj()
ui_Screen1.set_style_bg_img_src(clockbg_png, lv.PART.MAIN | lv.STATE.DEFAULT )

ui_Screen1_Label1 = lv.label(ui_Screen1)
ui_Screen1_Label1.set_text("2023-12-23")
ui_Screen1_Label1.set_width(lv.SIZE_CONTENT)	# 1
ui_Screen1_Label1.set_height(lv.SIZE_CONTENT)   # 1
ui_Screen1_Label1.set_x(10)
ui_Screen1_Label1.set_y(-41)
ui_Screen1_Label1.set_align( lv.ALIGN.CENTER)
ui_Screen1_Label1.set_style_text_color( lv.color_hex(0x84DCE5), lv.PART.MAIN | lv.STATE.DEFAULT )
ui_Screen1_Label1.set_style_text_opa(255, lv.PART.MAIN| lv.STATE.DEFAULT )
ui_Screen1_Label1.set_style_text_font( font_mc, lv.PART.MAIN | lv.STATE.DEFAULT )

ui_Screen1_Label2 = lv.label(ui_Screen1)
ui_Screen1_Label2.set_text("09:35 Tue")
ui_Screen1_Label2.set_width(lv.SIZE_CONTENT)	# 1
ui_Screen1_Label2.set_height(lv.SIZE_CONTENT)   # 1
ui_Screen1_Label2.set_x(10)
ui_Screen1_Label2.set_y(20)
ui_Screen1_Label2.set_align( lv.ALIGN.CENTER)
ui_Screen1_Label2.set_style_text_color( lv.color_hex(0xD6D4EA), lv.PART.MAIN | lv.STATE.DEFAULT )
ui_Screen1_Label2.set_style_text_opa(255, lv.PART.MAIN| lv.STATE.DEFAULT )
ui_Screen1_Label2.set_style_text_font( font_mc, lv.PART.MAIN | lv.STATE.DEFAULT )

lv.scr_load(ui_Screen1)