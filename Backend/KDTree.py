#    KDTree.py contains location tree for locations
#	 building the KD Tree takes nlogn time and
#	 look up time takes logn for a given location
#	 (Latitude and longitude) to find K nearest 
#	 locations.
#    
#
#    Author: Jerome Israel (fletcher.jerome@gmail.com)
#    Created: 11.06.14 | Updated: 11.06.14
#	 Comments: Took the idea of algorithm from http://en.wikipedia.org/wiki/K-d_tree
#		and implemented my own code
import Distance
import sys

class Node:

	#Initialize variables for the KDTree node
    def __init__(self , location, locationid, parent = None, leftchild = None, rightchild = None):
    	self.location = location
    	self.locationid = locationid
    	self.leftchild = leftchild
    	self.rightchild = rightchild
    	self.parent = parent
    	self.visited = False

    #Returns true if the parent node is empty
    def isRoot(self):
    	return not self.parent

    #Returns true if the node is a leaf node
    def isLeafNode(self):
    	return not (self.rightchild or self.leftchild)

    #returns if the node has a left child
    def hasLeftChild(self):
    	return self.leftchild

    #returns if the node has a right child
    def hasRightChild(self):
    	return self.rightchild

    #Returns true if its the left child to the parent
    def isLeftChilld(self):
    	return self.parent and self.parent.leftChild == self

    #Return true if its the right child to the parent
    def isRightChild(self):
    	return self.parent and self.parent.rightchild == self


 



class LocationTree:
	
	def __init__(self):
		self.root = None
		self.size = 0
		self.height = 0

	def length(self):
		return self.size

	def __len__(self):
		return self.size

	def __iter__(self):
		return self.root.__iter__()

	#Return the reference to root node
	def getRoot(self):
		return self.root
	#Put method to insert the node into the location tree
	def put(self, key, value):
		#Check if root is available
		if self.root:
			self._put(key, value, self.root, 0)
		#else create root node
		else:
			self.root = Node(key, value)

		self.size = self.size + 1

	#_put method does the actual insertion in to the tree
	def _put(self, location, locationid, currentnode, index):

		if(index == 0):
			invertedindex = 1
		else:
			invertedindex = 0

		#print "Put check "
		#print location[index] + " < " + currentnode.location[index] + " = " 
		#print (float(location[index]) < float(currentnode.location[index]))
		#print location
		#print list(location)
		if(float(location[index]) < float(currentnode.location[index])):
			#Insert into left child
			if currentnode.hasLeftChild() is None:
				currentnode.leftchild = Node(location, locationid, parent = currentnode)
			else:
				self._put(location,locationid, currentnode.leftchild, invertedindex)
				
		else:
			#Insert into the right child
			if currentnode.hasRightChild() is None:
				currentnode.rightchild = Node(location, locationid, parent = currentnode)
				
			else:
				self._put(location,locationid,currentnode.rightchild, invertedindex)
				
	'''
	# Prints the tree
	def printTree(self, node):
		if(node is None):
			print "Node is empty"

		else:
			print "Node data : "
			print node.locationid
			print node.location
			print "Parent node: "
			if(node.parent is not None):
				print node.parent.locationid
			if(node.hasRightChild):
				print "Right Child"
				self.printTree(node.rightchild)
			if(node.hasLeftChild):
				print "Left child"
				self.printTree(node.leftchild)
	'''
	#Search the tree for nearest neighbors
	def searchTree(self, location, nNeighbors = 5):
		
		#print "Searching Tree"
		#print location
		nodesList = []
		currentnode = self.root
		index = 0
		#Traverse from the root to the leaf and load all the nodes that matches the criteria
		while(currentnode is not None):
			currentnode.visited = False
			nodesList.append(currentnode)
			if(float(location[index]) < float(currentnode.location[index])):
				
				currentnode = currentnode.leftchild
			else:

				currentnode = currentnode.rightchild


			#Index variable is used to check for latitude and longitude as we traverse down the tree
			if(index == 0):
				index = 1
			else:
				index = 0

		#print len(nodesList)
		'''
		for node in nodesList:
			print node.locationid
			print node.location
			'''
		return self.findneighbors(self.root, location, 0, nNeighbors, nodesList)

	#Finds the nearest n neighbors and add the location ids to the list variable "neighbors"
	def findneighbors(self, node, location, index, neighbors, nodesList):

		if(index == 0):
			invertedindex = 1
		else:
			invertedindex = 0

		neighborsList = {}

		for n in nodesList:
			if node is None:
				#print "Node is none"
				return neighborsList

			else:
				self.getNodeNChildNodeDistance(neighbors, neighborsList, location, n)
				#search if the rightchild is closer to the target location
				if(n.rightchild is not None):
					#print "Searching for right child"
					self.getNodeNChildNodeDistance(neighbors, neighborsList, location, n.rightchild)
					#search if the right grandchild is closer
					if(n.rightchild.rightchild is not None):
						self.getNodeNChildNodeDistance(neighbors, neighborsList, location, n.rightchild.rightchild)
					#search if the left grandchild is closer
					if(n.rightchild.leftchild is not None):
						self.getNodeNChildNodeDistance(neighbors, neighborsList, location, n.rightchild.leftchild)
				#search if the left child is closer to the target location
				if(n.leftchild is not None):
					#print "searching for left child"
					self.getNodeNChildNodeDistance(neighbors, neighborsList, location, n.leftchild)
					#search if the right grandchild is closer
					if(n.leftchild.rightchild is not None):
						self.getNodeNChildNodeDistance(neighbors, neighborsList, location, n.rightchild.rightchild)
					#search if the left grandchild is closer
					if(n.leftchild.leftchild is not None):
						self.getNodeNChildNodeDistance(neighbors, neighborsList, location, n.rightchild.leftchild)
		#print neighborsList
		return neighborsList

	#fetch node and child nodes information
	def getNodeNChildNodeDistance(self, neighbors, neighborsList, location, n):
		if (n.visited):
			return neighborsList
		else:
			#print "On node : " + n.locationid
			#print "Distance between : (" + str(location[0]) + ", " + str(location[1]) + ") and (" + str(n.location[0]) + ", " + str(n.location[1]) + ")"
			distance = Distance.distance_on_unit_sphere(float(location[0]), float(location[1]), float(n.location[0]), float(n.location[1]))  * 3960
			n.visited = True
			#print distance
			if len(neighborsList) < neighbors:
				neighborsList[n.locationid] = distance
			else:
				neighborsList = self.getNearestNeighbors( neighborsList, distance, n)
			return neighborsList

	#Modifies the neighborsList to get the nearest neighbors
	def getNearestNeighbors(self, neighborsList, distance, n):
		tempdistance = sys.float_info.min
		templocationid = 0
		for nlocationid, ndistance in neighborsList.iteritems():
			if(tempdistance < ndistance):
				tempdistance = ndistance
				templocationid = nlocationid
		if(templocationid > 0):
			if(tempdistance > distance):
				del neighborsList[templocationid]
				neighborsList[n.locationid] = distance
		return neighborsList


