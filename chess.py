import pygame
import colors

from time import sleep

from board import Board
from piece import Piece, Pawn, Rook, Knight


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
				mx,my = e.pos
				print("mx,my",mx,my)
				xcell = board.get_cell_from_click(mx, my)
				print("Cell:", xcell)
				print("Piece:", xcell.get_piece())
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
