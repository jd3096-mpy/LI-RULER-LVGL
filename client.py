import usocket
import network

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    print('network status1:', sta_if.status())
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('dundundun', '30963096')
        print('network status2:', sta_if.status())
        while not sta_if.isconnected():
            pass
    print('network status3:', sta_if.status())
    
do_connect() 

s = usocket.socket(usocket.AF_INET,usocket.SOCK_STREAM)  
addr = usocket.getaddrinfo('192.168.91.16', 3096)[0][-1]
s.connect(addr)
s.send("esp32 micropython")
while True:
     data = s.recv(100)
     if data:
        print(str(data, 'utf8'), end='')
     else:
        break
s.close()

