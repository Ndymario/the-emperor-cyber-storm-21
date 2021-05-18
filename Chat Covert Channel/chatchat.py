# This is chat client 
import socket
from sys import stdout
from time import time

DEBUG = True

# chat client will listen from this server (given by teacher):
ip = "138.47.102.120"
port = 31337

# socket:
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))
data = s.recv(4096).decode()

# receive message, count the time delay and store in times[] array:
times = []

while (data.rstrip("\n") != "EOF"):
    
    stdout.write(data)
    stdout.flush()
    t0 = time()
    data = s.recv(4096).decode()
    t1 = time()
    
    delta = round(t1 - t0, 3)
    times.append(delta)     

    if (DEBUG):
        stdout.write(" {}\n".format(delta))
        stdout.flush()
s.close()


# transform time delay array times[] into binary form:
covertBin = ""
covertBinRev = ""       # reverse of covertBin

DIFF = 45       # the percent error allow between 2 time delay is 20%

t0 = times[0]


for i in times:
    if (i <= 0.06):
        covertBin += "0"
        covertBinRev += "1"
    else:
        covertBin += "1"
        covertBinRev += "0"

result = ""
i = 0
while (i < len(covertBin)):
    # store 8 chars from covertBin in b:    
    b = covertBin[i:i+8]
    # convert b to a decimal integer (stored in n) using int(,2):
    n = int(b, 2)
    # convert n into ASCII character using chr():   
    result += chr(n)   
    i += 8

if result.endswith('EOF'):
    result = result[:-3]

stdout.write(result + "\n")
