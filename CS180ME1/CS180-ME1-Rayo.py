import sys
import math


class Node():
	"""Node ADT for storing data for current config of the problem.\
		State -> coordinates\
		Parent -> Node\
		Action-> up, down, left, right, ne, nw, se, sw\
		PathCost -> f(n) = h(n) for greedy best-first search, f(n) = g(n) + h(n) for A* search"""
	def __init__(self, state, parent, action, g, h):
		self.state = state
		self.parent = parent
		self.action = action
		self.g = g
		self.h = h
		self.f = self.g + self.h

	def __str__(self):
		return str(self.state) + ':f=' + str(self.f) + ':g=' + str(self.g) + ':h=' + str(self.h)


class Map():
	def __init__(self, dim, matrix, source, dest, upcost, downcost, leftcost, rightcost, diagonalcost):
		"""Initialize the Maze ADT"""
		self.dimensions = dim
		self.matrix = matrix
		self.source = source
		self.destination = dest
		self.up = upcost
		self.down = downcost
		self.left = leftcost
		self.right = rightcost
		self.diag = diagonalcost
		self.pathCost = 0

	def solveGreedy(self):
		#Set up the solution path of the maze
		mazepath = []

		#do graph search as stated in the book
		frontier = []
		#checks if the source is some part of a wall, then no solution will exist
		if self.matrix[self.source[0]][self.source[1]] == 0:
			frontier.append(Node(self.source, None, None, 0, 0))
			print 'push ', self.source
		explored = []
		while 1:
			if len(frontier) == 0:
				return False
			frontier = sorted(frontier, key=lambda Node:Node.g)
			print 'frontier: ',
			for i in frontier:
				print i,
			print
			currentNode = frontier.pop(0)
			print 'pop ', currentNode.state
			mazepath.append(currentNode)
			currX, currY = currentNode.state
			if currentNode.state == self.destination:
				self.pathCost = currentNode.g
				return mazepath
			explored.append(currentNode)
			print 'explored: ',
			for i in explored:
				print i,
			print
			#Then expand the parentNode, pushing every children in the stack if not in frontier or explored set
			#Branching will be clockwise: nw, n, ne, e, se, s, sw, w
			possX = [currX - 1, currX, currX + 1]
			possY = [currY - 1, currY, currY + 1]
			self.matrix[currX][currY] = -1
			for x in possX:
				for y in possY:
					if self.isLegalMove(x, y) and not self.isExplored([x, y], frontier + explored):
						overheadDet = [currX - x, currY - y]
						additional = 0
						if overheadDet == [-1, -1] or overheadDet == [1, 1] or overheadDet == [-1, 1] or overheadDet == [1, -1]:
							additional = self.diag
						elif overheadDet == [0, 1]:
							additional = self.left
						elif overheadDet == [0, -1]:
							additional = self.right
						elif overheadDet == [1, 0]:
							additional = self.up
						elif overheadDet == [-1, 0]:
							additional = self.down
						frontier.append(Node([x, y], currentNode, 'W', currentNode.g + additional, 0))
						print 'push [%d, %d], cost=%d' % (x, y, additional)
			self.matrix[currX][currY] = 0


	def isLegalMove(self, a, b):
		return a in range(0, self.dimensions[0]) and b in range(0, self.dimensions[1]) and self.matrix[a][b] == 0

	def solveA(self):
		#Set up the solution path of the maze
		mazepath = []

		#do graph search as stated in the book
		frontier = []
		#checks if the source is some part of a wall, then no solution will exist
		if self.matrix[self.source[0]][self.source[1]] == 0:
			frontier.append(Node(self.source, None, None, 0, self.distance(self.source, self.destination)))
			print 'push ', self.source
		explored = []
		while 1:
			if len(frontier) == 0:
				return False
			frontier = sorted(frontier, key=lambda Node:Node.f)
			print 'frontier: ',
			for i in frontier:
				print i,
			print
			currentNode = frontier.pop(0)
			print 'pop ', currentNode.state
			mazepath.append(currentNode)
			currX, currY = currentNode.state
			if currentNode.state == self.destination:
				self.pathCost = currentNode.g
				return mazepath
			explored.append(currentNode)
			print 'explored: ',
			for i in explored:
				print i,
			print
			#Then expand the parentNode, pushing every children in the stack if not in frontier or explored set
			#Branching will be clockwise: nw, n, ne, e, se, s, sw, w
			possX = [currX - 1, currX, currX + 1]
			possY = [currY - 1, currY, currY + 1]
			self.matrix[currX][currY] = -1
			for x in possX:
				for y in possY:
					additional = 0
					if self.isLegalMove(x, y):
						overheadDet = [currX - x, currY - y]
						additional = 0
						if overheadDet == [-1, -1] or overheadDet == [1, 1] or overheadDet == [-1, 1] or overheadDet == [1, -1]:
							additional = self.diag
						elif overheadDet == [0, 1]:
							additional = self.left
						elif overheadDet == [0, -1]:
							additional = self.right
						elif overheadDet == [1, 0]:
							additional = self.up
						elif overheadDet == [-1, 0]:
							additional = self.down
						childnode = Node([x, y], currentNode, 'some action', currentNode.g + additional, self.distance([x, y], self.destination))
						if not self.isExplored([x, y], frontier + explored):
							frontier.append(childnode)
						else:
							for i in frontier:
								if i.state == childnode.state and i.g > childnode.g:
									i.g = childnode.g
									i.parent = childnode.parent
									i.h = childnode.h
									i.f = childnode.f
						print 'push [%d, %d], cost=%d' % (x, y, additional)
			self.matrix[currX][currY] = 0

	def isExplored(self, s, list):
		for i in list:
			if i.state == s:
				return True
		return False

	def distance(self, source, dest):
		#return math.sqrt(self.up*(dest[0] - source[0])**2 + self.right*(dest[1] - source[1])**2)
		return math.sqrt((dest[0] - source[0])**2 + (dest[1] - source[1])**2)

	def str(self):
		"""Prints the string representation of the Maze ADT"""
		print 'Dimensions: %d %d' % (self.dimensions[0], self.dimensions[1])
		print 'Map:'
		for row in range(self.dimensions[0]):
			for col in range(self.dimensions[1]):
				print '%d' % (self.matrix[row][col]),
			print
		print 'Source: ', self.source
		print 'Dest: ', self.destination
		print 'Up: ', self.up
		print 'Down: ', self.down
		print 'Left: ', self.left
		print 'Right: ', self.right
		print 'Diagonal: ', self.diag

if __name__ == '__main__':
	try:
		inputFile = open('input.txt', 'r')
	except IOError, message:
		print >> sys.stderr, 'Error opening file: ', message
		sys.exit(1)

	inputLines = inputFile.readlines()
	inputMatrix = []
	try:
		for i in range(len(inputLines)):
			if i == 0:
				Dim = inputLines[i].split()
				inputDim = [int(Dim[0]), int(Dim[1])]
			elif 1 <= i <= inputDim[0]:
				temp = inputLines[i].split()
				tempLine = []
				for j in range(inputDim[1]):
					tempLine.append(int(temp[j]))
				inputMatrix.append(tempLine)
			else:
				if inputLines[i].split()[0] == 'Source:':
					inputSource = [int(inputLines[i].split()[1]), int(inputLines[i].split()[2])]
				elif inputLines[i].split()[0] == 'Destination:':
					inputDest = [int(inputLines[i].split()[1]), int(inputLines[i].split()[2])]
				elif inputLines[i].split()[0] == 'Up:':
					inputUp = int(inputLines[i].split()[1])
				elif inputLines[i].split()[0] == 'Down:':
					inputDown = int(inputLines[i].split()[1])
				elif inputLines[i].split()[0] == 'Left:':
					inputLeft = int(inputLines[i].split()[1])
				elif inputLines[i].split()[0] == 'Right:':
					inputRight = int(inputLines[i].split()[1])
				elif inputLines[i].split()[0] == 'Diagonal:':
					inputDiag = int(inputLines[i].split()[1])
	except TypeError, IndexError:
		print 'Bad input detected.'
		sys.exit(1)

	MyMap = Map(inputDim, inputMatrix, inputSource, inputDest, inputUp, inputDown, inputLeft, inputRight, inputDiag)
	MyMap.str()

	print

	print 'greedy:'
	sol = MyMap.solveGreedy()
	try:
		inputFile = open('greedy.out', 'w')
	except IOError, message:
		print >> sys.stderr, 'Error creating file: ', message
		sys.exit(1)
	if sol:
		print '\nGREEDY SOLUTION:'
		for i in sol:
			print >> inputFile, '%d %d' % (i.state[0], i.state[1])
			print i
		print >> inputFile, MyMap.pathCost
	else:
		print 'no solution'

	print
	print 'a-star:'
	sol = MyMap.solveA()
	try:
		inputFile = open('astar.out', 'w')
	except IOError, message:
		print >> sys.stderr, 'Error creating file: ', message
		sys.exit(1)
	if sol:
		print '\nA* SOLUTION:'
		last = sol[-1]
		path = []
		while last is not None:
			path.insert(0, last)
			last = last.parent
		for i in path:
			print >> inputFile, '%d %d' % (i.state[0], i.state[1])
			print i
		print >> inputFile, MyMap.pathCost
	else:
		print 'no solution'