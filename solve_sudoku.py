from display import display_sudoku_solution
from datetime import datetime
import random, sys
from SAT import SAT
from SATExtra import SATExtra

if __name__ == "__main__":
    # for testing, always initialize the pseudorandom number generator to output the same sequence
    #  of values:
    # Uncomment this if doing the loop of tests
    random.seed(1)

    puzzle_name = "puzzle1"
    # puzzle_name = str(sys.argv[1][:-4])
    puzzle_path = "./puzzles/" + puzzle_name + ".cnf"
    sol_filename = "./solutions/" + puzzle_name + ".sol"

    # sat_extra = SATExtra(puzzle_path, all_constants=True)
    sat = SAT(puzzle_path)
    start = datetime.now()
    # result = sat.gsat_solver()
    result = sat.walksat_solver()

    # Uncomment the following block if you also are returning the steps in the walksat solvers
    ##############
    # num_fail = 0
    # success_steps = 0
    # result = None
    # for i in range(10):
    #     result, steps = sat_extra.walksat_solver()
    #     #result, steps = sat.walksat_solver()
    #     if not result:
    #         num_fail += 1
    #     else:
    #         success_steps += steps
    # print("Average steps for successful solving:", success_steps / (10 - num_fail))
    # print("Total times failed:", num_fail)
    ##############

    end = datetime.now()
    print("Time elapsed: ", end - start)

    if result:
        sat.write_solution(result, sol_filename)
        # sat_extra.write_solution(result, sol_filename)
        display_sudoku_solution(sol_filename)