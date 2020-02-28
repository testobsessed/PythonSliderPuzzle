from solve_by_choose_move import SolverOptimizeForLowerInversions
from slider_game import Board
import pytest

def test_solver_has_board():
    player = SolverOptimizeForLowerInversions([1,2,3,None])
    assert isinstance(player.board, Board)

def test_solver_detects_unsolvable_puzzle():
    player = SolverOptimizeForLowerInversions([1,3,2,None])
    player.solve()
    assert player.moves == []
    assert player.status == "Unsolvable"

def test_solver_chooses_the_move_that_solves_game():
    player = SolverOptimizeForLowerInversions([1, 2, None, 3])
    player.find_best_move()
    assert player.board.solved()

def test_solver_chooses_the_move_that_makes_board_closer_to_solved():
    player = SolverOptimizeForLowerInversions([None, 1, 3, 2])
    player.find_best_move()
    assert player.board.tiles == [1, None, 3, 2]

def test_solver_can_solve_a_game_requiring_2_steps():
    player = SolverOptimizeForLowerInversions([None, 1, 3, 2])
    player.solve()
    assert player.moves == [1, 2]
    assert player.board.solved()

def test_solver_can_get_available_moves():
    player = SolverOptimizeForLowerInversions([3, 2, 1, 8, 5, 6, 7, 4, None])
    assert player.get_available_moves() == [4, 6]

def test_solver_can_solve_a_2x2_requiring_5_steps():
    player = SolverOptimizeForLowerInversions([2, 3, None, 1])
    player.solve()
    assert player.moves == [1, 3, 2, 1, 3]
    assert player.board.solved()

def test_solver_can_solve_a_3x3_requiring_5_moves():
    # Note that this is no more difficult than the 2x2
    player = SolverOptimizeForLowerInversions([1, 2, 3, 4, 6, 8, 7, None, 5])
    player.solve()
    assert player.board.solved()

def test_solver_can_solve_a_3x3_requiring_many_moves():
    player = SolverOptimizeForLowerInversions([3, 2, 1, 8, 5, 6, 7, 4, None])
    player.solve()
    assert player.board.solved()

