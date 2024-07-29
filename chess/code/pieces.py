from settings import *

class Piece(pygame.sprite.Sprite):
    def __init__(self, surf, pos, white_pos, black_pos, groups):
        super().__init__(groups)
        self.image = surf
        self.original_image = self.image
        self.position = pos
        self.rect = self.image.get_frect(bottomleft=(BOARD_BOTTOM_LEFT[0] + pos[0] * TILESIZE,
                                                     BOARD_BOTTOM_LEFT[1] - pos[1] * TILESIZE))
        self.selected = False
        self.possible_moves = []
        self.white_pos = white_pos
        self.black_pos = black_pos

    def piece_selected(self):
        if self.selected:
            self.image = pygame.transform.grayscale(self.image)
            self.moves()
        else:
            self.image = self.original_image

    def update(self, dt):
        self.piece_selected()

class Pawn(Piece):
    def __init__(self, surf, pos, white_pos, black_pos, groups):
        super().__init__(surf, pos, white_pos, black_pos, groups)

    def moves(self):
        pass

class Knight(Piece):
    def __init__(self, surf, pos, white_pos, black_pos, groups):
        super().__init__(surf, pos, white_pos, black_pos, groups)

    def moves(self):
        pass
class Bishop(Piece):
    def __init__(self, surf, pos, white_pos, black_pos, groups):
        super().__init__(surf, pos, white_pos, black_pos, groups)

    def moves(self):
        pass

class Rook(Piece):
    def __init__(self, surf, pos, white_pos, black_pos, groups):
        super().__init__(surf, pos, white_pos, black_pos, groups)

    def moves(self):
        pass

class Queen(Piece):
    def __init__(self, surf, pos, white_pos, black_pos, groups):
        super().__init__(surf, pos, white_pos, black_pos, groups)

    def moves(self):
        pass

class King(Piece):
    def __init__(self, surf, pos, white_pos, black_pos, groups):
        super().__init__(surf, pos, white_pos, black_pos, groups)

    def moves(self):
        pass
