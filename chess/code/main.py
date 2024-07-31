import pygame
from settings import *
from support import  *

class Game:
    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Chess')
        self.clock = pygame.Clock()
        self.running = True
        self.import_assets()

        # game
        self.white_turn = True

        # board
        self.board_image = pygame.image.load(join('..', 'images', 'board.png')).convert_alpha()
        self.board_image = pygame.transform.scale_by(self.board_image, 5)
        self.board_rect = self.board_image.get_frect(topleft=(0,0))
        self.display_surface.blit(self.board_image, self.board_rect)

        # pieces
        self.white_pieces = WHITE_PIECES
        self.black_pieces = BLACK_PIECES
        self.white_position = WHITE_POSITION
        self.black_position = BLACK_POSITION

        self.update_board()

    def update_board(self):
        for i in range(len(self.white_pieces)):
            image = pygame.transform.scale_by(self.white_surfs[self.white_pieces[i]], 5)
            rect = image.get_frect(bottomleft=(self.board_rect.bottomleft[0] + self.white_position[i][0] * TILESIZE, self.board_rect.bottomleft[1] - self.white_position[i][1] * TILESIZE))
            self.display_surface.blit(image, rect)

        for i in range(len(self.black_pieces)):
            image = pygame.transform.scale_by(self.black_surfs[self.black_pieces[i]], 5)
            rect = image.get_frect(bottomleft=(self.board_rect.bottomleft[0] + self.black_position[i][0] * TILESIZE, self.board_rect.bottomleft[1] - self.black_position[i][1] * TILESIZE))
            self.display_surface.blit(image, rect)

    def import_assets(self):
        self.white_surfs = folder_importer('..', 'images', 'white pieces')
        self.black_surfs = folder_importer('..', 'images', 'black pieces')

    def draw_moves(self, moves):
        for move in moves:
            pygame.draw.circle(self.display_surface, (130, 151, 105),
                               ((move[0] * TILESIZE + TILESIZE/2), (self.board_rect.bottomleft[1] - move[1] * TILESIZE - TILESIZE/2)), 10)
    def pawn_moves(self, pos) -> list:
        possible_moves = []

        if self.white_turn:
            for i in range(1, 3 if pos[1] == 1 else 2):
                if (pos[0], pos[1] + i) not in self.white_position:
                    possible_moves.append((pos[0], pos[1] + i))
                else: break
        else:
            for i in range(-1, -3 if pos[1] == 6 else -2,  -1):
                if (pos[0], pos[1] + i) not in self.black_position:
                    possible_moves.append((pos[0], pos[1] + i))
                else: break
        return possible_moves

    def knight_moves(self, pos) -> list:
        if self.white_turn:
            ally_pos = self.white_position
        else:
            ally_pos = self.black_position
        possible_moves = []

        # vertical movement
        for vert in [x for x in range(-2, 3, 2) if x != 0]:
            for hor in range(-1, 2, 2):
                if self.white_turn:
                    if (pos[0] + hor, pos[1] + vert) not in self.white_position and 0 <= pos[0] + hor < 8 and 0 <= pos[1] + vert < 8:
                        possible_moves.append((pos[0] + hor, pos[1] + vert))
                else:
                    if (pos[0] + hor, pos[1] + vert) not in self.black_position and 0 <= pos[0] + hor < 8 and 0 <= pos[1] + vert < 8:
                        possible_moves.append((pos[0] + hor, pos[1] + vert))

        # horizontal movement
        for hor in [x for x in range(-2, 3, 2) if x != 0]:
            for vert in range(-1, 2, 2):
                if (pos[0] + hor, pos[1] + vert) not in ally_pos and 0 <= pos[0] + hor < 8 and 0 <= pos[1] + vert < 8:
                        possible_moves.append((pos[0] + hor, pos[1] + vert))

        return possible_moves

    def bishop_moves(self, pos) -> list:
        if self.white_turn:
            ally_pos = self.white_position
        else:
            ally_pos = self.black_position
        possible_moves = []

        # top left
        for target in [(-x, x) for x in range(1, 8)]:
            if (pos[0] + target[0], pos[1] + target[1]) not in ally_pos and 0 <= pos[0] + target[0] < 8 and 0 <= pos[1] + target[1] < 8:
                possible_moves.append((pos[0] + target[0], pos[1] + target[1]))
            else: break

        # bottom left
        for target in [(-x, -x) for x in range(1, 8)]:
            if (pos[0] + target[0], pos[1] + target[1]) not in ally_pos and 0 <= pos[0] + target[0] < 8 and 0 <= pos[1] + target[1] < 8:
                possible_moves.append((pos[0] + target[0], pos[1] + target[1]))
            else: break

        # top right
        for target in [(x, x) for x in range(1, 8)]:
            if (pos[0] + target[0], pos[1] + target[1]) not in ally_pos and 0 <= pos[0] + target[0] < 8 and 0 <= pos[1] + target[1] < 8:
                possible_moves.append((pos[0] + target[0], pos[1] + target[1]))
            else: break

        # bottom right
        for target in [(x, -x) for x in range(1, 8)]:
            if (pos[0] + target[0], pos[1] + target[1]) not in ally_pos and 0 <= pos[0] + target[0] < 8 and 0 <= pos[1] + target[1] < 8:
                possible_moves.append((pos[0] + target[0], pos[1] + target[1]))
            else: break

        return possible_moves

    def rook_moves(self, pos) -> list:
        if self.white_turn:
            ally_pos = self.white_position
        else:
            ally_pos = self.black_position
        possible_moves = []

        # right
        for x in [i for i in range(1, 8)]:
            if (pos[0] + x, pos[1]) not in ally_pos and 0 <= pos[0] + x < 8:
                possible_moves.append((pos[0] + x, pos[1]))
            else: break

        # left
        for x in [i for i in range(-1, -8, -1)]:
            if (pos[0] + x, pos[1]) not in ally_pos and 0 <= pos[0] + x < 8:
                possible_moves.append((pos[0] + x, pos[1]))
            else: break

        # up
        for y in [i for i in range(1, 8)]:
            if (pos[0], pos[1] + y) not in ally_pos and 0 <= pos[1] + y < 8:
                possible_moves.append((pos[0], pos[1] + y))
            else: break

        # down
        for y in [i for i in range(-1, -8, -1)]:
            if (pos[0], pos[1] + y) not in ally_pos and 0 <= pos[1] + y < 8:
                possible_moves.append((pos[0], pos[1] + y))
            else: break

        return possible_moves

    def queen_moves(self, pos) -> list:
        if self.white_turn:
            ally_pos = self.white_position
        else:
            ally_pos = self.black_position
        possible_moves = []

        # right
        for x in [i for i in range(1, 8)]:
            if (pos[0] + x, pos[1]) not in ally_pos and 0 <= pos[0] + x < 8:
                possible_moves.append((pos[0] + x, pos[1]))
            else: break

        # left
        for x in [i for i in range(-1, -8, -1)]:
            if (pos[0] + x, pos[1]) not in ally_pos and 0 <= pos[0] + x < 8:
                possible_moves.append((pos[0] + x, pos[1]))
            else: break

        # up
        for y in [i for i in range(1, 8)]:
            if (pos[0], pos[1] + y) not in ally_pos and 0 <= pos[1] + y < 8:
                possible_moves.append((pos[0], pos[1] + y))
            else: break

        # down
        for y in [i for i in range(-1, -8, -1)]:
            if (pos[0], pos[1] + y) not in ally_pos and 0 <= pos[1] + y < 8:
                possible_moves.append((pos[0], pos[1] + y))
            else: break

        # top left
        for target in [(-x, x) for x in range(1, 8)]:
            if (pos[0] + target[0], pos[1] + target[1]) not in ally_pos and 0 <= pos[0] + target[0] < 8 and 0 <= pos[1] + target[1] < 8:
                possible_moves.append((pos[0] + target[0], pos[1] + target[1]))
            else: break

        # bottom left
        for target in [(-x, -x) for x in range(1, 8)]:
            if (pos[0] + target[0], pos[1] + target[1]) not in ally_pos and 0 <= pos[0] + target[0] < 8 and 0 <= pos[1] + target[1] < 8:
                possible_moves.append((pos[0] + target[0], pos[1] + target[1]))
            else: break

        # top right
        for target in [(x, x) for x in range(1, 8)]:
            if (pos[0] + target[0], pos[1] + target[1]) not in ally_pos and 0 <= pos[0] + target[0] < 8 and 0 <= pos[1] + target[1] < 8:
                possible_moves.append((pos[0] + target[0], pos[1] + target[1]))
            else: break

        # bottom right
        for target in [(x, -x) for x in range(1, 8)]:
            if (pos[0] + target[0], pos[1] + target[1]) not in ally_pos and 0 <= pos[0] + target[0] < 8 and 0 <= pos[1] + target[1] < 8:
                possible_moves.append((pos[0] + target[0], pos[1] + target[1]))
            else: break

        return possible_moves

    def king_moves(self, pos)-> list:
        if self.white_turn:
            ally_pos = self.white_position
        else:
            ally_pos = self.black_position
        possible_moves = []

        for x in range(-1, 2):
            for y in range(-1, 2):
                if (pos[0] + x, pos[1] + y) not in ally_pos and 0 <= pos[0] + x < 8 and 0 <= pos[1] + y < 8 and (x, y) != (0,0):
                    possible_moves.append((pos[0] + x, pos[1] + y))

        return possible_moves

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(self.white_turn)
                    self.display_surface.blit(self.board_image, self.board_rect)
                    mouse_pos = (pygame.mouse.get_pos()[0] // TILESIZE, 7 - pygame.mouse.get_pos()[1] // TILESIZE)
                    selected_piece = None

                    # match location of mouse click with tile/piece
                    if self.white_turn:
                        if mouse_pos in self.white_position:
                            selected_piece = self.white_pieces[self.white_position.index(mouse_pos)]
                            piece_pos = mouse_pos
                            pygame.draw.rect(self.display_surface, (130, 151, 105),(mouse_pos[0] * TILESIZE,self.board_rect.bottomleft[1] - mouse_pos[1] * TILESIZE - TILESIZE, TILESIZE, TILESIZE))
                    else:
                        if mouse_pos in self.black_position:
                            selected_piece = self.black_pieces[self.black_position.index(mouse_pos)]
                            piece_pos = mouse_pos
                            pygame.draw.rect(self.display_surface, (130, 151, 105),(mouse_pos[0] * TILESIZE,self.board_rect.bottomleft[1] - mouse_pos[1] * TILESIZE - TILESIZE, TILESIZE, TILESIZE))

                    # if piece is selected and mouse click is in tile of a possible move, change location of piece, else pass
                    try:
                        for move in moves:
                            if mouse_pos == move:
                                if self.white_turn:
                                    self.white_position[self.white_position.index(piece_pos)] = move
                                    self.white_turn = False
                                else:
                                    self.black_position[self.black_position.index(piece_pos)] = move
                                    self.white_turn = True
                                pygame.draw.rect(self.display_surface, (130, 151, 105), (move[0] * TILESIZE, self.board_rect.bottomleft[1] - move[1] * TILESIZE - TILESIZE, TILESIZE, TILESIZE))
                    except UnboundLocalError:
                        pass

                    # determine possible moves of selected piece
                    if selected_piece:
                        match selected_piece:
                            case 'pawn': moves = self.pawn_moves(mouse_pos)
                            case 'knight': moves = self.knight_moves(mouse_pos)
                            case 'bishop': moves = self.bishop_moves(mouse_pos)
                            case 'rook': moves = self.rook_moves(mouse_pos)
                            case 'queen': moves = self.queen_moves(mouse_pos)
                            case 'king': moves = self.king_moves(mouse_pos)
                    else:
                        moves = []

                    print(moves)
                    self.update_board()
                    self.draw_moves(moves)
            # draw
            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()