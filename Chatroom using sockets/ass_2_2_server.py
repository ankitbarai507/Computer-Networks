import socket
import threading
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

port = 12347
s.bind(('', port))
s.listen(5)
print('socket listening')


def send_msg(c):
    while True:
        try:
            msg = input('>>>> ')
            #msg = sys.stdin.readline()
            bmsg=msg.encode()
            c.send(bmsg)
        except Exception as e:
            print('Connection has been Closed.....')
            return
        
def recv_msg(c):
    while True:
        try:
            data = c.recv(2048)
            if data:
                print("Recieved: "+data.decode())
            else:
                c.close()
                break
        except Exception as e:
            print('Connection Closed.....')
            return

            
while True:
    try:
        c, addr = s.accept()
        print('connected with', addr)
        try:
            t = threading.Thread(target=send_msg, args=(c,))
            t2= threading.Thread(target=recv_msg, args=(c,))
            t.start()
            t2.start()
        
        except Exception as e:
            print(str(e))
            s.close()
    except Exception as e: 
        c.close()
        
        print('closed connection with '+str(addr))
        continue
s.close()