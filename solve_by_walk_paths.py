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
                possible_path = self.walk_paths_from_state(resulting_board, [move], [self.board.tiles,resulting_board])
                if (possible_path != None):
                    self.paths.append(possible_path)
        return self.paths

    def walk_paths_from_state(self, board_state, moves, visitedstates):
        print("\nWALKING PATHS\nVISITED STATES:\n{}\nMOVES: {}\n".format(visitedstates, moves))
        newwhatifs = Board(board_state).lookahead()
        for newmove in newwhatifs:
            print("considering move: {}".format(newmove))
            newboard = newwhatifs[newmove]
            if (newboard == self.board.solution):
                # we're done
                moves.append(newmove)
                print("Done - found the exit")
                return moves
            elif (newmove == moves[-1]):
                # ignore this move - it just takes us back
                print("Ignoring reversal")
                pass
            elif (not newboard in visitedstates):
                # let's go again
                print("Not done, and not going somewhere we've been before")
                moves.append(newmove)
                visitedstates.append(newboard)
                return self.walk_paths_from_state(newwhatifs[newmove], moves, visitedstates)
            else:
                # this approach won't work
                print("Not a viable path")
                return None

    def find_shortest_path(self):
        all_paths = self.find_paths()
        print("FINDING SHORTEST\npaths:\n{}".format(all_paths))
        shortest_path = None
        for path in all_paths:
            if (shortest_path == None) or (len(shortest_path) > len(path)):
                shortest_path = path
        return shortest_path