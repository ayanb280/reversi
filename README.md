# Reversi

![A game in progress](/res/screenshot/gameplay.png)


## About the program

This is an implementation of the game of [Reversi](https://en.wikipedia.org/wiki/Reversi)
in Python. You can either play against the computer or against another human.
The computer player has three levels of difficulty.


## About the game

Reversi is a strategy board game for two players, played on an 8×8 board. There
are 64 identical *discs* which are white on one side and black on the other.
Players are assigned colours *black* and *white* and take turns to place discs
on the board with their colour facing up. During a move, any disc of the
opponent’s colour that lies in a straight line and is bounded by the disc just
placed and another disc of the current player’s colour, is flipped to the
current player’s colour. 

The objective of the game is to own the maximum number of discs by the time the
board is completely filled or there remain no moves available.


## How to run the program

The code is in [Python 3](https://www.python.org/) and requires the [Pygame](https://www.pygame.org/)
library. Install Pygame by running:

    $ pip install pygame

Then run [/src/main.py](/src/main.py) in Python 3.

    $ git clone 'https://github.com/ayanb280/reversi.git'
    $ cd reversi
    $ python src/main.py


## Implementation

The program uses [Minimax](https://en.wikipedia.org/wiki/Minimax) to look ahead
and choose moves for the computer player. Though minimax is optimized by
[alpha–beta pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning),
it is not possible to expand the entire game tree. So the computer looks ahead
only to a certain depth and assigns a [heuristic rating](http://www.mkorman.org/othello.pdf#subsection.2.2)
to each board state and plays that move which leads to the best state. The
look-ahead is performed on a separate thread so as not to hang up the UI.