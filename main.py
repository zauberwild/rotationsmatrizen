


from tkinter.constants import E, W
from pygame.constants import RESIZABLE
import classes
import pygame
import tkinter as tk
from math import pi


# * pygame screen init
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), RESIZABLE)
pygame.display.set_caption("3D View")
clock = pygame.time.Clock()

# * variables
a = 0.5			# angle on x axis
b = 0.4			# angle on z axis
zoom = 20.0		# zoom / multiplier

a_increment = 0.05
b_increment = 0.05
zoom_increment = 0.5


# * object creation
# ! change file-path here. (remember, the 3d-model has to be saved as an stl in ASCII-format. anything else won't work)
# Autodesk Fusion 360: when exporting a part as an STL, choose ASCII instead of binary
# info: https://en.wikipedia.org/wiki/STL_(file_format)
# also: this program isn't too efficient, so maybe choose a file with not too may vertices. The 3D-Benchy is way too much, for my pc at least
cube = classes.Object("./Test_Cube.stl")

# * functions for config view

def load_file():
	""" called by "load file"-button (c_load). re-initiates the cube object with another file"""
	print("loading new file")
	
def reset_view():
	""" called by c_reset. resets the view standard settings hardcoded in here"""
	print("resetting the view")

reset_view()	

def alpha_entry(s=0):
	""" called when entry is changed. updates alpha variable and slider"""
	global a
	a = float(a_entry.get())
	a_scale.set(a)
	
def alpha_scale(s=0):
	""" called when entry is changed. updates alpha variable and entry"""
	global a	
	a = float(a_scale.get())
	a_entry.delete(0, 'end')
	a_entry.insert(0,a)


def beta_entry(s=0):
	""" called when entry is changed. updates beta variable and slider"""
	global b	
	b = float(b_entry.get())
	b_scale.set(b)
	
def beta_scale(s=0):
	""" called when entry is changed. updates beta variable and entry"""
	global b	
	b = float(b_scale.get())
	b_entry.delete(0, 'end')
	b_entry.insert(0,b)
	
	
def zoom_entry(s=0):
	""" called when entry is changed. updates zoom variable and slider"""
	global zoom
	zoom = float(z_entry.get())
	z_scale.set(zoom)
	
def zoom_scale(s=0):
	""" called when entry is changed. updates zoom variable and entry"""
	global zoom
	zoom = float(z_scale.get())
	z_entry.delete(0, 'end')
	z_entry.insert(0,zoom)

# * build tkinter layout
root = tk.Tk()
root.title("Config")

tk.Grid.columnconfigure(root, 0, weight=1)

# control
c_frame = tk.Frame(root, background="#CCCCCC")
c_frame.grid(row=0, column=0)

c_load = tk.Button(c_frame, text="load file", command=load_file)
c_load.grid(row=0, column=0, padx=10, pady=10)

c_reset = tk.Button(c_frame, text="reset view", command=reset_view)
c_reset.grid(row=0,column=1, padx=10, pady=10)

c_beta_spin = tk.Button(c_frame, text="spin around z-axis")
c_beta_spin.grid(row=0, column=2, padx=10, pady=10)

# alpha value
a_frame = tk.Frame(root, background="#FF1010")
a_frame.grid(row=1, column=0, sticky=(W,E))

tk.Grid.columnconfigure(a_frame, 2, weight=1)
	
a_label = tk.Label(a_frame, text="Alpha (radiant):")
a_label.grid(row=0, column=0, padx=10, sticky=(W,E))

a_entry = tk.Entry(a_frame, width=10)
a_entry.bind("<Return>", alpha_entry)
a_entry.grid(row=0, column=1, padx=10, sticky=(W,E))
a_entry.insert(0,str(a))

a_scale = tk.Scale(a_frame, from_=-2*pi, to=2*pi, orient=tk.HORIZONTAL, resolution=a_increment, command=alpha_scale)
a_scale.set(a)
a_scale.grid(row=0, column=2, pady=10, padx=10, sticky=(W,E))

# beta value
b_frame = tk.Frame(root, background="#1010FF")
b_frame.grid(row=2, column=0, sticky=(W,E))

tk.Grid.columnconfigure(b_frame, 2, weight=1)

b_label = tk.Label(b_frame, text="Beta (radiant):", padx=10)
b_label.grid(row=0, column=0, padx=10, sticky=(W,E))

b_entry = tk.Entry(b_frame, width=10)
b_entry.grid(row=0, column=1, padx=10, sticky=(W,E))
a_entry.bind("<Return>", beta_entry)
b_entry.insert(0,str(b))

b_scale = tk.Scale(b_frame, from_=-pi, to=pi, orient=tk.HORIZONTAL, length=500, resolution=b_increment, command=beta_scale)
b_scale.set(b)
b_scale.grid(row=0, column=2, pady=10, padx=10, sticky=(W,E))

# zoom_factor
z_frame = tk.Frame(root, background="#10FF10")
z_frame.grid(row=3, column=0)
z_label = tk.Label(z_frame, text="Zoom factor:", padx=10)
z_label.grid(row=0, column=0)
z_entry = tk.Entry(z_frame)
z_entry.grid(row=0, column=1, padx=10)
z_entry.bind("<Return>", zoom_entry)
z_entry.insert(0,str(zoom))
z_scale = tk.Scale(z_frame, from_= 0, to=100, orient=tk.HORIZONTAL, length=500, resolution=zoom_increment, command=zoom_scale)
z_scale.set(zoom)
z_scale.grid(row=0, column=2, pady=5)

d = 0
c = 0

origin = classes.Vertex((0,0,0))

def update(period = int(1/FPS*1000)):
	global b,cube,a,zoom
	
	SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()
	
	#* input
	for event in pygame.event.get():
		if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:			# close window
			game_active = False

		# key pressed
		if event.type == pygame.KEYDOWN:
			pass


	origin.calculate(a,b,zoom,SCREEN_WIDTH/2, SCREEN_HEIGHT/2, (0,0,0))
	cube.calculate(a,b,zoom,SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

	screen.fill((0,0,0))

	pygame.draw.circle(screen, (255,255,0), origin.pos, 2)
	cube.draw(screen)
	
	pygame.display.flip()

	# b += b_increment
	# if b >= 200*pi:
	# 	b = 0
	


	a_label.after(period, update)


update(500)
root.mainloop()

exit()
# * main loop
active = True
while active:
	#* input
	for event in pygame.event.get():
		if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:			# close window
			game_active = False

		# key pressed
		if event.type == pygame.KEYDOWN:
			pass

	#*logic
	b += b_increment
	if b >= 2000*pi or b <= -2000*pi:
		b = 0

	cube.calculate(a, b, zoom)


	#* draw

	cube.draw()


	#* clock
	clock.tick(FPS)