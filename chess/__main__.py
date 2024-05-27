import pygame

from time import sleep

from board import Board
from handler import Handler
from move_handler import MoveHandler


def main(winx=600, winy=600):
	pygame.display.init()

	screen = pygame.display.set_mode((winx, winy))
	clock = pygame.time.Clock()

	done = False
	move = 0

	board = Board()

	board.setup()

	move_handler = MoveHandler(board)
	handler = Handler(board, screen, move_handler)

	handler.render()

	while not done:
		clock.tick(10)
		events = pygame.event.get()

		for e in events:
			if e.type == pygame.MOUSEBUTTONDOWN:
				mx,my = e.pos[0],e.pos[1]
				result = handler.handle_game_logic(mx, my)
				if result:
					print("Game Over.")
					done = True
					sleep(5)
					break
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_ESCAPE:
					done = True
					break

	pygame.display.quit()

if __name__ == "__main__":
	main()
