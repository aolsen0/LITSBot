This is an AI designed to play the board game Battle of LITS. The rules can be found [here](http://www.nestorgames.com/rulebooks/BATTLEOFLITS_EN.pdf).

This requires pytorch to run and colorama to display correctly. These can be installed with `pip install colorama` and `pip install torch`.

How to interface with `main.py`:
* It takes a couple seconds to boot up, after which a board must be input. If the first input line is `i`, the user must input a board by writing 10 lines, each with 10 characters from the set `{'X', 'O', ' '}`. Otherwise, a board will be created randomly.
* Subsequently, the following commands can be used:
	* `i` allows the user to input a piece on a second line. The use must specify the type of piece, and 8 numbers from 0-9 indicating the row and column coordinates of its four squares. For example, `L 7 4 7 5 7 6 8 6` Describes an L piece which covers the cells (7, 4), (7, 5), (7,6), and (8,6).
	* `g [time]` asks the AI to play the best move, and will not start searching a deeper leve of the game tree after the given number of seconds. The AI will continue searching layers of the game tree that it started before the given time limit, so this may take up to 4 times as long to run as specified.
	* `e [time]` is the same, except the best move is not automatically played.
	* `c` returns the number of legal moves.
	* `p` prints the top 16 moves, based only on a superficial evaluation and no deeper game tree searches.
	* `q` does the same, but with some additional bias to show moves which are less similar to moves already shown, even if they are not necessarily as good.
* Once there are no more legal moves, the relative score of the two players is printed.

There is also provided code for retraining existing models or training additional models if you desire. 