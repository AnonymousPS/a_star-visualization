import pygame
import random

pygame.init()

SIZE = 710
pygame.display.set_caption("maze generation algorithm")
WIN = pygame.display.set_mode((SIZE,SIZE))

WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
PURPLE = (161, 3, 252)
PINK = (0,255,255)

class cell:
	def __init__(self,row,col,SIZE,total_rows):
		self.row = row
		self.col = col
		self.total_rows = total_rows
		self.SIZE = SIZE

		self.neighbors = []
		self.color = PURPLE

	def get_pos(self):
		return (self.row,self.col)

	def is_barrier(self):
		return self.color == BLACK
	
	def is_visited(self):
		return self.color == WHITE

	def make_current(self):
		self.color = RED

	def make_barrier(self):
		self.color = BLACK

	def check_neighbors(self,grid):
		neighbors = []

		if self.row<self.total_rows-2 and not grid[self.row+2][self.col].is_visited():
			neighbors.append(grid[self.row+2][self.col])

		if self.row>1 and not grid[self.row-2][self.col].is_visited():
			neighbors.append(grid[self.row-2][self.col])

		if self.col<self.total_rows-2 and not grid[self.row][self.col+2].is_visited():
			neighbors.append(grid[self.row][self.col+2])

		if self.col>1 and not grid[self.row][self.col-2].is_visited():
			neighbors.append(grid[self.row][self.col-2])

		return neighbors

	def draw(self,WIN):
		pygame.draw.rect(WIN,self.color,(self.row*self.SIZE,self.col*self.SIZE,self.SIZE,self.SIZE))

	def reset(self):
		self.color = WHITE


def remove_wall(a,b,grid):
	x = (a.row + b.row)//2
	y = (a.col+b.col)//2
	grid[x][y].reset()
	return grid

def make_maze(WIDTH,gap,WIN):
	rows = WIDTH//gap

	grid =[[cell(i,j,gap,rows) for j in range(rows)] for i in range(rows)]

	stack = []

	for i in range(0,rows,2):
		for j in range(rows):
			grid[i][j].make_barrier()
			grid[j][i].make_barrier()



	current = grid[1][1]

	stack.append(current)

	while stack:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		
		neighbors = current.check_neighbors(grid)

		if neighbors:
			choosen_one = random.choice(neighbors)
			choosen_one.reset()
			grid = remove_wall(current,choosen_one,grid)
			current.reset()
			current = choosen_one
			if choosen_one not in stack:
				stack.append(choosen_one)
		else:
			current.reset()
			current = stack[-1]
			stack.remove(stack[-1])
		current.make_current()
		draw(WIN,WIDTH,gap,grid)

	current.reset()
	return grid

def draw(WIN,WIDTH,gap,grid):

	for rows in grid:
		for cells in rows:
			cells.draw(WIN)

	for i in range(0,WIDTH,gap):
		pygame.draw.line(WIN,BLACK,(0,i),(WIDTH,i))
		pygame.draw.line(WIN,BLACK,(i,0),(i,WIDTH))

	pygame.display.update()

def main(WIN,WIDTH):
	gap = 10
	grid = make_maze(WIDTH,gap,WIN)
	run = True
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		draw(WIN,WIDTH,gap,grid)

main(WIN,SIZE)
