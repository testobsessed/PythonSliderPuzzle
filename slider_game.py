from math import sqrt


class Board:

    def __init__(self, tile_config=[1, 2, 3, 4, 5, 6, 7, 8, None]):
        if not Board.valid(tile_config):
            raise RuntimeError(
                "Tile configuration invalid. Must be a 2x2 or larger square with sequential numbers and one blank tile.")
        self.tiles = tile_config
        self.numbers = self.get_tile_numbers()
        self.solution = sorted(self.numbers) + [None]
        self.blank_position = self.tiles.index(None)
        self.dimension = int(sqrt(len(self.tiles)))
        self.inversions = self.count_inversions()

    def tileat(self, position):
        return self.tiles[position]

    def solved(self):
        return self.tiles == self.solution

    def move(self, tile):
        if self.is_move_valid(tile):
            tile_position = self.tiles.index(tile)
            self.tiles[self.blank_position] = tile
            self.blank_position = tile_position
            self.tiles[tile_position] = None

    def neighbor_above(self, tile_position):
        above_position = tile_position - self.dimension
        at_top_edge = (above_position < 0)
        return ("Edge" if at_top_edge else self.tileat(above_position))

    def neighbor_right(self, tile_position):
        at_right_edge = ((tile_position % self.dimension) == (self.dimension - 1))
        return ("Edge" if at_right_edge else self.tileat(tile_position + 1))

    def neighbor_below(self, tile_position):
        below_position = tile_position + self.dimension
        return (self.tileat(below_position) if below_position < len(self.tiles) else "Edge")

    def neighbor_left(self, tile_position):
        at_left_edge = ((tile_position % self.dimension) == 0)
        return ("Edge" if at_left_edge else self.tileat(tile_position - 1))

    def tile_neighbors(self, tile):
        tile_position = self.tiles.index(tile)

        above = self.neighbor_above(tile_position)
        right = self.neighbor_right(tile_position)
        below = self.neighbor_below(tile_position)
        left = self.neighbor_left(tile_position)
        return [above, right, below, left]

    def is_move_valid(self, tile):
        # make sure there empty spot is a neighbor
        return (None in self.tile_neighbors(tile))

    def count_inversions(self):
        num_inversions = 0
        for num, tile in enumerate(self.numbers, start=0):
            for i in range(num + 1, len(self.numbers)):
                if (self.numbers[i] < tile):
                    num_inversions += 1
        return num_inversions

    def is_solvable(self):
        # start with the assumption that it is not solvable
        solvable = False

        # for an NxN puzzle where N is Even
        if (self.dimension % 2) == 0:
            # a puzzle NxN where N is Even is only solvable if:
            # ...Inversions are Odd and blank tile row # is Odd, OR
            # ...Inversions are Even and blank tile row # is Even
            blank_row = (self.tiles.index(None) // self.dimension) + 1
            if ((self.inversions % 2) == (blank_row % 2)): solvable = True

        # and for Odd...
        else:
            # a puzzle NxN where N is Odd is only solvable if Inversions is Even
            if ((self.inversions % 2) == 0): solvable = True

        return solvable

    def get_tile_numbers(self):
        # get a list of just the numbers in the tile config, sorted
        numbers = [item for item in self.tiles if isinstance(item, int)]
        return numbers

    def delta_from_solution(self):
        return self.solution_diff_score_from(self.tiles)

    def solution_diff_score_from(self, new_state):
        delta = 0
        for num, tile in enumerate(new_state, start=1):
            if (tile != None):
                delta += abs(tile - num)
        return delta

    def available_moves(self):
        return sorted([tile for tile in self.tile_neighbors(None) if isinstance(tile, int)])

    def lookahead(self):
        whatif = {}
        for tile in self.available_moves():
            board_state = self.tiles[:]
            tile_position = board_state.index(tile)
            none_position = board_state.index(None)
            board_state[tile_position] = None
            board_state[none_position] = tile
            whatif[tile] = board_state
        return whatif

    @staticmethod
    def valid(tile_config):
        # error out if the number of items in the list is too small
        # or if it's not a square
        is_at_least_2_square = (len(tile_config) >= 4) & (sqrt(len(tile_config)).is_integer())
        if not is_at_least_2_square:
            return False

        # error out if there is not one and only one blank space
        numbers = sorted([item for item in tile_config if isinstance(item, int)])
        has_one_space = (len(tile_config) - len(numbers) == 1)
        if not has_one_space:
            return False

        # detect if the tiles are not a set of sequential numbers
        has_sequential_numbers = True
        for num, tile in enumerate(numbers, start=1):
            if tile != num:
                has_sequential_numbers = False

        return has_sequential_numbers

    @staticmethod
    def get_boards(dimension):
        # generate the solution board
        solution = [place for place in range(1, dimension ** 2)] + [None]

        # get all the variations
        permutations = Board.get_permutations(solution)

        # remove the solution and filter out unsolvable boards
        permutations.remove(solution)
        return [board for board in permutations if Board(board).is_solvable()]

    @staticmethod
    def get_permutations(tiles):
        permutations = []
        if len(tiles) == 2:
            permutations.append([tiles[0], tiles[1]])
            permutations.append([tiles[1], tiles[0]])
        else:
            for n in range(0, len(tiles)):
                remainder = tiles[:]
                building_array = [tiles[n]]
                remainder.remove(tiles[n])
                variations = Board.get_permutations(remainder)
                for variation in variations:
                    permutations.append(building_array + variation)
        return permutations
