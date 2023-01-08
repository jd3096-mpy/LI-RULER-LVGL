import socket
import threading
import webbrowser

bind_ip = "192.168.91.16"  
bind_port = 3096 
 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)
 
print("[*] Listening on %s:%d" % (bind_ip, bind_port))
 
 
def handle_client(client_socket):
    while 1:
        request = client_socket.recv(1024)
        cmd=request.decode()
        print("[*] Received: %s " % cmd)
        if cmd=='GITHUB':
            webbrowser.open_new_tab('https://github.com/')
        elif cmd=='LVGL':
            webbrowser.open_new_tab('https://docs.lvgl.io/master/index.html')
        elif cmd=='CSDN':
            webbrowser.open_new_tab('https://www.csdn.net/')
        elif cmd=='MPY':
            webbrowser.open_new_tab('http://docs.micropython.org/en/latest/')
        #client_socket.send(b'ACK')
    #client_socket.close()
 
 
while True:
    client, addr = server.accept()
    print("[*] Accepted connection from: %s:%d" % (addr[0], addr[1]))
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()