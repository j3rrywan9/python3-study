# LC 51


class Solution:
    def solve_n_queens(self, n):
        def could_place(row, col):
            return cols[col] + hills[row - col] + dales[row + col] == 0

        def place_queen(row, col):
            cols[col] = 1
            hills[row - col] = 1
            dales[row + col] = 1
            queens.add((row, col))

        def remove_queen(row, col):
            cols[col] = 0
            hills[row - col] = 0
            dales[row + col] = 0
            queens.remove((row, col))

        def add_solution():
            solution = []

            for _, col in sorted(queens):
                solution.append('.' * col + 'Q' + '.' * (n - col - 1))

            output.append(solution)

        def backtrack(row):
            for col in range(n):
                if could_place(row, col):
                    place_queen(row, col)

                    if row + 1 == n:
                        add_solution()
                    else:
                        backtrack(row + 1)

                    remove_queen(row, col)

        cols = [0] * n
        hills = [0] * (2 * n - 1)
        dales = [0] * (2 * n - 1)
        queens = set()
        output = []

        backtrack(0)

        return output
