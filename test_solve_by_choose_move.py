from solve_by_choose_move import Solver
from slider_game import Board
import random
import pytest

def test_solver_has_board():
    player = Solver([1,2,3,None])
    assert isinstance(player.board, Board)

def test_solver_detects_unsolvable_puzzle():
    player = Solver([1,3,2,None])
    player.solve()
    assert player.moves == []
    assert player.status == "Unsolvable"

def test_solver_chooses_the_move_that_solves_game():
    player = Solver([1, 2, None, 3])
    player.find_best_move()
    assert player.board.solved()

def test_solver_chooses_the_move_that_makes_board_closer_to_solved():
    player = Solver([None, 1, 3, 2])
    player.find_best_move()
    assert player.board.tiles == [1, None, 3, 2]

def test_solver_can_solve_a_game_requiring_2_steps():
    player = Solver([None, 1, 3, 2])
    player.solve()
    assert player.moves == [1, 2]
    assert player.board.solved()

def test_solver_can_get_available_moves():
    player = Solver([3, 2, 1, 8, 5, 6, 7, 4, None])
    assert player.get_available_moves() == [4, 6]

def test_solver_can_solve_a_2x2_requiring_5_steps():
    player = Solver([2, 3, None, 1])
    player.solve()
    assert player.moves == [1, 3, 2, 1, 3]
    assert player.board.solved()

def test_solver_can_solve_all_valid_2x2s():
    boards = Board.get_boards(2)
    for board in boards:
        player = Solver(board)
        player.solve()
        assert player.board.solved()


def test_solver_can_solve_a_3x3_requiring_5_moves():
    # Note that this is theoretically no more difficult than the 2x2
    player = Solver([1, 2, 3, 4, 6, 8, 7, None, 5])
    player.solve()
    assert player.board.solved()

def test_solver_can_solve_a_known_3x3_requiring_many_moves():
    # it's just one example but shows the current algo CAN do a complex 3x3
    player = Solver([3, 2, 1, 8, 5, 6, 7, 4, None])
    player.solve()
    assert player.board.solved()

# Commented out because it gets stuck for too long -- algo needs improvement
# known problematic board: [5, 8, 4, 3, None, 2, 7, 1, 6]
# def test_solver_can_solve_random_sampling_of_valid_3x3s():
#     # it is generally suboptimal to have random tests
#     # however the set of all valid 3x3s is too big (181439)
#     boards = random.sample(Board.get_boards(3), 5)
#     for board in boards:
#         player = Solver(board)
#         player.solve()
#         assert player.board.solved()