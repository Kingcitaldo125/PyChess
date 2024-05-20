from pygame import image, transform


kinds = {
	"pawn":0,
	"rook":1,
	"knight":2,
	"bishop":3,
	"queen":4,
	"king":5,
}

class Piece():
	def __init__(self, piece_name, team):
		self.width = 35
		self.height = 50
		self.xoffset = 20
		self.yoffset = 10
		self.team = team
		self.kind = None
		self.moved = False

		#print(f"Loading {team} {piece_name}")
		self.image = image.load(f'images/{team}/{piece_name}.png').convert_alpha()
		self.image = transform.scale(self.image, (self.width, self.height))

	def set_moved(self):
		self.moved = True

	def render(self, rendertarget, x, y):
		rendertarget.blit(self.image, (x + self.xoffset, y + self.yoffset))

class Pawn(Piece):
	def __init__(self, team):
		super().__init__("pawn", team)
		self.kind = kinds["pawn"]

	def get_moves(self, x, y):
		if self.moved:
			if self.team == "white":
				return [(x, y+1)]
			return [(x, y-1)]
		else:
			if self.team == "white":
				return [(x, y+1), (x, y+2)]
			return [(x, y-1), (x, y-2)]

	def get_attacks(self, x, y):
		if self.team == "white":
			return [(x-1, y+1), (x+1, y+1)]
		return [(x-1, y-1), (x+1, y-1)]

class Rook(Piece):
	def __init__(self, team):
		super().__init__("rook", team)
		self.kind = kinds["rook"]

	def get_moves(self, x, y):
		moves = []

		for i in range(y):
			moves.append((x,i))

		for i in range(y + 1, 8):
			moves.append((x,i))

		for i in range(x):
			moves.append((i,y))

		for i in range(x + 1, 8):
			moves.append((i,y))

		return moves

	def get_attacks(self, x, y):
		return self.get_moves(x,y)

class Knight(Piece):
	def __init__(self, team):
		super().__init__("knight", team)
		self.kind = kinds["knight"]

	def get_moves(self, x, y):
		moves = [(x-2,y-1), (x+2,y-1), (x-2,y+1), (x+2,y+1)]
		return moves

	def get_attacks(self, x, y):
		return self.get_moves(x,y)

class Bishop(Piece):
	def __init__(self, team):
		super().__init__("bishop", team)
		self.kind = kinds["bishop"]

	def get_moves(self, x, y):
		moves = []
		half_size = 4

		# Need a better formula for the diagonal
		for i in range(16):
			xv = i - (half_size - x) - (half_size)
			yv = i - (half_size - y) - (half_size)

			if xv < 0 or xv > 7:
				continue

			if yv < 0 or yv > 7:
				continue

			if xv == x and yv == y:
				continue

			moves.append((xv,yv))

		xx = 8
		yy = 0
		while 1:
			xv = (xx + (x - half_size))
			yv = (yy + (y - half_size))

			if xv < 0 or yv > 7:
				break

			if xv == x and yv == y:
				xx -= 1
				yy += 1
				continue

			moves.append((xv,yv))
			xx -= 1
			yy += 1

		moves.append((y,x))

		return moves

	def get_attacks(self, x, y):
		return self.get_moves(x,y)

class Queen(Piece):
	def __init__(self, team):
		super().__init__("queen", team)
		self.kind = kinds["queen"]

	def get_moves(self, x, y):
		return Bishop(self.team).get_moves(x,y) + Rook(self.team).get_moves(x,y)

	def get_attacks(self, x, y):
		return self.get_moves(x,y)

class King(Piece):
	def __init__(self, team):
		super().__init__("king", team)
		self.kind = kinds["king"]

	def get_moves(self, x, y):
		moves = []

		for i in range(x-1, x+2, 1):
			if i < 0 or i > 7:
				continue

			for j in range(y-1, y+2, 1):
				if j < 0 or j > 7:
					continue
				if x == i and j == y:
					continue

				moves.append((i, j))

		return moves

	def get_attacks(self, x, y):
		return self.get_moves(x,y)
