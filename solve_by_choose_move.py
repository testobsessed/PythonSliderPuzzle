from slider_game import Board
import random


class Solver:
    def __init__(self, tile_config):
        self.board = Board(tile_config)
        self.moves = []
        self.visited_states = []
        self.status = "Solving..."
        self.locked_tiles = []

    def solve(self):
        if self.board.is_solvable():
            self.visited_states.append(self.get_board_state())
            while not self.board.solved():
                self.find_best_move()
        else:
            self.status = "Unsolvable"

    def get_available_moves(self):
        return sorted([tile for tile in self.board.tile_neighbors(None) if isinstance(tile, int)])

    def get_board_state(self):
        board_state = self.board.tiles[:]
        return board_state

    def move_randomly(self):
        available_moves = self.get_available_moves()
        print("available moves before shuffle: {}".format(available_moves))
        random.shuffle(available_moves)
        print("available moves after shuffle: {}".format(available_moves))
        for tile in available_moves:
            self.board.move(tile)
            if (self.board.tiles in self.visited_states):
                # if we've been here before, undo
                self.board.move(tile)
            else:
                self.moves.append(tile)
                self.visited_states.append(self.get_board_state())
                break

    def check_locks(self):
        # this is a really really dumb implementation - TEMPORARY
        self.locked_tiles = []

        # lock as much of the 1st row as possible
        for place in range(0, self.board.dimension):
            tile = place + 1
            if (self.board.tiles[place] == tile):
                self.locked_tiles.append(tile)
            else:
                break

    def find_best_move(self):
        possible_moves = self.board.lookahead()
        move_scores = {}
        for move in possible_moves:
            move_scores[move] = self.board.solution_diff_score_from(possible_moves[move])
            # only consider moves that don't get us back to a known state
            if (move in self.locked_tiles):
                move_scores[move] += 9999
            if (possible_moves[move] in self.visited_states):
                move_scores[move] += 999

        best_move = min(move_scores, key=move_scores.get)
        # print("BEST MOVE: {}".format(best_move))
        self.board.move(best_move)
        self.moves.append(best_move)
        self.visited_states.append(self.get_board_state())
        if (best_move in self.locked_tiles):
            self.locked_tiles.remove(best_move)
        self.check_locks()
