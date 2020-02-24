import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
if s:
    print("Connected.")
while True:
    msg = input(">>> ")
    s.sendto(msg.encode(), ('192.168.43.24', 1234))
    if msg == 'bye':
        s.close()
        print("Conection closed.")
        break
    msg, address = s.recvfrom(2048)
    print("<<<", msg.decode())