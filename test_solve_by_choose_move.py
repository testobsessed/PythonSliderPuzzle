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

def test_solver_can_solve_a_hard_3x3_requiring_many_moves():
    # it's just one example but shows the current algo CAN do a complex 3x3
    player = Solver([5, 8, 4, 3, None, 2, 7, 1, 6])
    player.solve()
    assert player.board.solved()

def test_solver_can_handle_reddit_puzzles():
    # see
    # https://www.reddit.com/r/dailyprogrammer/comments/62ktmx/20170331_challenge_308_hard_slider_game_puzzle/
    # for original
    puzzle1 = Solver([None, 1, 2, 4, 8, 3, 7, 6, 5])
    puzzle1.solve()
    assert puzzle1.board.solved()
    assert len(puzzle1.moves) == 8

    puzzle2 = Solver([1, 8, 2, None, 4, 3, 7, 6, 5])
    puzzle2.solve()
    assert puzzle2.board.solved()
    assert len(puzzle2.moves) == 9

    puzzle3 = Solver([7, 6, 4, None, 8, 1, 2, 3, 5])
    puzzle3.solve()
    assert puzzle3.board.solved()
    # current algo takes 111 moves -- clearly something to work on
    # assert len(puzzle3.moves) == 25

def test_solver_can_solve_a_4x4():
    solver = Solver([1, 2, 3, 4, 6, 8, 7, None, 5, 9, 10, 11, 12, 13, 14, 15])
    solver.solve()
    assert solver.board.solved()

def test_solver_can_solve_random_sampling_of_valid_3x3s():
    # it is generally suboptimal to have random tests
    # however the set of all valid 3x3s is too big (181439)
    # note also that this test can never fail (no asserts) and
    # is for information only.
    print("\n\nThe following trials provide insight into the efficiency of the current algorithm...")
    random.seed()
    boards = random.sample(Board.get_boards(3), 20)
    for board in boards:
        player = Solver(board[:])
        player.solve()
        if (player.board.solved()):
            print("Solved {} in {} moves.".format(board, len(player.moves)))
        else:
            print("Unable to solve {} after {} moves".format(board, len(player.moves)))

# known problematic boards:
# [8, 7, 2, None, 1, 4, 6, 5, 3] took 249 moves
# [None, 4, 7, 6, 8, 5, 2, 1, 3] took 344 moves
# [5, None, 7, 3, 2, 1, 8, 4, 6] took 267 moves
# [2, 7, 1, 5, 6, None, 3, 4, 8] took 241 moves
# [5, 6, 4, 7, None, 2, 8, 3, 1] took 260 moves

# Not solved in > 500 moves:
# [1, None, 2, 5, 3, 6, 4, 8, 7]
# [1, 2, None, 4, 3, 5, 8, 7, 6]
# [1, 2, None, 5, 3, 6, 4, 8, 7]
# [1, 2, 3, None, 4, 6, 8, 7, 5]
# [1, 2, 3, 6, 8, 4, None, 7, 5]
# [1, 2, 4, 3, 5, 6, 8, None, 7]
# [1, 2, 4, 3, 5, 6, 8, 7, None]
# [1, 3, 2, 4, 5, 6, 8, 7, None]
# [1, 6, 3, 5, None, 2, 4, 8, 7]
# [4, 2, 1, 3, 6, 5, 8, 7, None]
# [4, 2, 1, 3, 6, 5, 8, None, 7]
# [4, 2, 1, 3, 5, 6, 7, 8, None]
# [7, 8, 1, None, 5, 3, 4, 6, 2]
