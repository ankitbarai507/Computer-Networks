import socket
import select
import sys
import threading
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

port = 12237
s.bind(('', port))
s.listen(5) 
print('socket listening')

clients = []

def clienthandle_thread(c, addr):
    global clients
    while True:
        try:
            
            msg1 = c.recv(1024)
            msg1 = msg1.decode()
            num1=int(msg1)

            msg2 = c.recv(1024)
            msg2 = msg2.decode()
            num2=int(msg2)

            if msg1 and msg2:
                print("Recieved from : " + str(addr) + " : " + msg1+' and '+msg2)
                add=num1+num2
                sub=num1-num2
                str1='Addition of '+str(num1)+' and '+str(num2)+' is '+str(add)
                str2='Subtraction of '+str(num1)+' and '+str(num2)+' is '+str(sub)
                c.send(str1.encode())
                c.send(str2.encode())

            else:
                print('else')
                clients.remove(c)
                break
               
        except Exception as e:
            print("Connection Closed....")
            c.close()
            break


count = 0
while True:
    c, addr = s.accept()  # c is connection object
    count += 1
    print('connected with', addr)
    clients.append(c)
    # create new thread to handle the client
    t = threading.Thread(target=clienthandle_thread, args=(c, addr))
    t.start()

c.close()  
s.close()