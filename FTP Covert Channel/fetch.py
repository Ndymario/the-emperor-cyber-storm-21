#The Emporer: Than Nguyen, Austin Harvey, Jackson Sikes, Nolan Yelverton, Thomas Nguyen, John Norris, Trinh Vo, Luke McMillan

#python 3 ftp covert channel decoder; call python file with -x argument (fetch.py -x) to secify specify IP, PORT, USER, and PASSWORD or call python file without -x argument to use default server info below

from ftplib import FTP
import sys

#function for decoding binary msg
def decode(chars):
    output = ""
    for char in chars:
        output += chr(int(char, 2))
    return output

def getFiles():
    try:
        #from ftp-tutorial code provided
        # connect and login to the FTP server
        ftp = FTP()
        ftp.connect(IP, PORT)
        ftp.login(USER, PASSWORD)
        ftp.set_pasv(USE_PASSIVE)
        # navigate to the specified directory and list files
        ftp.cwd(FOLDER)
        global files
        files = []
        ftp.dir(files.append)
        # exit the FTP server
        ftp.quit()
    except ConnectionRefusedError:
        print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\nNo connection could be made.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        exit()
try:
    #retrieve usr defined FTP server details
    if(sys.argv[1] == "-x"):
        IP = input("Enter server IP: ")
        PORT = int(input("Enter port: "))
        USER = input("Enter username: ")
        PASSWORD = input("Enter password: ")
        FOLDER = input("Enter folder: ")
        METHOD = int(input("Enter number of bits to consider: "))
        USE_PASSIVE = True # set to False if the connection times out

except IndexError:
    # default FTP server details
    IP = "138.47.102.120"
    PORT = 21
    USER = "anonymous"
    PASSWORD = ""
    FOLDER = input("Enter folder: ")
    METHOD = int(input("Enter number of bits to consider: "))
    USE_PASSIVE = True # set to False if the connection times out

getFiles()

#build single msg string from list of files
ftpMsg = ""
if(METHOD == 10):
    for file in files:
        char = file[:10]
        ftpMsg += char
    ftpMsg = ftpMsg[:len(ftpMsg) - (len(ftpMsg) % 7)] #take off padding from string
elif(METHOD == 7):
    for file in files:
        if(file[:3] == "---"):
            char = file[3:10]
            ftpMsg += char

#replace "-" with 0 and everything else with 1 to build msg in binary
binaryMsg = ""
for char in ftpMsg:
    if(char == "-"):
        binaryMsg += "0"
    else:
        binaryMsg += "1"

#split binaryMsg into "bytes"
chars = [binaryMsg[i:i+7] for i in range(0, len(binaryMsg), 7)]
print(decode(chars))
