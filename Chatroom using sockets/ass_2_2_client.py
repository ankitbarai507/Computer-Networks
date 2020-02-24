import socket
import threading
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 12347
s.connect(('192.168.43.24', port))
print('Connected to server')

def send_msg(s):
    while True:
        try:
            msg = input(">>>> ")
            bmsg = msg.encode()
            s.send(bmsg)
            if msg.lower()=='bye':
                s.close()
                break
        except Exception as e:
            print("Connection closed, no more messages can be sent.")
            break
    return

def recv_msg(s):
    while True:
        try:
            data = s.recv(2048)
            if s:
                print("Recieved:", data.decode())
            else:
                s.close()
                return
        except Exception as e:
            print("Connection closed, no more accepting messges from server.")
            return

try:
    t1 = threading.Thread(target=send_msg, args=(s,))
    t2= threading.Thread(target=recv_msg, args=(s,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
except Exception as e:
    print(str(e))
    s.close()