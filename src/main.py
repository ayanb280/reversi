# Author: Ayan Banerjee <ayanb280@gmail.com>

from copy import deepcopy
import sys
import threading
import pygame
import reversi


TO_WORDS = {
    reversi.BLACK: 'Black',
    reversi.WHITE: 'White'
}


class App:
    def __init__(self):
        # Initialize variables, load images, sounds, fonts.
        pygame.init()
        pygame.font.init()

        self.BGCOLOR = (11, 118, 48)
        self.FGCOLOR = (55, 200, 100)
        self.WINDOWCOLOR = (180, 200, 220)

        self.ONE_IMG = pygame.image.load('res/img/one.png')
        self.TWO_IMG = pygame.image.load('res/img/two.png')

        self.EASY_IMG = pygame.image.load('res/img/1-star.png')
        self.MEDIUM_IMG = pygame.image.load('res/img/2-star.png')
        self.HARD_IMG = pygame.image.load('res/img/3-star.png')

        self.BLACK_IMG = pygame.image.load('res/img/black.png')
        self.WHITE_IMG = pygame.image.load('res/img/white.png')
        self.BLACK_IMG_SMALL = pygame.image.load('res/img/black-small.png')
        self.WHITE_IMG_SMALL = pygame.image.load('res/img/white-small.png')

        self.MOVE_SOUND = pygame.mixer.Sound('res/sound/move.wav')

        self.BLACK_COL = (0, 0, 0)
        self.WHITE_COL = (255, 255, 255)

        self.FONT_NORMAL = pygame.font.Font('res/font/Nunito-Regular.ttf', 22)
        self.FONT_BIG = pygame.font.Font('res/font/Nunito-ExtraBold.ttf', 35)
        self.FONT_HUGE = pygame.font.Font('res/font/Nunito-Black.ttf', 70)

        self.SCREENWIDTH = 640
        self.SCREENHEIGHT = 480

        self.MOUSEX = 0
        self.MOUSEY = 0

        self.FPS = 50
        self.ABORTED = False
        self.UNDO_STACK = []

        self.WINDOW = pygame.display.set_mode(
            (self.SCREENWIDTH, self.SCREENHEIGHT))
        self.CLOCK = pygame.time.Clock()
        pygame.display.set_caption('Reversi')
        self.human = self.computer = None

    def run(self):
        # Run the program
        while True:
            self.select_mode()
            if self.gamemode == 'singleplayer':
                self.select_player()
                self.select_algorithm()
                self.game = reversi.Game(
                    human=self.human, algorithm=self.algorithm)
                self.play_single()
            else:
                self.game = reversi.Game()
                self.play_multi()
            if not self.ABORTED:
                self.display_winner()
            else:
                self.ABORTED = False

    def quit(self):
        # Exit
        pygame.quit()
        sys.exit()

    def select_mode(self):
        # Display screen to select singleplayer/multiplayer game
        msg = self.FONT_BIG.render('Select Game Mode', True, self.BLACK_COL)
        choice1 = self.FONT_NORMAL.render('One Player', True, self.BLACK_COL)
        choice2 = self.FONT_NORMAL.render('Two Player', True, self.BLACK_COL)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.MOUSEMOTION:
                    self.MOUSEX, self.MOUSEY = event.pos
                elif event.type == pygame.MOUSEBUTTONUP:
                    if 170 < self.MOUSEX < 290 and 220 < self.MOUSEY < 360:
                        self.gamemode = 'singleplayer'
                        return
                    if 350 < self.MOUSEX < 470 and 220 < self.MOUSEY < 360:
                        self.gamemode = 'multiplayer'
                        return
            self.WINDOW.fill(self.BGCOLOR)
            if 170 < self.MOUSEX < 290 and 220 < self.MOUSEY < 360:
                pygame.draw.rect(self.WINDOW, self.FGCOLOR,
                                 (170, 220, 120, 140))
            if 350 < self.MOUSEX < 470 and 220 < self.MOUSEY < 360:
                pygame.draw.rect(self.WINDOW, self.FGCOLOR,
                                 (350, 220, 120, 140))

            self.WINDOW.blit(msg, (320 - msg.get_rect().width /
                                   2, 150 - msg.get_rect().height / 2))
            self.WINDOW.blit(self.ONE_IMG, (200, 240))
            self.WINDOW.blit(self.TWO_IMG, (380, 240))
            self.WINDOW.blit(
                choice1, (230 - choice1.get_rect().width / 2, 310))
            self.WINDOW.blit(
                choice2, (410 - choice2.get_rect().width / 2, 310))

            pygame.display.update()
            self.CLOCK.tick(self.FPS)

    def select_player(self):
        # Display screen to select player color
        msg = self.FONT_BIG.render('Select Color', True, self.BLACK_COL)
        choice1 = self.FONT_NORMAL.render('Black', True, self.BLACK_COL)
        choice2 = self.FONT_NORMAL.render('White', True, self.BLACK_COL)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.MOUSEMOTION:
                    self.MOUSEX, self.MOUSEY = event.pos
                elif event.type == pygame.MOUSEBUTTONUP:
                    if 170 < self.MOUSEX < 290 and 220 < self.MOUSEY < 360:
                        self.human = reversi.BLACK
                        self.computer = reversi.WHITE
                        return
                    if 350 < self.MOUSEX < 470 and 220 < self.MOUSEY < 360:
                        self.human = reversi.WHITE
                        self.computer = reversi.BLACK
                        return
            self.WINDOW.fill(self.BGCOLOR)
            if 170 < self.MOUSEX < 290 and 220 < self.MOUSEY < 360:
                pygame.draw.rect(self.WINDOW, self.FGCOLOR,
                                 (170, 220, 120, 140))
            if 350 < self.MOUSEX < 470 and 220 < self.MOUSEY < 360:
                pygame.draw.rect(self.WINDOW, self.FGCOLOR,
                                 (350, 220, 120, 140))

            self.WINDOW.blit(msg, (320 - msg.get_rect().width /
                                   2, 150 - msg.get_rect().height / 2))
            self.WINDOW.blit(self.BLACK_IMG, (210, 250))
            self.WINDOW.blit(self.WHITE_IMG, (390, 250))
            self.WINDOW.blit(
                choice1, (230 - choice1.get_rect().width / 2, 310))
            self.WINDOW.blit(
                choice2, (410 - choice2.get_rect().width / 2, 310))

            pygame.display.update()
            self.CLOCK.tick(self.FPS)

    def select_algorithm(self):
        # Display screen to select difficulty level: Easy, Medium or Hard
        msg = self.FONT_BIG.render(
            'Select Difficulty Level', True, self.BLACK_COL)
        choice1 = self.FONT_NORMAL.render('Easy', True, self.BLACK_COL)
        choice2 = self.FONT_NORMAL.render('Medium', True, self.BLACK_COL)
        choice3 = self.FONT_NORMAL.render('Hard', True, self.BLACK_COL)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.MOUSEMOTION:
                    self.MOUSEX, self.MOUSEY = event.pos
                elif event.type == pygame.MOUSEBUTTONUP:
                    if 100 < self.MOUSEX < 220 and 220 < self.MOUSEY < 360:
                        self.algorithm = 'easy'
                        return
                    if 260 < self.MOUSEX < 380 and 220 < self.MOUSEY < 360:
                        self.algorithm = 'medium'
                        return
                    if 420 < self.MOUSEX < 540 and 220 < self.MOUSEY < 360:
                        self.algorithm = 'hard'
                        return
            self.WINDOW.fill(self.BGCOLOR)
            if 100 < self.MOUSEX < 220 and 220 < self.MOUSEY < 360:
                pygame.draw.rect(self.WINDOW, self.FGCOLOR,
                                 (100, 220, 120, 140))
            if 260 < self.MOUSEX < 380 and 220 < self.MOUSEY < 360:
                pygame.draw.rect(self.WINDOW, self.FGCOLOR,
                                 (260, 220, 120, 140))
            if 420 < self.MOUSEX < 540 and 220 < self.MOUSEY < 360:
                pygame.draw.rect(self.WINDOW, self.FGCOLOR,
                                 (420, 220, 120, 140))

            self.WINDOW.blit(msg, (320 - msg.get_rect().width /
                                   2, 150 - msg.get_rect().height / 2))
            self.WINDOW.blit(self.EASY_IMG, (130, 240))
            self.WINDOW.blit(self.MEDIUM_IMG, (290, 240))
            self.WINDOW.blit(self.HARD_IMG, (450, 240))
            self.WINDOW.blit(
                choice1, (160 - choice1.get_rect().width / 2, 310))
            self.WINDOW.blit(
                choice2, (320 - choice2.get_rect().width / 2, 310))
            self.WINDOW.blit(
                choice3, (480 - choice3.get_rect().width / 2, 310))

            pygame.display.update()
            self.CLOCK.tick(self.FPS)

    def play_single(self):
        # Play a singleplayer (human-computer) game
        self.UNDO_STACK = []
        self.computer_thinking = False
        self.moves = self.game.avl_moves()
        self.draw()
        pygame.time.wait(500)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.MOUSEMOTION:
                    self.MOUSEX, self.MOUSEY = event.pos
                elif not self.computer_thinking and event.type == pygame.MOUSEBUTTONUP:
                    if 432 < self.MOUSEX < 630 and 382 < self.MOUSEY < 420:
                        self.ABORTED = True
                        return
                    elif 432 < self.MOUSEX < 630 and 332 < self.MOUSEY < 370:
                        if self.UNDO_STACK:
                            self.MOVE_SOUND.play()
                            self.game = self.UNDO_STACK.pop()
                            self.moves = self.game.avl_moves()
                            self.draw()
                            break
                    elif self.game.player == self.human:
                        self.MOUSEX, self.MOUSEY = event.pos
                        pos = ((self.MOUSEY - 20) // 50,
                               (self.MOUSEX - 20) // 50)
                        if pos in self.moves:
                            self.UNDO_STACK.append(deepcopy(self.game))
                            self.MOVE_SOUND.play()
                            self.game.move(pos)
                            self.game.switch_turn()
                            self.moves = self.game.avl_moves()
                            self.draw()
                            break
            if self.moves == []:
                self.draw()
                if self.game.is_over():
                    break
                else:
                    pygame.time.wait(1500)
                    self.game.switch_turn()
                    self.moves = self.game.avl_moves()
            elif self.game.player == self.computer:
                # Generate computer move on a different thread so as not to
                # block the GUI
                if not self.computer_thinking:
                    self.computer_thinking = True
                    comp_thread = threading.Thread(
                        target=self.play_computer_move)
                    comp_thread.start()
            self.draw()
            self.CLOCK.tick(self.FPS)
        self.winner = self.game.winner()

    def play_computer_move(self):
        # Generate and play a computer move
        pygame.time.wait(500)
        pos = self.game.get_move()
        self.MOVE_SOUND.play()
        self.game.board.set(self.computer, pos)
        self.draw()
        pygame.time.wait(500)
        self.game.move(pos)
        self.game.switch_turn()
        self.moves = self.game.avl_moves()
        self.draw()
        self.computer_thinking = False

    def play_multi(self):
        # Play a multiplayer (human-human) game
        self.UNDO_STACK = []
        self.moves = self.game.avl_moves()
        while not self.game.is_over():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.MOUSEMOTION:
                    self.MOUSEX, self.MOUSEY = event.pos
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.MOUSEX, self.MOUSEY = event.pos
                    if 432 < self.MOUSEX < 630 and 382 < self.MOUSEY < 420:
                        self.ABORTED = True
                        return
                    elif 432 < self.MOUSEX < 630 and 332 < self.MOUSEY < 370:
                        if self.UNDO_STACK != []:
                            self.MOVE_SOUND.play()
                            self.game = self.UNDO_STACK.pop()
                            self.moves = self.game.avl_moves()
                            self.draw()
                            break
                    else:
                        pos = ((self.MOUSEY - 20) // 50,
                               (self.MOUSEX - 20) // 50)
                        if pos in self.moves:
                            self.UNDO_STACK.append(deepcopy(self.game))
                            self.MOVE_SOUND.play()
                            self.game.move(pos)
                            self.game.switch_turn()
                            self.moves = self.game.avl_moves()
                            break
            if self.moves == []:
                self.draw()
                pygame.time.wait(500)
                self.game.switch_turn()
                self.moves = self.game.avl_moves()
            self.draw()
            self.CLOCK.tick(self.FPS)
        self.winner = self.game.winner()

    def draw(self):
        # Draw the game GUI
        self.WINDOW.fill(self.WINDOWCOLOR)
        pygame.draw.rect(self.WINDOW, self.BGCOLOR, (19, 19, 402, 402), 0)
        pygame.draw.rect(self.WINDOW, self.BLACK_COL, (19, 19, 402, 402), 1)
        if 432 < self.MOUSEX < 630 and 382 < self.MOUSEY < 420:
            pygame.draw.rect(self.WINDOW, (255, 50, 50),
                             (432, 382, 198, 38), 0)
        else:
            pygame.draw.rect(self.WINDOW, (220, 0, 0), (432, 382, 198, 38), 0)
        pygame.draw.rect(self.WINDOW, self.BLACK_COL, (432, 382, 198, 38), 2)
        endgame_msg = self.FONT_NORMAL.render(
            'End Game', True, (255, 255, 255))
        if 432 < self.MOUSEX < 630 and 332 < self.MOUSEY < 370:
            pygame.draw.rect(self.WINDOW, (255, 50, 50),
                             (432, 332, 198, 38), 0)
        else:
            pygame.draw.rect(self.WINDOW, (220, 0, 0), (432, 332, 198, 38), 0)
        pygame.draw.rect(self.WINDOW, self.BLACK_COL, (432, 332, 198, 38), 2)
        undo_msg = self.FONT_NORMAL.render('Undo', True, (255, 255, 255))
        for i in range(8):
            for j in range(8):
                pygame.draw.rect(self.WINDOW, self.BLACK_COL,
                                 (50 * j + 20, 50 * i + 20, 50, 50), 1)
                if self.gamemode == 'multiplayer' or self.game.player == self.human:
                    if (i, j) in self.moves:
                        pygame.draw.circle(
                            self.WINDOW, self.FGCOLOR, (50 * j + 45, 50 * i + 45), 4)
                if 50 * j + 20 < self.MOUSEX < 50 * j + \
                        70 and 50 * i + 20 < self.MOUSEY < 50 * i + 70:
                    pygame.draw.rect(self.WINDOW, self.FGCOLOR,
                                     (50 * j + 21, 50 * i + 21, 48, 48))
                if self.game.board.get((i, j)) == reversi.BLACK:
                    self.WINDOW.blit(
                        self.BLACK_IMG, (50 * j + 25, 50 * i + 25))
                elif self.game.board.get((i, j)) == reversi.WHITE:
                    self.WINDOW.blit(
                        self.WHITE_IMG, (50 * j + 25, 50 * i + 25))

        blk = self.FONT_NORMAL.render(
            ' = ' + str(self.game.score(reversi.BLACK)), True, (0, 0, 0))
        wht = self.FONT_NORMAL.render(
            ' = ' + str(self.game.score(reversi.WHITE)), True, (0, 0, 0))
        ptr = self.FONT_NORMAL.render('*', True, (255, 0, 0))

        self.WINDOW.blit(self.BLACK_IMG_SMALL, (480, 30))
        self.WINDOW.blit(self.WHITE_IMG_SMALL, (480, 70))
        self.WINDOW.blit(blk, (505, 30))
        self.WINDOW.blit(wht, (505, 70))
        if self.game.is_over():
            msg = 'Game over'
        elif self.moves == []:
            msg = TO_WORDS[self.game.player] + ' has no moves left. Passing to ' + \
                TO_WORDS[reversi.opp(self.game.player)]
        elif self.gamemode != 'singleplayer':
            msg = TO_WORDS[self.game.player] + '\'s turn'
        elif self.game.player == self.human:
            msg = 'Your turn'
        elif self.game.player == self.computer:
            msg = 'Computer is thinking'

        if self.game.player == reversi.BLACK:
            self.WINDOW.blit(ptr, (460, 30))
        else:
            self.WINDOW.blit(ptr, (460, 70))

        msg = self.FONT_NORMAL.render(msg, True, (0, 0, 0))
        self.WINDOW.blit(msg, (20, 450 - msg.get_rect().height / 2))
        self.WINDOW.blit(
            endgame_msg,
            (531 - endgame_msg.get_rect().width / 2,
             401 - endgame_msg.get_rect().height / 2))
        self.WINDOW.blit(undo_msg, (531 - undo_msg.get_rect().width /
                                    2, 351 - undo_msg.get_rect().height / 2))
        pygame.display.update()

    def display_winner(self):
        # Display the color of the winning player
        if self.winner is not None:
            msg = TO_WORDS[self.winner] + ' wins!'
        else:
            msg = 'Draw'

        black_rect = pygame.Surface((640, 480))
        black_rect.set_alpha(220)
        black_rect.fill(self.BLACK_COL)
        self.WINDOW.blit(black_rect, (0, 0))
        msg = self.FONT_HUGE.render(msg, True, (255, 255, 255))
        self.WINDOW.blit(msg, (320 - msg.get_rect().width /
                               2, 240 - msg.get_rect().height / 2))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    return
            self.CLOCK.tick(self.FPS)


if __name__ == '__main__':
    app = App()
    app.run()
