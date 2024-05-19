import pygame

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

		#print(f"Loading {team} {piece_name}")
		self.image = pygame.image.load(f'images/{team}/{piece_name}.png').convert_alpha()
		self.image = pygame.transform.scale(self.image, (self.width, self.height))

	def render(self, rendertarget, x, y):
		rendertarget.blit(self.image, (x + self.xoffset, y + self.yoffset))

class Pawn(Piece):
	def __init__(self, team):
		super().__init__("pawn", team)
		self.kind = kinds["pawn"]

	def get_moves(self):
		return []

class Rook(Piece):
	def __init__(self, team):
		super().__init__("rook", team)
		self.kind = kinds["rook"]

	def get_moves(self):
		return []

class Knight(Piece):
	def __init__(self, team):
		super().__init__("knight", team)
		self.kind = kinds["knight"]

	def get_moves(self):
		return []

class Bishop(Piece):
	def __init__(self, team):
		super().__init__("bishop", team)
		self.kind = kinds["bishop"]

	def get_moves(self):
		return []

class Queen(Piece):
	def __init__(self, team):
		super().__init__("queen", team)
		self.kind = kinds["queen"]

	def get_moves(self):
		return []

class King(Piece):
	def __init__(self, team):
		super().__init__("king", team)
		self.kind = kinds["king"]

	def get_moves(self):
		return []
