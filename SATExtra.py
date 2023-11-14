import random
from collections import deque
from SAT import SAT

# Author: Ben Williams '25
# Date: October 21st, 2023


class SATExtra(SAT):
    def __init__(self, cnf_file, all_constants=True):
        super(SATExtra, self).__init__(cnf_file)
        self.constants = self.get_single_var_constants()
        if all_constants:
            self.add_implied_constants()
        print("All constants", self.constants)
        print(f'Total of {len(self.constants)} constants out of {len(self.variables) - 1} variables')

    # Find all the variables that are constants, only from constraints that
    #   have one variable in them.
    #   Returns a set of variables
    def get_single_var_constants(self):
        new_constants = set()
        for clause in self.clauses:
            if len(clause) == 1:
                new_constants.add(list(clause)[0])
        return new_constants

    # Done after we get the easy constants. Use the constants to infer which other variables
    #   MUST be either True or False. We maintain a queue of clauses to look at
    def add_implied_constants(self):
        queue = deque()
        # Would like to use a set here for efficiency, but we can't hash other sets into this set so a list is
        #   the best we can do
        fully_evaluated_clauses = []

        # Create the queue of clauses related to the original constants to examine first
        for clause in self.clauses:
            for var in clause:
                if var in self.constants or (-1 * var) in self.constants:
                    queue.append(clause)

        while len(queue) > 0:
            clause = queue.popleft()
            non_constant_var = None
            two_non_constants = False
            # Check clause to see if there is only one variable that is not a constant
            for var in clause:
                if var not in self.constants and (-1 * var) not in self.constants:
                    # If there are two undefined variables, we cannot reason about them
                    if non_constant_var:
                        two_non_constants = True
                        break
                    non_constant_var = var

            # If there is only one undefined variable
            if not two_non_constants and non_constant_var:
                self.constants.add(non_constant_var)
                # Do not visit this clause again
                fully_evaluated_clauses.append(clause)
                for other_clause in self.clauses:
                    if non_constant_var in other_clause or (-1 * non_constant_var) in other_clause:
                        if other_clause not in fully_evaluated_clauses:
                            queue.append(other_clause)

    # A slightly modified walksat that does not change any of the constants
    # Parameter: h - Randomly flip a variable in an unsatisfied clause with probability h. 0 <= h <= 1
    # Parameter: max_steps - The maximum number of assignments we will try before giving up
    def walksat_solver(self, h=0.3, max_steps=100000):
        # Generate a completely random assignment
        assignment = [(True if random.random() < 0.5 else False) for i in range(len(self.variables) - 1)]
        # Now go through all the constants and manually set those in the assignment
        for constant in self.constants:
            if constant < 0:
                assignment[abs(constant) - 1] = False
            else:
                assignment[constant - 1] = True
        steps = 0

        while not self.is_valid_assignment(assignment):
            steps += 1
            if steps > max_steps:
                print(f'Maximum steps of {max_steps} taken in Walksat solver')
                return None, steps

            # Uncomment this to see how the algorithm gets stuck at local minima
            # if steps % 1000 == 0:
            #     print(steps, assignment)

            # Get the random unsatisfied clause
            unsatisfied_clause = self.get_unsatisfied_clause(assignment)

            # Chance to randomly flip a variable in the clause
            if random.random() > 1 - h:
                flip_var = abs(random.choice(list(unsatisfied_clause)))
                # Do not flip a constant
                while flip_var in self.constants or (-1 * flip_var) in self.constants:
                    flip_var = abs(random.choice(list(unsatisfied_clause)))
                assignment[flip_var - 1] = not assignment[flip_var - 1]
                continue

            # Otherwise, pick the best variable and flip it
            var_candidates = [abs(var) for var in unsatisfied_clause]
            flip_var = self.get_best_flip(assignment, var_candidates)
            assignment[flip_var - 1] = not assignment[flip_var - 1]

        print("Total steps:", steps)
        # Uncomment if doing looped testing and want to calculate how many steps are taken on average
        return assignment#, steps

    # A modified version of getting the best variable to flip that ignores constants
    def get_best_flip(self, assignment, var_list=None):
        best_score = -1
        best_vars = []

        # This will be the case for gsat, but we supply a var_list for walksat
        if not var_list:
            var_list = range(1, len(self.variables))

        for var in var_list:
            if var in self.constants or (-1 * var) in self.constants:
                continue
            score = self.get_score(var, assignment)
            if score > best_score:
                best_score = score
                best_vars = [var]
                continue
            elif score == best_score:
                best_vars.append(var)

        # Return a random variable of the best variables
        # print(best_score, len(best_vars), best_vars)
        return random.choice(best_vars)


if __name__ == "__main__":
    random.seed(1)
    puzzle_1_test = SATExtra("./puzzles/puzzle1.cnf")
    result = puzzle_1_test.walksat_solver()
    print(result)





