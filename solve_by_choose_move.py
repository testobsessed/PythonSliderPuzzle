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
            while (not self.board.solved()) and (self.status != "stuck"):
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
        # ONLY WORKS for 3x3s, not 4x4s

        self.locked_tiles = []

        # if 1 is in the 1 place, lock it
        if (self.board.tiles[0] == 1):
            self.locked_tiles.append(1)
            # and if 2 AND 3 are in place, lock them
            if (self.board.tiles[1] == 2 and self.board.tiles[2] == 3):
                self.locked_tiles.append(2)
                self.locked_tiles.append(3)

        if ((self.board.dimension == 3) and
                (1 in self.locked_tiles) and
                (self.board.tiles[3] == 4) and
                (self.board.tiles[6] == 7)
        ):
            self.locked_tiles.append(4)
            self.locked_tiles.append(7)

    def find_best_move(self):
        possible_moves = self.board.lookahead()
        move_scores = {}
        for move in possible_moves:
            move_scores[move] = self.board.solution_diff_score_from(possible_moves[move])
            # only consider moves that don't get us back to a known state
            if (move in self.locked_tiles):
                move_scores[move] += 9999
            if len(self.visited_states) > 0 and (possible_moves[move] == self.visited_states[-1]):
                move_scores[move] += 99999
            if (possible_moves[move] in self.visited_states):
                move_scores[move] += 99

        best_move = min(move_scores, key=move_scores.get)
        # print("BEST MOVE: {}".format(best_move))
        self.board.move(best_move)
        self.moves.append(best_move)
        self.visited_states.append(self.get_board_state())
        # if (best_move in self.locked_tiles):
        #     self.locked_tiles.remove(best_move)
        self.check_locks()
        if (len(self.moves) > 500):
            self.status = "stuck"
