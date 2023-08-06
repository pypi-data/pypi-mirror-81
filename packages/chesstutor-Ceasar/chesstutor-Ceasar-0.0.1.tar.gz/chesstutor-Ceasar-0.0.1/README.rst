
********************************************************************************
Chess Tutor
********************************************************************************

Improve your chess skills by playing human-computer chess on the command line.

The program will use a chess engine to calculate the top three moves in the
current position, and display them to the player in a random order without
revealing the scores. The player attempts to choose the best move. Then program
reveals the score and chooses the best move for black.

Set up
********************************************************************************

Install the stockfish chess engine (Mac OS)::

    brew install stockfish

Create the environment::

    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt

Then play::

    python chesstutor.py
