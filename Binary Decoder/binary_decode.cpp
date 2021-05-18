#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Prototype our function
char* binToASCII(int binDecodeLen, char* bin);

int main(int argc, char *argv[]){

    // Declare a variable to store the input file
    FILE *fp;

    // Create a buffer variable for the read file
    char buff[4096];
    memset(buff, 0, 4096);

    // Read the input file
    fp = fopen(argv[1], "r");
    fgets(buff, 4096, (FILE*)fp);

    // Determine the length of the encoded text
    int len;
    len = strlen(buff) - 1;

    // Check to see what ASCII type to use
    if(len % 8 == 0 && len % 7 == 0){
        // Decode the binary, and print the decoded text to the screen
        char* decoded1 = binToASCII(7, buff);
        char* decoded2 = binToASCII(8, buff);
        printf("Decoded message:\n%s\nLen: 7\n", decoded1);
        printf("Decoded message:\n%s\nLen: 8\n", decoded2);
        // Free up the space used by the variables
        free(decoded1);
        free(decoded2);
    }
    else if(len % 8 == 0){
        // Decode the binary, and print the decoded text to the screen
        char* decoded = binToASCII(8, buff);
        printf("Decoded message:\n%s\nLen: 8\n", decoded);
        // Free up the space used by the variables
        free(decoded);
    }
    else if(len % 7 == 0){
        char* decoded = binToASCII(7, buff);
        printf("Decoded message:\n%s\nLen: 7\n", decoded);
        // Free up the space used by the variables
        free(decoded);
    }
    
    else{
        printf("Failed to determine the ASCII type automatically\n");
        printf("printing both types\n");
        // Decode the binary, and print the decoded text to the screen
        char* decoded1 = binToASCII(7, buff);
        char* decoded2 = binToASCII(8, buff);
        printf("Decoded message: %s\nLen: 7\n", decoded1);
        printf("Decoded message: %s\nLen: 8\n", decoded2);
        // Free up the space used by the variables
        free(decoded1);
        free(decoded2);
    };

    return 0;
}

char* binToASCII(int binDecodeLen, char* bin){
    // Allocate and set memory for a veriable to store our decoded text
    char* decoded = (char*)malloc(4096);
    memset(decoded, 0, 4096);
    // Create a variable to store our chars as we convert them
    char tempChar[10];

    // Calculate the length of the encoded text
    int len;
    len = strlen(bin);

    // Keep track of the "backspace offset"
    int offset = 0;

    // Loop through every "chuck" of binary and convert it to ASCII
    for(int i = 0; i * binDecodeLen < len; i++){
        memcpy(tempChar, &bin[i * binDecodeLen], binDecodeLen);
        tempChar[binDecodeLen + 1] = '\0';
        if(strtol(tempChar, NULL, 2) == '\x08'){
            decoded[i - 1 - offset] = 0;
            offset += 2;
        }
        else{
            decoded[i - offset] = strtol(tempChar, NULL, 2);
        }
    }

    return decoded;
}