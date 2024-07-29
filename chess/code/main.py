import pygame
from settings import *
from support import  *
from pieces import *

class Game:
    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Chess')
        self.clock = pygame.Clock()
        self.running = True
        self.import_assets()

        # group
        self.all_sprites = pygame.sprite.Group()
        self.white_sprites = pygame.sprite.Group()
        self.black_sprites = pygame.sprite.Group()

        # board
        self.board_image = pygame.image.load(join('..', 'images', 'board.png')).convert_alpha()
        self.board_image = pygame.transform.scale_by(self.board_image, 5)
        self.board_rect = self.board_image.get_frect(topleft=(0,0))

        self.white_position = WHITE_POSITION
        self.black_position = BLACK_POSITION

        self.create_pieces()

        self.get_positions()
            ## MAKE VAR FOR WHITE PIECES MAYBE DONT USE CONSTANT
    def create_pieces(self):
        for i in range(len(WHITE_PIECES)):
            piece_image = pygame.transform.scale_by(self.white_pieces_sprites[WHITE_PIECES[i]], 5)
            pos = (self.white_position[i][0], self.white_position[i][1])
            match WHITE_PIECES[i]:
                case 'pawn':   Pawn(piece_image, pos, self.white_position, self.black_position, (self.all_sprites, self.white_sprites))
                case 'knight': Knight(piece_image, pos, self.white_position, self.black_position, (self.all_sprites, self.white_sprites))
                case 'bishop': Bishop(piece_image, pos, self.white_position, self.black_position, (self.all_sprites, self.white_sprites))
                case 'rook':   Rook(piece_image, pos, self.white_position, self.black_position, (self.all_sprites, self.white_sprites))
                case 'queen':  Queen(piece_image, pos, self.white_position, self.black_position, (self.all_sprites, self.white_sprites))
                case 'king':   King(piece_image, pos, self.white_position, self.black_position, (self.all_sprites, self.white_sprites))

        for i in range(len(BLACK_PIECES)):
            piece_image = pygame.transform.scale_by(self.black_pieces_sprites[BLACK_PIECES[i]], 5)
            pos = (self.black_position[i][0], self.black_position[i][1])
            match BLACK_PIECES[i]:
                case 'pawn':   Pawn(piece_image, pos, self.white_position, self.black_position, (self.all_sprites, self.black_sprites))
                case 'knight': Knight(piece_image, pos, self.white_position, self.black_position, (self.all_sprites, self.black_sprites))
                case 'bishop': Bishop(piece_image, pos, self.white_position, self.black_position, (self.all_sprites, self.black_sprites))
                case 'rook':   Rook(piece_image, pos, self.white_position, self.black_position, (self.all_sprites, self.black_sprites))
                case 'queen':  Queen(piece_image, pos, self.white_position, self.black_position, (self.all_sprites, self.black_sprites))
                case 'king':   King(piece_image, pos, self.white_position, self.black_position, (self.all_sprites, self.black_sprites))

    def get_positions(self):
        self.white_position = [sprite.position for sprite in self.white_sprites]
        self.black_position = [sprite.position for sprite in self.black_sprites]
        print(self.white_position)
        print(self.black_position)

    def import_assets(self):
        self.white_pieces_sprites = folder_importer('..', 'images', 'white pieces')
        self.black_pieces_sprites = folder_importer('..', 'images', 'black pieces')

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for sprite in self.all_sprites:
                        sprite.selected = False
                        if sprite.rect.collidepoint(mouse_pos):
                            sprite.selected = True

            # update
            self.all_sprites.update(dt)

            # draw
            self.display_surface.blit(self.board_image, self.board_rect)
            self.all_sprites.draw(self.display_surface)
            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()