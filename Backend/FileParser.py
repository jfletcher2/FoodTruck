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
import Distance

class FileParser():

    #Initialize variables for the FileParser class
    def __init__(self , inputfile, filetype):
        self.inputfile = inputfile
        self.filetype = filetype
        self.addresslookup = {'address' : {}}
        self.nearestLocation = {}
        self.filecontent = {}
        self.fileheader = {}

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
                        #Load all the values on to file content
                        rowContents = {'data' : row}
                        self.filecontent[row[0]] = rowContents
                
        else:
            print "***File Type not supported***"

    #Loads the addresslookup variable for each address lookup
    #Each address string is split in to list of characters and
    #loaded into the addresslookup dictionary word by word
    #("eg. 'Hello st' will be {'H'{'e'{'l'{'l'{'o'{' '{'s'{'t':<locationid>}}}}}}}})")
    def loadAddressLookup(self, addresscolname):
        print addresscolname
        addressIndex = self.fileheader[addresscolname]
        print 'Column index : ' 
        print addressIndex
        i = 0
        for key, val in self.filecontent.iteritems():
            locationid = key
            tempaddress = val['data'][int(addressIndex)]
            #Splits the string in to lists of characters
            tempchar = list(tempaddress)
            #print locationid + "  :-->  " 
            #print templist
            FileParser.loadaddressdictionaryfromlist(self, tempchar, locationid)
            
            #FileParser.recurse(self, self.addresslookup['address'] ,tempchar, locationid)

    def loadaddressdictionaryfromlist(self, listchar, locationid):
        print listchar
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
               # self.addresslookup = templookup
            i = i + 1
            print templookup
    
    def calculateDistance(self):
        i = 0
        for row in self.filecontent:
            i = i + 1
            print row[5],row[14], row[15]
            
            if(i > 1):
                try:
                    print Distance.distance_on_unit_sphere(37.7901490737255, -122.398658184604, 
                                                        float(row[14]), float(row[15])) * 3960
                except ValueError:
                    pass
            else:
                print row
            if(i>50):
                break

    #ParseFile method manages all the parsing operations
    def parseFile(self, columnnames):
        if(self.inputfile != ''):
            FileParser.readFile(self)
            #print self.filecontent
            #print self.fileheader
            FileParser.loadAddressLookup(self, columnnames['address'])
            print self.addresslookup
        else:
            print 'Please enter a valid data file.'


