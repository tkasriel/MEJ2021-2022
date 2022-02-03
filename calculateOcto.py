import time
from tqdm import tqdm
import sys


COLORS = 3
deltaTime = 0.5
seen = set()


def main():
	global COLORS, deltaTime, seen
	adj = generateShapes()
	compareShapes(adj)
	countShapes()

def generateShapes():
	adj = []
	lastTime = 0
	for i in tqdm(range(COLORS ** 8)):
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
		triangle.sort(key=comp)
		adj.append(triangle)

	return adj

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
		try:
			inp = int(inp)
		except Exception:
			raise ValueError("Command-line argument must be a number")

		if inp <= 1:
			raise ValueError("Number of colors must be at least 2")
		COLORS = inp
	main()