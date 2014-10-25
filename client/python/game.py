##############################################################################
# game.py - Responsible for generating moves to give to client.py            #
# Moves via stdout in the form of "# # # #" (block index, # rotations, x, y) #
# Important function is find_move, which should contain the main AI          #
##############################################################################

import sys
import json

# Simple point class that supports equality, addition, and rotations
class Point:
    x = 0
    y = 0

    # Can be instantiated as either Point(x, y) or Point({'x': x, 'y': y})
    def __init__(self, x=0, y=0):
        if isinstance(x, dict):
            self.x = x['x']
            self.y = x['y']
        else:
            self.x = x
            self.y = y

    def __add__(self, point):
        return Point(self.x + point.x, self.y + point.y)

    def __eq__(self, point):
        return self.x == point.x and self.y == point.y

    # rotates 90deg counterclockwise
    def rotate(self, num_rotations):
        if num_rotations == 1: return Point(-self.y, self.x)
        if num_rotations == 2: return Point(-self.x, -self.y)
        if num_rotations == 3: return Point(self.y, -self.x)
        return self

    def distance(self, point):
        return abs(point.x - self.x) + abs(point.y - self.y)

class State:
    blocks = []
    board = []
    utility = []
    to_move = -1

    def __init__(self, blocks, board, utility, to_move):
      self.blocks = blocks
      self.board = board
      self.utility = utility
      self.to_move = to_move

class Game:
    blocks = []
    grid = []
    bonus_squares = []
    my_number = -1
    dimension = -1 # Board is assumed to be square
    turn = -1

    def __init__(self, args):
        self.interpret_data(args)

        def update_score(self, score, block, point):
        all_points = [points + point for points in block]
        if set(all_points) & set(self.bonus_squares):
            return score + 3*len(block)
        else:
            return score + len(block)

    def actions(self, state):
        N = self.dimension - 1
        moves = []
        for block in self.blocks:
        for rotations in range(0, 4):
            new_block = self.rotate_block(block, rotations)
            for i in range(0, N * N):
                x = i / N
                y = i % N
                if self.can_place(new_block, Point(x,y)):
                    moves.append(new_block, Point(x,y))
        return moves

    def result(state, (block, point)):
        new_score = self.update_score(state.score, block, point)
        new_board = deepcopy(state.board)
        for (x,y) in [points + point for points in block]:
            new_board[x][y] = state.player
        new_player = (player + 1) % 4
        new_blocks = deepcopy(state.blocks)
        new_blocks.remove(block)
        return State(to_move=new_player, board=new_board, utility=new_score, blocks=blocks)

    def utility(self, state):

        player = state.player
        board = state.board
        score = state.score

        N = self.dimension - 1
        k = 2  # num_points + k * score
        C = 4  # Distance from liberties to be tested

        def free_space(x, y):
            if x < 0 or x > N or y < 0 or y > N: 
                return False
            if x != 0 and board[x-1][y] == player:
                return False
            if x != N and board[x+1][y] == player:
                return False
            if y != 0 and board[x][y-1] == player:
                return False
            if y != N and board[x][y+1] == player:
                return False
            return board[x][y] == -1

        def calc_liberties():
            liberties = []
            for i in range(0, N * N):
                x = i / N
                y = i % N
                if board[x][y] == player:
                    for point in [(x-1,y-1), (x-1,y+1), (x+1,y-1), (x+1,y+1)]:
                        if free_space(*point):
                            if point not in liberties:
                                liberties.append(point)
            return liberties


        liberties = calc_liberties()
        empty_points = []
        for point in libteries:
            for x_offset in range(C):
                for y_offset in range(C - x_offset):
                    new_point = (point.x + x_offset, point.y + y_offset)
                    if free_space(*new_point):
                        if new_point not in empty_points:
                            empty_points.append(new_point)

        num_points = len(empty_points)
        return num_points + k * score


    # find_move is your place to start. When it's your turn,
    # find_move will be called and you must return where to go.
    # You must return a tuple (block index, # rotations, x, y)
    def find_move(self):
        moves = []
        N = self.dimension
        for index, block in enumerate(self.blocks):
            for i in range(0, N * N):
                x = i / N
                y = i % N

                for rotations in range(0, 4):
                    new_block = self.rotate_block(block, rotations)
                    if self.can_place(new_block, Point(x, y)):
                        return (index, rotations, x, y)

        return (0, 0, 0, 0)

    # Checks if a block can be placed at the given point
    def can_place(self, block, point):
        onAbsCorner = False
        onRelCorner = False
        N = self.dimension - 1

        corners = [Point(0, 0), Point(N, 0), Point(N, N), Point(0, N)]
        corner = corners[self.my_number]

        for offset in block:
            p = point + offset
            x = p.x
            y = p.y
            if (x > N or x < 0 or y > N or y < 0 or self.grid[x][y] != -1 or
                (x > 0 and self.grid[x - 1][y] == self.my_number) or
                (y > 0 and self.grid[x][y - 1] == self.my_number) or
                (x < N and self.grid[x + 1][y] == self.my_number) or
                (y < N and self.grid[x][y + 1] == self.my_number)
            ): return False

            onAbsCorner = onAbsCorner or (p == corner)
            onRelCorner = onRelCorner or (
                (x > 0 and y > 0 and self.grid[x - 1][y - 1] == self.my_number) or
                (x > 0 and y < N and self.grid[x - 1][y + 1] == self.my_number) or
                (x < N and y > 0 and self.grid[x + 1][y - 1] == self.my_number) or
                (x < N and y < N and self.grid[x + 1][y + 1] == self.my_number)
            )

        if self.grid[corner.x][corner.y] < 0 and not onAbsCorner: return False
        if not onAbsCorner and not onRelCorner: return False

        return True

    # rotates block 90deg counterclockwise
    def rotate_block(self, block, num_rotations):
        return [offset.rotate(num_rotations) for offset in block]

    # updates local variables with state from the server
    def interpret_data(self, args):
        if 'error' in args:
            debug('Error: ' + args['error'])
            return

        if 'number' in args:
            self.my_number = args['number']

        if 'board' in args:
            self.dimension = args['board']['dimension']
            self.turn = args['turn']
            self.grid = args['board']['grid']
            self.blocks = args['blocks'][self.my_number]
            self.bonus_squares = args['board']['bonus_squares']

            for index, block in enumerate(self.blocks):
                self.blocks[index] = [Point(offset) for offset in block]

        if (('move' in args) and (args['move'] == 1)):
            send_command(" ".join(str(x) for x in self.find_move()))

    def is_my_turn(self):
        return self.turn == self.my_number

def get_state():
    return json.loads(raw_input())

def send_command(message):
    print message
    sys.stdout.flush()

def debug(message):
    send_command('DEBUG ' + str(message))

def main():
    setup = get_state()
    game = Game(setup)

    while True:
        state = get_state()
        game.interpret_data(state)

if __name__ == "__main__":
    main()
