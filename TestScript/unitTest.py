#    unitTest.py contains all unit test scipts
#
#    Author: Jerome Israel
#    Created: 11.12.11 | Updated: 11.08.14
#
# ------------------------------------------

#!/usr/bin/env python

import unittest
import os
from os import sys, path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import Backend.Distance
import Backend.KDTree
import Backend.FileParser
import config
# Here's our "unit".
def IsOdd(n):
    return n % 2 == 1

#Unit test case to test distance method.
class distanceTest(unittest.TestCase):

    def testPositive(self):
        self.failUnless(Backend.Distance.distance_on_unit_sphere(1, 10, 1, -1) > 0)

    def testZero(self):
        self.failUnless(Backend.Distance.distance_on_unit_sphere(1, -1, 1, -1) == 0)

#Unit test case to test KD tree
class testKDTree(unittest.TestCase):

    def testEmptyRoot(self):
    	lTree = Backend.KDTree.LocationTree()

        self.failUnless(lTree.getRoot() is None)

    def testNonEmptyRoot(self):
        lTree = Backend.KDTree.LocationTree()

        lTree.put((1,-1), "1234")

        self.failUnless(lTree.getRoot() is not None)
        self.failUnless(lTree.length() > 0)

    def testRightChild(self):
        lTree = Backend.KDTree.LocationTree()

        lTree.put((1,-1), "1234")
        lTree.put((2,1), "RightChild")
        self.failUnless(lTree.getRoot() is not None)
        self.failUnless(lTree.length() > 1)
        self.failUnless(lTree.getRoot().hasRightChild() is not None)

    def testLeftChild(self):
        lTree = Backend.KDTree.LocationTree()

        lTree.put((1,-1), "1234")
        lTree.put((.5,1), "LeftChild")
        self.failUnless(lTree.getRoot() is not None)
        self.failUnless(lTree.length() > 1)
        self.failUnless(lTree.getRoot().hasRightChild() is None)
        self.failUnless(lTree.getRoot().hasLeftChild() is not None)

    def testLeafNode(self):
    	lTree = Backend.KDTree.LocationTree()

        lTree.put((1,-1), "1234")
        lTree.put((.5,1), "LeftChild")
        self.failUnless(lTree.getRoot().hasLeftChild().isLeafNode() is True)

#Unit test case for FileParser.py
class testFileParser(unittest.TestCase):
	'''
	def testReadFile(self):
		fp = Backend.FileParser.FileParser("TestScript/TestData.csv" , "csv")
		fp.parseFile(config.file['columnnames'])
		print len(fp.fileheader)
		self.failUnless(len(fp.fileheader) > 0)
	'''
def main():
    unittest.main()

if __name__ == '__main__'and __package__ is None:
    
    main()