import machine
import ili9XXX
import lvgl as lv
import espidf as esp
import time
from machine import Pin

bl=Pin(15,Pin.OUT)
bl.on()
#-------------images----------------
def load_image(filename):
    filename='/image/'+filename+'.png'
    with open(filename,'rb') as f:
        png_data = f.read()
    img=lv.img_dsc_t({
      'data_size': len(png_data),
      'data': png_data
    })
    return img
#weabg_png = load_image('weabg')


#------------init----------------
disp = ili9XXX.st7789(width=280, height=240,miso=41, mosi=14, clk=21, cs=47, dc=48, rst=13, mhz=40,spihost=esp.HSPI_HOST,rot=-2)
lv.init()
#------------fonts-----------------
import fs_driver
fs_drv = lv.fs_drv_t()
fs_driver.fs_register(fs_drv, 'S')
font1 = lv.font_load("S:/font/ui_font_Font1.bin")
fonttitle = lv.font_load("S:/font/ui_font_fonttitle.bin")
fontdt = lv.font_load("S:/font/ui_font_datetime.bin")
#-----------function-------------
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

def WIFI_Connect():
    #返回值: 1 正常 2网络问题 3未找到配置
    wlan = network.WLAN(network.STA_IF) 
    try:
        f = open('wifi.txt', 'r') 
        info = json.loads(f.read())
        f.close()
        print(info)
    except:
        return 3
    wlan.active(True)   
    start_time=time.time()              
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(info['SSID'], info['PASSWORD'])
        while not wlan.isconnected():
            if time.time()-start_time > 10 :             
                wlan.active(False)
                print('WIFI Connected Timeout!')
                return 2
    print('network information:', wlan.ifconfig())
    return 1

#-----------screen---------------
logo_screen = lv.obj()
logo_screen.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN | lv.STATE.DEFAULT )
logo_screen.set_style_bg_opa(255, lv.PART.MAIN| lv.STATE.DEFAULT )
main_screen=lv.obj()
blank_screen=lv.obj()

def event_retry(evt):
    global button
    code = evt.get_code()
    if code == lv.EVENT.CLICKED:
        button='retry'
def event_AP(evt):
    global button
    code = evt.get_code()
    if code == lv.EVENT.CLICKED:
        logo_screen.clean()
        button='AP'
    
#---------------start here---------
def wifi_check():
    spinner = lv.spinner(logo_screen, 800, 60)
    spinner.set_size(40, 40)
    spinner.align(lv.ALIGN.CENTER, 0, 35)
    spinner.set_style_arc_color( lv.color_hex(0x00A1E6), lv.PART.MAIN | lv.STATE.DEFAULT )
    spinner.set_style_arc_opa(100, lv.PART.MAIN| lv.STATE.DEFAULT )

    obj = lv.img(logo_screen)
    obj.set_src(logo_png)
    obj.align(lv.ALIGN.CENTER, 0, -40)

    wifi_label = lv.label(logo_screen)
    wifi_label.set_style_text_font(font1, 0)
    wifi_label.set_text('WIFI连接中...')
    wifi_label.align(lv.ALIGN.CENTER, 0, 80)

    lv.scr_load(logo_screen)
    r=WIFI_Connect()
    if r==1:
        wifi_label.set_text("WIFI已连接")
        spinner.delete()
        obj = lv.img(logo_screen)
        obj.set_src(done_png)
        obj.align(lv.ALIGN.CENTER, 0, 33)
        obj.set_style_opa(lv.OPA._0,0)
        test_Animation(obj, 0)
    elif r==2:
        wifi_label.set_text("WIFI连接失败 请检查网络")
        spinner.delete()
        btn1 = lv.btn(lv.scr_act())
        btn1.add_event_cb(event_retry,lv.EVENT.ALL, None)
        btn1.align(lv.ALIGN.CENTER,-50,35)
        label=lv.label(btn1)
        label.set_style_text_font(font1, 0)
        label.set_text("重试")
        btn2 = lv.btn(lv.scr_act())
        btn2.add_event_cb(event_AP,lv.EVENT.ALL, None)
        btn2.align(lv.ALIGN.CENTER,50,35)
        label2=lv.label(btn2)
        label2.set_style_text_font(font1, 0)
        label2.set_text("配网")
        while button=='':
            pass
        if button=='AP':
            utils.AP.startAP()
        elif button=='retry':
            logo_screen.clean()
            machine.reset() 
    elif r==3:
        wifi_label.set_text("未找到配置文件 请配网")
        spinner.delete()
        btn2 = lv.btn(lv.scr_act())
        btn2.add_event_cb(event_AP,lv.EVENT.ALL, None)
        btn2.align(lv.ALIGN.CENTER,0,35)
        label2=lv.label(btn2)
        label2.set_style_text_font(font1, 0)
        label2.set_text("配网")
        while button!='AP':
            pass
        print('--------AP START---------')
        utils.AP.startAP()
wifi_check()
gc.collect()
time.sleep(1)
#-------------------------------MAIN--------------------------------------
main_cb=''
def scroll_begin_event(e):
    if e.get_code() == lv.EVENT.SCROLL_BEGIN:
        a = lv.anim_t.__cast__(e.get_param())
        if a:
            a.time = 0

tabview = lv.tabview(lv.scr_act(), lv.DIR.LEFT, 80)
tabview.get_content().add_event_cb(scroll_begin_event, lv.EVENT.SCROLL_BEGIN, None)

tab_btns = tabview.get_tab_btns()
btnm_map = ["time", "lock", "set"]
tab_btns.set_map(btnm_map)
tab_btns.set_style_bg_color(lv.palette_darken(lv.PALETTE.GREY, 3), 0)
tab_btns.set_style_text_color(lv.palette_lighten(lv.PALETTE.GREY, 5), 0)
tab_btns.set_style_border_side(lv.BORDER_SIDE.RIGHT, lv.PART.ITEMS | lv.STATE.CHECKED)
tab_btns.set_style_text_font(font1, 0)
#tab_btns.set_style_bg_img_src(done, lv.PART.ITEMS)


tab1 = tabview.add_tab("天气")
#tab1.set_style_bg_img_src(weabg_png, lv.PART.MAIN | lv.STATE.DEFAULT )
tab1.set_style_bg_color( lv.color_hex(0xBCA1BA), lv.PART.MAIN | lv.STATE.DEFAULT )
tab1.set_style_bg_opa(255, lv.PART.MAIN| lv.STATE.DEFAULT )
tab1.set_style_bg_grad_color( lv.color_hex(0xADE3F6), lv.PART.MAIN | lv.STATE.DEFAULT )
tab1.set_style_bg_main_stop( 0, lv.PART.MAIN | lv.STATE.DEFAULT )
tab1.set_style_bg_grad_stop( 255, lv.PART.MAIN | lv.STATE.DEFAULT )
tab1.set_style_bg_grad_dir( lv.GRAD_DIR.VER, lv.PART.MAIN | lv.STATE.DEFAULT )
tab2 = tabview.add_tab("开锁")
tab2.set_style_bg_color( lv.color_hex(0x1DE5EA), lv.PART.MAIN | lv.STATE.DEFAULT )
tab2.set_style_bg_opa(255, lv.PART.MAIN| lv.STATE.DEFAULT )
tab2.set_style_bg_grad_color( lv.color_hex(0xB588F7), lv.PART.MAIN | lv.STATE.DEFAULT )
tab2.set_style_bg_main_stop( 0, lv.PART.MAIN | lv.STATE.DEFAULT )
tab2.set_style_bg_grad_stop( 255, lv.PART.MAIN | lv.STATE.DEFAULT )
tab2.set_style_bg_grad_dir( lv.GRAD_DIR.VER, lv.PART.MAIN | lv.STATE.DEFAULT )
tab3 = tabview.add_tab("设置")
tab3.set_style_bg_color( lv.color_hex(0x00F7A7), lv.PART.MAIN | lv.STATE.DEFAULT )
tab3.set_style_bg_opa(255, lv.PART.MAIN| lv.STATE.DEFAULT )
tab3.set_style_bg_grad_color( lv.color_hex(0x04F5ED), lv.PART.MAIN | lv.STATE.DEFAULT )
tab3.set_style_bg_main_stop( 0, lv.PART.MAIN | lv.STATE.DEFAULT )
tab3.set_style_bg_grad_stop( 255, lv.PART.MAIN | lv.STATE.DEFAULT )
tab3.set_style_bg_grad_dir( lv.GRAD_DIR.VER, lv.PART.MAIN | lv.STATE.DEFAULT )

tabview.get_content().clear_flag(lv.obj.FLAG.SCROLLABLE)

listb = lv.list(tab2)
listb.set_size(212, 212)
listb.center()

def refresh_lock():
    addr=[]
    name=[]
    addr,name=utils.blelock.refresh()
    print(addr,name)
    listb.clean()
    for i in range(len(name)):
        listb.add_btn(lv.SYMBOL.BLUETOOTH,name[i])
    float_btn = lv.btn(listb)
    float_btn.set_size(50, 50)
    float_btn.add_flag(lv.obj.FLAG.FLOATING)
    float_btn.align(lv.ALIGN.BOTTOM_RIGHT, 0, -listb.get_style_pad_right(lv.PART.MAIN))
    float_btn.add_event_cb(lambda evt: refresh_lock_event_cb(evt,listb), lv.EVENT.ALL, None)
    float_btn.set_style_radius(lv.RADIUS_CIRCLE, 0)
    float_btn.set_style_bg_img_src(lv.SYMBOL.REFRESH, 0)
    float_btn.set_style_text_font(lv.theme_get_font_large(float_btn), 0)
    float_btn.move_foreground()

def refresh_lock_event_cb(e,listb):
    global main_cb
    code = e.get_code()
    float_btn = e.get_target()
    if code == lv.EVENT.CLICKED:
        print('refresh click')
        main_cb='refresh'

float_btn = lv.btn(listb)
float_btn.set_size(50, 50)
float_btn.add_flag(lv.obj.FLAG.FLOATING)
float_btn.align(lv.ALIGN.BOTTOM_RIGHT, 0, -listb.get_style_pad_right(lv.PART.MAIN))
float_btn.add_event_cb(lambda evt: refresh_lock_event_cb(evt,listb), lv.EVENT.ALL, None)
float_btn.set_style_radius(lv.RADIUS_CIRCLE, 0)
float_btn.set_style_bg_img_src(lv.SYMBOL.REFRESH, 0)
float_btn.set_style_text_font(lv.theme_get_font_large(float_btn), 0)

city,weather=utils.weather.get_weather()
gc.collect()

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
dd=str(rdt[0])+'-'+str(rdt[1])+'-'+str(rdt[2])+' '+weekday
hh=str(rdt[4])
mm=str(rdt[5])
if len(hh)==1:
    hh='0'+hh
if len(mm)==1:
    mm='0'+mm
dt = lv.label(tab1)
dt.set_text(dd)
dt.set_width(lv.SIZE_CONTENT)	# 1
dt.set_height(lv.SIZE_CONTENT)   # 1
dt.set_x(0)
dt.set_y(-85)
dt.set_align( lv.ALIGN.CENTER)
dt.set_style_text_font(fontdt, lv.PART.MAIN | lv.STATE.DEFAULT )
dt2 = lv.label(tab1)
dt2.set_text(hh+':'+mm)
dt2.set_width(lv.SIZE_CONTENT)	# 1
dt2.set_height(lv.SIZE_CONTENT)   # 1
dt2.set_x(0)
dt2.set_y(-55)
dt2.set_align( lv.ALIGN.CENTER)
dt2.set_style_text_font(fontdt, lv.PART.MAIN | lv.STATE.DEFAULT )

# city=['\u6c88\u9633', '101070101']
# weather=['\u6674', '-16', '-2', '\u6674', '115', '\u4e1c\u5317\u98ce', '1', '-11', '58']

imgthe = lv.img(tab1)
imgthe.set_src(them_png)
imgthe.align(lv.ALIGN.CENTER, 15, 60)
imgwea = lv.img(tab1)
imgwea.set_src(sun_png)
imgwea.align(lv.ALIGN.CENTER, 55, 0)
temp,humi=dht11_get()
labelt = lv.label(tab1)
labelt.set_style_text_font(font1, 0)
labelt.set_text('温度:'+temp+'℃')
labelt.align(lv.ALIGN.CENTER, 70, 50)
labelh = lv.label(tab1)
labelh.set_style_text_font(font1, 0)
labelh.set_text('湿度:'+humi+'%')
labelh.align(lv.ALIGN.CENTER, 70, 75)
label = lv.label(tab1)
label.set_style_text_font(font1, 0)
label.set_text("当日天气:"+weather[0]+"\n"
               "最高温度:"+weather[2]+'℃'+"\n"
               "最低温度:"+weather[1]+'℃'+"\n"
               "空气质量:"+weather[4]+"\n"
               "风向:"+weather[5]+"\n"
               "风力级数:"+weather[6]+"\n"
               )
label.align(lv.ALIGN.CENTER, -55, 35)

#refresh_lock()
# while 1:
#     if main_cb=='refresh':
#         print('looking for lock')
#         refresh_lock()
#         main_cb=''

