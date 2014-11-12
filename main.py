#    Used the sample main.py from Mike Dory | dory.me for
#    the skeleton starter code
#
#    Author: Jerome Israel
#    Created: 11.12.11 | Updated: 11.08.14
#
# ------------------------------------------

#!/usr/bin/env python
import os.path
import tornado.escape
from tornado.escape import json_encode
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import config
import Backend.FileParser as fileparser
import json

# import and define tornado-y things
from tornado.options import define
define("port", default=5000, help="run on the given port", type=int)


# application settings and handle mapping info
class Application(tornado.web.Application):
    def __init__(self):
        
        #Instance of FileParser
        self.fp = None

        #Prepare and load data
        self.driver()

        #Request Handler
        handlers = [
            (r"/([^/]+)?", MainHandler, { 'fileParser' : self.fp }), 
        ]

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

    # Driver method: Drives all parsing and data structure/load operations
    def driver(self):

        filename = config.file['filename']

        path = config.file['path']

        inputFile = path + filename
        filetype = config.file['type']

        self.fp = fileparser.FileParser(inputFile, filetype)
        self.fp.parseFile(config.file['columnnames'])


# the main page
class MainHandler(tornado.web.RequestHandler):

    #Initialize method to pass in instance variables from driver method(Application class)
    def initialize(self, fileParser):
        self.fp = fileParser
        self.AddressIndex = self.fp.addresslookup['address']
        self.filecontent = self.fp.filecontent
        self.fileheader = self.fp.fileheader
        self.locationTree = self.fp.locationTree
        self.response = {'resonse' : {}}

    #Handles all get calls
    def get(self, q):

        if(q is None):
            self.render(
                "main.html",
                page_title='Food Truck search',
                page_heading='Food Truck:'
            )

        #Handle fetchAddress call
        if(q == "fetchAddress"):
            #print "Please fetch the address"
            
            preaddress = self.get_argument("preaddress")
            
            self.write(json.dumps(self.fetchAddress(str(preaddress))))

        #Handle fetchNeighborsFromAddress call
        if(q == "fetchNeighborsFromAddress"):

            address = self.get_argument("address")

            addressMap = self.fetchAddress(str(address))

            result = self.getNeighboursFromAddress(addressMap, address)

            self.write(json.dumps(result))

        #Handle fetchNeighborsFromLocation call
        if(q == "fetchNeighborsFromLocation"):

            latitude  = self.get_argument("latitude")
            longitude = self.get_argument("longitude")

            result = self.getNeighboursFromLocation(latitude, longitude)

            self.write(json.dumps(result))


    #Searches for the nearest neighbors and returns the location data
    def getNeighboursFromAddress(self, addressMap, address):

        try:
            searchlocationid = addressMap[address]
            #look up for latitude and longitude of the location id
            searchlocationdata = self.filecontent[searchlocationid]['data']
            #search the location tree
            neighbors = self.locationTree.searchTree(eval(searchlocationdata[self.fileheader['Location']]))

            #consolidate results to a map
            return self.getNeighbourLocationData(neighbors)

        except KeyError:
            return { 'success' : False,
                    'errorMessage' : 'Location not found'}

    #Searched for the nearest neighbours based on the input location
    def getNeighboursFromLocation(self, latitude, longitude):

        #search the location tree
        neighbors = self.locationTree.searchTree((latitude, longitude))

        #consolidate results to a map
        return self.getNeighbourLocationData(neighbors)

    #getNeighbourLocationData loops through the neighbors dictionary and fetches all necessary data
    def getNeighbourLocationData(self, neighbors):

        result = {"success" : True, "result" : {}}

        tempResult = result["result"]

        for locationid, distance in neighbors.iteritems():
            tempResult[locationid] = {
                              'name' : self.filecontent[locationid]['data'][self.fileheader['Applicant']],
                              'type' : self.filecontent[locationid]['data'][self.fileheader['FacilityType']],
                              'food' : self.filecontent[locationid]['food'],
                              'address' : self.filecontent[locationid]['data'][self.fileheader['Address']],
                              'latitude' : eval(self.filecontent[locationid]['data'][self.fileheader['Location']])[0],
                              'longitude' : eval(self.filecontent[locationid]['data'][self.fileheader['Location']])[1],
                              'status' : self.filecontent[locationid]['data'][self.fileheader['Status']],
                              'distance' : round(distance, 2)
                            }
                          
            
        return result


    #search the address and send the first five matches
    def fetchAddress(self, preaddress):
        
        #Split the input preaddress to array
        searchaddress = list(preaddress)
        tempaddresses = self.AddressIndex

        tempAddress = ''

        #Check for address
        for c in searchaddress:
            if(c in tempaddresses):
                tempaddresses = tempaddresses.get(c)
                tempAddress = tempAddress + c
            elif(c.upper() in tempaddresses):
                tempaddresses = tempaddresses.get(c.upper())
                tempAddress = tempAddress + c.upper()
            elif(c.lower() in tempaddresses):
                tempaddresses = tempaddresses.get(c.lower())
                tempAddress = tempAddress + c.lower()
            else:
                pass
        
        possibleAddresses = {}

        possibleAddresses = self.recurse(tempaddresses, possibleAddresses, tempAddress)

        return possibleAddresses

    def recurse(self, d, possibleAddresses, tempAddress):

        if type(d)==type({}):

            for k in d:

                tempAdd = tempAddress + k
                possibleAddresses = self.recurse(d[k], possibleAddresses, tempAdd)
        else:
            if(len(possibleAddresses) < 5):
                possibleAddresses[tempAddress] =  d

        return possibleAddresses



# RAMMING SPEEEEEEED!
def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(tornado.options.options.port)

    # start it up
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
