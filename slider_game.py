from math import sqrt
from typing import List, Union


class Board:

    def __init__(self, tile_config = [1,2,3,4,5,6,7,8,None]):
        if not Board.valid(tile_config):
            raise RuntimeError("Tile configuration invalid. Must be a 2x2 or larger square with sequential numbers and one blank tile.")
        self.tiles = tile_config
        self.solution = Board.numbers(tile_config) + [None]
        self.blank_position = self.tiles.index(None)
        self.dimension = int(sqrt(len(self.tiles)))

    def tileat(self, position):
        return self.tiles[position]

    def rowcol(self, position):
        row = position // self.dimension
        col = position % self.dimension
        return [row, col]

    def solved(self):
        return self.tiles == self.solution

    def move(self, tile):
        if self.is_move_valid(tile):
            tile_position = self.tiles.index(tile)
            self.tiles[self.blank_position] = tile
            self.blank_position = tile_position
            self.tiles[tile_position] = None

    def rowcol_of_tile(self, tile):
        tile_position = self.tiles.index(tile)
        return self.rowcol(tile_position)

    def position_neighbor_above(self, tile_position):
        above_position = tile_position - self.dimension
        return (self.tileat(above_position) if above_position >= 0 else "Edge")

    def position_neighbor_right(self, tile_position):
        if ((tile_position % self.dimension) < (self.dimension - 1)):
            right = self.tileat(tile_position + 1)
        else:
            right = "Edge"
        return right

    def position_neighbor_below(self, tile_position):
        if (tile_position + self.dimension < len(self.tiles)):
            below = self.tileat(tile_position + self.dimension)
        else:
            below = "Edge"
        return below

    def position_neighbor_left(self, tile_position):
        if ((tile_position % self.dimension) != 0):
            left = self.tileat(tile_position - 1)
        else:
            left = "Edge"
        return left

    def tile_neighbors(self, tile):
        tile_position = self.tiles.index(tile)

        above = self.position_neighbor_above(tile_position)
        right = self.position_neighbor_right(tile_position)
        below = self.position_neighbor_below(tile_position)
        left = self.position_neighbor_left(tile_position)
        return [above, right, below, left]

    def is_move_valid(self, tile):
        # make sure there empty spot is a neighbor
        return (None in self.tile_neighbors(tile))

    @staticmethod
    def numbers(tile_config):
        # get a list of just the numbers in the tile config, sorted
        numbers = list(filter(lambda item: type(item) is int, tile_config))
        numbers.sort()
        return numbers

    @staticmethod
    def valid(tile_config):
        # error out if the number of items in the list is too small
        # or if it's not a square
        is_at_least_2_square = (len(tile_config) >= 4) & (sqrt(len(tile_config)).is_integer())
        if not is_at_least_2_square:
            return False

        # error out if there is not one and only one blank space
        numbers = Board.numbers(tile_config)
        has_one_space = (len(tile_config) - len(numbers) == 1)
        if not has_one_space:
            return False

        # detect if the tiles are not a set of sequential numbers
        numbers.sort()
        has_sequential_numbers = True
        for num, tile in enumerate(numbers, start = 1):
            if tile != num:
                has_sequential_numbers = False

        return has_sequential_numbers

