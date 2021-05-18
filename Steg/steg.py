#############################################################
# Team: The Emperor
# Names: Jackson Sikes, Thomas Nguyen, Austin Harvey, John Norris, Luke McMillan, Nolan Yelverton, Than Nguyen, Trinh Vo
# Date: 5/7/21
# Version: Python 3.8
# Description: This is a program that can store or retrieve files hidden inside of other files
#############################################################

import sys

#initializes the values for the potential inputs to the program
store = False
retrieve = False
bitMode = False
byteMode = False
hiddenFile = False
offset = 0
interval = 1
SENTINEL = bytearray([0x0, 0xff, 0x0, 0x0, 0xff, 0x0])

#checks to see if enough values were inputted into the program
#and if there aren't enough it prompts the user with the correct usage
args = sys.argv
args.pop(0)

if(len(args) < 4):
    sys.exit('Usage: python3 steg.py -(sr) -(bB) -o<int> [-i<int>] -w<file> [-h<file>]')
    
#takes the inputted arguments from the terminal and sets them into the program
for arg in args:
    pre = arg[:2]
    
    if(pre == '-s'):
        store = True
    
    elif(pre == '-r'):
        retrieve = True
    
    elif(pre == '-b'):
        bitMode = True
        
    elif(pre =='-B'):
        byteMode = True
        
    elif(pre == '-o'):
        offset = int(arg[2:])
        
    elif(pre == '-i'):
        interval = int(arg[2:])
        
    elif(pre == '-w'):
        wrapper = arg[2:]
        
    elif(pre == '-h'):
        hiddenFile = True
        hidden = arg[2:]
        
    else:
        sys.stdout.write(f"{arg} is not right \n")
        sys.stdout.write("Unrecognized input. Try again using:\n")
        sys.exit("python3 steg.py -(sr) -(bB) -o<int> [-i<int>] -w<file> [-h<file>]")
        
if(store and not hiddenFile):
    sys.exit("You just tried to store a file, but didn't provide it")
        
#tries to open the file that was inputted as the wrapper file
try:
    file = open(wrapper, 'rb')
    wrapperData = bytearray(file.read())
    
    if(store):
        hide = open(hidden, 'rb')
        hiddenData = bytearray(hide.read())
    
except:
    sys.exit("Couldn't find your file. Try providing a file in this directory.")

#checks whether you are storing, or retrieving a file. And if you are in bitMode or byteMode    
if(store):
    if(bitMode):
        #loops through the wrapper file adding the MSB of the hidden file to the LSB of the wrapper
        for i in range(len(hiddenData)):
            for j in range(8):
                wrapperData[offset] &= 0b11111110
                wrapperData[offset] |= ((hiddenData[i] & 0b10000000) >> 7)
                hiddenData[i] = (hiddenData[i] << 1) & (2**8 -1)
                offset += interval
        
        #adds the SENTINEL so you know where the file stops when retrieving 
        for i in range(len(SENTINEL)):
            for j in range(8):
                wrapperData[offset] &= 0b11111110
                wrapperData[offset] |= ((SENTINEL[i] & 0b10000000) >> 7)
                SENTINEL[i] = (SENTINEL[i] << 1) & (2**8 - 1)
                offset += interval
                
    elif(byteMode):
        #replaces the byte of the wrapper with the byte from the hidden file
        for i in range(len(hiddenData)):
            wrapperData[offset] = hiddenData[i]
            offset += interval
        
        #replaces the byte of the wrapper with the byte of the SENTINEL
        for i in range(len(SENTINEL)):
            wrapperData[offset] = SENTINEL[i]
            offset += interval
    else:
        sys.exit()
    
    #actually writes the editted file back to the original
    wrapperOut = open(wrapper, 'wb')
    wrapperOut.write(wrapperData)
    wrapperOut.close()
            
elif(retrieve):
    
    hiddenFile = bytearray()
    
    #sets the counter to check the SENTINEL
    count = 0
    
    if(bitMode):
        
        while(offset < len(wrapperData)):            
            b = 0
            
            #checks to see if the sentinel has already been found
            if(count == len(SENTINEL) - 1):
                break
            
            #gets the latest byte
            for j in range(8):
                #print(b)
                b |= (wrapperData[offset] & 0b1)
                
                if j < 7:
                    b = (b << 1) & (2**8 - 1)
                    offset += interval
            
            #if the current bit is a sentinel bit add to the count, and if it isn't reset it
            if(b == SENTINEL[count]):
                count += 1
                
            else:
                count = 0
                
            #adds the bit to the hiddenFile and increments the interval
            hiddenFile.append(b)
            offset += interval
        
                   
    
    elif(byteMode):
        
        while(offset < len(wrapperData)):
            b = wrapperData[offset]
            
            #checks if the sentinel has been found
            #and if the current byte is apart of the sentinel
            if(count == len(SENTINEL) -1):
                break
            
            elif(b == SENTINEL[count]):
                count += 1
            
            else:
                count = 0
            
            #keeps adding to the file if the end conditions are not met
            offset += interval
            hiddenFile.append(b)
            
    else:
        sys.exit()            
    
    #gets rid of the sentinel bits from the file
    for i in range(len(SENTINEL) - 1):
        hiddenFile.pop()
    
    sys.stdout.buffer.write(hiddenFile)
    
else:
    sys.exit()
