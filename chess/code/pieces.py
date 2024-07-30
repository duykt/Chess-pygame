from settings import *

class Piece(pygame.sprite.Sprite):
    def __init__(self, surf, pos, white_pos, black_pos, side, groups):
        super().__init__(groups)
        self.image = surf
        self.original_image = self.image
        self.position = pos
        self.rect = self.image.get_frect(bottomleft=(BOARD_BOTTOM_LEFT[0] + pos[0] * TILESIZE,
                                                     BOARD_BOTTOM_LEFT[1] - pos[1] * TILESIZE))
        self.selected = False
        self.side = side

        if self.side == 'white':
            self.ally_pos = white_pos
            self.enemy_pos = black_pos
        else:
            self.ally_pos = black_pos
            self.enemy_pos = white_pos


    def piece_selected(self):
        if self.selected:
            self.image = pygame.transform.grayscale(self.image)
            self.possible_moves = self.moves()
        else:
            self.image = self.original_image

    def update(self, dt, white_pos, black_pos):
        self.piece_selected()
        if self.side == 'white':
            self.ally_pos = white_pos
            self.enemy_pos = black_pos
        else:
            self.ally_pos = black_pos
            self.enemy_pos = white_pos

class Pawn(Piece):
    def __init__(self, surf, pos, white_pos, black_pos, side, groups):
        super().__init__(surf, pos, white_pos, black_pos, side, groups)

    def moves(self):
        pass

class Knight(Piece):
    def __init__(self, surf, pos, white_pos, black_pos, side, groups):
        super().__init__(surf, pos, white_pos, black_pos, side, groups)

    def moves(self):
        pass
class Bishop(Piece):
    def __init__(self, surf, pos, white_pos, black_pos, side, groups):
        super().__init__(surf, pos, white_pos, black_pos, side, groups)

    def moves(self):
        pass

class Rook(Piece):
    def __init__(self, surf, pos, white_pos, black_pos, side, groups):
        super().__init__(surf, pos, white_pos, black_pos, side, groups)

    def moves(self):
        possible_moves = []
        # calculate movement to the left
        for row in range(-1, -8, -1):
            if (self.position[0] + row, self.position[1]) not in self.ally_pos and self.position[0] + row >= 0:
                possible_moves.append((self.position[0] + row, self.position[1]))
                if (self.position[0] + row, self.position[1]) in self.enemy_pos:
                    break
            else:
                break

        # movement to the right
        for row in range(1, 8):
            if (self.position[0] + row, self.position[1]) not in self.ally_pos and self.position[0] + row < 8:
                possible_moves.append((self.position[0] + row, self.position[1]))
                if (self.position[0] + row, self.position[1]) in self.enemy_pos:
                    break
            else:
                break

        # movement up
        for col in range(1, 8):
            if (self.position[0], self.position[1] + col) not in self.ally_pos and self.position[1] + col < 8:
                possible_moves.append((self.position[0], self.position[1] + col))
                if (self.position[0], self.position[1] + col) in self.enemy_pos:
                    break
            else:
                break

        # movement down
        for col in range(-1, -8, -1):
            if (self.position[0], self.position[1] + col) not in self.ally_pos and self.position[1] + col >= 0:
                possible_moves.append((self.position[0], self.position[1] + col))
                if (self.position[0], self.position[1] + col) in self.enemy_pos:
                    break
            else:
                break
        return possible_moves

class Queen(Piece):
    def __init__(self, surf, pos, white_pos, black_pos, side, groups):
        super().__init__(surf, pos, white_pos, black_pos, side, groups)

    def moves(self):
        pass

class King(Piece):
    def __init__(self, surf, pos, white_pos, black_pos, side, groups):
        super().__init__(surf, pos, white_pos, black_pos, side, groups)

    def moves(self):
        pass
