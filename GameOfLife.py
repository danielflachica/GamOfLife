# Conway's Game of Life | CSC615M
# Guide: https://robertheaton.com/2018/07/20/project-2-game-of-life/
# Submitted by: Daniel Lachica (12/14/19)

import random
import time
from colorama import init, Fore, Back, Style
''' NOTE: you may need to run "pip install colorama" first to see the colored grid in motion '''
''' NOTE: If you're on windows OS, uncomment line #39 '''

class Game:
	def __init__(self, width, height):
		self.width = width
		self.height = height

	def init_grid_state(self, threshold):
		grid = []
		for h in range(0, self.height):
			row = []
			for w in range(0, self.width):
				random_num = random.random()
				if random_num >= threshold:
					row.append(0)
				else:
					row.append(1)
			grid.append(row)
		return grid

	def init_dead_state(self):
		grid = []
		for h in range(0, self.height):
			row = []
			for w in range(0, self.width):
				row.append(0)
			grid.append(row)
		return grid

	def render(self, grid_state):
		# init(convert=True)	# Uncomment if on Windows
		for h in range(0, self.height):
			for w in range(0, self.width):
				if grid_state[h][w] == 1:
					print(Fore.WHITE + Style.BRIGHT + '* ' + Style.RESET_ALL, end='')
				else:
					print(Style.DIM + '* ' + Style.RESET_ALL, end='')
			print()

	def get_neighbors(self, grid_state, x, y):
		neighbors = []
		# initialize all neighbors to 0/dead
		b, t, r, l, br, tr, bl, tl = 0, 0, 0, 0, 0, 0, 0, 0

		# perform grid edge and corner checks before updating neighbors list
		if y < self.height-1:	
			b = grid_state[y+1][x]
		if y > 0:
			t = grid_state[y-1][x]
		if x < self.width-1:
			r = grid_state[y][x+1]
		if x > 0:
			l = grid_state[y][x-1]
		if y < self.height-1 and x < self.width-1:
			br = grid_state[y+1][x+1]
		if y > 0 and x < self.width-1:
			tr = grid_state[y-1][x+1]
		if y < self.height-1 and x > 0:
			bl = grid_state[y+1][x-1]
		if y > 0 and x > 0:
			tl = grid_state[y-1][x-1]

		neighbors.extend((t, b, l, r, tl, tr, bl, br))
		return neighbors

	def get_next_state(self, prev_state):
		next_state = self.init_dead_state()			# Initialize grid to all 'dead' cells

		for h in range(0, self.height):				# Update 'alive' cells based on rules as applied to prev_state
			for w in range(0, self.width):
				live_neighbor_cnt = self.get_neighbors(prev_state, w, h).count(1)

				# if current cell is alive
				if prev_state[h][w] == 1:		
					if live_neighbor_cnt <= 1: 		# Any live cell with 0 or 1 live neighbors becomes dead, because of underpopulation
						next_state[h][w] = 0
					elif live_neighbor_cnt <= 3:	# Any live cell with 2 or 3 live neighbors stays alive, because its neighborhood is just right
						next_state[h][w] = 1
					elif live_neighbor_cnt > 3:		# Any live cell with more than 3 live neighbors becomes dead, because of overpopulation
						next_state[h][w] = 0
				# if current cell is dead
				else:
					if live_neighbor_cnt == 3:		# Any dead cell with exactly 3 live neighbors becomes alive, by reproduction
						next_state[h][w] = 1
		return next_state


if __name__ == "__main__":
	GRID_WIDTH, GRID_HEIGHT = 60, 60
	THRESHOLD = 0.25

	game = Game(GRID_WIDTH, GRID_HEIGHT)
	init_state = game.init_grid_state(THRESHOLD)

	curr_state = init_state
	game.render(curr_state)
	while 1:
		next_state = game.get_next_state(curr_state)
		curr_state = next_state
		game.render(curr_state)
		time.sleep(.250)
