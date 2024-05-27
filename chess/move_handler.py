from piece import Bishop, Rook, Knight


class MoveHandler():
	def __init__(self, board):
		self.board = board
		self.moves = []

	def get_moves(self):
		return self.moves

	def set_moves(self, moves):
		self.moves = moves

	def reset_moves(self):
		self.moves = []

	def valid_move(self, move_cell, move_piece, selected_piece, print_why=False):
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
			if selected_piece.team == move_piece.team:
				if print_why:
					print("Trying to conquer a teammate")
				return False

		return True

	def handle_pawn_moves(self, xcell, xpiece, piece_moves):
		# Handle the special case with pawns where it can intermingle
		# attack paths with move paths

		# Attacks are only valid for cells in the forward-diagonal path
		# that contain a pawn's enemy piece
		attacks = xpiece.get_attacks(xcell.x, xcell.y)
		newmoves = []

		for m in piece_moves:
			x,y = m[0],m[1]
			cell = self.board.get_cell_from_coord(x,y)

			if cell == -1:
				continue

			if not cell.occupied():
				newmoves.append((x,y))

		for m in attacks:
			x,y = m[0],m[1]
			cell = self.board.get_cell_from_coord(x,y)

			if cell == -1:
				continue

			if cell.occupied():
				if cell.get_piece().team == xpiece.team:
					continue
				newmoves.append((x,y))

		return newmoves

	def show_moves(self):
		for m in self.moves:
			mcell = self.board.get_cell_from_coord(m[0], m[1])
			if mcell != -1:
				mcell.show_moves()

	def _get_neighbors(self, curmoves, visited, xpiece, x, y):
		# Look for the current piece's neighbors along its moves path
		# that are not being blocked by existing pieces
		neighbors = []

		for i in range(x - 1, x + 2):
			if i < 0 or i > 7:
				continue

			for j in range(y - 1, y + 2):
				if j < 0 or j > 7:
					continue

				if (i,j) not in curmoves:
					continue

				ijcell = self.board.get_cell_from_coord(i,j)

				if ijcell.occupied():
					ijpiece = ijcell.get_piece()

					if ijpiece.team != xpiece.team:
						neighbors.append((i,j))
						visited.add((i,j))
					continue

				neighbors.append((i,j))

		return neighbors

	def _los_help(self, curmoves, visited, xpiece, x, y):
		visited.add((x,y))

		neighbors = self._get_neighbors(curmoves, visited, xpiece, x, y)

		for n in neighbors:
			nx,ny = n[0],n[1]

			if (nx, ny) not in visited:
				self._los_help(curmoves, visited, xpiece, nx, ny)

	def handle_los_from_cell(self, xcell, xpiece, xmoves):
		# Walk along the path denoted by by piece's moves
		# Do a DFS to see if any other pieces are blocking the piece's path
		# If the other piece is an enemy piece, include that in the path
		# Otherwise, exclude teammate pieces from the path
		visited = set([])
		curmoves = [mv for mv in xmoves]
		newmoves = []

		self._los_help(curmoves, visited, xpiece, xcell.x, xcell.y)

		for m in xmoves:
			if m not in visited:
				continue

			newmoves.append(m)

		return newmoves

	def filter_moves(self, xcell, xpiece, xmoves):
		# Knight can jump over pieces
		if type(xpiece) == Knight:
			newmoves = []

			for m in xmoves:
				mcell = self.board.get_cell_from_coord(m[0], m[1])

				if mcell == -1:
					continue

				if mcell.occupied():
					mpiece = mcell.get_piece()

					if mpiece.team == xpiece.team:
						continue

				newmoves.append(m)

			return newmoves

		return self.handle_los_from_cell(xcell, xpiece, xmoves)

	def handle_queen_moves(self, xcell, xpiece):
		# Handle odd pathfinding bug which includes excluded tiles
		bmoves = Bishop(xpiece.team).get_moves(xcell.x, xcell.y)
		rmoves = Rook(xpiece.team).get_moves(xcell.x, xcell.y)

		xbmoves = self.filter_moves(xcell, xpiece, bmoves)
		xrmoves = self.filter_moves(xcell, xpiece, rmoves)

		return xbmoves + xrmoves
