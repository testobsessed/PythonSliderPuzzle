from slider_puzzle_generator import Generator
from slider_game import Board
import pytest

def test_generator_has_board():
    assert isinstance(Generator(2).board, Board)

def test_generator_board_is_solved():
    assert Generator(2).board.tiles == [ 1, 2, 3, None]

def test_can_generate_3x3_boards_1_move_from_solved():
    results = Generator(3).inmoves(1)
    assert len(results) == 2
    assert [[1, 2, 3, 4, 5, 6, 7, None, 8], [8]] in results
    assert [[1, 2, 3, 4, 5, None, 7, 8, 6], [6]] in results

def test_can_generate_3x3_boards_2_moves_from_solved():
    results = Generator(3).inmoves(2)
    assert len(results) == 4
    assert [[ 1, 2, 3, 4, 5, 6, None, 7, 8 ], [8, 7]] in results
    assert [[ 1, 2, 3, 4, None, 6, 7, 5, 8 ], [8, 5]] in results
    assert [[ 1, 2, 3, 4, None, 5, 7, 8, 6 ], [6, 5]] in results
    assert [[ 1, 2, None, 4, 5, 3, 7, 8, 6 ], [6, 3]] in results

def test_can_generate_3x3_boards_3_moves_from_solved():
    results = Generator(3).inmoves(3)
    assert len(results) == 0
    assert [[ 1, None, 2, 4, 5, 3, 7, 8, 6], []] in results

def test_get_next_paths_from_state():
    paths = Generator(3).get_next_paths_from_state([ 1, 2, 3, 4, 5, 6, 7, 8, None ], [])
    assert len(paths) == 2
    assert [[1, 2, 3, 4, 5, 6, 7, None, 8], [8]] in paths
    assert [[1, 2, 3, 4, 5, None, 7, 8, 6], [6]] in paths

def test_iterate_to_solution():
    results = Generator(3).inmoves(25)
    counter = 0
    solution = None
    print("\n*********************************\nGENERATED {} RESULTS\n".format(len(results)))
    example = results[6792]
    print("\nExample result\n   board {}\n   solution{}".format(example[0], example[1]))
    for item in results:
        counter += 1
        if item[0] == [7, 6, 4, None, 8, 1, 2, 3, 5]:
            solution = item[1]
            break
    if (solution != None):
        print("\n\nFOUND IT AFTER CHECKING {} RESULTS!\n   {}".format(counter, solution))
    else:
        print("\n\nTHEY LIED. Searched {} results and found nothing.".format(counter))

def test_all_2x2s():
    print("\n")
    all_valid_boards = Board.get_boards(2)
    generated_solutions = [
        [[ 1, 2, 3, None], []]
    ]
    for move_count in range(1, 10):
        generated_solutions.extend(Generator(2).inmoves(move_count))
    # for thing in solutions:
    #     print(solutions[thing])
    for board in all_valid_boards:
        solved = None
        for solution in generated_solutions:
            if (solution[0] == board):
                if (solved == None or len(solved) > len(solution[1])):
                    solved = solution[1]
                    solved.reverse()
        print("Puzzle {} solution {}".format(board, solved))

def test_all_3x3s():
    print("\n")
    all_valid_boards = Board.get_boards(3)
    generated_solutions = [
        [[ 1, 2, 3, 4, 5, 6, 7, 8, None], []]
    ]
    solved_in_10 = []
    not_solved_in_10 = []
    for move_count in range(1, 25):
        generated_solutions.extend(Generator(3).inmoves(move_count))
    # for thing in solutions:
    #     print(solutions[thing])
    for board in all_valid_boards:
        solved = None
        for solution in generated_solutions:
            if (solution[0] == board):
                if (solved == None or len(solved) > len(solution[1])):
                    solved = solution[1]
                    solved.reverse()
                    break
        if (solved != None):
            solved_in_10.append([board, solved])
        else:
            not_solved_in_10.append(board)

        # print("Puzzle {} solution {}".format(board, solved))
    print("Count of valid 3x3s = {}".format(len(all_valid_boards)))
    print("Solved in 100 moves or less = {}".format(len(solved_in_10)))
    print("Remaining boards = {}".format(len(not_solved_in_10)))

    # Count of valid 3x3s = 181439
    # Solved in 20 moves or less = 37808
    # Remaining boards = 143631