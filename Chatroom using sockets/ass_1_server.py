import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

port = 12347
s.bind(('', port))
s.listen()
print('Socket is listening')

while True:
    try:
        c, addr = s.accept()
        print('Connected with', addr)
        while True:
            msg = input('Enter message for client: ')
            bmsg = msg.encode()
            c.send(bmsg) 
            msg_from_client = c.recv(2048).decode()
            print('Server received: ', msg_from_client)
            if msg_from_client.lower() == 'bye':
                c.close()
                print('Closed connection from', addr)
                break

    except Exception as e:  # it will detect the close of connection by client and will close the connection object to that client
        c.close()
        
        print('Closed connection from', addr)
        continue
s.close()