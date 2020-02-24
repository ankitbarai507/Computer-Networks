import socket


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

def bits2string(frame,generator = '11101011'):
    frame = frame[:len(frame)-len(generator)+1]
    message = ""
    while frame != "":
        f = ""
        for i in frame[:8]:
            f += i
        i = bin_to_dec(f)
        i = chr(i)
        message = message + i
        frame = frame[8:]
    return message

def crc_check(frame, generator = '11101011'):
    rem_frame = divide(frame,generator)
    rem_true = '0' * (len(generator) - 1)
    if rem_frame == rem_true:
        return True
    return False



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 12347
s.connect(('127.0.0.1', port))
print('Connected to server')
generator = '11101011'
f = open('output.txt','w+')
count_nak=0
while True:
    try:
        frame = s.recv(1024).decode()

        check = False
        while not check:
            check = crc_check(frame)
            ack = 'ok'
            nack = 'nak'
            if(check):
                frame = bits2string(frame)
                f.write(frame)
                print(frame,end="")
                s.sendall(ack.encode())
            else:
                s.sendall(nack.encode())
                count_nak+=1
                frame = s.recv(1024).decode()
    except Exception as e:
        s.close()
        print("\nClosed connection with the server",)
        break
print('count_nak=',count_nak)
f.close()