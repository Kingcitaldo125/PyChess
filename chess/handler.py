import pygame

import colors

from piece import Piece, Pawn, Rook, Knight


class Handler():
	def __init__(self, board, screen):
		self.board = board
		self.screen = screen
		self.turn = 0
		self.selected_piece = None
		self.selected_cell = None
		self.moves = []

		self.print_turn()

	def render(self):
		self.screen.fill(colors.black)
		self.board.render(self.screen)
		pygame.display.flip()

	def valid_move(self, move_cell, move_piece, print_why=False):
		if move_cell.x < 0 or move_cell.x > 7:
			if print_why:
				print("Cell x coord out of bounds")
			return False

		if move_cell.y < 0 or move_cell.y > 7:
			if print_why:
				print("Cell y coord out of bounds")
			return False

		if (move_cell.x, move_cell.y) not in self.moves:
			if print_why:
				print("Not a valid move coordinate", self.moves)
			return False
		
		if move_piece is not None:
			if self.selected_piece.team == move_piece.team:
				if print_why:
					print("Trying to conquer a teammate")
				return False

		return True

	def other_team(self, team):
		return "white" if team == "black" else "black"

	def get_team_from_turn(self):
		return "white" if self.turn == 1 else "black"

	def print_turn(self):
		print("White's turn" if self.turn == 1 else "Black's turn")

	def handle_pawn_moves(self, xcell, xpiece, piece_moves):
		attacks = xpiece.get_attacks(xcell.x, xcell.y)

		for m in piece_moves:
			x,y = m[0],m[1]
			cell = self.board.get_cell_from_coord(x,y)

			if cell == -1:
				continue

			if not cell.occupied():
				self.moves.append((x,y))

		for m in attacks:
			x,y = m[0],m[1]
			cell = self.board.get_cell_from_coord(x,y)

			if cell == -1:
				continue

			if cell.occupied():
				if cell.get_piece().team == xpiece.team:
					continue
				self.moves.append((x,y))

	def filter_moves(self, xpiece):
		newmoves = []

		for m in self.moves:
			mcell = self.board.get_cell_from_coord(m[0], m[1])

			if mcell == -1:
				continue

			if mcell.occupied():
				if mcell.get_piece().team == xpiece.team:
					continue

			newmoves.append(m)

		self.moves = newmoves.copy()

	def show_moves(self):
		for m in self.moves:
			mcell = self.board.get_cell_from_coord(m[0], m[1])
			if mcell != -1:
				mcell.show_moves()

	def handle_game_logic(self, mx, my):
		self.board.reset_cells()

		xcell = self.board.get_cell_from_click(mx, my)
		xpiece = xcell.get_piece()
		check = False

		# Evaluate a check condition before moving the piece
		if xpiece is not None:
			check = self.board.evaluate_check(xpiece.team)
			if check:
				print(f"{xpiece.team} in check.")

		# Set and render the potential moves for the selected cell
		if xpiece is not None and self.selected_piece is None:
			if xpiece.team != self.get_team_from_turn():
				print("Not that player's turn.")
				return

			xcell.select()
			piece_moves = xpiece.get_moves(xcell.x, xcell.y)

			# Check for valid/invalid pawn moves/attacks
			if type(xpiece) == Pawn:
				self.handle_pawn_moves(xcell, xpiece, piece_moves)
			else:
				self.moves = [pm for pm in piece_moves]

			self.filter_moves(xpiece)
			self.show_moves()

		if self.selected_piece is not None:
			if not self.valid_move(xcell, xpiece):
				print(f"Not a valid_move: {self.selected_cell} -> {xcell}")
				self.selected_piece = None
				self.selected_cell = None
				self.moves = []
				self.render()
				return

			# Move the piece into the new cell
			self.selected_cell.set_piece(None)
			self.selected_cell.unselect()
			xcell.set_piece(self.selected_piece)
			self.selected_piece.set_moved()

			check = self.board.evaluate_check(self.selected_piece.team)
			if check:
				print(f"{self.selected_piece.team} in check.")

				# Revert the move
				self.selected_cell.set_piece(self.selected_piece)
				self.selected_cell.select()
				xcell.set_piece(None)
				self.selected_piece.unset_moved()

				self.render()
				return

			# Change the player's turn
			self.turn = 1 if self.turn == 0 else 0
			self.print_turn()

			oteam = self.other_team(self.selected_piece.team)
			check = self.board.evaluate_check(oteam)
			if check:
				print(f"{oteam} in check.")

			self.moves = []
			self.selected_piece = None
			self.selected_cell = None
		else:
			self.selected_piece = xpiece
			self.selected_cell = xcell

		self.render()
