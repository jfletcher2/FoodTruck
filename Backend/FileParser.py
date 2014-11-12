#    FileParser.py contains the FileParser class
#	 which contains all the methods necessary for
#	 parsing the file
#    
#
#    Author: Jerome Israel (fletcher.jerome@gmail.com)
#    Created: 11.05.14 | Updated: 11.05.14
#
# ------------------------------------------

import csv
import KDTree


class FileParser():

    #Initialize variables for the FileParser class
    def __init__(self , inputfile, filetype):
        self.inputfile = inputfile
        self.filetype = filetype
        self.addresslookup = {'address' : {}}
        self.nearestLocation = {}
        self.filecontent = {}
        self.fileheader = {}
        self.locationTree = KDTree.LocationTree()
        
    #Reads the data from the file and loads filecontent and fileheader variable
    def readFile(self):
        if(self.filetype == 'csv'):

            with open(self.inputfile, 'rb') as f:
                reader = csv.reader(f)
                header = []
                i = 0

                for row in reader:
                    
                    if(i == 0):
                        #Set some value other than 0 so that 
                        #the header will not be overwritten by the values
                        i = 99

                        j = 0
                        #loads the file header information and the index for each column
                        for headerval in row:
                            self.fileheader[headerval] = j
                            j = j + 1
                    else:
                        #Load all the values on to filecontent only is location data is provided
                        if(row[self.fileheader['Latitude']] and row[self.fileheader['Status']] != 'EXPIRED'):
                            rowContents = {'data' : row,
                                           'food' : row[self.fileheader['FoodItems']].split(':')}
                            self.filecontent[row[0]] = rowContents
                
        else:

            pass

    #Loads the addresslookup variable for each address lookup
    #Each address string is split in to list of characters and
    #loaded into the addresslookup dictionary word by word
    #("eg. 'Hello st' will be {'H'{'e'{'l'{'l'{'o'{' '{'s'{'t':<locationid>}}}}}}}})")
    def loadAddressLookup(self, addresscolname):

        addressIndex = self.fileheader[addresscolname]
        i = 0
        for key, val in self.filecontent.iteritems():
            locationid = key
            tempaddress = val['data'][int(addressIndex)]
            #Splits the string in to lists of characters
            tempchar = list(tempaddress)
            FileParser.loadaddressdictionaryfromlist(self, tempchar, locationid)

    #loadaddressdictionaryfromlist loads the addresslookup dictionary from char list (listchar)
    def loadaddressdictionaryfromlist(self, listchar, locationid):

        templookup = self.addresslookup.get('address')
        i = 1
        for c in listchar:
            if c in templookup:
                templookup = templookup[c]
            else:
                if(len(listchar) == i):
                    templookup[c] = locationid
                else:
                    templookup[c] = {}
                templookup = templookup[c]
            i = i + 1


    #Initializes and loads the location tree(KDTree)
    def loadLocationTree(self):
        #Create a list of location from the input data
        locationlist = []
        for key, value in self.filecontent.iteritems():

            locationlist.append((eval((value['data'][self.fileheader['Location']])), key))

        #Sort the location list based on Latitude
        locationlist.sort(key=lambda tup: tup[0])

        locationlistlength = len(locationlist)

        #Calculate the median
        if(locationlistlength % 2):
            median = locationlistlength / 2
        else:
            median = (locationlistlength + 1) / 2
        
        #insert the root of the location tree
        self.locationTree.put(locationlist[median][0], locationlist[median][1])

        #insert all the other elements
        for i in range(len(locationlist)):
            if(i == median):
                continue
            else:
                self.locationTree.put(locationlist[i][0], locationlist[i][1])

        return self.locationTree

    #ParseFile method manages all the parsing operations
    def parseFile(self, columnnames):
        if(self.inputfile != ''):

            self.readFile()
            self.loadAddressLookup(columnnames['address'])

            locTree = self.loadLocationTree()

            return self.addresslookup['address']
        else:
            pass


