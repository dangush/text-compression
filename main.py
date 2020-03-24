from Node import Node
from BinarySearchTree import binary_search_tree
import pickle
import os

def main():

    option = int(input("Welcome to Text Compression. Enter 1 to compress, 2 to decompress, 3 to exit.\n"))

    while option != 3:

        if option == 1:

            inputfilename = input("Enter filename to compress (Format: name.txt)\n")

            charlist = list()

            existingchars = dict()



            #get characters and their frequencies
            with open(inputfilename) as f:
                for line in f:
                    for ch in line:
                        if ch in existingchars:
                            existingchars[ch] += 1
                        else:
                            existingchars[ch] = 1

            #Turn dictionary into list of nodes
            for key in existingchars:
                charlist.append(Node(existingchars[key], str(key)))

            #Sort based on nodes' freq
            charlist.sort(key=lambda node: node.freq, reverse=True)

            print("Constructing tree...")


            #Here each of the last two character nodes of the list are put into a new node with a frequency of the two 
            #character nodes' frequencies combined.
            #The last two character nodes, now placed into a new node, are removed- the new node replaces the second
            #to last one, and the list is shortened by one. 
             
            while len(charlist) != 1:

                totalFreq = charlist[-1].freq + charlist[-2].freq
                newNode = Node(totalFreq, None)
                newNode.left = charlist[-1]
                newNode.right = charlist[-2]
                charlist[-2] = newNode
                del charlist[-1]
                charlist.sort(key=lambda node: node.freq, reverse=True)


            huffmantree = binary_search_tree(charlist[0]) #Make our loaded node an actual, defined tree.

            table = dict() #We'll store the new bit values from our tree in here for easy lookup.

            huffmantree.filltable(huffmantree.root, "", table, huffmantree.root.freq) #Fill the dictionary
            print("Table completed...")

            outputbinary = "" #Where we're storing compressed text!

            with open(inputfilename) as f:
                for line in f:
                    for ch in line:
                        outputbinary += table[ch]

            outputbinary_length = len(outputbinary)

            #Adding zeros to make result fit into bytearray

            extrazeros = 8 - (len(outputbinary) % 8)
            for i in range(0, extrazeros):
                outputbinary += "0"

            #Adding the header to the outputbinary
            header = bin(outputbinary_length)[2:]

            while not len(header) % 8 == 0:
                header = "0" + header

            if outputbinary_length < 255:
                header = "0000000000000000" + header
            elif 255 < outputbinary_length < 65535:
                header = "00000000" + header


            final_outputbinary = header + outputbinary

            #Converting the string into a bytearray and writing into the file.

            b = bytearray()
            for i in range(0, len(final_outputbinary), 8):
                b.append(int(final_outputbinary[i:i+8], 2))

            exportfilename = input("Enter name for compressed file. Don't include extension.\n") + ".bin"

            with open(exportfilename, 'wb') as f:
                f.write(bytes(b))
            f.close()

            #Save huffman tree into the same file.
            save(huffmantree, exportfilename)

            print("Done. Check out " + exportfilename + ". Back to menu.")


        elif option == 2:
            exportfilename = input("Enter name of file to decompress (Format: name.bin)\n")

            inputbinary = ""
            inputbinarylength = ""
            #Convert bitstream into string.

            with open(exportfilename, "rb") as f:
                for i in range(0,3): #First three bytes determine length of binary to be read/considered.
                    byte = f.read(1)
                    byte_num = int.from_bytes(byte, byteorder='big')
                    byte_2 = str(bin(byte_num)[2:])
                    str_byte = makeFullByte(byte_2)
                    inputbinarylength = inputbinarylength + str_byte

                inputbinarylength = int(inputbinarylength, 2)

                for j in range(0, inputbinarylength, 8): #Now we reading the rest of the bytes, putting the bits all in one string.
                    byte = f.read(1)
                    byte_num = int.from_bytes(byte, byteorder='big')
                    byte_2 = str(bin(byte_num)[2:])
                    str_byte = makeFullByte(byte_2)
                    inputbinary = inputbinary + str_byte

                print("Loading binary...")

                huffmantree = load(f)

            inputbinary = inputbinary[:inputbinarylength] #Getting rid of any extra zeros used to pad out byte.

            print("Decompressing...")
            letterFound = False
            originalfile = open('original.txt', 'w')

            k =0
            while k < len(inputbinary): #Special edition for loop
                cur = huffmantree.root
                letter = ''

                letterFound = False

                while letterFound == False:
                    direction = inputbinary[k]

                    if direction == '1':
                        cur = cur.left
                        if cur.char != None:
                            letterFound = True
                            letter = cur.char
                            originalfile.write(letter)
                    if direction == '0':
                        cur = cur.right
                        if cur.char != None:
                            letterFound = True
                            letter = cur.char
                            originalfile.write(letter)

                    k += 1

            print("Done! Check 'original.txt'")

        else:
            print("Unrecognized option.")

        option = int(input("Welcome to Text Compression. Enter 1 to compress, 2 to decompress, 3 to exit.\n"))

#Maybe try to make this recursive as a challange? Idk
def decode(start, inputbinary, i, originalfile):
    direction = inputbinary[i]

    if direction == '1':
        if start.char != None:
            return start.char
        else:
            decode(start.left, inputbinary, i - 1, originalfile)
    if direction == '0':
        if start.char != None:
            return start.char
        else:
            decode(start.right, inputbinary, i - 1, originalfile)

def save(tree, filename):
    #APPEND BINARY
    exportfile = open(filename, 'ab')
    pickle.dump(tree, exportfile)
    exportfile.close()

def load(exportfile):
    tree = pickle.load(exportfile)
    exportfile.close()
    return tree

def makeFullByte(num):
    while len(num) % 8 != 0:
        num = "0" + num
    return num


main()



