from slider_game import Board
import random

# An attempt at a brute force solution by recursively walking
# all paths.
#
# It doesn't work because there are too many possibilities.

class Solver:
    def __init__(self, tile_config):
        self.start_state = tile_config[:]
        self.board = Board(tile_config)
        self.solutions = {}
        self.recursed = 0
        self.all_paths = []
        self.solution_path = []

    def solve(self):
        moves = self.find_shortest_path()
        self.solution_path = moves
        if (moves != None):
            for move in moves:
                self.board.move(move)
        else:
            print("CRUD. Could not find a solution for {}.".format(self.start_state))
        return self.board.solved()

    def find_all_paths_from_point(self, board_state, completed_moves, previous_states, paths_so_far):
        all_paths = paths_so_far[:]
        available_moves = Board(board_state).lookahead()
        for move in available_moves:
            new_board_state = available_moves[move]
            path = completed_moves[:]
            if (new_board_state == self.board.solution):
                # we're done
                path.append(move)
                all_paths.append(path)
            elif (len(completed_moves) > 0) and (move == completed_moves[-1]):
                # ignore attempts to undo
                pass
            elif (len(path) > 2):
                path.append(move)
                path.append("R")
                all_paths.append(path)
            elif (new_board_state in previous_states):
                path.append(move)
                path.append("X")
                all_paths.append(path)
            else:
                path.append(move)
                previous_states.append(board_state)
                all_paths.extend(self.find_all_paths_from_point(new_board_state, path, previous_states, all_paths))
        return all_paths

    def find_shortest_path(self):
        self.all_paths = self.find_all_paths_from_point(self.start_state, [], [], [])
        shortest_path = None
        for path in self.all_paths:
            if (not isinstance(path[-1], int)):
                # skip the ones marked as not viable
                pass
            elif (shortest_path == None) or (len(shortest_path) > len(path)):
                shortest_path = path
        return shortest_path