import math
import string
import sys
import numpy as np
from egcd import egcd 
alphabet = "abcdefghijklmnopqrstuvwxyz"
letter_to_index = dict(zip(alphabet, range(len(alphabet))))
index_to_letter = dict(zip(range(len(alphabet)), alphabet))

#Caesar_Cipher Algorithm
def Caesar_Cipher(PlainText,Key):
    """
    encrypt the input string based on the key and return encrypted message as a string.
    Args:
        PlainText: string.
        Key: integer.
    Returns:
        CipherText: string.
    """ 
    
    CipherText = "" 
    # traverse text 
    for i in range(len(PlainText)): 
        if (PlainText[i]== '\n'):
            continue
        else:
            char = PlainText[i] 
    
            # Encrypt_uppercase_characters 
            if (char.isupper()): 
                CipherText += chr((ord(char) + Key-65) % 26 + 65) 
    
            # Encrypt_lowercase_characters 
            else: 
                CipherText += chr((ord(char) + Key - 97) % 26 + 97) 
   
    CipherText=CipherText.upper()
    return CipherText 
    
#Play_Fair_Cipher Algorithm
def find_position(key_matrix,letter):
    """
    find the row number and column number of a given letter in the given key_matrix.
    Args:
        key_matrix: 5*5 matrix of characters.
        letter: char.
    Returns:
        x: integer.
        y: integer.
    """ 
    
    x = y = 0
    for i in range(5):
        for j in range(5):
            if key_matrix[i][j]==letter:
                x=i        #row number
                y=j        #column number

    return x,y

def Play_Fair_Cipher(plaintext,keyword):
    """
    encrypt the input string based on the key and return encrypted message as a string.
    Args:
        PlainText: string.
        keyword  : string.
    Returns:
        CipherText: string.
    """ 
    kay_as_list=[]
    plaintext=plaintext.upper()
    plaintext = plaintext.replace(" ","")
    keyword=keyword.upper()
    keyword = keyword.replace(" ","")
    alpha='abcdefghijklmnopqrstuvwxyz'
    alpha=alpha.upper()

    #Create Key Matrix
    
    #fill the kay_as_list with the key
    for e in keyword:
        if e not in kay_as_list:
            kay_as_list.append(e)


    #complete the kay_as_list with alphapet 
    for e in alpha:
        if e not in kay_as_list:
            if e=='J':
                continue
            else:
                kay_as_list.append(e)
    
    #convert list into 5*5 matrix for key_matrix
    keyword_matrix=[]
    for e in range(5):
        keyword_matrix.append('')
        
    keyword_matrix[0]=kay_as_list[0:5]
    keyword_matrix[1]=kay_as_list[5:10]
    keyword_matrix[2]=kay_as_list[10:15]
    keyword_matrix[3]=kay_as_list[15:20]
    keyword_matrix[4]=kay_as_list[20:25]

    #plaintext
    message=[]
    for  character in plaintext:
        message.append(character)

    #even length
    i=0
    l=int(len(message)/2)
    #padding with X if there is 2 consecutive equal char  
    for both in range(l):
        if message[i]== message[i+1]:
            message.insert(i+1,'X')
        i=i+2
        
    #padding with X in case the message of odd length
    if len(message)%2==1:
        message.append("X")
    i=0
    new_message=[]
    l=int(len(message)/2)+1
    
    for g in range(len(message)):
        if message[g] == 'J':
            message[g] = 'I'
    

    #split message and put in new message matrix
    for x in range(1,l):
        new_message.append(message[i:i+2])
        i=i+2    
   
    #Encryption
    q=0
    cipher_as_list=[]
    for e in new_message:
        p1,q1=find_position(keyword_matrix,e[0])
        p2,q2=find_position(keyword_matrix,e[1])
        #the two letters in the same row --> take the letter in the right in the same row for encryption
        if p1==p2:
                if q1==4:
                        q1=-1
                if q2==4:
                        q2=-1
                cipher_as_list.append(keyword_matrix[p1][q1+1])
                cipher_as_list.append(keyword_matrix[p1][q2+1])
                
        #the two letters in the same column --> take the letter in the down in the same column for encryption      
        elif q1==q2:
                if p1==4:
                        p1=-1
                if p2==4:
                        p2=-1
                cipher_as_list.append(keyword_matrix[p1+1][q1])
                cipher_as_list.append(keyword_matrix[p2+1][q2])
                
        #general case: the two letters in different rows and columns
        else:
            cipher_as_list.append(keyword_matrix[p1][q2])
            cipher_as_list.append(keyword_matrix[p2][q1])

    
    cipher_text=''.join(cipher_as_list)  #convert cipher list which represent cipher text into a string. 
    return cipher_text

#Hill_Cipher Algorithm
def getKeyMatrix(key):
    """
    convert key array into matrix 2*2 or 3*3.
    Args:
        key: array of integers.
    Returns:
        key_Matrix: 2*2 or 3*3 matrix.
    """ 
    if(len(key)==4):
       key_Matrix =np.reshape(key,(2,2))
      
    
    elif(len(key)==9):
       key_Matrix =np.reshape(key,(3,3))
       
    else:
        return("Error")
        
    return(np.matrix(key_Matrix))
    
def Hill_Cipher(message, key):
    """
    Encrypt input message.
    Args:
        message: string
        key: array of integers.
    Returns:
        Encrypted_Message:string.
    """ 
    
    Encrypted_Message = ""
    message=message.replace(" ","")  #remove spaces 
    message = message.lower()        #lower case of messag
    message_in_numbers = []
    key = getKeyMatrix(key)          #obtain key_Matrix
    
    # padding with x according to shape of key_Matrix
    if(key.shape[0] == 2):
        if(len(message) %2 !=0):
            message = message + 'x'
    elif(key.shape[0] == 3):
        if(len(message) %3 !=0):
            if(len(message) %3 ==1):
                message = message + 'xx'
            else:
                message = message + 'x' 
        
    #save message as an list of integers based on char index 
    for letter in message:
        message_in_numbers.append(letter_to_index[letter])
        
    #split message based key shape (2*2) or (3*3)
    split_PlainText = [
        message_in_numbers[i : i + int(key.shape[0])]
        for i in range(0, len(message_in_numbers), int(key.shape[0]))
    ]
    
    for P in split_PlainText:
        P = np.transpose(np.asarray(P))[:, np.newaxis]

        numbers = np.dot(key, P) % len(alphabet)
        n = numbers.shape[0]  # length of encrypted message (in numbers)

        # Map back to get encrypted text
        for idx in range(n):
            number = int(numbers[idx, 0])
            Encrypted_Message += index_to_letter[number]
            
    Encrypted_Message=Encrypted_Message.upper()
    return Encrypted_Message
    
#Vigenere_Cipher Algorithm
def generateKey(message,key,mode):  
    """
    Generate key with the same lengh on message based on the message length and mode.
    Args:
        message: string
        key: string.
    Returns:
        key:string.
    """ 
    key=key.upper()   
    message=message.upper()
    key = list(key) 

    if len(message) == len(key): 
        return(key) 
    else: 
        #mode == false : repeating mode key --> repeat the key to get key and message of equal length
        if(mode == False) :
            
            for i in range(len(message) -len(key)): 
                key.append(key[i % len(key)]) 
            return("" . join(key)) 
        else: 
            #mode == true : auto mode key  --> complete the key with the message to get key and message of equal length
            for i in range(len(message) -len(key)): 
                key.append(message[i % len(key)]) 
            return("" . join(key))

def Vigenere_Cipher(message,key,mode): 
    """
    Encrypt the input meaasge.
    Args:
        message: string.
        key: string.
    Returns:
        cipher_text:string.
    """ 
    key = generateKey(message,key,mode)
    message=message.upper()
    
    cipher_text = [] 
    
    for i in range(len(message)): 
        if (message[i]== '\n'):
            continue
            
        else:
            x = ((ord(message[i])%65 + ord(key[i])%65)) %26
            x += ord('A') 
            cipher_text.append(chr(x)) 
    
    return("" . join(cipher_text))
    
#Vernam_Cipher Algorithm
def Vernam_Cipher(PlainText, key):
    """
    Encrypt the input meaasge.
    Args:
        PlainText: string.
        key: string.
    Returns:
        cipher_text:string.
    """ 
    PlainText = PlainText.upper()
    key  = key.upper()
    cipher_text = "";
    ptr = 0;
    for char in PlainText:
        cipher_text = cipher_text + chr((((ord(char)-65) ^ (ord(key[ptr])-65))%26)+65);
        ptr = ptr + 1;
        if ptr == len(key):
              ptr = 0;
    return cipher_text

def main ():
    print("                                        Welcome_to_Classical_Ciphers                                       \n\n")
    
    print("Select your desired Cipher:\n")
    
    while(1):
        print(" 1  Caesar_Cipher\n 2  Play_Fair_Cipher\n 3  Hill_Cipher\n 4  Vigenere_Cipher\n 5  Vernam_Cipher\n 0 Exit\n")
        sel = input()
        if sel == "1":
            #Caesar_Cipher
            input_1 =open('Caesar/caesar_plain.txt',"r")
            fl=input_1.readlines() 
            output_1=open('Caesar/caesar_cipher.txt',"w")
            key1=input("Enter key for Caesar_cipher:  ")
           
            for x in fl: 
                result=Caesar_Cipher(x[:-1],int(key1))
                output_1.write(result)
                output_1.write("\n")
            
            output_1.close()
            print("\n")
            continue    
        elif sel == "2":
            #Play_Fair_Cipher
            input_2=open('PlayFair/playfair_plain.txt',"r")
            f2=input_2.readlines() 
            output_2=open('PlayFair/playfair_cipher.txt',"w")
            key2=input("Enter key for Playfair_cipher:  ")
            for x in f2: 
                result=Play_Fair_Cipher(x[:-1],key2)
                output_2.write(result)
                output_2.write("\n")
        
            output_2.close()
            print("\n")
            continue
        #Hill_Cipher
        elif sel == "3":
            m=input("Enter 2 for 2*2 key or 3 for 3*3 key for Hill_Cipher :  ")
            key3=[]
            if(int(m)==2):
                input_3=open('Hill/hill_plain_2x2.txt',"r")
                f3=input_3.readlines() 
                print("Enter key for Hill_Cipher row by row: ")
                for i in range(4):
                    key=input()
                    key3.append(int(key))


            else:
                input_3=open('Hill/hill_plain_3x3.txt',"r")
                f3=input_3.readlines()
                print("Enter key for Hill_cipher row by row: ")
                for i in range(9):
                    key=input()
                    key3.append(int(key)) 

            output_3=open('Hill/hill_cipher.txt',"w")
            
            for x in f3: 
                result=Hill_Cipher(x[:-1],key3)
                output_3.write(result)
                output_3.write("\n")
            
            output_3.close() 
            print("\n")
            continue
            
            #Vigenere_Cipher
        elif sel == "4":
            
            input_4 = open('Vigenere/vigenere_plain.txt',"r")
            f4=input_4.readlines() 
            key4=input("Enter key for vigenere_cipher: ")
            output_4=open('Vigenere/vigenere_cipher.txt',"w")
            mode=input("Enter false for repeated encryption or true for autokey encryption : ")
            if(mode == "false"):
                for x in f4: 
                    result=Vigenere_Cipher(x[:-1], key4 , False)
                    output_4.write(result)
                    output_4.write("\n")
            else:
                for x in f4: 
                    result=Vigenere_cipher_algor(x[:-1], key4 , True)
                    output_4.write(result)
                    output_4.write("\n")

            output_4.close()
            print("\n")
            continue
            
           #Vernam_Cipher 
        elif sel == "5":
            input_5 =open('Vernam/vernam_plain.txt',"r")
            f5=input_5.readlines() 
            output_5=open('Vernam/vernam_cipher.txt',"w")
            key5=input("Enter key for vernam_cipher: ")
            for x in f5: 
                result=Vernam_Cipher(x[:-1],key5)
                output_5.write(result)
                output_5.write("\n")
            
            output_5.close()
            print("\n")
            continue
        elif sel == "0":
            break
        else:
            print("Invalid Operation: please Enter a Correct Number\n\n")
            continue
    
    
    
    
    
    

    
    

    
    

    
    

    
    
main()