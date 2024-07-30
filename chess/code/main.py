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
    def pawn_moves(self, pos):
        possible_moves = []
        for i in range(1, 3 if pos[1] == 1 else 2):
            if (pos[0], pos[1] + i) not in self.white_position:
                possible_moves.append((pos[0], pos[1] + i))
            else: break
        return possible_moves

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.display_surface.blit(self.board_image, self.board_rect)
                    mouse_pos = (pygame.mouse.get_pos()[0] // TILESIZE, 7 - pygame.mouse.get_pos()[1] // TILESIZE)
                    selected_piece = None

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

                    match selected_piece:
                        case 'pawn': moves = self.pawn_moves(mouse_pos)
                        case 'knight': pass
                        case 'bishop': pass
                        case 'rook': pass
                        case 'queen': pass
                        case 'king': pass
                    print(moves)
                    self.draw_moves(moves)

                    for move in moves:
                        if mouse_pos == move:
                            if self.white_turn:
                                self.white_position[self.white_position.index(piece_pos)] = move
                                self.white_turn = False
                            else:
                                self.black_position[self.black_position.index(piece_pos)] = move
                                self.white_turn = True
                            pygame.draw.rect(self.display_surface, (130, 151, 105), (move[0] * TILESIZE, self.board_rect.bottomleft[1] - move[1] * TILESIZE - TILESIZE, TILESIZE, TILESIZE))

            # draw
            self.update_board()
            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()