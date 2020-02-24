import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 1234))
print("Server Started")

while True:
    print("Waiting For Connection......")
    data, address = s.recvfrom(1024)
    print("Connected to {}".format(address))
    if data.decode() == 'bye':
        print('disconnected from {}'.format(address))
        continue
    print("Message from Client:",data.decode())
    msg = input(">>> ")
    s.sendto(msg.encode(), address)