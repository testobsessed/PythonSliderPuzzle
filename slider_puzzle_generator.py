from slider_game import Board
class Generator:
    def __init__(self, dimension):
        self.dimension = dimension
        solution = []
        for num in range(1, dimension**2):
            solution.append(num)
        solution.append(None)
        self.starting_state = solution
        self.board = Board(solution)

    def inmoves(self, num_moves):
        paths = []
        check_states = {
            0: [
                [self.starting_state, []]
            ]
        }
        for depth in range(num_moves):
            at_depth = (depth == num_moves - 1)
            check_states[depth+1] = []
            for state in check_states[depth]:
                if at_depth:
                    paths.extend(self.get_next_paths_from_state(state[0], state[1]))
                else:
                    check_states[depth+1].extend(self.get_next_paths_from_state(state[0], state[1]))

        return paths

    def get_next_paths_from_state(self, tiles, path_to_state):
        self.board.tiles = tiles
        paths = []
        lookahead = self.board.lookahead()
        for move in lookahead:
            if (len(path_to_state) == 0):
                paths.append([lookahead[move], [move]])
            elif (path_to_state[-1] != move):
                paths.append([lookahead[move], path_to_state + [move]])
        return paths