from qiskit import *

sim = Aer.get_backend('aer_simulator')  # choose the simulator to execute our circuit on


# Use qutrits to describe the possible states
# |00> corresponds to an empty cell
# |01> the cell contains o
# |11> the cell contains x

def make_grid(result):
    """Prepares the quantum circuit representing the grid and initializes it to the previous result."""
    cells = []
    for i in range(9):
        cells.append(QuantumRegister(2, name='cell_' + str(i)))
    grid = QuantumCircuit(*cells, ClassicalRegister(18))
    for i in range(9):
        if result[i * 2:i * 2 + 2] == '01':
            grid.x(i * 2 + 1)
        elif result[i * 2:i * 2 + 2] == '11':
            grid.x(i * 2)
            grid.x(i * 2 + 1)
    return grid


def o_superposition(grid, cell1, cell2):
    """Puts the two qutrits in an equal superposition of |0100> and |0001> states."""
    grid.h(cell1 * 2 + 1)
    grid.cx(cell1 * 2 + 1, cell2 * 2 + 1)
    grid.x(cell1 * 2 + 1)


def x_superposition(grid, cell1, cell2):
    """Puts the two qutrits in an equal superposition of |1100> and |0011> states."""
    grid.h(cell1 * 2)
    grid.cx(cell1 * 2, cell2 * 2 + 1)
    grid.x(cell1 * 2)
    grid.cx(cell1 * 2, cell1 * 2 + 1)
    grid.cx(cell2 * 2 + 1, cell2 * 2)


def measure_grid(grid):
    """Measure each qutrit."""
    for i in range(18):
        grid.measure(i, i)


def run_simulator(grid, sim):
    """Run the circuit on the simulator."""
    counts = sim.run(grid, shots=1).result().get_counts()
    result = next(iter(counts))
    return result[::-1]


def check_state(state):
    """Check the qutrit states."""
    if state == '00':
        return ' .'
    elif state == '01':
        return ' o'
    else:
        return ' x'


def print_grid(result):
    """Prints the grid in the conventional format."""
    for i in range(9):
        print('|' + check_state(result[i * 2:i * 2 + 2]) + ' ', end='')
        if (i + 1) % 3 == 0:
            print('|')


def check_full(result):
    """Check if the grid is full."""
    full = True
    for i in range(9):
        if not (result[i * 2:i * 2 + 2] == '01' or result[i * 2:i * 2 + 2] == '11'):
            full = False
    return full


def player_o():
    """Player o input."""
    move = input("Player o: ")
    return move


def player_x():
    """Player x input."""
    move = input("Player x: ")
    return move


def check_format(last_move):
    """Check if the input is in the correct format."""
    if len(last_move) == 1:
        return True
    if len(last_move) == 3 and last_move[1] == ',':
        return True
    return False


def check_index(last_move):
    """Check if the cell index is within the range."""
    if len(last_move) == 1:
        if 0 <= int(last_move) <= 8:
            return True
        else:
            return False
    if 0 <= int(last_move[2]) <= 8:
        return True
    return False


def check_not_repeated(last_move):
    if len(last_move) == 3:
        return last_move[0] != last_move[2]
    return True


def check_occupied(last_move, cells):
    """Check if the entered cell is already occupied"""
    if cells[int(last_move[0])] != ' .':
        return False
    if len(last_move) == 3:
        if cells[int(last_move[2])] != ' .':
            return False
    return True


def check_move(last_move, cells):
    """Check if the player has entered a valid move."""
    if not check_format(last_move) or not check_index(last_move) or not check_not_repeated(last_move):
        print('Please enter the move in the correct format \'a\' or \'a,b\', where 0 <= a,b <= 8, and a!=b.')
        return False
    if not check_occupied(last_move, cells):
        print('Please enter only the unoccupied cells.')
        return False
    return True


def print_intermediate(cells, last_move, n, player):
    """Print the grid inbetween measurements."""
    for i in range(9):
        if str(i) in last_move:
            if len(last_move) > 1:
                print('|' + player + str(n) + ' ', end='')
                cells[i] = player + str(n)
            else:
                print('| ' + player + ' ', end='')
                cells[i] = ' ' + player
        else:
            print('|' + cells[i] + ' ', end='')
        if (i + 1) % 3 == 0:
            print('|')


def update_cells(result):
    """Update the cells after measurement."""
    cells = [' .'] * 9
    for i in range(9):
        cells[i] = check_state(result[i * 2:i * 2 + 2])
    return cells


def check_winner(cells):
    """Check if there is a winner."""
    win_states = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    for (x, y, z) in win_states:
        if cells[x] == cells[y] == cells[z] != ' .':
            print('The winner is Player ' + cells[x] + '!')
            return True
    return False


def play_game(sim):
    result = '0' * 18
    cells = [' .'] * 9
    k = 0
    while not check_full(result):
        winner = False
        n = 1
        grid = make_grid(result)
        while ' .' in cells:
            if k % 2 == 0:
                last_move = player_x()
                while not check_move(last_move, cells):
                    last_move = player_x()
                print_intermediate(cells, last_move, n, 'x')
                if len(last_move) > 1:
                    x_superposition(grid, int(last_move[0]), int(last_move[2]))
                else:
                    grid.x(int(last_move) * 2)
                    grid.x(int(last_move) * 2 + 1)
                    winner = check_winner(cells)
                    if winner:
                        break
            else:
                last_move = player_o()
                while not check_move(last_move, cells):
                    last_move = player_o()
                print_intermediate(cells, last_move, n, 'o')
                if len(last_move) > 1:
                    o_superposition(grid, int(last_move[0]), int(last_move[2]))
                else:
                    grid.x(int(last_move) * 2 + 1)
                    winner = check_winner(cells)
                    if winner:
                        break
            n = n + 1
            k = k + 1
        if winner:
            break
        measure_grid(grid)
        result = run_simulator(grid, sim)
        print('Collapsed:')
        print_grid(result)
        cells = update_cells(result)
        winner = check_winner(cells)
        if winner:
            break
    if not winner:
        print('Draw.')


if __name__ == "__main__":
    play_game(sim)
