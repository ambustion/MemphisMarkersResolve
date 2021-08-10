import socket
import struct
import time
TCP_IP = '127.0.0.1'
TCP_PORT = 9060
BUFFER_SIZE = 1024

def convertBinaryTC(data):
    tc = struct.unpack("5B", data)
    tc = tc[1:]
    timecode = list(tc)
    tc2 = []
    for x in timecode:
        x = str(str(x).zfill(2))
        tc2.append(x)
    tc3 = ":".join(tc2)
    return tc3

def connect():
    MESSAGE=b'connect'
    Mlen = len(MESSAGE)
    mLenbytes=struct.pack("i" , Mlen)
    with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as s:
        s.connect((TCP_IP, TCP_PORT))
        s.send(mLenbytes)
        s.send(MESSAGE)
        data=s.recv(BUFFER_SIZE)
    print('Received', repr(data))

def gettc():
    MESSAGE=b'gettc'
    Mlen=len(MESSAGE)
    mLenbytes=struct.pack("i" , Mlen)
    with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as s:
        s.setsockopt(socket.IPPROTO_TCP , socket.TCP_NODELAY , 1)
        ls = []
        s.connect((TCP_IP, TCP_PORT))
        s.sendall(mLenbytes)
        s.sendall(MESSAGE)
        time.sleep(1)
        data=s.recv(BUFFER_SIZE)
    print('Received' , repr(data))
    tc = convertBinaryTC(data)
    return tc
def play(playbackspeed = 1):

    MESSAGE=b'play'
    Mlen = len(MESSAGE)
    mLenbytes=struct.pack("i", Mlen)
    speed = struct.pack("f", playbackspeed)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((TCP_IP, TCP_PORT))
        s.send(mLenbytes)
        s.send(MESSAGE)
        s.send(speed)
        data=s.recv(BUFFER_SIZE)
    print('Received', repr(data))
def settc(timecode):

    MESSAGE=b'goto'
    tc = timecode.split(":")
    sendtc=[]
    Mlen=len(MESSAGE)
    mLenbytes=struct.pack("i", Mlen)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY , 1)
        s.connect((TCP_IP, TCP_PORT))
        s.sendall(mLenbytes)
        s.sendall(MESSAGE)
        for x in tc:
            newx = bytes(x,'utf-8')
            sendtc.append(newx)
        sendtc = struct.pack("4B",int(sendtc[0]),int(sendtc[1]),int(sendtc[2]),int(sendtc[3]))
        s.sendall(sendtc)
        time.sleep(1)
        data=s.recv(BUFFER_SIZE)
    print('Received' , repr(data))
