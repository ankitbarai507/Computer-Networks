import socket
import random


def bin_to_dec(a):
    a = int(a)
    dec = 0
    i = 0
    while a > 0:
        b = a % 10
        a = a // 10
        dec += b * (2 ** i)
        i += 1
    return dec


def divide(data, poly_func):
    tmp_list = list(data)
    d = ""
    l = len(poly_func)
    p = bin_to_dec(poly_func)
    c = 1

    for i in range(len(data)-l+1):
        if tmp_list[i] == '0':
            c += 1
        if c >= 2 and tmp_list[i] == '0':
            d += "0"
        if tmp_list[i] == '1':
            d += "1"
            c = 1
            ts = ""
            s = tmp_list[i:i+l]
            for x in s:
                ts += x
            s = bin_to_dec(ts)
            tmp = s ^ p
            tmp = bin(tmp)
            tmp = tmp[2:]
            tmp = '0' * (l - len(tmp)) + tmp
            tmp_list[i:i+l] = tmp

    # print(d)
    rem = tmp_list[len(data)-l+1:len(data)]
    remstr = ''
    for x in rem:
        remstr += x
    return remstr


def crc(data, generator='11101011'):
    # standard polynomial crc8
    # 11101011
    l = len(generator)
    dt = data + '0' * (l-1)
    data = str(data)+str(divide(dt, generator))
    return data



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')
port = 12347
s.bind(('', port))
s.listen(5)
print('socket listening')


while True:
    try:
        c, addr = s.accept()
        print('connected with', addr)

        while True:
            n = 12
            filename = 'data.txt'
            with open(filename) as f:
                frame_count = 0
                while True:
                    frame = f.read(n)
                    frame_count += 1
                    if not frame:
                        # print("End of file")
                        c.close()
                        break
                    bframe = ""
                    for i in frame:
                        bframe += '0' * (8 - len(bin(ord(i))[2:])) + bin(ord(i))[2:]
                    data_to_send = crc(bframe)
                    
                    ri = random.randint(1,100)
                    if (ri % 2) == 0:
                        ri = random.randint(0,len(data_to_send))
                        bframe_err = list(data_to_send)
                        bframe_err[ri] = str(int(bframe_err[ri]) ^ 1)
                        data_to_send = ""
                        for i in bframe_err:
                            data_to_send += i
                    try:
                        c.send(data_to_send.encode())
                    except Exception as e:
                        print('send error= ',e)
                    tries = 1
                    while True:
                        print("Waiting Acknowledgement......")
                        ack = c.recv(1024).decode()
                        print("Received : ",ack.upper())
                        if ack.lower() == 'ok':
                            print("Frame sent successfully!!!")
                            print("Moving to next Frame.....")
                            break
                        else:
                            print("Error during Transmission!")
                            print("Retrying Frame.....")
                            data_to_send = crc(bframe)
                            
                            # ri = random.randint(1,100)
                            # if ri % 2 == 0:
                            #     ri = random.randint(0,len(data_to_send))
                            #     bframe_err = list(data_to_send)
                            #     bframe_err[ri] = int(bframe_err[ri]) ^ 1
                            #     data_to_send = ""
                            #     for i in bframe_err:
                            #         data_to_send += i

                            c.send(data_to_send.encode())
                            tries += 1
                    print('Frame ', frame_count, ' required ', tries, ' tries for sending')
                break
    except Exception as e:
        c.close()
        print('closed connection with '+str(addr)+str(e))
        continue
s.close()