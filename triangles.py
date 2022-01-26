
WIDTH = 800
HEIGHT = int(float(WIDTH) / 3.5 * 2)
arr = [0.5 for i in range(8)]
tri_size = 30
tri_top = round(tri_size * sqrt(3))
xs = [11, 12, 13, 14, 15, 16, 13, 14]
ys = [3, 3, 3, 3, 3, 3, 4, 2]

def setup():
	global WIDTH, HEIGHT, arr, tri_size, tri_top
	size(WIDTH, HEIGHT)
	background(0,0,0)
	redraw()

def main():
	
	for y in range(10):
		for x in range(30):
			# Coloring
			index = (x + 4*y) % 8
			fill(arr[index] * 255, arr[index] * 255, arr[index] * 255)
			for i in range(len(xs)):
				if x == xs[i] and y == ys[i]:
					fill(arr[index]*100, arr[index] * 255, arr[index]*255)

			# ∆ triangle
			if (x+y) % 2 == 0:
				x1 = tri_size * (x+1)
				y1 = y * tri_top

				x2 = tri_size * x
				y2 = (y+1) * tri_top

				x3 = tri_size * (x+2)
				y3 = (y+1) * tri_top

				
				triangle(x1, y1, x2, y2, x3, y3)
			else:
				# _
				# v triangle
				x1 = tri_size * (x+1)
				y1 = (y+1) * tri_top

				x2 = tri_size * x
				y2 = y * tri_top

				x3 = tri_size * (x+2)
				y3 = y * tri_top

				triangle(x1, y1, x2, y2, x3, y3)

def mouseClicked():
	topX = mouseX / (tri_size * 2)
	topY = mouseY / tri_top
	dy = mouseY % tri_top
	dx =  mouseX % (tri_size * 2)

	if (dy > 0):
		if dx < tri_size:
			ratio = float(dx) / float(dy)
			if ratio < 1 / sqrt(3):
				topX -= 0.5
		else:
			ratio = float(tri_size * 2 - dx) / float(dy)
			if ratio < 1 / sqrt(3):
				topX += 0.5
	index = (int(2 * topX) + 4*floor(topY)) % 8
	print (int(2 * topX), floor(topY))
	arr[index] = 1 if arr[index] == 0.5 else 0.5

def draw():
	main()