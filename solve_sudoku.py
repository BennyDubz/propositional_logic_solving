from display import display_sudoku_solution
from datetime import datetime
import random, sys
from SAT import SAT

if __name__ == "__main__":
    # for testing, always initialize the pseudorandom number generator to output the same sequence
    #  of values:
    random.seed(1)
    puzzle_name = "rows"
    # puzzle_name = str(sys.argv[1][:-4])
    puzzle_path = "./puzzles/" + puzzle_name + ".cnf"
    sol_filename = "./solutions/" + puzzle_name + ".sol"

    sat = SAT(puzzle_path)
    start = datetime.now()
    result = sat.gsat_solver()
    #result = sat.walksat_solver()
    end = datetime.now()
    print("Time elapsed: ", end - start)
    print(result)

    if result:
        sat.write_solution(result, sol_filename)
        display_sudoku_solution(sol_filename)