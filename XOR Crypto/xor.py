#####################################################
# Team: The Emperor
# Members: Jackson Sikes, Austin Harvey, Nolan Yelverton, Than Nguyen, Thomas Nguyen, Trinh Vo, John Norris, Luke McMillan
# Description: XOR encryptor/decryptor
# Date: 05/07/21
#####################################################

from sys import stdin, stdout, argv, exit

DEBUG = False
lenMatch = True

# Try to open the key in the current directory. If it doesn't exist, exit the program and tell the user to put
#  a key in the directory 
try:
    file = open("key", "rb")
except OSError:
    print("A key could not be found. Please put a key named 'key' in the current directory and try again. \n")
    exit()

# Read the file
key = bytearray(file.read())
if(DEBUG):
    print(key)
    print("\n")

# Read the input buffer
cypher = bytearray(stdin.buffer.read())
if(DEBUG):
    print(cypher)
    print("\n")

# Determine the length of how big the buffer needs to be, then create a byte array of that size
byteLen = len(cypher)
byteBuffer = bytearray(byteLen)

if(DEBUG):
    print("byteLen: {}\n".format(byteLen))
    print("keyLen: {}\n".format(len(key)))
    exit()

# Check and see if the key and text are not the same length, and set lenMatch to false is they are not the same length
if (byteLen != len(key)):
    lenMatch = False

if (lenMatch):
    # XOR each byte of the cypher text to decrypt it
    for byte in range (byteLen):
        byteBuffer[byte] = cypher[byte] ^ key[byte]

    # Write the output to stdout buffer
    stdout.buffer.write(byteBuffer)

else:
    if(len(key) > byteLen):
        # XOR each byte of plain text to encrypt it
        for byte in range (byteLen):
            byteBuffer[byte] = cypher[byte] ^ key[byte]
    else:
        # Loop through cypher and XOR it with the key
        cypherRemaining = byteLen
        index = 0
        while(cypherRemaining != 0):
            # index % key will give us the correct key index of any given length of cypher text
            byteBuffer[index] = cypher[index] ^ key[index % len(key)]
            index += 1
            cypherRemaining -= 1

    
    # Write the output to stdout buffer
    stdout.buffer.write(byteBuffer)
