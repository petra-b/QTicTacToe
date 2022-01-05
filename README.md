# QTicTacToe
Quantum version of the game Tic Tac Toe.

This game was inspired by the game at [this site](https://quantumtictactoe.com/).

### Installation

The game requires the qiskit python library, which can be installed using pip.

### About the game

The special quantum feature added on top of the classical game is a possibility of making a move (writing x or o) which is a superposition over two cells, 
instead of choosing one cell. That is, upon playing a move, the piece can be "spread" in superposition across two cells - upon measurement the piece
will collapse into one of the cells with probability 50%. The measurement of the grid is performed each time the grid is full (each cell is either 
occupied by x or o, or the cell is in superposition).

### Rules

Players x and o play in turn, starting with x. Upon the move each player can choose one of the two options: making a classical move (choosing one cell) 
or a quantum move (choosing a superposition of two cells). The cells are indexed from 0 to 8, and the move has to be in format 'a' or 'a,b', 
where 0 <= a,b <= 8, and a != b. Once the grid is full, each superposition is collapsed, filling in one of the two possible cells. The winning criteria are
the same as in the classical game.

