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
    paths = player.find_paths()
    assert paths == [[1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2], [3]]

def test_find_shortest_path():
    player = Solver([1, 2, None, 3])
    assert player.find_shortest_path() == [3]

def test_solver_can_solve_all_valid_2x2s():
    boards = Board.get_boards(2)
    for board in boards:
        player = Solver(board)
        player.solve()
        assert player.board.solved()

def test_solver_can_solve_a_3x3_requiring_1_move():
    player = Solver([1, 2, 3, 4, 5, 6, 7, None, 8])
    player.solve()
    assert player.board.solved()

# def test_solver_can_solve_a_3x3_requiring_5_moves():
#     player = Solver([1, 2, 3, 4, 6, 8, 7, None, 5])
#     player.solve()
#     assert player.board.solved()
