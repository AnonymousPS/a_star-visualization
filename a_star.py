import pygame
import random

pygame.init()

SIDE = 500
pygame.display.set_caption("A* algorithm")
WIN = pygame.display.set_mode((SIDE,SIDE))

WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
PURPLE = (161, 3, 252)
PINK = (0,255,255)

class cell:
	def __init__(self,row,col,side,total_rows):
		self.row = row
		self.col = col
		self.total_rows = total_rows
		self.side = side

		self.f_score = float("inf")
		self.g_score = float("inf")
		self.camefrom = None
		self.neighbors = []
		self.color = WHITE

	def get_pos(self):
		return (self.row,self.col)

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == BLUE

	def is_end(self):
		return self.color == GREEN

	def make_path(self):
		self.color = PURPLE

	def make_barrier(self):
		self.color = BLACK

	def make_start(self):
		self.color = BLUE
		self.f_score = 0
		self.g_score = 0

	def make_open(self):
		self.color = PINK

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

		if self.row>0 and self.col>0 and not grid[self.row-1][self.col-1].is_barrier():
			self.neighbors.append(grid[self.row-1][self.col-1])

		if self.row>0 and self.col<self.total_rows-1 and not grid[self.row-1][self.col+1].is_barrier():
			self.neighbors.append(grid[self.row-1][self.col+1])

		if self.row<self.total_rows-1 and self.col<self.total_rows-1 and not grid[self.row+1][self.col+1].is_barrier():
			self.neighbors.append(grid[self.row+1][self.col+1])

		if self.row<self.total_rows-1 and self.col>0 and not grid[self.row+1][self.col-1].is_barrier():
			self.neighbors.append(grid[self.row+1][self.col-1])
	
	def draw(self,WIN):
		pygame.draw.rect(WIN,self.color,(self.row*self.side,self.col*self.side,self.side,self.side))

	def reset(self):
		if self.is_start():
			self.f_score = float("inf")
			self.g_score = float("inf")
		self.color = WHITE

def make_grid(WIDTH,gap):
	rows = WIDTH//gap
	return [[cell(i,j,gap,rows) for j in range(rows)] for i in range(rows)]


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
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		
		current = lowest_node(open_set)
		

		if current == end:
			node = current.camefrom
			while node!=start and node:
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

def random_map(grid,barriers):
	choices = [[i,j] for i in range(50) for j in range(50)]
	for i in range(barriers):
		pos = random.choice(choices)
		choices.remove(pos)
		grid[pos[0]][pos[1]].make_barrier()
	i,j = random.choice(choices)
	grid[i][j].make_start()
	start = grid[i][j]
	choices.remove([i,j])
	i,j = random.choice(choices)
	grid[i][j].make_end()
	end = grid[i][j]
	return start,end,grid

def main(WIN,WIDTH):
	gap = 10
	grid = make_grid(WIDTH,gap)
	start,end,grid = random_map(grid,0)
	run = True
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					grid = make_grid(WIDTH,gap)
					start,end,grid = random_map(grid,0)
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
			if not start and spot != end:
				spot.make_start()
				start = spot
			elif not end and spot!=start:
				spot.make_end()
				end = spot 
			elif spot != start and spot != end:
				spot.make_barrier()
		if pygame.mouse.get_pressed()[2]:
			i,j = pygame.mouse.get_pos()
			i//=gap
			j//=gap
			spot = grid[i][j]
			if spot == start:
				start = None
			if spot == end:
				end = None
			spot.reset()

		draw(WIN,WIDTH,gap,grid)

main(WIN,SIDE)