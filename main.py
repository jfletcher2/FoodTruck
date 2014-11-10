#    Sample main.py Tornado file
#    (for Tornado on Heroku)
#
#    Author: Mike Dory | dory.me | Jerome Israel
#    Created: 11.12.11 | Updated: 11.08.14
#    Contributions by Tedb0t, gregory80
#
# ------------------------------------------

#!/usr/bin/env python
import os.path
import tornado.escape
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

        self.AddressIndex = {}
        #Prepare and load data
        self.driver()

        #Request Handler
        handlers = [
            (r"/([^/]+)?", MainHandler, { 'AddressIndex' : self.AddressIndex}), 
        ]

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

    # Driver method: Drives all parsing and data structure/load operations
    def driver(self):
        #print config.file['filename'] 
        filename = config.file['filename']

        print config.file['path']
        path = config.file['path']

        print os.path.isfile(path + filename)
        inputFile = path + filename
        filetype = config.file['type']
        fp = fileparser.FileParser(inputFile, filetype)
        self.AddressIndex = fp.parseFile(config.file['columnnames'])

        #print self.AddressIndex
        #fp.calculateDistance()

# the main page
class MainHandler(tornado.web.RequestHandler):

    #Initialize method to pass in instance variables from driver method(Application class)
    def initialize(self, AddressIndex):
        self.AddressIndex = AddressIndex


    #Handles all get calls
    def get(self, q):
        if 'GOOGLEANALYTICSID' in os.environ:
            google_analytics_id = os.environ['GOOGLEANALYTICSID']
        else:
            google_analytics_id = False

        if(q is None):
            self.render(
                "main.html",
                page_title='Food Truck search',
                page_heading='Food stop:',
                google_analytics_id=google_analytics_id,
            )

        print "Get method called"
        print q
        if(q == "fetchAddress"):
            print "Please fetch the address"
            
            preaddress = self.get_argument("preaddress")
            
            self.write(json.dumps(self.fetchAddress(str(preaddress))))

    #search the address and send the first five matches
    def fetchAddress(self, preaddress):
        
        #Split the input preaddress to array
        searchaddress = list(preaddress)
        print searchaddress
        tempaddresses = self.AddressIndex
        print self.AddressIndex

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
                print "Invalid address"

        print tempAddress

        
        possibleAddresses = {}

        possibleAddresses = self.recurse(tempaddresses, possibleAddresses, tempAddress)
        '''
        for key , val in tempaddresses:
            if(type(tempaddresses.get(key)) is dict):
                tempDict = tempaddresses.get(key)
                while (type(tempDict) is dict):
                    pass
        print tempaddresses
        '''
        #print possibleAddresses
        return possibleAddresses

    def recurse(self, d, possibleAddresses, tempAddress):
        if type(d)==type({}):
            for k in d:
                tempAdd = tempAddress + k
                possibleAddresses = self.recurse(d[k], possibleAddresses, tempAdd)
        else:
            if(len(possibleAddresses) < 5):
                possibleAddresses[tempAddress] =  d
            #print possibleAddresses
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
