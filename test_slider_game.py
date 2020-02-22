from slider_game import Board
import pytest

def test_board_init():
    puzzle = Board()
    assert isinstance(puzzle.tiles, list)

def test_default_board():
    puzzle = Board()
    assert puzzle.tiles == [1, 2, 3, 4, 5, 6, 7, 8, None]

def test_board_init_takes_starting_state():
    puzzle = Board([3, 2, 1, 4, 5, 6, 7, 8, None])
    assert puzzle.tileat(0) == 3

def test_board_knows_dimensions():
    puzzle = Board([3, 2, 1, 4, 5, 6, 7, 8, None])
    assert puzzle.dimension == 3

def test_board_converts_position_to_rowcol():
    puzzle = Board()
    assert puzzle.rowcol(0) == [0, 0]
    assert puzzle.rowcol(1) == [0, 1]
    assert puzzle.rowcol(2) == [0, 2]
    assert puzzle.rowcol(3) == [1, 0]
    assert puzzle.rowcol(4) == [1, 1]
    assert puzzle.rowcol(5) == [1, 2]
    assert puzzle.rowcol(6) == [2, 0]
    assert puzzle.rowcol(7) == [2, 1]
    assert puzzle.rowcol(8) == [2, 2]

def test_board_can_find_row_col_of_tile():
    puzzle = Board([2, 3, 1, None])
    assert puzzle.rowcol_of_tile(2) == [0,0]
    assert puzzle.rowcol_of_tile(3) == [0,1]
    assert puzzle.rowcol_of_tile(1) == [1,0]
    assert puzzle.rowcol_of_tile(None) == [1, 1]

def test_board_knows_0_tiles_is_not_valid():
    assert not Board().valid([])

def test_board_knows_1_tile_is_not_valid():
    assert not Board().valid([1])

def test_board_knows_4_tiles_is_valid():
    assert Board().valid([1, 2, 3, None])

def test_board_knows_9_tiles_is_valid_regardless_of_order():
    assert Board().valid([3, 2, 1, 8, 5, 6, 7, 4, None])

def test_board_knows_8_tiles_is_not_valid():
    assert not Board().valid([1, 2, 3, 4, 5, 6, 7, None])

def test_board_knows_when_there_is_no_space():
    assert not Board().valid([1, 2, 3, 4])

def test_board_knows_when_there_is_more_than_one_space():
    assert not Board().valid([1, 2, None, None])

def test_board_knows_when_tiles_numbers_are_not_sequential():
    assert not Board().valid([1, 5, 2, None])

def test_board_init_throws_error_if_board_too_small():
    with pytest.raises(RuntimeError) as excinfo:
        puzzle = Board([0, None])
    assert 'Tile configuration invalid' in str(excinfo.value)

def test_board_init_throws_error_if_tiles_not_sequential():
    with pytest.raises(RuntimeError) as excinfo:
        puzzle = Board([3, 5, 6, None])
    assert 'Tile configuration invalid' in str(excinfo.value)

def test_board_init_throws_error_if_board_has_no_space():
    with pytest.raises(RuntimeError) as excinfo:
        puzzle = Board([1,2,3,4])
    assert 'Tile configuration invalid' in str(excinfo.value)

def test_board_has_a_solution():
    puzzle = Board([1,3,2,None])
    assert puzzle.solution == [1,2,3,None]

def test_board_can_tell_when_solved():
    puzzle = Board([1,2,3,None])
    assert puzzle.solved()

def test_board_can_tell_when_not_solved():
    puzzle = Board([2,3,1,None])
    assert not puzzle.solved()

def test_board_knows_where_the_blank_is():
    puzzle = Board([2,3,1,None])
    assert puzzle.blank_position == 3

def test_board_can_move_piece():
    puzzle = Board([2, 3, 1, None])
    puzzle.move(3)
    assert puzzle.tiles == [2, None, 1, 3]

def test_board_knows_when_a_move_is_valid():
    puzzle = Board([2, 3, 1, None])
    assert puzzle.is_move_valid(3)

def test_board_knows_when_a_move_is_not_valid():
    puzzle = Board([2, 3, 1, None])
    assert not puzzle.is_move_valid(2)

def test_board_cannot_make_diagonal_move():
    puzzle = Board([2, 3, 1, None])
    puzzle.move(2)
    assert puzzle.tiles == [2, 3, 1, None]

def test_board_can_list_edges_as_neighbors():
    puzzle = Board([2, 3, 1, None])
    assert puzzle.tile_neighbors(2) == ["Edge", 3, 1, "Edge"]
    assert puzzle.tile_neighbors(3) == ["Edge", "Edge", None, 2]
    assert puzzle.tile_neighbors(1) == [2, None, "Edge", "Edge"]
    assert puzzle.tile_neighbors(None) == [3, "Edge", "Edge", 1]

def test_board_can_list_neighbors_for_middle_tile():
    puzzle = Board([1,2,3,4,5,6,7,None,8])
    assert puzzle.tile_neighbors(5) == [2, 6, None, 4]

def test_board_cannot_move_if_tile_surrounded():
    puzzle = Board([1,2,3,4,5,6,7,None,8])
    puzzle.move(2)
    assert puzzle.tiles == [1,2,3,4,5,6,7,None,8]

