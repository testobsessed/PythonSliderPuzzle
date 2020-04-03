from slider_game import Board
import tracemalloc
import random
import gc



class Solver:
    def __init__(self, tile_config):
        self.start_state = tile_config[:]
        self.board = Board(tile_config)
        self.solutions = {}
        self.recursed = 0
        self.all_paths = []
        self.solution_path = []
        self.shortest_solution = None

    def solve(self):
        # moves = self.find_shortest_path()
        # self.solution_path = moves
        self.find_all_paths_from_point(self.start_state, [], [], [])
        if (self.shortest_solution != None):
            for move in self.shortest_solution:
                self.board.move(move)
        else:
            print("Could not find a solution for {}.".format(self.start_state))
        return self.board.solved()

    def find_all_paths_from_point(self, board_state, completed_moves, previous_states, paths_so_far):
        all_paths = paths_so_far[:]
        available_moves = self.lookahead(board_state)
        print("\nGoing into path search loop.\nBoard state: {} \nAvailable Moves: {}".format(board_state, available_moves))
        move_scores = self.prioritize(available_moves)
        print("Move Scores: {}".format(move_scores))
        move_priorities = sorted(move_scores, key = move_scores.get)
        for move in move_priorities:
            new_board_state = available_moves[move]
            path = completed_moves[:]
            if (new_board_state == self.board.solution):
                # we're done
                path.append(move)
                all_paths.append(path)
                if (self.shortest_solution == None):
                    self.shortest_solution = path
                elif (len(path) < len(self.shortest_solution)):
                    self.shortest_solution = path
            elif (len(completed_moves) > 0) and (move == completed_moves[-1]):
                # ignore attempts to undo
                pass
            elif (self.shortest_solution != None) and (len(all_paths) > 9000):
                all_paths.append(["Z"])
                break  # you have a solution, just give up
            elif ((len(path) >= 30) or
                      ((self.shortest_solution != None) and
                       (len(path) + 1) >= len(self.shortest_solution))):
                # give up
                path.append(move)
                path.append("L")
                all_paths.append(path)
            elif (new_board_state in previous_states):
                path.append(move)
                path.append("X")
                all_paths.append(path)
            else:
                path.append(move)
                previous_states.append(board_state)
                all_paths.extend(self.find_all_paths_from_point(new_board_state, path, previous_states, all_paths))
        print("Returning from find_all_paths_from_point\nExplored {} paths".format(len(all_paths)))
        if (self.shortest_solution != None):
            print("...shortest path has {} moves\n  > {}".format(len(self.shortest_solution),self.shortest_solution))
        else:
            print("...no solution yet.\n")
        return all_paths

    def prioritize(self, possibilities):
        scores = {}
        for move in possibilities:
            # print("\nWorking on move {}".format(move))
            board_state = possibilities[move]
            move_score = self.sum_scores(board_state)
            # lookahead_score = 0
            # lookahead = self.lookahead(board_state)
            # for board in lookahead:
            #     lookahead_score += self.sum_scores(lookahead[board])
            # scores[move] = move_score + lookahead_score
            scores[move] = move_score
        # gc.collect()
        # tracemalloc.start(10)
        #
        # snapshot = tracemalloc.take_snapshot()
        # top_stats = snapshot.statistics('lineno')
        # print("[ Top 10 ]")
        # for stat in top_stats[:10]:
        #     print(stat)
        # stats = snapshots[-1].filter_traces().compare_to(self.snapshots[-2], 'filename')
        # for stat in stats[:10]:
        #     print("{} new KiB {} total KiB {} new {} total memory blocks: ".format(stat.size_diff / 1024, stat.size / 1024,
        #                                                          stat.count_diff, stat.count))
        return scores

    def sum_scores(self, tiles):
        score = 0
        print("Scoring board state: {}".format(tiles))
        inversions = self.count_inversions(tiles) * 10
        deltapos = self.count_delta_from_position(tiles) * 10
        deltarowcol = self.count_delta_from_rowcol(tiles) * 10
        countneighbor = self.count_delta_from_neighbor(tiles)
        print("inversion {} | deltapos {} | deltarowcol {} | neighbor {}".format(inversions, deltapos, deltarowcol, countneighbor))
        return inversions + deltarowcol + deltapos + countneighbor

    def count_inversions(self, tiles):
        numbers = [item for item in tiles if isinstance(item, int)]
        num_inversions = 0
        for num, tile in enumerate(numbers, start=0):
            for i in range(num + 1, len(numbers)):
                if (numbers[i] < tile):
                    num_inversions += 1
        # print("...inversions is {}".format(num_inversions))
        return num_inversions

    def count_delta_from_position(self, tiles):
        delta = 0
        for num, tile in enumerate(tiles, start=1):
            if (tile != None):
                delta += abs(tile - num)
        # print("...position delta is {}".format(delta))
        return delta

    def count_delta_from_rowcol(self, tiles):
        delta = 0
        for num, tile in enumerate(tiles, start=1):
            if (tile == None):
                tile = (self.board.dimension)**2
            tilerow = (num // self.board.dimension) + 1
            tilecol = ((num + 1) % self.board.dimension) + 1
            tilerow_solution = (tile // self.board.dimension) + 1
            tilecol_solution = ((tile + 1) % self.board.dimension) + 1
            delta = (abs(tilerow_solution - tilerow)) + (abs(tilecol_solution - tilecol))
        # print("...rowcol delta is {}".format(delta))
        return delta

    def count_delta_from_neighbor(self, tiles):
        count = 0
        for num, tile in enumerate(tiles, start=0):
            neighbor_positions = self.neighbor_indices(tiles, num)
            for neighbor in neighbor_positions:
                if (tile!= None and tiles[neighbor] != None):
                    count += abs(tile - tiles[neighbor])
        count += 8 - tiles.index(None)
        return count

    def lookahead(self, board):
        available_moves = self.get_available_moves_from(board)
        none_position = board.index(None)
        whatif = {}
        for tile in available_moves:
            whatif_board = board[:]
            tile_position = board.index(tile)
            whatif_board[tile_position] = None
            whatif_board[none_position] = tile
            whatif[tile] = whatif_board
        return whatif

    def get_available_moves_from(self, board):
        none_index = board.index(None)
        neighbor_indices = self.neighbor_indices(board, none_index)
        moves = []

        for position in neighbor_indices:
            moves.append(board[position])

        return sorted(moves)

    def neighbor_indices(self, board, position):
        neighbor_indices = []

        upper = position - self.board.dimension
        if (upper >= 0):
            neighbor_indices.append(upper)

        right = position % self.board.dimension
        if (right != self.board.dimension - 1):
            neighbor_indices.append(position + 1)

        lower = position + self.board.dimension
        if (lower < len(board)):
            neighbor_indices.append(lower)

        left = position % self.board.dimension
        if (left != 0):
            neighbor_indices.append(position - 1)

        return neighbor_indices

