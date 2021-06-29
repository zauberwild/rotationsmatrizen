



import pygame
from math import cos, pi, sin



# * pygame screen init
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# * variables
a = 0.2			# angle on x axis
b = 0.4			# angle on z axis
zoom = 40.0		# zoom / multiplier

angle_increment = 0.1
zoom_increment = 0.5

values_changed = True


# * CLASSES
class Point:

	def __init__(self, x, y, z, c=(255,255,255), r = 5):
		self.x = -x					# coordinates in 3D
		self.y = -y
		self.z = z

		self.c = c 					# color
		self.r = r					# radius of drawn dot

		self.u = 0					# coordinates in 2D-projection (u = width, v = height)
		self.v = 0

	def calculate(self):
		x = self.x					# coordinates in 3D
		y = self.y
		z = self.z

		self.u = zoom * (x*cos(b) - y*sin(b))
		self.v = zoom * (z*cos(a) + (x*sin(b) + y*cos(b)) * sin(a))

		sx, sy = int(self.u), int(self.v)

		sx += SCREEN_WIDTH/2
		sy *= -1
		sy += SCREEN_HEIGHT/2

		self.pos = (sx, sy)

	def draw(self):

		pygame.draw.circle(screen, self.c, self.pos, self.r)



# * object creation
points = []

# axis points
i = 50000
points.append(Point(-i,0,0, c=(255,0,0)))
points.append(Point(i,0,0, c=(255,0,0)))
points.append(Point(0,-i,0, c=(0,255,0)))
points.append(Point(0,i,0, c=(0,255,0)))
points.append(Point(0,0,-i, c=(0,0,255)))
points.append(Point(0,0,i, c=(0,0,255)))

# cube points
i = 2
points.append(Point(i,i,-i))
points.append(Point(-i,i,-i))
points.append(Point(-i,-i,-i))
points.append(Point(i,-i,-i))

points.append(Point(i,i,i))
points.append(Point(-i,i,i))
points.append(Point(-i,-i,i))
points.append(Point(i,-i,i))

# pyramid points
i = 5
points.append(Point(i,i,0, c=(255,255,0)))
points.append(Point(-i,i,0, c=(255,255,0)))
points.append(Point(-i,-i,0, c=(255,255,0)))
points.append(Point(i,-i,0, c=(255,255,0)))
points.append(Point(0,0,i*1.5, c=(255,255,0)))

# cylinder points
i = 3
n_points_cylinder = 10
for j in range(n_points_cylinder):
	x = i * cos(j*(2*pi/n_points_cylinder))
	y = i * sin(j*(2*pi/n_points_cylinder))
	points.append(Point(x,y,i*1.5, c=(255,0,255), r=0))
	points.append(Point(x,y,i*-1.5, c=(255,0,255), r=0))


# * MAIN LOOP
active = True
while active:
	# * input
	for event in pygame.event.get():        
		if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:      # close window
			active = False

		# key pressed
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q:
				a += angle_increment
				values_changed = True
			elif event.key == pygame.K_a:
				a -= angle_increment
				values_changed = True
			elif event.key == pygame.K_w:
				b += angle_increment
				values_changed = True
			elif event.key == pygame.K_s:
				b -= angle_increment
				values_changed = True
			elif event.key == pygame.K_e:
				zoom += zoom_increment
				values_changed = True
			elif event.key == pygame.K_d:
				zoom -= zoom_increment
				values_changed = True
			
			print("a={0}; b={1}, zoom={2}".format(a,b,zoom))

	
	# * logic
	# recalculate
	if values_changed:
		values_changed = False

		for i in points:
			i.calculate()

	
	# * draw

		screen.fill((0,0,0))

		# points
		for i in points[19::]:
			i.draw()

		# axis lines
		pygame.draw.line(screen, (255,0,0), points[0].pos, points[1].pos)
		pygame.draw.line(screen, (0,255,0), points[2].pos, points[3].pos)
		pygame.draw.line(screen, (0,0,255), points[4].pos, points[5].pos)


		# cube lines
		for i in  range(6,9):
			pygame.draw.line(screen, (255,255,255), points[i].pos, points[i+1].pos)
		pygame.draw.line(screen, (255,255,255), points[i+1].pos, points[6].pos)
		for i in  range(10,13):
			pygame.draw.line(screen, (255,255,255), points[i].pos, points[i+1].pos)
		pygame.draw.line(screen, (255,255,255), points[i+1].pos, points[10].pos)
		for i in  range(6,10):
			pygame.draw.line(screen, (255,255,255), points[i].pos, points[i+4].pos)
		
		# pyramid lines
		for i in  range(14,17):
			pygame.draw.line(screen, (255,255,0), points[i].pos, points[i+1].pos)
			pygame.draw.line(screen, (255,255,0), points[i].pos, points[18].pos)
		pygame.draw.line(screen, (255,255,0), points[i+1].pos, points[14].pos)
		pygame.draw.line(screen, (255,255,0), points[i+1].pos, points[18].pos)

		# cylinder lines
		for i in range(19,19+n_points_cylinder*2-2):
			pygame.draw.line(screen, (255,0,255), points[i].pos, points[i+2].pos)
			if i % 2 == 0:
				pygame.draw.line(screen, (255,0,255), points[i].pos, points[i-1].pos)
		pygame.draw.line(screen, (255,0,255), points[i+2].pos, points[i-n_points_cylinder-6].pos)
		pygame.draw.line(screen, (255,0,255), points[i+1].pos, points[i-n_points_cylinder-7].pos)
		pygame.draw.line(screen, (255,0,255), points[i+2].pos, points[i+1].pos)


	pygame.display.flip()


	# * clock
	clock.tick(60)      # framerate
	#b += 0.005
	values_changed = True
