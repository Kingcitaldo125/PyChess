import pygame
import colors

from time import sleep

from board import Board
from piece import Piece, Pawn, Rook, Knight

def handle_moves(board, cell, piece):
	if piece is None:
		return

	cell.select()

	#print("Piece:", piece)
	moves = piece.get_moves(cell.x, cell.y)
	#print("Piece moves:", moves)

	for m in moves:
		x,y = m[0],m[1]

		if x < 0 or x > 7:
			continue

		if y < 0 or y > 7:
			continue

		mcell = board.get_cell_from_coord(m[0], m[1])
		mcell.show_moves()

def main(winx=600, winy=600):
	pygame.display.init()

	screen = pygame.display.set_mode((winx, winy))
	clock = pygame.time.Clock()

	done = False
	move = 0

	board = Board()

	board.setup()

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

				handle_moves(board, xcell, xpiece)

			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_ESCAPE:
					done = True

		screen.fill(colors.black)

		board.render(screen)

		pygame.display.flip()
		#clock.tick(60)
		sleep(0.1)

	pygame.display.quit()

if __name__ == "__main__":
	main()
