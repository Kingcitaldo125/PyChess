import pygame
import colors

from time import sleep

from board import Board
from piece import Piece, Pawn, Rook, Knight


def valid_move(moves, selected_cell, selected_piece, move_cell, move_piece):
	if move_cell.x < 0 or move_cell.x > 7:
		return False

	if move_cell.y < 0 or move_cell.y > 7:
		return False

	if (move_cell.x, move_cell.y) not in moves:
		return False
	
	if move_piece is not None:
		if selected_piece.team == move_piece.team:
			return False

	return True

def get_team_from_turn(turn):
	return "white" if turn == 1 else "black"

def render(screen, board):
	screen.fill(colors.black)
	board.render(screen)
	pygame.display.flip()

def main(winx=600, winy=600):
	pygame.display.init()

	screen = pygame.display.set_mode((winx, winy))
	clock = pygame.time.Clock()

	done = False
	move = 0

	board = Board()

	board.setup()

	render(screen, board)

	turn = 0
	selected_piece = None
	selected_cell = None
	moves = []

	print("White's turn" if turn == 1 else "Black's turn")

	while not done:
		mx = 0
		my = 0

		events = pygame.event.get()

		for e in events:
			if e.type == pygame.MOUSEBUTTONDOWN:
				board.reset_cells()

				mx,my = e.pos
				xcell = board.get_cell_from_click(mx, my)
				xpiece = xcell.get_piece()

				# Set and render the potential moves for the selected cell
				if xpiece is not None and selected_piece is None:
					if xpiece.team != get_team_from_turn(turn):
						print("Not that player's turn.")
						continue

					xcell.select()
					moves = xpiece.get_moves(xcell.x, xcell.y)
					for m in moves:
						mcell = board.get_cell_from_coord(m[0], m[1])

						if mcell == -1:
							continue

						mcell.show_moves()

				if selected_piece is not None:
					if not valid_move(moves, selected_cell, selected_piece, xcell, xpiece):
						print(f"Not a valid_move: {selected_cell} -> {xcell}")
						selected_piece = None
						selected_cell = None
						moves = []
						render(screen, board)
						continue

					# Move the piece into the new cell
					selected_cell.set_piece(None)
					selected_cell.unselect()
					xcell.set_piece(selected_piece)

					# Change the player's turn
					turn = 1 if turn == 0 else 0
					print("White's turn" if turn == 1 else "Black's turn")

					selected_piece = None
					selected_cell = None
				else:
					selected_piece = xpiece
					selected_cell = xcell

				render(screen, board)
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_ESCAPE:
					done = True

		#clock.tick(60)
		sleep(0.1)

	pygame.display.quit()

if __name__ == "__main__":
	main()
