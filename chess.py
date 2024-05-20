import pygame

from time import sleep

from board import Board
from handler import Handler


def main(winx=600, winy=600):
	pygame.display.init()

	screen = pygame.display.set_mode((winx, winy))
	clock = pygame.time.Clock()

	done = False
	move = 0

	board = Board()

	board.setup()

	handler = Handler(board, screen)
	handler.render()

	while not done:
		events = pygame.event.get()

		for e in events:
			if e.type == pygame.MOUSEBUTTONDOWN:
				mx,my = e.pos[0],e.pos[1]
				handler.handle_game_logic(mx, my)
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_ESCAPE:
					done = True

		#clock.tick(60)
		sleep(0.1)

	pygame.display.quit()

if __name__ == "__main__":
	main()
