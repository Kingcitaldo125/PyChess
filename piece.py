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
		self.xoffset = 0
		self.yoffset = 0
		self.team = team
		self.kind = None

		#print(f"Loading {team} {piece_name}")
		self.image = pygame.image.load(f'images/{team}/{piece_name}.png').convert_alpha()

	def render(self, rendertarget, x, y):
		rendertarget.blit(self.image, (x + self.xoffset, y + self.yoffset))

class Pawn(Piece):
	def __init__(self, team):
		super().__init__("pawn", team)
		self.width = 35
		self.height = 50
		self.xoffset = 20
		self.yoffset = 10
		self.kind = kinds["pawn"]
		self.image = pygame.transform.scale(self.image, (self.width, self.height))

	def get_moves(self):
		return []

class Rook(Piece):
	def __init__(self, team):
		super().__init__("rook", team)
		self.width = 35
		self.height = 50
		self.xoffset = 12
		self.yoffset = 0
		self.kind = kinds["rook"]
		self.image = pygame.transform.scale(self.image, (self.width, self.height))

	def get_moves(self):
		return []

class Knight(Piece):
	def __init__(self, team):
		super().__init__("knight", team)
		self.width = 35
		self.height = 50
		self.xoffset = 12
		self.yoffset = 0
		self.kind = kinds["knight"]
		self.image = pygame.transform.scale(self.image, (self.width, self.height))

	def get_moves(self):
		return []
