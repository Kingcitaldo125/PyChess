import pygame

import colors

from piece import kinds, Pawn, Queen


class Handler():
	def __init__(self, board, screen, move_handler):
		self.board = board
		self.screen = screen
		self.turn = 0
		self.selected_piece = None
		self.selected_cell = None
		self.move_handler = move_handler

		self.print_turn()

	def render(self):
		self.screen.fill(colors.black)
		self.board.render(self.screen)
		pygame.display.flip()

	def other_team(self, team):
		return "white" if team == "black" else "black"

	def get_team_from_turn(self):
		return "white" if self.turn == 1 else "black"

	def print_turn(self):
		print("White's turn" if self.turn == 1 else "Black's turn")

	def evaluate_check(self, team):
		for row in self.board.get_cells():
			for cell in row:
				if not cell.occupied():
					continue

				piece = cell.get_piece()

				if piece.team == team:
					continue

				piece_moves = piece.get_moves(cell.x, cell.y)
				moves = self.move_handler.filter_moves(cell, piece, piece_moves)

				if type(piece) == Pawn:
					moves = self.move_handler.handle_pawn_moves(cell, piece, moves)
				elif type(piece) == Queen:
					moves = self.move_handler.handle_queen_moves(cell, piece)

				for m in moves:
					mcell = self.board.get_cell_from_coord(m[0], m[1])

					if mcell == -1:
						continue

					if mcell.occupied():
						mpiece = mcell.get_piece()

						if mpiece.kind == kinds["king"] and mpiece.team == team:
							print(f"{mpiece.team} king found in cell {mcell} by {cell}")
							return True
		return False

	def handle_game_logic(self, mx, my):
		self.board.reset_cells()

		xcell = self.board.get_cell_from_click(mx, my)
		xpiece = xcell.get_piece()
		check = False

		# Evaluate a check condition before moving the piece
		if xpiece is not None:
			oteam = self.other_team(xpiece.team)
			check = self.evaluate_check(oteam)
			if check:
				print(f"{oteam} in check.")

		# Set and render the potential moves for the selected cell
		if xpiece is not None and self.selected_piece is None:
			if xpiece.team != self.get_team_from_turn():
				print("Not that player's turn.")
				return

			xcell.select()
			piece_moves = xpiece.get_moves(xcell.x, xcell.y)

			# Check for valid/invalid pawn moves/attacks
			if type(xpiece) == Pawn:
				piece_moves = self.move_handler.handle_pawn_moves(xcell, xpiece, piece_moves.copy())
			elif type(xpiece) == Queen:
				piece_moves = self.move_handler.handle_queen_moves(xcell, xpiece)
			else:
				pm = [p for p in piece_moves]
				piece_moves = self.move_handler.filter_moves(xcell, xpiece, pm)

			self.move_handler.set_moves(piece_moves)
			self.move_handler.show_moves()

		# Handle a potential piece move with a currently selected piece
		if self.selected_piece is not None:
			if not self.move_handler.valid_move(xcell, xpiece, self.selected_piece, print_why=False):
				print(f"Not a valid_move: {self.selected_cell} -> {xcell}")
				self.selected_piece = None
				self.selected_cell = None
				self.move_handler.reset_moves()
				self.render()
				return

			# Move the piece into the new cell
			self.selected_cell.set_piece(None)
			self.selected_cell.unselect()
			xcell.set_piece(self.selected_piece)
			self.selected_piece.set_moved()

			# Change the player's turn
			self.turn = 1 if self.turn == 0 else 0
			self.print_turn()

			oteam = self.other_team(self.selected_piece.team)

			# Evaluate check condition after the piece move
			check = self.evaluate_check(oteam)
			if check:
				print(f"{oteam} in check.")

			self.move_handler.reset_moves()
			self.selected_piece = None
			self.selected_cell = None
		else:
			self.selected_piece = xpiece
			self.selected_cell = xcell

		self.render()
