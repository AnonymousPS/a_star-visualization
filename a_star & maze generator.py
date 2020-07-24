import pygame
import random

pygame.init()

SIZE = 710
pygame.display.set_caption("path_finder")
WIN = pygame.display.set_mode((SIZE,SIZE))

WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (242, 255, 0)
BLACK = (0,0,0)
PURPLE = (161, 3, 252)
AQUA = (0,255,255)

class cell:
	def __init__(self,row,col,SIZE,total_rows):
		self.row = row
		self.col = col
		self.total_rows = total_rows
		self.SIZE = SIZE

		self.f_score = float("inf")
		self.g_score = float("inf")
		self.camefrom = None
		self.neighbors = []

		self.color = WHITE

		self.visited = False

	def get_pos(self):
		return (self.row,self.col)

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == YELLOW

	def is_end(self):
		return self.color == GREEN

	def is_visited(self):
		return self.visited

	def make_visited(self):
		self.visited = True
	
	def make_current(self):
		self.color = RED

	def make_path(self):
		self.color = PURPLE

	def make_barrier(self):
		self.color = BLACK

	def make_start(self):
		self.color = YELLOW
		self.f_score = 0
		self.g_score = 0

	def make_open(self):
		self.color = AQUA

	def make_closed(self):
		self.color = RED

	def make_end(self):
		self.color = GREEN

	def update_neighbors(self,grid):

		if self.row<self.total_rows-1 and not grid[self.row+1][self.col].is_barrier():
			self.neighbors.append(grid[self.row+1][self.col])

		if self.row>0 and not grid[self.row-1][self.col].is_barrier():
			self.neighbors.append(grid[self.row-1][self.col])

		if self.col<self.total_rows-1 and not grid[self.row][self.col+1].is_barrier():
			self.neighbors.append(grid[self.row][self.col+1])

		if self.col>0 and not grid[self.row][self.col-1].is_barrier():
			self.neighbors.append(grid[self.row][self.col-1])
	
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
		if self.is_start():
			self.f_score = float("inf")
			self.g_score = float("inf")
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
			choosen_one.make_visited()
			grid = remove_wall(current,choosen_one,grid)
			current.make_visited()
			current = choosen_one
			if choosen_one not in stack:
				stack.append(choosen_one)
		else:
			current.make_visited()
			current = stack[-1]
			stack.remove(stack[-1])

	return grid

def draw(WIN,WIDTH,gap,grid):
	
	for rows in grid:
		for cells in rows:
			cells.draw(WIN)

	for i in range(0,WIDTH,gap):
		pygame.draw.line(WIN,BLACK,(0,i),(WIDTH,i))
		pygame.draw.line(WIN,BLACK,(i,0),(i,WIDTH))

	pygame.display.update()


def h(p1,p2):
	x1,y1 = p1
	x2,y2 = p2
	return abs(x1-x2) + abs(y1-y2)
	
def lowest_node(open_set):
	lowest = open_set[0]
	mini = lowest.f_score

	for node in open_set:
		if node.f_score < mini:
			mini = node.f_score
			lowest = node

	return lowest

def A_star(draw,grid,start,end):
	
	open_set = [start]
	
	while open_set:
		quit()
		
		current = lowest_node(open_set)
		

		if current == end:
			node = current.camefrom
			while node!=start and node:
				quit()
				node.make_path()
				node = node.camefrom
				draw()
			return

		open_set.remove(current)
		current.make_closed()

		for neighbor in current.neighbors:
			temp_g_score = current.g_score + 1

			if temp_g_score < neighbor.g_score:
				neighbor.camefrom = current
				neighbor.g_score = temp_g_score
				neighbor.f_score = temp_g_score + h(end.get_pos(),neighbor.get_pos())
				if not neighbor in open_set:
					open_set.append(neighbor)
					neighbor.make_open()

		start.make_start()
		end.make_end()
		draw()
	
	print("no solution")
def quit():
	for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
def main(WIN,WIDTH):
	gap = 10
	grid = make_maze(WIDTH,gap,WIN)
	start = None
	end = None
	run = True
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					grid = make_maze(WIDTH,gap,WIN)
					start = None
					end = None
				if event.key == pygame.K_SPACE:
					if start and end:
						for rows in grid:
							for node in rows:
								node.update_neighbors(grid)

						A_star(lambda:draw(WIN,WIDTH,gap,grid),grid,start,end)

		if pygame.mouse.get_pressed()[0]:
			i,j = pygame.mouse.get_pos()
			i//=gap
			j//=gap
			spot = grid[i][j]
			if not start and spot != end and not spot.is_barrier():
				spot.make_start()
				start = spot
			elif not end and spot!=start and not spot.is_barrier():
				spot.make_end()
				end = spot
		if pygame.mouse.get_pressed()[2]:
			i,j = pygame.mouse.get_pos()
			i//=gap
			j//=gap
			spot = grid[i][j]
			if spot == start:
				start = None
			if spot == end:
				end = None
			if not spot.is_barrier():
				spot.reset()

		draw(WIN,WIDTH,gap,grid)

main(WIN,SIZE)