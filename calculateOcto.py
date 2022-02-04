import time
from tqdm import tqdm
import sys, os


COLORS = 3
deltaTime = 0.5
seen = set()
bufferFile = "buffer.csv"

def main():
	global COLORS, deltaTime, seen
	init()
	generateShapes()
	compareShapes()
	countShapes()
	cleanup()

def init():
	try:
		file = open(bufferFile, "x")
		file.close()
	except FileExistsError:
		# file was already created
		# so, we erase everything in the file
		print ("Found existing buffer file, clearing contents...")
		file = open(bufferFile, "w")
		file.close()

def cleanup():
	try:
		os.remove(bufferFile)
	except FileNotFoundError:
		print ("buffer file not found")




def generateShapes():
	adj = []
	lastTime = 0
	string = ["" for _ in range(8)]
	print ("Creating shapes...")
	for i in tqdm(range(COLORS ** 8)):

		# If size is too large, we print to a buffer file
		if len(adj) > 1E6:
			print ("\n### Adjacency list is too large, dumping to buffer ###")
			file = open(bufferFile, "a")
			for i in tqdm(range(len(adj))):
				shape = adj[i]
				for side in shape:
					file.write(",".join(map(lambda x: str(x), side)) + "\n")
				file.write("\n")
			file.close()
			adj = []
			print ("\nBack to creating shapes...")

		# Generate string corresponding to octahedron
		for j in range(8):
			string[j] = str((i // (COLORS ** j)) % COLORS)
		
		shape = []
		for j in range(8):

			# We'll now compute the adjacency matrix for each side
			adj1 = int(string[j-1])
			adj2 = int(string[(j+1)%8])
			adj3 = int(string[(j+5)%8] if j % 2 == 1 else string[(j+3)%8])

			# Normalize
			temp = sorted([adj1, adj2, adj3])

			# [adj1, adj2, adj3, self] with adj1 <= adj2 <= adj3
			temp.append(int(string[j]))
			shape.append(temp)

		# Normalize
		shape.sort(key=comp)
		adj.append(shape)

	print ("\nOne last dump to buffer")
	file = open(bufferFile, "a")
	for i in tqdm(range(len(adj))):
		shape = adj[i]
		for side in shape:
			file.write(",".join(map(lambda x: str(x), side)) + "\n")
		file.write("\n")
	file.close()

def comp(a):
	return a[0] * (COLORS+1) ** 3 + a[1] * (COLORS+1) ** 2 + a[2] * (COLORS+1) + a[3]


def compareShapes(adj):
	lastTime = 0
	for i, triangle in tqdm(enumerate(adj)):
		# Add hash to set
		hsh = hashOcto(triangle)
		seen.add(hsh)

def hashOcto(shape):
	temp = []

	# Convert to string
	for side in shape:
		temp.append("".join(map(lambda x: str(x), side)))

	# Count colors
	colors = [0 for i in range(COLORS)]
	for side in shape:
		colors[side[3]] += 1
	colors = list(map(lambda x: str(x), colors))
	
	# HASH + colors
	return int(str(hash("".join(temp))) + "".join(colors))

def countShapes():
	shapes = {}
	lastTime = 0
	for o, shape in tqdm(enumerate(seen)):
		string = str(shape)[-COLORS:]

		# Count shapes
		if not(string in shapes.keys()):
			shapes[string] = 0
		shapes[string] += 1

	keys = sorted(shapes.keys())
	for key in keys:
		print(key+" : " + str(shapes[key]))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		inp = sys.argv[1]
		if inp == "--help":
			print ("######### Brute Force Implementation to solve our problem in MeJ 2021-22 #########")
			print ("This script can be run with python3.")
			print ("It takes one optional command-line argument, number of colors")
			sys.exit(0)
		try:
			inp = int(inp)
		except Exception:
			raise ValueError("Number of colors must be a number")

		if inp <= 1:
			raise ValueError("Number of colors must be at least 2")
		COLORS = inp
	main()