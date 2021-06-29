

from ast import Str
from math import sqrt, cos, sin
from os import times
import time
from typing import AnyStr, List
import pygame

class Vertex:

	def __init__(self, coordinate: List):
		""" point in 3-dimensional space. Also calculates its position on a 2-dimensional projection 
		- coordinate: list of coordinate of vertex (x,y,z) in float or int
		"""
		self.x = coordinate[0]
		self.y = coordinate[1]
		self.z = coordinate[2]
		
		self.pos = [0,0]
	
	def calculate(self, alpha: float, beta: float, zoom: float, off_x: int, off_y: int, offset: list[int,int,int]):
		""" calculates the position of the projection on the screen
		- alpha: rotation of x-axis
		- beta: rotation of z-axis
		- zoom: multiplier. >1: scale up, <1 scales down, =1 does nothing, =0 zeroes out
		- off_x, off_y: offset on the screen
		- offset: offset of the actual coordinates of this point (used to center the model)
		"""
		x, y, z = self.x - offset[0], self.y - offset[1], self.z - offset[2]
		self.pos[0] = (zoom * (x*cos(beta) - y*sin(beta))) + off_x
		self.pos[1] = (zoom * (z*cos(alpha) + (x*sin(beta) + y*cos(beta)) * sin(alpha))) + off_y


class Line:
	""" two vertices connected to a line """

	def __init__(self, ver1: Vertex, ver2: Vertex):
		""" creates a line from two vertices
		- ver1, ver2: Vertex-objects of the end-points of the list
		"""
		self.ver1 = ver1
		self.ver2 = ver2
		
		self.diff = []
		self.diff.append(self.ver2.x - self.ver1.x)
		self.diff.append(self.ver2.y - self.ver1.y)
		self.diff.append(self.ver2.z - self.ver1.z)
		
		self.abs_val_without_sqr = self.diff[0]**2 + self.diff[1]**2 + self.diff[2]**2
		
		self.abs_val = sqrt(self.abs_val_without_sqr)
		

	def get_difference(self):
		""" returns the difference of coordinates in list with 3 items """
		return self.diff


	def get_abs_val_without_sqr(self):
		""" returns the absolute value, but without the squareroot. usefull for fast calculations """
		return self.abs_val_without_sqr


	def get_abs_val(self):
		""" returns the absolute value """
		return self.abs_val

	
	def calculate(self, alpha: float, beta: float, zoom: float, off_x: int, off_y: int, offset: list[float, float, float]):
		""" calculates the position of the projection on the screen 
		- alpha: rotation of x-axis
		- beta: rotation of z-axis
		- zoom: multiplier. >1: scale up, <1 scales down, =1 does nothing, =0 zeroes out
		- off_x, off_y: offset on the screen
		- offset: offset of the actual coordinates
		"""

		self.ver1.calculate(alpha, beta, zoom, off_x, off_y, offset)
		self.ver2.calculate(alpha, beta, zoom, off_x, off_y, offset)
				

	def draw(self, screen):
		""" draws the line onto the the screen
		- screen: screen object from pygame
		"""
		pygame.draw.line(screen, (255,255,255), self.ver1.pos, self.ver2.pos)



class Facet:

	normal = None						# normal vertex of plane

	ver1, ver2, ver3 = None, None, None				# vertices of the three points of a triangle

	def __init__(self, normal: Vertex, ver1: Vertex, ver2: Vertex, ver3: Vertex):
		""" creates a triangular facet
		- normal:	normal vector of facet
		- ver1, ver2, and ver3:	vertices / "corner-points" of the triangle
		give all vectors as a list with three elements (x,y,z) either in float or string
		"""

		# convert to float
		for idx, val in enumerate(normal):
			normal[idx] = float(val)
		for idx, val in enumerate(ver1):
			ver1[idx] = float(val)
		for idx, val in enumerate(ver2):
			ver2[idx] = float(val)
		for idx, val in enumerate(ver3):
			ver3[idx] = float(val)

		self.normal = Vertex(normal)
		self.ver1 = Vertex(ver1)
		self.ver2 = Vertex(ver2)
		self.ver3 = Vertex(ver3)


def check_line_for_duplicate(line1: Line, line2: Line):
	""" checks if a line object is already in a list of lines
	- line: line object to test
	- lines: list of lines to compare to
	- returns True, when duplicate; False if not a duplicate
	"""

	# compare the lengths of the two lines
	if line1.get_abs_val_without_sqr() != line2.get_abs_val_without_sqr():
		return False
		
	# if we got here, the two lines in question are at the same length

	# now check every coordinate, starting with x 
	# always compare both points, in case the lines are duplicates, but facing the other way
	if (line1.ver1.x == line2.ver1.x and line1.ver2.x == line2.ver2.x) or (line1.ver1.x == line2.ver2.x and line1.ver2.x == line2.ver1.x):
		# now y
		if (line1.ver1.y == line2.ver1.y and line1.ver2.y == line2.ver2.y) or (line1.ver1.y == line2.ver2.y and line1.ver2.y == line2.ver1.y):
			# last, but not least, z
			if (line1.ver1.z == line2.ver1.z and line1.ver2.z == line2.ver2.z) or (line1.ver1.z == line2.ver2.z and line1.ver2.z == line2.ver1.z):

				# at this point the two lines are certainly duplicates, either facing the same way or not
				return True
	
	# we got to this point without any "return True", so the lines are not duplicates
	return False



class Object:

	def __init__(self, absolute_path: AnyStr):
		""" Objects class: generates all connected vertices and draws them onto a projection plane
		- absolute_path:	absolute path to stl-file
		"""
		
		# attributes
		self.facets = []				# list of all facets of the object
		self.lines = []				# list of all connected vertices (like A->B, not 0->A & no duplicates)
		self.offset = [0,0,0]

		# save params
		self.path = absolute_path

		self.load_object()
	
	
	def load_object(self):
		""" reads the file and calculates all lines for the wireframe
		"""

		st = time.time()

		# * read file
		file = open(self.path)
		lines = []

		i=0
		for line in file:
			lines.append(line.split())
			i+=1

		file.close()

		# * get facets
		i=0
		for idx, line in enumerate(lines):
			if line[0] == "facet":
				normal = line[2:5]
				ver1 = lines[idx+2][1:4]
				ver2 = lines[idx+3][1:4]
				ver3 = lines[idx+4][1:4]

				self.facets.append(Facet(normal, ver1, ver2, ver3))

			i+=1

		# * figure all lines out and append to all_lines
		all_lines = []
		i=0
		for idx, facet in enumerate(self.facets):
			# create lines
			lines = [Line(facet.ver1, facet.ver2),
						Line(facet.ver2, facet.ver3),
						Line(facet.ver3, facet.ver1)
					]

			for line in lines:
				all_lines.append(line)
			
			i+=1

		#* remove all duplicates
		i=0
		for idx1, line1 in enumerate(all_lines):
			for idx2, line2 in enumerate(all_lines):
				
				# if same index, we are comparing the line to itself
				if idx1 == idx2:
					continue
					
				# if different lengths, the two lines are not identical
				if line1.get_abs_val_without_sqr() != line2.get_abs_val_without_sqr():
					continue
					
				# if same points, the lines are identical
				# compares ver1 with ver1 and ver2 with ver2, and also compares ver1 with ver2 and ver2 with ver1
				if check_line_for_duplicate(line1, line2):

					# the two lines are identical. the first one will be saved permanently, the other one will be deleted
					self.lines.append(line1)
					all_lines.remove(line2)
				
			i+=1
			
		#* calculate the offset of the model to position it in the center
		x_cords = []
		y_cords = []
		z_cords = []
		
		# collect all coordinates of every point
		for i in self.lines:
			x, y, z = i.ver1.x, i.ver1.y, i.ver1.z
			x_cords.append(x)
			y_cords.append(y)
			z_cords.append(z)
			x, y, z = i.ver2.x, i.ver2.y, i.ver2.z
			x_cords.append(x)
			y_cords.append(y)
			z_cords.append(z)
			
		# get the smallest and biggest distance for each axis, then subtract and divide by two for the middle point
		min_x, max_x = min(x_cords), max(x_cords)
		min_y, max_y = min(y_cords), max(y_cords)
		min_z, max_z = min(z_cords), max(z_cords)
		self.offset[0] = min_x + (max_x-min_x)/2
		self.offset[1] = min_y + (max_y-min_y)/2
		self.offset[2] = min_z + (max_z-min_z)/2
		

		et = time.time()

		print("---------------------------------------")
		print("path:", self.path)
		print("offset [x,y,z]:", self.offset)
		print("number of facets:", len(self.facets))
		print("number of lines:", len(self.lines))
		print("time needed:", str(et-st))
		print("---------------------------------------")

	def calculate(self, alpha: float, beta: float, zoom: float, off_x: int, off_y: int):
		""" calculates the position of the lines on the screen 
		- alpha: rotation of x-axis
		- beta: rotation of z-axis
		- zoom: multiplier. >1: scale up, <1 scales down, =1 does nothing, =0 zeroes out
		- off_x, off_y: offset on the screen
		"""

		for i in self.lines:
			i.calculate(alpha, beta, zoom, off_x, off_y, self.offset)
	
	def draw(self, screen):
		""" draws the object onto the screen 
		- screen: screen object of pygame
		"""

		for i in self.lines:
			i.draw(screen)
