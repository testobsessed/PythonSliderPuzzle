from slider_game import Board
import random


class Solver:
    def __init__(self, tile_config):
        self.board = Board(tile_config)
        self.solutions = {}
        self.recursed = 0
        self.paths = []

    def solve(self):
        moves = self.find_shortest_path()
        for move in moves:
            self.board.move(move)

    def find_paths(self):
        whatifs = self.board.lookahead()
        for move in whatifs:
            resulting_board = whatifs[move]
            if (resulting_board == self.board.solution):
                # we're done, got it in 1
                self.paths.append([move])
            else:
                self.paths.append(self.walk_paths_from_state(resulting_board, [move], [self.board.tiles,resulting_board]))
        return self.paths

    def walk_paths_from_state(self, board_state, moves, visitedstates):
        newwhatifs = Board(board_state).lookahead()
        for newmove in newwhatifs:
            newboard = newwhatifs[newmove]
            if (newboard == self.board.solution):
                # we're done
                moves.append(newmove)
                return moves
            elif (not newboard in visitedstates):
                # let's go again
                visitedstates.append(newboard)
                moves.append(newmove)
                return self.walk_paths_from_state(newwhatifs[newmove], moves, visitedstates)
            else:
                # this approach won't work
                pass

    def find_shortest_path(self):
        all_paths = self.find_paths()
        shortest_path = None
        for path in all_paths:
            if (shortest_path == None) or (len(shortest_path) > len(path)):
                shortest_path = path
        return shortest_path