import sys

inputs = sys.argv

#removes the file name from the inputs of the program
inputs.pop(0)

#determines whether to encrypt or decrypt using the provided key
enORdecrypt = inputs.pop(0)

#sets the key
key = inputs.pop(0)



try:
    while(True):
        #gets input from the terminal
        phrase = input()
        
        #sets variables to be used
        crypt = 0
        kindex = 0
        C = []
        lower = 0
        a = 0
        nonletter = True
        
        if(phrase == "D"):
            break
        
        #sets a variable to determine if the code is encrypting or decrypting
        if(enORdecrypt == '-e'):
            crypt = 1

        elif(enORdecrypt == '-d'):
            crypt = -1
        
        #loops through the input phrase to encrypt/decrypt it
        for letter in phrase:
            letter = ord(letter)
            #Determines if the letter is capital or not in order to determine what values to use
            if(letter >= ord('A') and letter <= ord('Z')):
                lower = ord('A')
                nonletter = False

            elif(letter >= ord('a') and letter <= ord('z')):
                lower = ord('a')
                nonletter = False
                
            else:
                nonletter = True
                C.append(chr(letter))
                
            if(not nonletter):
                #keeps the index of the key within bounds and loops through if the phrase is longer
                keynotLetter = True
                while(keynotLetter):
                        
                    kindex %= len(key)
                    keyI = ord(key[kindex])
                    kindex += 1
                    
                    #Determines if the key letter is capital to use the correct factors
                    if(keyI >= ord('A') and keyI <= ord('Z')):
                        a = ord('A')
                        keynotLetter = False
                        
                    elif(keyI >= ord('a') and keyI <= ord('z')):
                        a = ord('a')
                        keynotLetter = False
                           
                #calculates the encrypted/decrypted character and adds it to a list and only
                #encrypt/decrypts the letters of the alphabet
                C.append(chr((letter - lower + crypt*(ord(key[kindex - 1]) - a) + 26) % 26 + lower))
                #print(f"CAdd: {chr((letter - lower + crypt*(ord(key[kindex - 1]) - a) + 26) % 26 + lower)}")


        sys.stdout.write(f"{''.join(C)}\n")
    
except:
    sys.stdout.write('\n')
    sys.stdout.close()
