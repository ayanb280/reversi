# Author: Ayan Banerjee <ayanb280@gmail.com>

import math
from copy import deepcopy


BLACK, WHITE = -1, 1


def opp(player):
    if player == BLACK:
        return WHITE
    elif player == WHITE:
        return BLACK


class Board:
    # Represents a game board

    def __init__(self):
        self.board = [[None for i in range(8)] for j in range(8)]
        self.set(BLACK, (3, 4))
        self.set(BLACK, (4, 3))
        self.set(WHITE, (3, 3))
        self.set(WHITE, (4, 4))

    def get(self, pos):
        (x, y) = pos
        return self.board[x][y]

    def set(self, player, pos):
        (x, y) = pos
        self.board[x][y] = player

    def move(self, player, pos):
        self.set(player, pos)
        for d in [(1, 0), (-1, 0), (0, 1), (0, -1),
                  (1, 1), (-1, 1), (1, -1), (-1, -1)]:
            (curx, cury) = pos
            (dx, dy) = d
            (endx, endy) = self.bracket_piece(player, pos, d)
            if endx is not None and endy is not None:
                curx += dx
                cury += dy
                while (curx, cury) != (endx, endy):
                    self.set(player, (curx, cury))
                    curx += dx
                    cury += dy

    def bracket_piece(self, player, pos, d):
        (x, y) = pos
        (dx, dy) = d
        x += dx
        y += dy
        while x in range(8) and y in range(8):
            if self.get((x, y)) is None:
                break
            elif self.get((x, y)) == player:
                return (x, y)
            else:
                x += dx
                y += dy
        return (None, None)

    def move_score(self, player, pos):
        count = 0
        for d in [(1, 0), (-1, 0), (0, 1), (0, -1),
                  (1, 1), (-1, 1), (1, -1), (-1, -1)]:
            (cur_x, cur_y) = pos
            (dx, dy) = d
            (end_x, end_y) = self.bracket_piece(player, pos, d)
            if end_x is not None and end_y is not None:
                cur_x += dx
                cur_y += dy
                while (cur_x, cur_y) != (end_x, end_y):
                    count += 1
                    cur_x += dx
                    cur_y += dy
        return count

    def is_valid(self, player, pos):
        (x, y) = pos
        if x not in range(8) or y not in range(8):
            return False
        elif self.get(pos) is not None:
            return False
        else:
            if self.move_score(player, (x, y)) == 0:
                return False
            else:
                return True

    def avl_moves(self, player):
        moves = []
        for i in range(8):
            for j in range(8):
                if self.is_valid(player, (i, j)):
                    moves.append((i, j))
        return moves

    def count(self, player):
        count = 0
        for i in range(8):
            for j in range(8):
                if self.get((i, j)) == player:
                    count += 1
        return count

    def basic_evaluate(self, player):
        return self.count(player) - self.count(opp(player))

    def evaluate(self, player):
        if not self.avl_moves(player):
            if not self.avl_moves(opp(player)):
                return (self.count(player) -
                        self.count(opp(player))) * math.inf

                # Piece difference
        x = self.count(player)
        y = self.count(opp(player))
        if x > y:
            p = 100 * x / (x + y)
        elif x < y:
            p = -100 * y / (x + y)
        else:
            p = 0

        # Corner occupancy
        x = y = 0
        for pos in [(0, 0), (7, 0), (0, 7), (7, 7)]:
            if self.get(pos) == player:
                x += 1
            elif self.get(pos) == opp(player):
                y += 1
        c = 25 * (x - y)

        # Corner closeness
        x = y = 0
        for pos in[(0, 1), (1, 0), (1, 1), (6, 0), (7, 1), (6, 1),
                   (0, 6), (1, 7), (1, 6), (6, 7), (7, 6), (6, 6)]:
            if self.get(pos) == player:
                x += 1
            elif self.get(pos) == opp(player):
                y += 1
        l = -12.5 * (x - y)

        # Mobility
        x = len(self.avl_moves(player))
        y = len(self.avl_moves(opp(player)))
        if x > y:
            m = 100 * x / (x + y)
        elif x < y:
            m = -100 * y / (x + y)
        else:
            m = 0

        return p + c + l + m

    def gen_basic_move(self, player):
        moves = self.avl_moves(player)
        if not moves:
            return None
        else:
            best_pos = moves[0]
            best_score = -math.inf
            for pos in moves:
                child = deepcopy(self)
                child.move(player, pos)
                cur_score = child.evaluate(player)
                if cur_score > best_score:
                    best_pos = pos
                    best_score = cur_score
            return best_pos

    def gen_minimax_move(self, player, depth=5):
        moves = self.avl_moves(player)
        if not moves:
            return None
        else:
            best_pos = moves[0]
            best_score = -math.inf
            for pos in moves:
                board = deepcopy(self)
                board.move(player, pos)
                cur_score = board.minimax(opp(player), player, depth - 1)
                if cur_score > best_score:
                    best_pos = pos
                    best_score = cur_score
            return best_pos

    def minimax(
            self,
            cur_player,
            maxplayer,
            depth=3,
            alpha=-
            math.inf,
            beta=math.inf):
        if depth == 0:
            return self.evaluate(maxplayer)
        else:
            moves = self.avl_moves(cur_player)
            if not moves:
                if not self.avl_moves(opp(cur_player)):
                    return self.evaluate(maxplayer)
                else:
                    child = deepcopy(self)
                    return child.minimax(
                        opp(cur_player), maxplayer, depth, alpha, beta)
            else:
                if cur_player == maxplayer:
                    v = -math.inf
                    for pos in moves:
                        child = deepcopy(self)
                        child.move(cur_player, pos)
                        v = max(
                            v,
                            child.minimax(
                                opp(cur_player),
                                maxplayer,
                                depth - 1,
                                alpha,
                                beta))
                        alpha = max(alpha, v)
                        if beta <= alpha:
                            break
                    return v
                else:
                    v = math.inf
                    for pos in moves:
                        child = deepcopy(self)
                        child.move(cur_player, pos)
                        v = min(
                            v,
                            child.minimax(
                                opp(cur_player),
                                maxplayer,
                                depth - 1,
                                alpha,
                                beta))
                        beta = min(beta, v)
                        if beta <= alpha:
                            break
                    return v


class Game():
    # Represents a human-vs-computer game of Reversi

    def __init__(self, human=None, algorithm=None):
        self.board = Board()
        self.human = human
        self.computer = opp(human)
        self.player = BLACK
        self.algorithm = algorithm

    def get_move(self):
        if self.algorithm == 'easy':
            return self.board.gen_basic_move(self.computer)
        elif self.algorithm == 'medium':
            return self.board.gen_minimax_move(self.computer, 3)
        elif self.algorithm == 'hard':
            return self.board.gen_minimax_move(self.computer, 4)

    def move(self, pos):
        self.board.move(self.player, pos)

    def switch_turn(self):
        self.player = opp(self.player)

    def is_over(self):
        if not self.board.avl_moves(BLACK) and not self.board.avl_moves(WHITE):
            return True
        else:
            return False

    def avl_moves(self):
        return self.board.avl_moves(self.player)

    def is_valid(self, pos):
        return self.board.is_valid(self.player, pos)

    def winner(self):
        if self.board.count(WHITE) > self.board.count(BLACK):
            return WHITE
        elif self.board.count(WHITE) < self.board.count(BLACK):
            return BLACK
        else:
            return None

    def score(self, player):
        return self.board.count(player)
