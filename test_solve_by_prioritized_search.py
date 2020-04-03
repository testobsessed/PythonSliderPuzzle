from solve_by_prioritized_search import Solver
from slider_game import Board
import pytest

def test_solver_has_board():
    player = Solver([1,2,3,None])
    assert isinstance(player.board, Board)

def test_solver_chooses_the_move_that_solves_game():
    player = Solver([1, 2, None, 3])
    player.solve()
    assert player.board.solved()

def test_solver_can_solve_a_game_requiring_rotation():
    player = Solver([1, None, 3, 2])
    player.solve()
    assert player.board.solved()

def test_find_paths_gives_up_on_longer_solution():
    player = Solver([1, 2, None, 3])
    paths = player.find_all_paths_from_point([1, 2, None, 3], [], [], [])
    assert paths == [[3], [1, "L"]]

# def test_find_shortest_path():
#     player = Solver([1, 2, None, 3])
#     shortest_path = player.find_shortest_path()
#     assert shortest_path == [3]

def test_2x2_with_3_out_of_place_solved_in_1_move():
    player = Solver([1, 2, None, 3])
    assert player.solve()
    assert player.shortest_solution == [3]

def test_2x2_with_2_out_of_place_solved_in_1_move():
    player = Solver([1, None, 3, 2])
    assert player.solve()
    assert player.shortest_solution == [2]

def test_2x2_with_1_out_of_place_solved_in_2_moves():
    player = Solver([None, 2, 1, 3])
    assert player.solve()
    assert player.shortest_solution == [1, 3]

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
    assert len(paths) == 4
    assert [5, "X"] in paths
    assert [4, "X"] in paths
    assert [8, "X"] in paths
    assert [2, "X"] in paths

def test_find_all_paths_ignores_undo_moves():
    config = [1, 2, 3, 4, 5, 6, 7, None, 8]
    mock_visited_states = [
        [1, 2, 3, 4, None, 6, 7, 5, 8]
    ]
    previous_moves = [7]
    player = Solver(config)
    paths = player.find_all_paths_from_point(config, previous_moves, mock_visited_states, [])
    assert paths == [
        [7, 8],
        [7, 5, "L"]
    ]

def test_solver_can_solve_a_3x3_when_8_out_of_place():
    player = Solver([1, 2, 3, 4, 5, 6, 7, None, 8])
    player.solve()
    assert player.shortest_solution == [8]
    assert player.board.solved()

def test_solver_can_solve_a_3x3_when_6_out_of_place():
    player = Solver([1, 2, 3, 4, 5, None, 7, 8, 6])
    player.solve()
    assert player.shortest_solution == [6]
    assert player.board.solved()

def test_can_solve_a_3x3_requiring_2_moves():
    player = Solver([1, 2, 3, 4, 5, 6, None, 7, 8])
    player.solve()
    assert player.shortest_solution == [7, 8]
    assert player.board.solved()

def test_can_solve_a_3x3_requiring_4_moves():
    player = Solver([None, 1, 2, 4, 5, 3, 7, 8, 6])
    player.solve()
    assert player.shortest_solution == [1, 2, 3, 6]
    assert player.board.solved()

def test_can_solve_a_3x3_with_a_hole_in_the_middle():
    player = Solver([1, 2, 3, 4, None, 5, 7, 8, 6])
    player.solve()
    assert player.shortest_solution == [5, 6]
    assert player.board.solved()

def test_solver_can_solve_a_3x3_requiring_5_moves():
    player = Solver([1, 2, 3, 4, 6, 8, 7, None, 5])
    player.solve()
    assert player.shortest_solution == [5, 8, 6, 5, 8]
    assert player.board.solved()

def test_solver_can_solve_a_3x3_requiring_10_moves():
    player = Solver([5, 1, 2, 4, 6, 3, None, 7, 8])
    player.solve()
    print("I solved it in {} moves!\n{}".format(len(player.solution_path), player.solution_path))
    assert player.board.solved()

def test_solver_can_handle_reddit_puzzle_1():
    # see
    # https://www.reddit.com/r/dailyprogrammer/comments/62ktmx/20170331_challenge_308_hard_slider_game_puzzle/
    # for original puzzles for next 3 tests
    puzzle = Solver([None, 1, 2, 4, 8, 3, 7, 6, 5])
    puzzle.solve()
    assert puzzle.board.solved()
    assert puzzle.shortest_solution == [1, 2, 3, 5, 6, 8, 5, 6]

def test_solver_can_handle_reddit_puzzle_2():
    puzzle = Solver([1, 8, 2, None, 4, 3, 7, 6, 5])
    puzzle.solve()
    assert puzzle.board.solved()
    assert puzzle.shortest_solution == [4, 8, 2, 3, 5, 6, 8, 5, 6]

def test_solver_can_find_path_from_partially_solved_reddit_puzzle():
    # puzzle [7, 6, 4, None, 8, 1, 2, 3, 5]
    # after moves [ 7, 6, 4, 1]
    puzzle = Solver([6, 4, 1, 7, 8, None, 2, 3, 5])
    puzzle.solve()
    print("I solved it in {} moves!\n{}".format(len(puzzle.solution_path), puzzle.solution_path))
    assert puzzle.board.solved()

def test_solver_can_find_path_from_partially_solved_reddit_puzzle2():
    # puzzle [7, 6, 4, None, 8, 1, 2, 3, 5]
    # after moves [7, 6, 4, 1, 8, 3, 5, 8, 3, 4]
    puzzle = Solver([6, None, 1, 7, 4, 3, 2, 5, 8])
    puzzle.solve()
    print("I solved it in {} moves!\n{}".format(len(puzzle.solution_path), puzzle.solution_path))
    assert puzzle.board.solved()

def test_solver_can_find8_path_from_partially_solved_reddit_puzzle3():
    # puzzle [7, 6, 4, None, 8, 1, 2, 3, 5]
    # after moves [7, 6, 4, 1, 8, 3, 5, 8, 3, 4, 1, 3, 4, 7, 2, 5]
    puzzle = Solver([6, 1, 3, 2, 7, 4, 5, None, 8])
    puzzle.solve()
    print("I solved it in {} moves!\n{}".format(len(puzzle.solution_path), puzzle.solution_path))
    assert puzzle.board.solved()

def test_solver_can_find_path_from_partially_solved_reddit_puzzle():
    puzzle = Solver([6, 4, 1, 7, 8, None, 2, 3, 5])
    puzzle.solve()
    print("I solved it in {} moves!\n{}".format(len(puzzle.solution_path), puzzle.solution_path))
    assert puzzle.board.solved()

def test_solver_can_handle_reddit_puzzle_3():
    puzzle = Solver([7, 6, 4, None, 8, 1, 2, 3, 5])
    puzzle.solve()
    print("I solved it in {} moves!\n{}".format(len(puzzle.solution_path), puzzle.solution_path))
    assert puzzle.board.solved()
    # original algo in choose move solution took 111 moves
    # rowcol score add yields 449 moves
    # multiply yields 261 moves
    # manually the shortest path I've found to date is 38 moves:
    # [ 7, 6, 4, 1, 5, 3, 8, 5, 3, 8, 2, 7, 6, 4, 1, 3, 5, 2, 7,
    #   6, 4, 1, 2, 4, 5, 8, 7, 6, 4, 5, 6, 7, 8, 6, 5, 4, 7, 8 ]
    # Still searching for a solution that's just 25 moves
    # UPDATE! Found it through a brute force search.
    # [8, 6, 4, 1, 6, 3, 5, 6, 3, 5, 2, 8, 7, 4, 1, 3, 5, 2, 8, 7, 4, 1, 2, 5, 6]
    #assert len(puzzle.solution_path) == 25

def test_can_count_0_inversions():
    tiles = [1,2,3,4,5,6,7,None,8]
    assert 0 == Solver(tiles).count_inversions(tiles)

def test_can_count_1_inversion():
    tiles = [1, 2, 3, 4, 5, 6, 8, 7, None]
    assert 1 == Solver(tiles).count_inversions(tiles)

def test_can_count_2_inversions():
    tiles = [1, 2, 3, 4, 5, 8, 6, 7, None]
    assert 2 == Solver(tiles).count_inversions(tiles)

def test_can_count_0_positional_delta():
    tiles = [1, 2, 3, None]
    assert Solver(tiles).count_delta_from_position(tiles) == 0

def test_can_count_2_positional_delta():
    tiles = [1, 2, None, 3]
    assert Solver(tiles).count_delta_from_position(tiles) == 1

def test_can_count_0_rowcol_delta():
    tiles = [1, 2, 3, None]
    assert Solver(tiles).count_delta_from_rowcol(tiles) == 0

def test_can_count_2_rowcol_delta():
    tiles = [1, 2, None, 3]
    assert Solver(tiles).count_delta_from_rowcol(tiles) == 2

def test_should_choose_move_worst_positioned_tile():
    tiles = [1, 8, 2, 4, None, 3, 7, 6, 5]
    solver = Solver(tiles)
    possibilities = solver.lookahead(tiles)
    move_scores = solver.prioritize(possibilities)
    move_priorities = sorted(move_scores, key=move_scores.get)
    assert move_priorities[0] == 8

def test_can_get_available_moves():
    puzzle = Solver([1, None, 3, 2])
    assert puzzle.get_available_moves_from([1, None, 3, 2]) == [1, 2]

def test_can_provide_lookahead():
    puzzle = Solver([1, None, 3, 2])
    assert puzzle.lookahead([1, None, 3, 2]) == {1: [None, 1, 3, 2], 2: [1, 2, 3, None]}

def test_score_neighbors_all_in_order():
    tiles = [1,2,3,None]
    assert Solver(tiles).count_delta_from_neighbor(tiles) == 6

def test_score_neighbors_jumbled():
    tiles = [7, 6, 4, None, 8, 1, 2, 3, 5]
    assert Solver(tiles).count_delta_from_neighbor(tiles) == 54




