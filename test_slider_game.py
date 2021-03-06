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

def test_board_can_count_0_inversions():
    assert 0 == Board([1,2,3,4,5,6,7,None,8]).inversions

def test_board_can_count_1_inversion():
    assert 1 == Board([1, 2, 3, 4, 5, 6, 8, 7, None]).inversions

def test_board_can_count_2_inversions():
    assert 2 == Board([1, 2, 3, 4, 5, 8, 6, 7, None]).inversions

def test_board_can_tell_if_a_3x3_config_is_solvable():
    assert Board([1, 2, 3, 4, 5, 6, 7, 8, None]).is_solvable()

def test_board_can_tell_if_a_3x3_config_is_not_solvable():
    assert not Board([1, 2, 3, 4, 5, 6, 8, 7, None]).is_solvable()

def test_board_can_tell_if_a_2x2_config_is_solvable():
    puzzle = Board([1, None, 3, 2])
    assert puzzle.is_solvable()

def test_board_can_tell_if_a_2x2_config_is_not_solvable():
    assert not Board([1, None, 2, 3]).is_solvable()
    assert not Board([1, 3, 2, None]).is_solvable()

def test_board_can_report_delta_to_solution():
    assert Board([1, 2, 3, None]).delta_from_solution() == 0
    assert Board([1, 2, None, 3]).delta_from_solution() == 1

def test_board_can_provide_lookahead():
    puzzle = Board([1, None, 3, 2])
    assert puzzle.lookahead() == {1: [None, 1, 3, 2], 2: [1, 2, 3, None]}

def test_board_can_list_available_moves():
    puzzle = Board([1, None, 3, 2])
    assert puzzle.available_moves() == [1,2]

def test_board_can_report_diff_score_to_possible_new_state():
    puzzle = Board([1, None, 3, 2])
    assert puzzle.solution_diff_score_from([None, 1, 3, 2]) == 3

def test_board_can_generate_all_valid_2x2_permutations():
    puzzles = Board.get_boards(2)
    assert [1, 2, 3, None] not in puzzles # does not include solution
    assert[1, 3, 2, None] not in puzzles # does not include invalid config
    assert [1, 2, None, 3] in puzzles # does include a known valid config
    for puzzle in puzzles:
        assert Board.valid(puzzle) # and all the others are valid

def test_board_can_generate_all_2d_permutations():
    assert sorted(Board.get_permutations([1, 2])) == [[1, 2], [2, 1]]

def test_board_can_generate_all_2x2_permutations():
    assert Board.get_permutations([1, 2, 3, None]) == [
        [1, 2, 3, None],
        [1, 2, None, 3],
        [1, 3, 2, None],
        [1, 3, None, 2],
        [1, None, 2, 3],
        [1, None, 3, 2],
        [2, 1, 3, None],
        [2, 1, None, 3],
        [2, 3, 1, None],
        [2, 3, None, 1],
        [2, None, 1, 3],
        [2, None, 3, 1],
        [3, 1, 2, None],
        [3, 1, None, 2],
        [3, 2, 1, None],
        [3, 2, None, 1],
        [3, None, 1, 2],
        [3, None, 2, 1],
        [None, 1, 2, 3],
        [None, 1, 3, 2],
        [None, 2, 1, 3],
        [None, 2, 3, 1],
        [None, 3, 1, 2],
        [None, 3, 2, 1]
    ]