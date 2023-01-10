import machine
import ili9XXX
import lvgl as lv
import espidf as esp
import time
from machine import Pin,RTC,Timer
import touch
import usocket
import network,ntptime

#--------------NTPTIME------------
ntptime.NTP_DELTA = 3155644800
ntptime.host = 'ntp1.aliyun.com'
#--------settings--------
SSID='dundundun'
PASSWORD='30963096'
SERVER='192.168.91.16'
PORT=3096
screen=False
bs=Pin(0,Pin.IN,Pin.PULL_UP)
rtc=RTC()
bl=Pin(15,Pin.OUT)
bl.on()

def ntp_get():
    for i in range(6):
        try:            
            ntptime.settime()      
            print("ntp time(BeiJing): ",rtc.datetime())
            return True
        except:
            print("Can not get time!")
        time.sleep_ms(500)
        
def showtime(t):
    print('time fresh')
    rdt=rtc.datetime()
    ww=rdt[3]
    if ww==0:
        weekday='MON'
    elif ww==1:
        weekday='TUE'
    elif ww==2:
        weekday='WED'
    elif ww==3:
        weekday='THU'
    elif ww==4:
        weekday='FRI'
    elif ww==5:
        weekday='SAT'
    elif ww==6:
        weekday='SUN'
    dd=str(rdt[0])+'-'+str(rdt[1])+'-'+str(rdt[2])
    hh=str(rdt[4])
    mm=str(rdt[5])
    if len(hh)==1:
        hh='0'+hh
    if len(mm)==1:
        mm='0'+mm
    Scr_clock_Label1.set_text(dd)
    Scr_clock_Label2.set_text(hh+':'+mm+' '+weekday)

    
#-------------images----------------
def load_image(filename):
    filename='/ico/'+filename+'.png'
    with open(filename,'rb') as f:
        png_data = f.read()
    img=lv.img_dsc_t({
      'data_size': len(png_data),
      'data': png_data
    })
    return img
csdn_png = load_image('cs')
github_png = load_image('github')
lvgl_png = load_image('lvgl')
mpy_png = load_image('mpy')
done_png = load_image('done')
logo_png = load_image('logo')
error_png = load_image('error')
clockbg_png = load_image('clockbg')

import fs_driver
fs_drv = lv.fs_drv_t()
fs_driver.fs_register(fs_drv, 'S')
font_mc = lv.font_load("S:ui_font_mc.bin")

def test_Animation(TargetObject, delay):
    PropertyAnimation_0 = lv.anim_t()
    PropertyAnimation_0.init()
    PropertyAnimation_0.set_path_cb(lv.anim_t.path_ease_in_out)
    PropertyAnimation_0.set_time(1100)
    PropertyAnimation_0.set_var(TargetObject)
    PropertyAnimation_0.set_custom_exec_cb(lambda a, v: TargetObject.set_style_opa(v,0))
    PropertyAnimation_0.set_delay(delay + 0)
    PropertyAnimation_0.set_repeat_count(0)
    PropertyAnimation_0.set_repeat_delay(0) #+ 1000
    PropertyAnimation_0.set_playback_delay(0)
    PropertyAnimation_0.set_playback_time(0)
    PropertyAnimation_0.set_early_apply(False)
    PropertyAnimation_0.set_values(0, 255)
    PropertyAnimation_0.set_get_value_cb(lambda a: TargetObject.get_style_opa(0))
    lv.anim_t.start(PropertyAnimation_0)
    print ("test_Animation")



#------------init----------------
disp = ili9XXX.st7789(width=300, height=240,miso=41, mosi=14, clk=21, cs=47, dc=48, rst=13, mhz=40,spihost=esp.HSPI_HOST,rot=-2,colormode=ili9XXX.COLOR_MODE_RGB)
tp=touch.CST816S()
lv.init()

#-------------screen connect------------
scr = lv.scr_act()
scr.set_style_bg_color(lv.color_hex(0xd0d0d0), lv.PART.MAIN)

spinner = lv.spinner(lv.scr_act(), 800, 60)
spinner.set_size(50, 50)
spinner.align(lv.ALIGN.CENTER, 10, 35)
spinner.set_style_arc_color( lv.color_hex(0x00A1E6), lv.PART.MAIN | lv.STATE.DEFAULT )
spinner.set_style_arc_opa(100, lv.PART.MAIN| lv.STATE.DEFAULT )

obj = lv.img(lv.scr_act())
obj.set_src(logo_png)
obj.align(lv.ALIGN.CENTER, 10, -40)

wifi_label = lv.label(lv.scr_act())
wifi_label.set_text('RULER connecting...')
wifi_label.align(lv.ALIGN.CENTER, 10, 80)

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    print('network status1:', sta_if.status())
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, PASSWORD)
        print('network status2:', sta_if.status())
        while not sta_if.isconnected():
            pass
    print('network status3:', sta_if.status())
    
do_connect()

spinner.delete()


try:
    s = usocket.socket(usocket.AF_INET,usocket.SOCK_STREAM)  
    addr = usocket.getaddrinfo(SERVER, PORT)[0][-1]
    s.connect(addr)
    s.send("RULER connected!")
except:
    obj = lv.img(lv.scr_act())
    obj.set_src(error_png)
    obj.align(lv.ALIGN.CENTER, 10, 33)
    obj.set_style_opa(lv.OPA._0,0)
    test_Animation(obj, 0)
    wifi_label.set_text("SERVER NOT FOUND")
    while 1:
        pass
    

obj = lv.img(lv.scr_act())
obj.set_src(done_png)
obj.align(lv.ALIGN.CENTER, 10, 33)
obj.set_style_opa(lv.OPA._0,0)
test_Animation(obj, 0)    
wifi_label.set_text("RULER connected!")

ntp_get()
lv.scr_act().clean()

#---------------screen button------------------
Scr_btn = lv.obj()

Scr_btn.set_style_bg_color(lv.color_hex(0xf0f0f0), lv.PART.MAIN)

style = lv.style_t()
style.init()
style.set_radius(30)

style_pr = lv.style_t()
style_pr.init()
style_pr.set_outline_width(30)
style_pr.set_outline_opa(lv.OPA.TRANSP)
style_pr.set_translate_y(5)
style_pr.set_shadow_ofs_y(3)
style_pr.set_bg_color(lv.palette_darken(lv.PALETTE.BLUE, 2))
style_pr.set_bg_grad_color(lv.palette_darken(lv.PALETTE.BLUE, 4))

btn_select=''

class BTN():
    def __init__(self, x,y,text,png):
        self.text=text
        self.btn=lv.btn(Scr_btn)                        
        self.btn.add_style(style, 0)
        self.btn.add_style(style_pr, lv.STATE.PRESSED)
        self.btn.set_size(120, 100)
        self.btn.center()
        self.btn.set_x(x)
        self.btn.set_y(y)
        self.btn.add_event_cb(self.btn_event_cb, lv.EVENT.ALL, None)
        self.label = lv.label(self.btn)
        self.label.set_text(text)
        self.label.center()
        self.label.set_y(35)
        self.obj = lv.img(self.btn)
        self.obj.set_src(png)
        self.obj.align(lv.ALIGN.CENTER, 0, -15)
    
    def btn_event_cb(self,evt):
        global btn_select
        code = evt.get_code()
        btn = evt.get_target()
        if code == lv.EVENT.CLICKED:
            btn_select=self.text

        
btn1=BTN(-55,-60,'CSDN',csdn_png)
btn2=BTN(75,-60,'GITHUB',github_png)
btn3=BTN(-55,60,'LVGL',lvgl_png)
btn4=BTN(75,60,'MPY',mpy_png)

#--------------------screen clock-----------------
Scr_clock = lv.obj()
Scr_clock.set_style_bg_img_src(clockbg_png, lv.PART.MAIN | lv.STATE.DEFAULT )

Scr_clock_Label1 = lv.label(Scr_clock)
Scr_clock_Label1.set_text("2023-12-23")
Scr_clock_Label1.set_width(lv.SIZE_CONTENT)	# 1
Scr_clock_Label1.set_height(lv.SIZE_CONTENT)   # 1
Scr_clock_Label1.set_x(10)
Scr_clock_Label1.set_y(-41)
Scr_clock_Label1.set_align( lv.ALIGN.CENTER)
Scr_clock_Label1.set_style_text_color( lv.color_hex(0x84DCE5), lv.PART.MAIN | lv.STATE.DEFAULT )
Scr_clock_Label1.set_style_text_opa(255, lv.PART.MAIN| lv.STATE.DEFAULT )
Scr_clock_Label1.set_style_text_font( font_mc, lv.PART.MAIN | lv.STATE.DEFAULT )

Scr_clock_Label2 = lv.label(Scr_clock)
Scr_clock_Label2.set_text("09:35 Tue")
Scr_clock_Label2.set_width(lv.SIZE_CONTENT)	# 1
Scr_clock_Label2.set_height(lv.SIZE_CONTENT)   # 1
Scr_clock_Label2.set_x(10)
Scr_clock_Label2.set_y(20)
Scr_clock_Label2.set_align( lv.ALIGN.CENTER)
Scr_clock_Label2.set_style_text_color( lv.color_hex(0xD6D4EA), lv.PART.MAIN | lv.STATE.DEFAULT )
Scr_clock_Label2.set_style_text_opa(255, lv.PART.MAIN| lv.STATE.DEFAULT )
Scr_clock_Label2.set_style_text_font( font_mc, lv.PART.MAIN | lv.STATE.DEFAULT )

lv.scr_load(Scr_clock)

def change_screen(t):
    print('switch screen')
    global screen
    while not bs.value():
        pass
    if screen:
        lv.scr_load(Scr_clock)
    else:
        lv.scr_load(Scr_btn)
    screen=not screen
    
bs.irq(handler=change_screen, trigger=Pin.IRQ_RISING)
tim=Timer(1)
tim.init(period=5000, callback=showtime)

while 1:
    if btn_select!='':
        print(btn_select)
        if btn_select=='CSDN':
            s.send("CSDN")
            print('csdn send???')
        elif btn_select=='GITHUB':
            s.send("GITHUB")
        elif btn_select=='LVGL':
            s.send("LVGL")
        elif btn_select=='MPY':
            s.send("MPY")
        btn_select=''



