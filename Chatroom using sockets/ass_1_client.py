import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 12347
s.connect(('192.168.43.24', port))
print('Connected to server')
while True:
    print('client recieved:', s.recv(1024).decode())
    try:
        msg = input('enter message for server: ')
        bmsg = msg.encode()
        s.sendall(bmsg)
        if msg.lower() == 'bye':
            print('Client closing connection ...')
            s.close()
            print('Closed')
            break
    except Exception as e:
        s.close()
        print('except', str(e))