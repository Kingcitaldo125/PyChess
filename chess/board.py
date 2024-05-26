import pygame

import colors

from piece import kinds, Piece, Pawn, Rook, Knight, Bishop, Queen, King

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
		self.selected = False
		self.showingmoves = False
		self.render_params = (self.cellx, self.celly, cell_width, cell_height)

	def __str__(self):
		str1 = str(self.x) + "," + str(self.y)
		str2 = "(" + str(self.cellx) + "," + str(self.celly) + ")"

		return str1 + " " + str2

	def occupied(self):
		return self.piece is not None

	def get_piece(self):
		return self.piece

	def set_piece(self, piece):
		self.piece = piece

	def select(self):
		self.selected = True

	def unselect(self):
		self.selected = False

	def show_moves(self):
		self.showingmoves = True

	def unshow_moves(self):
		self.showingmoves = False

	def render(self, rendertarget):
		width = 2 if self.highlight else 0

		pygame.draw.rect(rendertarget, self.color, self.render_params, width)

		if self.selected:
			pygame.draw.rect(rendertarget, colors.brightgreen, self.render_params, 2)

		if self.showingmoves:
			pygame.draw.rect(rendertarget, colors.brightyellow, self.render_params, 2)

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
		if x < 0 or x > 7:
			return -1

		if y < 0 or y > 7:
			return -1

		return self.cells[y][x]

	def get_cell_from_click(self, x, y):
		cx = x//cell_width
		cy = y//cell_height

		if cx < 0 or cx > 7:
			return -1

		if cy < 0 or cy > 7:
			return -1

		return self.cells[cy][cx]

	def reset_cells(self):
		for i in range(8):
			for j in range(8):
				cell = self.get_cell_from_coord(i, j)
				cell.unselect()
				cell.unshow_moves()

	def set_piece(self, piece, x, y, setup=False):
		self.get_cell_from_coord(x, y).set_piece(piece)

	def setup(self):
		for i in range(8):
			self.set_piece(Pawn("white"), i, 1)

		for i in range(8):
			self.set_piece(Pawn("black"), i, 6)
		
		self.set_piece(Rook("black"), 0, 7)
		self.set_piece(Rook("black"), 7, 7)

		self.set_piece(Rook("white"), 0, 0)
		self.set_piece(Rook("white"), 7, 0)

		self.set_piece(Knight("black"), 1, 7)
		self.set_piece(Knight("black"), 6, 7)

		self.set_piece(Knight("white"), 1, 0)
		self.set_piece(Knight("white"), 6, 0)

		self.set_piece(Bishop("black"), 2, 7)
		self.set_piece(Bishop("black"), 5, 7)

		self.set_piece(Bishop("white"), 2, 0)
		self.set_piece(Bishop("white"), 5, 0)

		self.set_piece(Queen("white"), 3, 0)
		self.set_piece(Queen("black"), 3, 7)

		self.set_piece(King("white"), 4, 0)
		self.set_piece(King("black"), 4, 7)

	def evaluate_check_help(self, ecell, epiece, eteam):
		moves = epiece.get_moves(ecell.x, ecell.y)

		for m in moves:
			mcell = self.get_cell_from_coord(m[0], m[1])

			if mcell == -1:
				continue

			if mcell.occupied():
				mpiece = mcell.get_piece()
				if mpiece.kind == kinds["king"] and mpiece.team == eteam:
					print(f"{mpiece.team} king found in cell {mcell}")
					return True

		return False

	def evaluate_check(self, team):
		for row in self.cells:
			for cell in row:
				if not cell.occupied():
					continue

				piece = cell.get_piece()

				if piece.team == team:
					continue

				ech = self.evaluate_check_help(cell, piece, team)

				if ech == True:
					return True

		return False

	def render(self, rendertarget):
		for row in self.cells:
			for cell in row:
				cell.render(rendertarget)
