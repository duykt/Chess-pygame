# implement stalemate and fix formatting

import pygame
import pygame_menu
from settings import *
from support import  *
import time

class Game:
    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Chess')
        self.clock = pygame.Clock()
        self.running = True
        self.import_assets()
        self.display_surface.fill((30, 30, 30))
        self.font = pygame.font.Font(None, 15)

        # game
        self.white_turn = True
        self.king_checked = False
        self.pawn_promotion = False
        self.last_move = str

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

        # data
        self.white_taken = []
        self.black_taken = []
        self.white_points = 0
        self.black_points = 0
        self.moves_list = {}
        self.move_count = 0
        self.promotion_options = {}

        # update
        self.update_board()
        self.update_ui()

    def update_board(self):
        # draw board notation
        for i in range(len(LETTERS)):
            if i % 2 == 0: color = (230, 234, 215)
            else: color = (69, 77, 95)

            text_surf = self.font.render(LETTERS[i], True, color)
            text_rect = text_surf.get_frect(bottomleft=(self.board_rect.bottomleft[0] + 2 + i * TILESIZE, self.board_rect.bottomleft[1]))
            self.display_surface.blit(text_surf, text_rect)

            num_surf = self.font.render(str(8-i), True, color)
            num_rect = num_surf.get_frect(bottomleft=(self.board_rect.topright[0] - 7, self.board_rect.topright[1] + 12 + i * TILESIZE))
            self.display_surface.blit(num_surf, num_rect)

        # draw white pieces
        for i in range(len(self.white_pieces)):
            image = pygame.transform.scale_by(self.white_surfs[self.white_pieces[i]], 5)
            rect = image.get_frect(bottomleft=(self.board_rect.bottomleft[0] + self.white_position[i][0] * TILESIZE, self.board_rect.bottomleft[1] - self.white_position[i][1] * TILESIZE))
            self.display_surface.blit(image, rect)

        # draw black pieces
        for i in range(len(self.black_pieces)):
            image = pygame.transform.scale_by(self.black_surfs[self.black_pieces[i]], 5)
            rect = image.get_frect(bottomleft=(self.board_rect.bottomleft[0] + self.black_position[i][0] * TILESIZE, self.board_rect.bottomleft[1] - self.black_position[i][1] * TILESIZE))
            self.display_surface.blit(image, rect)


    def import_assets(self):
        self.white_surfs = folder_importer('..', 'images', 'white pieces')
        self.black_surfs = folder_importer('..', 'images', 'black pieces')


    def draw_moves(self, moves):
        for move in moves:
            pygame.draw.circle(self.display_surface, (150, 180, 105),
                               ((move[0] * TILESIZE + TILESIZE/2), (self.board_rect.bottomleft[1] - move[1] * TILESIZE - TILESIZE/2)), 10)


    def get_moves(self, piece, pos, enemy=None, ally=None) -> list:
        if self.white_turn:
            if ally is None:
                ally_pos = self.white_position
            else:
                ally_pos = ally

            if enemy is None:
                enemy_pos = self.black_position
            else:
                enemy_pos = enemy
            ally_pieces = self.white_pieces

        else:
            if ally is None:
                ally_pos = self.black_position
            else:
                ally_pos = ally

            if enemy is None:
                enemy_pos = self.white_position
            else:
                enemy_pos = enemy
            ally_pieces = self.black_pieces

        possible_moves = []

        if piece == 'pawn':
            # check vertical moves
            if self.white_turn:
                for y in range(1, 3 if pos[1] == 1 else 2):
                    if (pos[0], pos[1] + y) in enemy_pos or pos[1] + y > 7:
                        break
                    elif (pos[0], pos[1] + y) not in ally_pos:
                        possible_moves.append((pos[0], pos[1] + y))
                    else: break
            else:
                for y in range(-1, -3 if pos[1] == 6 else -2,  -1):
                    if (pos[0], pos[1] + y) in enemy_pos or pos[1] + y < 0:
                        break
                    elif (pos[0], pos[1] + y) not in ally_pos:
                        possible_moves.append((pos[0], pos[1] + y))
                    else: break


            # check if pawn can take diagonally
            for x in [-1, 1]:
                y = 1 if self.white_turn else -1
                if (pos[0] + x, pos[1] + y) in enemy_pos:
                    possible_moves.append((pos[0] + x, pos[1] + y))

            # en passant
            # check if last moved piece was a pawn
            try:
                if self.moves_list[self.move_count][0] == 'pawn':
                    # check if pawn moved two spaces
                    if self.white_turn: squares_moved = self.moves_list[self.move_count][1][1] - self.moves_list[self.move_count][2][1]
                    else: squares_moved = self.moves_list[self.move_count][2][1] - self.moves_list[self.move_count][1][1]

                    if squares_moved == 2:
                        if self.moves_list[self.move_count][2][0] == pos[0] + 1 and self.moves_list[self.move_count][2][1] == pos[1]:
                            if self.white_turn: possible_moves.append((pos[0] + 1, pos[1] + 1))
                            else: possible_moves.append((pos[0] + 1, pos[1] - 1))

                        elif self.moves_list[self.move_count][2][0] == pos[0] - 1 and self.moves_list[self.move_count][2][1] == pos[1]:
                            if self.white_turn: possible_moves.append((pos[0] - 1, pos[1] + 1))
                            else: possible_moves.append((pos[0] - 1, pos[1] - 1))

            except KeyError: pass

        if piece == 'knight':
            # vertical movement
            for vert in [x for x in range(-2, 3, 2) if x != 0]:
                for hor in range(-1, 2, 2):
                    if self.white_turn:
                        if (pos[0] + hor, pos[1] + vert) not in ally_pos and 0 <= pos[0] + hor < 8 and 0 <= pos[1] + vert < 8:
                            possible_moves.append((pos[0] + hor, pos[1] + vert))
                    else:
                        if (pos[0] + hor, pos[1] + vert) not in ally_pos and 0 <= pos[0] + hor < 8 and 0 <= pos[1] + vert < 8:
                            possible_moves.append((pos[0] + hor, pos[1] + vert))

            # horizontal movement
            for hor in [x for x in range(-2, 3, 2) if x != 0]:
                for vert in range(-1, 2, 2):
                    if (pos[0] + hor, pos[1] + vert) not in ally_pos and 0 <= pos[0] + hor < 8 and 0 <= pos[1] + vert < 8:
                            possible_moves.append((pos[0] + hor, pos[1] + vert))

        if piece == 'bishop' or piece == 'queen':
            # top left
            for target in [(-x, x) for x in range(1, 8)]:
                if (pos[0] + target[0], pos[1] + target[1]) not in ally_pos and 0 <= pos[0] + target[0] < 8 and 0 <= pos[1] + target[1] < 8:
                    possible_moves.append((pos[0] + target[0], pos[1] + target[1]))
                    if (pos[0] + target[0], pos[1] + target[1]) in enemy_pos: break
                else: break

            # bottom left
            for target in [(-x, -x) for x in range(1, 8)]:
                if (pos[0] + target[0], pos[1] + target[1]) not in ally_pos and 0 <= pos[0] + target[0] < 8 and 0 <= pos[1] + target[1] < 8:
                    possible_moves.append((pos[0] + target[0], pos[1] + target[1]))
                    if (pos[0] + target[0], pos[1] + target[1]) in enemy_pos: break
                else: break

            # top right
            for target in [(x, x) for x in range(1, 8)]:
                if (pos[0] + target[0], pos[1] + target[1]) not in ally_pos and 0 <= pos[0] + target[0] < 8 and 0 <= pos[1] + target[1] < 8:
                    possible_moves.append((pos[0] + target[0], pos[1] + target[1]))
                    if (pos[0] + target[0], pos[1] + target[1]) in enemy_pos: break
                else: break

            # bottom right
            for target in [(x, -x) for x in range(1, 8)]:
                if (pos[0] + target[0], pos[1] + target[1]) not in ally_pos and 0 <= pos[0] + target[0] < 8 and 0 <= pos[1] + target[1] < 8:
                    possible_moves.append((pos[0] + target[0], pos[1] + target[1]))
                    if (pos[0] + target[0], pos[1] + target[1]) in enemy_pos: break
                else: break

        if piece == 'rook' or piece == 'queen':
            # right
            for x in [i for i in range(1, 8)]:
                if (pos[0] + x, pos[1]) not in ally_pos and 0 <= pos[0] + x < 8:
                    possible_moves.append((pos[0] + x, pos[1]))
                    if (pos[0] + x, pos[1]) in enemy_pos: break
                else: break

            # left
            for x in [i for i in range(-1, -8, -1)]:
                if (pos[0] + x, pos[1]) not in ally_pos and 0 <= pos[0] + x < 8:
                    possible_moves.append((pos[0] + x, pos[1]))
                    if (pos[0] + x, pos[1]) in enemy_pos: break
                else: break

            # up
            for y in [i for i in range(1, 8)]:
                if (pos[0], pos[1] + y) not in ally_pos and 0 <= pos[1] + y < 8:
                    possible_moves.append((pos[0], pos[1] + y))
                    if (pos[0], pos[1] + y) in enemy_pos: break
                else: break

            # down
            for y in [i for i in range(-1, -8, -1)]:
                if (pos[0], pos[1] + y) not in ally_pos and 0 <= pos[1] + y < 8:
                    possible_moves.append((pos[0], pos[1] + y))
                    if (pos[0], pos[1] + y) in enemy_pos: break
                else: break

        if piece == 'king':
            # king movement
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if (pos[0] + x, pos[1] + y) not in ally_pos and 0 <= pos[0] + x < 8 and 0 <= pos[1] + y < 8 and (x, y) != (0,0):
                        possible_moves.append((pos[0] + x, pos[1] + y))

            # castle
            ks_castle = True
            qs_castle = True
            if self.white_turn:
                past_moves = [self.moves_list[i] for i in self.moves_list if i % 2 == 1]
            else:
                past_moves = [self.moves_list[i] for i in self.moves_list if i % 2 == 0]

            for move in past_moves:
                if move[0] == 'king':
                    ks_castle = False; qs_castle = False
                    break
                elif move[0] == 'rook':
                    if self.white_turn:
                        if move[1] == (7, 0): ks_castle = False
                        if move[1] == (0, 0): qs_castle = False
                    else:
                        if move[1] == (7, 7): ks_castle = False
                        if move[1] == (0, 7): qs_castle = False

            castle_moves = []
            if ks_castle:
                    if any((pos[0] + x, pos[1]) in ally_pos for x in range(1, 3)):
                        castle_moves = []
                    else:
                        for x in range(1, 3):
                            castle_moves.append((pos[0] + x, pos[1]))
            for move in castle_moves:
                possible_moves.append(move)

            castle_moves = []
            if qs_castle:
                if any((pos[0] - x, pos[1]) in ally_pos for x in range(1, 4)):
                    castle_moves = []
                else:
                    for x in range(1, 3):
                        castle_moves.append((pos[0] - x, pos[1]))
            for move in castle_moves:
                possible_moves.append(move)

        return possible_moves


    def take_piece(self, pos) -> bool:
        if self.white_turn:
            ally_pieces = self.white_pieces
            ally_pos = self.white_position
            taken_pieces = self.white_taken
            enemy_pos = self.black_position
            enemy_pieces = self.black_pieces
        else:
            ally_pieces = self.black_pieces
            ally_pos = self.black_position
            taken_pieces = self.black_taken
            enemy_pos =  self.white_position
            enemy_pieces = self.white_pieces

        # general function
        if pos in enemy_pos:
            taken_piece = enemy_pieces.pop(enemy_pos.index(pos))
            taken_pieces.append(taken_piece)
            enemy_pos.remove(pos)
            if self.white_turn: self.white_points += POINTS[taken_piece]
            else: self.black_points += POINTS[taken_piece]

            return True

        # en passant
        if ally_pieces[ally_pos.index(pos)] == 'pawn':
            if self.white_turn: pos = (pos[0], pos[1] - 1)
            else: pos = (pos[0], pos[1] + 1)

            if pos in enemy_pos:
                taken_piece = enemy_pieces.pop(enemy_pos.index(pos))
                taken_pieces.append(taken_piece)
                enemy_pos.remove(pos)
                if self.white_turn: self.white_points += POINTS[taken_piece]
                else: self.black_points += POINTS[taken_piece]
                return True
        return False


    def check(self, ally_pos=None, enemy_pos=None, enemy_pieces=None):
        if self.white_turn:
            if enemy_pieces is None:
                enemy_pieces = self.black_pieces
            if enemy_pos is None:
                enemy_pos = self.black_position
            if ally_pos:
                king_pos = ally_pos[self.white_pieces.index('king')]
            else:
                king_pos = self.white_position[self.white_pieces.index('king')]
        else:
            if enemy_pieces is None:
                enemy_pieces = self.white_pieces
            if enemy_pos is None:
                enemy_pos = self.white_position
            if ally_pos:
                king_pos = ally_pos[self.black_pieces.index('king')]
            else:
                king_pos = self.black_position[self.black_pieces.index('king')]

        enemy_possible_moves = set()

        if self.white_turn: self.white_turn = False
        else: self.white_turn = True

        for i in range(len(enemy_pieces)):
            for move in self.get_moves(enemy_pieces[i], enemy_pos[i], ally_pos, enemy_pos):
                enemy_possible_moves.add(move)

        if self.white_turn: self.white_turn = False
        else: self.white_turn = True

        return king_pos in enemy_possible_moves


    def get_checked_moves(self, moves, selected_piece, piece_pos):
        valid_moves = []
        invalid_moves = []

        for move in moves:
            if self.white_turn:
                temp_pos = [pos for pos in self.white_position]
                temp_pos[temp_pos.index(piece_pos)] = move

                enemy_pos = [pos for pos in self.black_position]
                enemy_pieces = [piece for piece in self.black_pieces]

            else:
                temp_pos = [pos for pos in self.black_position]
                temp_pos[temp_pos.index(piece_pos)] = move

                enemy_pos = [pos for pos in self.white_position]
                enemy_pieces = [piece for piece in self.white_pieces]

            if not self.check(temp_pos):
                valid_moves.append(move)

            if move in enemy_pos:
                enemy_pieces.pop(enemy_pos.index(move))
                enemy_pos.remove(move)

                if not self.check(temp_pos, enemy_pos, enemy_pieces):
                    valid_moves.append(move)
                if self.check(temp_pos, enemy_pos, enemy_pieces) and move in valid_moves:
                    invalid_moves.append(move)

        return list(set(valid_moves) - set(invalid_moves))


    def add_moves_list(self, piece, pos, category):
        self.move_count += 1
        self.moves_list[self.move_count] = (piece, pos, category)


    def castle(self, piece, original_pos, move):
        if self.white_turn:
            ally_pos = self.white_position
            ally_pieces = self.white_pieces
        else:
            ally_pos = self.black_position
            ally_pieces = self.black_pieces

        if piece != 'king' or abs(original_pos[0] - move[0]) != 2:
            return
        else:
            if original_pos[0] - move[0] == -2:
                rook_pos = (original_pos[0] + 3, original_pos[1])
                ally_pos[ally_pos.index(rook_pos)] = (move[0] - 1, move[1])
                self.moves_list[self.move_count].append('ks_castle')
            else:
                rook_pos = (original_pos[0] - 4, original_pos[1])
                ally_pos[ally_pos.index(rook_pos)] = (move[0] + 1, move[1])
                self.moves_list[self.move_count].append('qs_castle')


    def update_ui(self):
        # draw rect for bg
        pygame.draw.rect(self.display_surface, (60, 60, 60),(645, 250, 310, 140))

        # text displaying 'white' and 'black'
        text_font = pygame.font.Font(None, 50)
        text_surf = text_font.render('White', True, 'white')
        text_rect = text_surf.get_frect(topleft=(655, 325))
        self.display_surface.blit(text_surf, text_rect)

        text_surf = text_font.render('Black', True, 'white')
        text_rect = text_surf.get_frect(bottomleft=(655, 320))
        self.display_surface.blit(text_surf, text_rect)

        # displaying icon of pieces taken
        for i in range(len(self.white_taken)):
            piece_surf = self.black_surfs[self.white_taken[i]]
            piece_rect = piece_surf.get_frect(bottomleft=(655 + (16 * i), 375))
            self.display_surface.blit(piece_surf, piece_rect)

        for i in range(len(self.black_taken)):
            piece_surf = self.white_surfs[self.black_taken[i]]
            piece_rect = piece_surf.get_frect(topleft=(655 + (16 * i), 260))
            self.display_surface.blit(piece_surf, piece_rect)

        # turn indicator
        if self.white_turn:
            pygame.draw.circle(self.display_surface, (80, 200, 120), (762, 345), 4)
        else:
            pygame.draw.circle(self.display_surface, (80, 200, 120), (762, 300), 4)


    def update_points(self):
        # display points
        text_font = pygame.font.Font(None, 20)

        points = abs(self.white_points - self.black_points)
        if self.white_points > self.black_points:
            text_surf = text_font.render(f'+{points}', True, 'white')
            text_rect = text_surf.get_frect(bottomleft=(655 + (16 * len(self.white_taken)), 375))
            self.display_surface.blit(text_surf, text_rect)

        elif self.black_points > self.white_points:
            text_surf = text_font.render(f'+{points}', True, 'white')
            text_rect = text_surf.get_frect(topleft=(655 + (16 * len(self.black_taken)), 260))
            self.display_surface.blit(text_surf, text_rect)


    def draw_promotion(self):
        self.promotion_options = {}
        if self.white_turn:
            for i in range(len(self.white_pieces)):
                if self.white_pieces[i] == 'pawn' and self.white_position[i][1] == 7:
                    pos = self.white_position[i]
                    self.update_board()
                    pygame.draw.rect(self.display_surface, 'black', (pos[0] * TILESIZE, 0, 80, 320))
                    pygame.draw.rect(self.display_surface, 'white', (pos[0] * TILESIZE + 3, 3, 74, 314))

                    queen_surf = pygame.transform.scale_by(self.white_surfs['queen'], 5)
                    self.display_surface.blit(queen_surf, (pos[0] * TILESIZE, 0))
                    self.promotion_options['queen'] = (pos[0], pos[1])

                    knight_surf = pygame.transform.scale_by(self.white_surfs['knight'], 5)
                    self.display_surface.blit(knight_surf, (pos[0] * TILESIZE, 80))
                    self.promotion_options['knight'] = (pos[0], pos[1] - 1)

                    rook_surf = pygame.transform.scale_by(self.white_surfs['rook'], 5)
                    self.display_surface.blit(rook_surf, (pos[0] * TILESIZE, 160))
                    self.promotion_options['rook'] = (pos[0], pos[1] - 2)

                    bishop_surf = pygame.transform.scale_by(self.white_surfs['bishop'], 5)
                    self.display_surface.blit(bishop_surf, (pos[0] * TILESIZE, 240))
                    self.promotion_options['bishop'] = (pos[0], pos[1] - 3)


        else:
            for i in range(len(self.black_pieces)):
                if self.black_pieces[i] == 'pawn' and self.black_position[i][1] == 0:
                    pos = self.black_position[i]
                    self.update_board()
                    pygame.draw.rect(self.display_surface, 'black', (pos[0] * TILESIZE, 320, 80, 320))
                    pygame.draw.rect(self.display_surface, 'white', (pos[0] * TILESIZE + 3, 323, 74, 314))

                    queen_surf = pygame.transform.scale_by(self.black_surfs['queen'], 5)
                    self.display_surface.blit(queen_surf, (pos[0] * TILESIZE, 560))
                    self.promotion_options['queen'] = (pos[0], pos[1])

                    knight_surf = pygame.transform.scale_by(self.black_surfs['knight'], 5)
                    self.display_surface.blit(knight_surf, (pos[0] * TILESIZE, 480))
                    self.promotion_options['knight'] = (pos[0], pos[1] + 1)

                    rook_surf = pygame.transform.scale_by(self.black_surfs['rook'], 5)
                    self.display_surface.blit(rook_surf, (pos[0] * TILESIZE, 400))
                    self.promotion_options['rook'] = (pos[0], pos[1] + 2)

                    bishop_surf = pygame.transform.scale_by(self.black_surfs['bishop'], 5)
                    self.display_surface.blit(bishop_surf, (pos[0] * TILESIZE, 320))
                    self.promotion_options['bishop'] = (pos[0], pos[1] + 3)


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

                    # match location of mouse click with tile/piece
                    if self.white_turn and not self.pawn_promotion:
                        if mouse_pos in self.white_position:
                            selected_piece = self.white_pieces[self.white_position.index(mouse_pos)]
                            piece_pos = mouse_pos
                            pygame.draw.rect(self.display_surface, (150, 180, 105),(mouse_pos[0] * TILESIZE,self.board_rect.bottomleft[1] - mouse_pos[1] * TILESIZE - TILESIZE, TILESIZE, TILESIZE))
                    if not self.white_turn and not self.pawn_promotion:
                        if mouse_pos in self.black_position:
                            selected_piece = self.black_pieces[self.black_position.index(mouse_pos)]
                            piece_pos = mouse_pos
                            pygame.draw.rect(self.display_surface, (150, 180, 105),(mouse_pos[0] * TILESIZE,self.board_rect.bottomleft[1] - mouse_pos[1] * TILESIZE - TILESIZE, TILESIZE, TILESIZE))

                    # if piece is selected and mouse click is in tile of a possible move, change location of piece, else pass
                    if not self.pawn_promotion:
                        try:
                            for move in moves:
                                if mouse_pos == move:
                                    original_pos = piece_pos
                                    self.last_move = move
                                    self.move_count += 1

                                    if self.white_turn:
                                        self.white_position[self.white_position.index(piece_pos)] = self.last_move
                                        self.moves_list[self.move_count] = [last_selected_piece, original_pos, self.last_move]

                                        if self.take_piece(self.last_move): self.moves_list[self.move_count].append('take')
                                        self.castle(last_selected_piece, original_pos, self.last_move)
                                        if move[1] == 7 and last_selected_piece == 'pawn':
                                            self.pawn_promotion = True
                                            break

                                        self.white_turn = False
                                        self.king_checked = self.check()
                                    else:
                                        self.black_position[self.black_position.index(piece_pos)] = self.last_move
                                        self.moves_list[self.move_count] = [last_selected_piece, original_pos, self.last_move]

                                        if self.take_piece(self.last_move): self.moves_list[self.move_count].append('take')
                                        self.castle(last_selected_piece, original_pos, self.last_move)
                                        if move[1] == 0 and last_selected_piece == 'pawn':
                                            self.pawn_promotion = True
                                            break

                                        self.white_turn = True
                                        self.king_checked = self.check()

                                    self.update_ui()
                                    self.update_points()
                                    if self.king_checked:
                                        self.moves_list[self.move_count].append('check')

                                    self.white_taken = sorted(self.white_taken, key=lambda piece: (POINTS[piece], piece))
                                    self.black_taken = sorted(self.black_taken, key=lambda piece: (POINTS[piece], piece))
                        except UnboundLocalError:
                            pass

                    if self.pawn_promotion and mouse_pos in self.promotion_options.values():
                        for piece, pos in self.promotion_options.items():
                            if pos == mouse_pos:
                                if self.white_turn:
                                    self.white_pieces[self.white_position.index(self.promotion_options['queen'])] = piece
                                    self.white_turn = False
                                    self.pawn_promotion = False
                                    self.king_checked = self.check()
                                    self.white_points += POINTS[piece] - 1
                                else:
                                    self.black_pieces[self.black_position.index(self.promotion_options['queen'])] = piece
                                    self.white_turn = True
                                    self.pawn_promotion = False
                                    self.king_checked = self.check()
                                    self.black_points += POINTS[piece] - 1
                                self.update_ui()
                                self.update_points()
                                if self.king_checked:
                                    self.moves_list[self.move_count].append('check')

                    # get desired pawn promotion
                    if self.pawn_promotion:
                        self.draw_promotion()
                        break

                    # highlight squares of moved piece
                    try:
                        pygame.draw.rect(self.display_surface, (150, 180, 105), (original_pos[0] * TILESIZE, self.board_rect.bottomleft[1] - original_pos[1] * TILESIZE - TILESIZE, TILESIZE, TILESIZE))
                        pygame.draw.rect(self.display_surface, (120, 150, 75), (self.last_move[0] * TILESIZE, self.board_rect.bottomleft[1] - self.last_move[1] * TILESIZE - TILESIZE, TILESIZE, TILESIZE))
                    except UnboundLocalError: pass

                    # draw 'checked' indicator
                    if self.king_checked:
                        king_pos = self.white_position[self.white_pieces.index('king')] if self.white_turn else self.black_position[self.black_pieces.index('king')]
                        pygame.draw.rect(self.display_surface, (233, 52, 43), (king_pos[0] * TILESIZE, self.board_rect.bottomleft[1] - king_pos[1] * TILESIZE - TILESIZE, TILESIZE, TILESIZE))

                    # determine possible moves of selected piece
                    if selected_piece:
                        last_selected_piece = selected_piece
                        moves = self.get_moves(selected_piece, piece_pos)
                        moves = self.get_checked_moves(moves, selected_piece, piece_pos)
                    else:
                        moves = []

                    # Calculate checkmate
                    if self.king_checked:
                        if self.white_turn:
                            pairs = [(self.white_pieces[i], self.white_position[i]) for i in range(len(self.white_pieces))]
                        else:
                            pairs = [(self.black_pieces[i], self.black_position[i]) for i in range(len(self.black_pieces))]
                        if any(len(self.get_checked_moves(self.get_moves(pair[0], pair[1]), pair[0], pair[1])) != 0 for pair in pairs):
                            pass
                        else:
                            self.running = False

                    self.update_board()
                    self.draw_moves(moves)


            # draw
            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()