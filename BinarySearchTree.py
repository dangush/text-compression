class binary_search_tree:

    #Not the usual way to construct from what I'm aware, but
    #this is designed for my use case, where the 'tree' already exists
    def __init__(self, node):
        self.root = node


    def filltable(self, start, binaryoutput, table, rootvalue):
        #True is left, False is right
        if start.char == None:

            binaryoutput += "1"
            binaryoutput = self.filltable(start.left, binaryoutput, table, rootvalue)
            binaryoutput += "0"
            binaryoutput = self.filltable(start.right, binaryoutput, table, rootvalue)

        if start.char != None:  #This if statement makes sure that a frequency node doesn't get entered into table.
            table[start.char] = binaryoutput

        if start.freq == rootvalue: #To escape recursion and return the table we're looking for.
            return table
        return binaryoutput[0:-1]




