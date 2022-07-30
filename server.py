import sys
import time
import socket

server_status = True
message = b''
port = 4545

def server_run():
    global server_status
    global message
    global port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', port))
        s.listen(50)  # Сколько соединения
        while server_status:
            try:
                client, addr = s.accept()
            except KeyboardInterrupt as err:
                s.close()
                print('err')
                break
            else:
                message = client.recv(1024)
                client.close()
                print(f'IP: {addr}')
                print('Message: ', message.decode('utf-8'))


def server_stop():
    time.sleep(3)
    global server_status
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('127.0.0.1', port))
        s.send('Server down'.encode('utf-8'))  # send byte 'localhost' or '127.0.0.1'
        s.close()
        print('Controller server closed')
        server_status = False
        sys.exit()

    
print('Server started!')
    

