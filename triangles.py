import random

WIDTH = 800
HEIGHT = int(float(WIDTH) / 3.5 * 2)
arr = [0.5 for i in range(8)]
tri_size = 30
tri_top = round(tri_size * sqrt(3))
xs = [11, 12, 13, 14, 15, 16, 13, 14]
ys = [3, 3, 3, 3, 3, 3, 4, 2]
COLORS = 4
seen = []


def setup():
	global WIDTH, HEIGHT, arr, tri_size, tri_top
	size(WIDTH, HEIGHT)
	background(0,0,0)
	# redraw()
	# update()
	adj = generateTriangles()
	compareTriangles(adj)

def update():
	
	for y in range(10):
		for x in range(30):
			# Coloring
			index = (x + 4*y) % 8
			fill(arr[index] * 255, arr[index] * 255, arr[index] * 255)
			for i in range(len(xs)):
				if x == xs[i] and y == ys[i]:
					fill(arr[index]*100, arr[index] * 255, arr[index]*255)

			# /\ triangle
			if (x+y) % 2 == 0:
				x1 = tri_size * (x+1)
				y1 = y * tri_top

				x2 = tri_size * x
				y2 = (y+1) * tri_top

				x3 = tri_size * (x+2)
				y3 = (y+1) * tri_top

				
				triangle(x1, y1, x2, y2, x3, y3)
			else:
				# \/ triangle
				x1 = tri_size * (x+1)
				y1 = (y+1) * tri_top

				x2 = tri_size * x
				y2 = y * tri_top

				x3 = tri_size * (x+2)
				y3 = y * tri_top

				triangle(x1, y1, x2, y2, x3, y3)

def findTriangle():
	string = ""
	for num in arr:
		string += str(floor(num))
	triangle = []
	for j in range(8):
		adj1 = int(string[j-1])
		adj2 = int(string[(j+1)%8])
		adj3 = int(string[(j+5)%8] if j % 2 == 1 else string[(j+3)%8])
		temp = sorted([adj1, adj2, adj3])
		temp.append(int(string[j]))
		triangle.append(temp)
	triangle.sort(key=triangleComp)
	print(triangle)

def debugTriangles():
	boundsX = (100, 360)
	boundsY = (50, 210)

	for i in range(3000):
		x = random.randint(boundsX[0], boundsX[1])
		y = random.randint(boundsY[0], boundsY[1])
		topX = int(float(x) / float(tri_size * 2))
		topY = int(float(y) / float(tri_top))
		dx = x - (int(topX) * tri_size * 2)
		dy = int(y - (int(topY) * tri_top))


		# print (dx, dy)
		# print (int(topX)*2, int(topY))
		# print (x, y, dx+(int(topX) * tri_size*2), dy+(int(topY) * tri_top))
		stroke(0, 0, 255)
		noFill()
		rect(topX * tri_size * 2, int(topY) * tri_top, tri_size*2, tri_top)

		# stroke(0, 255, 0)
		if (dy > 0):
			if topY % 2 == 1:
				if dx < tri_size:
					ratio = float(dx) / float(dy)
					if ratio < 1.0 / sqrt(3):
						# stroke(0, 0, 255)
						topX = float(topX) - 0.5
				else:
					# print ("test")
					ratio = float(tri_size * 2 - dx) / float(dy)
					if ratio < 1.0 / sqrt(3):
						# stroke(255, 0, 0)
						topX = float(topX) + 0.5
			else:
				if dx < tri_size:
					ratio = float(dx) / float(tri_top - dy)
					if ratio < 1.0 / sqrt(3):
						# stroke(0, 0, 255)
						topX = float(topX) - 0.5
				else:
					# print ("test")

					ratio = float(tri_size * 2 - dx) / float(tri_top - dy)
					if ratio < 1.0 / sqrt(3):
						# stroke(255, 0, 0)
						topX = float(topX) + 0.5
		index = (int(2 * topX) + 4*floor(topY)) % 8
		
		if index == 6:
			stroke(0, 255, 0)
		elif index == 5:
			stroke(0, 0, 255)
		else:
			stroke(255, 0, 0)
		rect(x, y, 1, 1)

def generateTriangles():
	adj = []
	for i in range(COLORS ** 8):
		# Generate string corresponding to octahedron
		string = ""
		for j in range(8):
			string += str((i // (COLORS ** j)) % COLORS)

		
		triangle = []
		for j in range(8):

			# We'll now compute the adjacency matrix for each side
			adj1 = int(string[j-1])
			adj2 = int(string[(j+1)%8])
			adj3 = int(string[(j+5)%8] if j % 2 == 1 else string[(j+3)%8])

			# Normalize
			temp = sorted([adj1, adj2, adj3])

			# [adj1, adj2, adj3, self] with adj1 <= adj2 <= adj3
			temp.append(int(string[j]))
			triangle.append(temp)

		# Normalize
		triangle.sort(key=triangleComp)
		adj.append(triangle)

	return adj

def compareTriangles(adj):
	for triangle in adj:
		if not checkSame(triangle):
			seen.append(triangle)
	countTriangles()


def countTriangles():
	triangles = {}
	for shape in seen:
		colors = [0 for i in range(COLORS)]
		for side in shape:
			colors[side[3]] += 1
		string = ""
		for i,color in enumerate(colors):
			string += str(color)+"s"+str(i)+":"
		if not(string in triangles.keys()):
			triangles[string] = 0
		triangles[string] += 1

	keys = sorted(triangles.keys())
	for key in keys:
		print(key+" : " + str(triangles[key]))




def triangleComp(side):
	return side[0] * 1000 + side[1] * 100 + side[2] * 10 + side[3]


def checkSame(triangle):
	for seenTriangle in seen:
		same = True
		for i, side in enumerate(seenTriangle):
			for j, adj in enumerate(side):
				adj = side[j]
				if triangle[i][j] != side[j]:
					same = False
		if same:
			return True

	return False



def mouseClicked():
	topX = int(float(mouseX) / float(tri_size * 2))
	topY = int(float(mouseY) / float(tri_top))
	dx = mouseX - (int(topX) * tri_size * 2)
	dy = int(mouseY - (int(topY) * tri_top))


	# stroke(0, 0, 255)
	# noFill()
	# rect(topX * tri_size * 2, int(topY) * tri_top, tri_size*2, tri_top)

	if (dy > 0):
		if topY % 2 == 1:
			if dx < tri_size:
				ratio = float(dx) / float(dy)
				if ratio < 1.0 / sqrt(3):
					# stroke(0, 0, 255)
					topX = float(topX) - 0.5
			else:
				# print ("test")
				ratio = float(tri_size * 2 - dx) / float(dy)
				if ratio < 1.0 / sqrt(3):
					# stroke(255, 0, 0)
					topX = float(topX) + 0.5
		else:
			if dx < tri_size:
				ratio = float(dx) / float(tri_top - dy)
				if ratio < 1.0 / sqrt(3):
					# stroke(0, 0, 255)
					topX = float(topX) - 0.5
			else:
				# print ("test")

				ratio = float(tri_size * 2 - dx) / float(tri_top - dy)
				if ratio < 1.0 / sqrt(3):
					# stroke(255, 0, 0)
					topX = float(topX) + 0.5
	index = (int(2 * topX) + 4*floor(topY)) % 8
	arr[index] = 1 if arr[index] == 0.5 else 0.5
	findTriangle()
	update()

		

def draw():
	pass