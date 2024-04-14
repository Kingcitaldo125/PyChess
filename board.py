import pygame
import colors

from piece import Piece, Pawn, Rook, Knight

cell_width = 75
cell_height = 75


class Cell():
	def __init__(self, color, x, y, cellx, celly):
		self.x = x
		self.y = y
		self.cellx = cellx
		self.celly = celly
		self.color = color
		self.highlight = False
		self.piece = None
		self.render_params = (self.cellx, self.celly, cell_width, cell_height)

	def __str__(self):
		str1 = str(self.x) + "," + str(self.y)
		str2 = "(" + str(self.cellx) + "," + str(self.celly) + ")"

		return str1 + " " + str2

	def get_piece(self):
		return self.piece

	def set_piece(self, piece):
		self.piece = piece

	def render(self, rendertarget):
		width = 2 if self.highlight else 0

		pygame.draw.rect(rendertarget, self.color, self.render_params, width)

		if self.piece:
			self.piece.render(rendertarget, self.cellx, self.celly)

class Board():
	def __init__(self):
		self.cells = []
		self.chosen_cell = None

		first_col = colors.cream
		second_col = colors.green

		ypos = 0
		alt = 0
		for y in range(8):
			xpos = 0
			row = []

			for x in range(8):
				ccol = first_col if alt == 0 else second_col
				row.append(Cell(ccol, x, y, xpos, ypos))

				xpos += cell_width
				alt = 1 if alt == 0 else 0

			self.cells.append(row)
			ypos += cell_height
			alt = 1 if alt == 0 else 0

	def get_cell_from_coord(self, x, y):
		if x < 0 or x > 8:
			return -1

		if y < 0 or y > 8:
			return -1

		return self.cells[y][x]

	def get_cell_from_click(self, x, y):
		cx = x//75
		cy = y//75

		if cx < 0 or cx > 8:
			return -1

		if cy < 0 or cy > 8:
			return -1

		print("cx,cy",cx,cy)

		return self.cells[cy][cx]

	def set_piece(self, piece, x, y):
		self.get_cell_from_coord(x, y).set_piece(piece)

	def setup(self):
		for i in range(8):
			self.set_piece(Pawn("white"), i, 1)

		for i in range(8):
			self.set_piece(Pawn("black"), i, 6)

	def render(self, rendertarget):
		for row in self.cells:
			for cell in row:
				cell.render(rendertarget)
