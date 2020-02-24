import socket
import select
import sys
import threading
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 12237
s.connect(('192.168.43.24', port))
flag = False

def send_msg(s):
    while True:
        try:
            msg = input('Number 1 = ')
            bmsg=msg.encode()
            s.send(bmsg)
            msg = input('Number 2 = ')
            bmsg=msg.encode()
            s.send(bmsg)
            msg = input('Enter bye to leave this service else enter anything: ')
            if msg.lower() == 'bye':
                s.close()
                return
        except Exception as e:
            print('Connection already closed')
            return
        
def recv_msg(s):
    while True:
        try:
            data = s.recv(2048)
            if len(data)!=0:
                print("Recieved:", data.decode())
            else:
                s.close()
                return
        except Exception as e:
            print("Connection closed by client.")
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