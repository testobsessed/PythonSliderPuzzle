from solve_by_walk_paths import Solver
from slider_game import Board
import pytest

def test_solver_has_board():
    player = Solver([1,2,3,None])
    assert isinstance(player.board, Board)

# def test_solver_chooses_the_move_that_solves_game():
#     player = Solver([1, 2, None, 3])
#     player.solve()
#     assert player.board.solved()
#
# def test_solver_can_solve_a_game_requiring_rotation():
#     player = Solver([1, None, 3, 2])
#     player.solve()
#     assert player.board.solved()

def test_find_paths_can_map_solutions():
    player = Solver([1, 2, None, 3])
    paths = player.find_all_paths_from_point([1, 2, None, 3], [], [], [])
    assert paths == [[1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2], [3]]

def test_find_shortest_path():
    player = Solver([1, 2, None, 3])
    shortest_path = player.find_shortest_path()
    assert shortest_path == [3]

def test_2x2_with_3_out_of_place_solved_in_1_move():
    player = Solver([1, 2, None, 3])
    assert player.solve()
    assert player.solution_path == [3]

def test_2x2_with_2_out_of_place_solved_in_1_move():
    player = Solver([1, None, 3, 2])
    assert player.solve()
    assert player.solution_path == [2]

def test_2x2_with_1_out_of_place_solved_in_2_moves():
    player = Solver([None, 2, 1, 3])
    assert player.solve()
    assert player.solution_path == [1, 3]

def test_2x2_requires_multiple_moves():
    assert Solver([2, 3, 1, None]).solve()
    assert Solver([None, 3, 2, 1]).solve()

def test_solver_can_solve_all_valid_2x2s():
    boards = Board.get_boards(2)
    for board in boards:
        assert Solver(board).solve()

def test_find_all_paths_eliminates_circular_paths():
    config = [1, 2, 3, 4, None, 5, 7, 8, 6]
    mock_visited_states = [
        [1, None, 3, 4, 2, 5, 7, 8, 6],
        [1, 2, 3, None, 4, 5, 7, 8, 6],
        [1, 2, 3, 4, 5, None, 7, 8, 6],
        [1, 2, 3, 4, 8, 5, 7, None, 6]
    ]
    player = Solver(config)
    paths = player.find_all_paths_from_point(config, [], mock_visited_states, [])
    assert paths == [
        [2, "X"],
        [4, "X"],
        [5, "X"],
        [8, "X"]
    ]

def test_find_all_paths_ignores_undo_moves():
    config = [1, 2, 3, 4, 5, 6, 7, None, 8]
    mock_visited_states = [
        [1, 2, 3, 4, None, 6, 7, 5, 8]
    ]
    previous_moves = [7]
    player = Solver(config)
    paths = player.find_all_paths_from_point(config, previous_moves, mock_visited_states, [])
    assert paths == [
        [7, 5, "X"],
        [7, 8]
    ]

def test_solver_can_solve_a_3x3_when_8_out_of_place():
    player = Solver([1, 2, 3, 4, 5, 6, 7, None, 8])
    player.solve()
    assert player.solution_path == [8]
    assert player.board.solved()

def test_solver_can_solve_a_3x3_when_6_out_of_place():
    player = Solver([1, 2, 3, 4, 5, None, 7, 8, 6])
    player.solve()
    assert player.solution_path == [6]
    assert player.board.solved()

def test_can_solve_a_3x3_requiring_2_moves():
    player = Solver([1, 2, 3, 4, 5, 6, None, 7, 8])
    player.solve()
    assert player.solution_path == [7, 8]
    assert player.board.solved()

def test_can_solve_a_3x3_requiring_4_moves():
    player = Solver([None, 1, 2, 4, 5, 3, 7, 8, 6])
    player.solve()
    for path in player.all_paths:
        print("---> {}".format(path))
    assert player.solution_path == [1, 2, 3, 6]
    assert player.board.solved()

# def test_can_solve_a_3x3_with_a_hole_in_the_middle():
#     player = Solver([1, 2, 3, 4, None, 5, 7, 8, 6])
#     player.solve()
#     for path in player.all_paths:
#         print("---> {}".format(path))
#     assert player.solution_path == [5, 6]
#     assert player.board.solved()

# def test_can_solve_a_3x3_requiring_2_moves():
#     player = Solver([1, 2, 3, 4, 5, 6, None, 7, 8])
#     player.solve()
#     assert player.solution_path == [7, 8]
#     assert player.board.solved()

def test_solver_can_solve_a_3x3_requiring_5_moves():
    player = Solver([1, 2, 3, 4, 6, 8, 7, None, 5])
    player.solve()
    assert player.board.solved()

def test_solver_can_handle_reddit_puzzles():
    # see
    # https://www.reddit.com/r/dailyprogrammer/comments/62ktmx/20170331_challenge_308_hard_slider_game_puzzle/
    # for original
    puzzle1 = Solver([None, 1, 2, 4, 8, 3, 7, 6, 5])
    puzzle1.solve()
    for path in puzzle1.all_paths:
        print("---> {}".format(path))
    assert puzzle1.board.solved()
    assert len(puzzle1.solution_path) == 8

    puzzle2 = Solver([1, 8, 2, None, 4, 3, 7, 6, 5])
    puzzle2.solve()
    assert puzzle2.board.solved()
    assert len(puzzle2.solution_path) == 9

    puzzle3 = Solver([7, 6, 4, None, 8, 1, 2, 3, 5])
    puzzle3.solve()
    assert puzzle3.board.solved()
    # current algo takes 111 moves -- clearly something to work on
    # assert len(puzzle3.moves) == 25
