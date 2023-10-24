import random
# Author: Ben Williams '25
# Date: October 17th, 2023


# General propositional logic solver implementation
class SAT:
    def __init__(self, cnf_file):
        # For going to the variable given a sentence
        self.sentence_var_ref = dict()
        # For going to the sentence given a variable
        self.var_sentence_ref = dict()

        # We initialize the variables with a single index so that we do not have +- 0 in the clauses
        #   This 0 ends up being ignored
        self.variables = [0]
        self.clauses = self.get_clauses(cnf_file)

    # Parses the file to get all the clauses
    def get_clauses(self, cnf_file):
        f = open(cnf_file, "r")
        clauses = []

        # Each line is a clause
        for line in f:
            clause = set()
            # Each space represents an "or" between different sentences
            for sentence in line.split():
                # Check if it is negated
                if sentence[0] == '-':
                    # If we have not seen this sentence before
                    # We ignore the first character as it is just the negation
                    if sentence[1:] not in self.sentence_var_ref.keys():
                        self.variables.append(len(self.variables))
                        self.sentence_var_ref[sentence[1:]] = len(self.variables) - 1
                        self.var_sentence_ref[len(self.variables) - 1] = sentence[1:]
                    clause.add(-1 * self.sentence_var_ref[sentence[1:]])
                else:
                    # If we have not seen this sentence before
                    if sentence not in self.sentence_var_ref.keys():
                        self.variables.append(len(self.variables))
                        self.sentence_var_ref[sentence] = len(self.variables) - 1
                        self.var_sentence_ref[len(self.variables) - 1] = sentence
                    clause.add(self.sentence_var_ref[sentence])

            clauses.append(clause)

        f.close()
        return clauses

    # Solves and returns the solution to the propositional logic problem stored in the class
    # Parameter: h - In the solver, randomly flip an assignment with probability h. 0 <= h <= 1
    # Parameter: max_steps - The maximum number of assignments we will try before giving up
    def gsat_solver(self, h=0.1, max_steps=100000):
        # Generate a completely random assignment
        assignment = [(True if random.random() < 0.5 else False) for i in range(len(self.variables) - 1)]
        steps = 0

        while not self.is_valid_assignment(assignment):
            steps += 1
            if steps > max_steps:
                print(f'Maximum steps of {max_steps} taken in GSAT solver')
                return None

            # With some chance, randomly flip an assignment
            if random.random() > (1 - h):
                flip_index = random.randint(0, len(assignment) - 1)
                assignment[flip_index] = not assignment[flip_index]
                continue

            # Otherwise, pick the best possible variable to flip and flip it
            flip_var = self.get_best_flip(assignment)
            assignment[flip_var - 1] = not assignment[flip_var - 1]

        print("Total steps:", steps)
        return assignment

    # A faster method to find the solution to the propositional logic problem stored in the class
    # Parameter: h - Randomly flip a variable in an unsatisfied clause with probability h. 0 <= h <= 1
    # Parameter: max_steps - The maximum number of assignments we will try before giving up
    def walksat_solver(self, h=0.3, max_steps=100000):
        # Generate a completely random assignment
        assignment = [(True if random.random() < 0.5 else False) for i in range(len(self.variables) - 1)]
        steps = 0

        while not self.is_valid_assignment(assignment):
            steps += 1
            if steps > max_steps:
                print(f'Maximum steps of {max_steps} taken in Walksat solver')
                return None

            # Get the random unsatisfied clause
            unsatisfied_clause = self.get_unsatisfied_clause(assignment)

            # Chance to randomly flip a variable in the clause
            if random.random() > 1 - h:
                flip_index = abs(random.choice(list(unsatisfied_clause))) - 1
                assignment[flip_index] = not assignment[flip_index]
                continue

            # Otherwise, pick the best variable and flip it
            var_candidates = [abs(var) for var in unsatisfied_clause]
            flip_var = self.get_best_flip(assignment, var_candidates)
            assignment[flip_var - 1] = not assignment[flip_var - 1]

        print("Total steps:", steps)
        return assignment, steps

    # Returns a random unsatisfied clause given an assignment
    def get_unsatisfied_clause(self, assignment):
        unsatisfied_clauses = []

        for clause in self.clauses:
            if not self.is_clause_true(clause, assignment):
                unsatisfied_clauses.append(clause)

        return random.choice(unsatisfied_clauses)

    # Given an assignment, return True if it satisfies all clauses, False otherwise
    def is_valid_assignment(self, assignment):
        for clause in self.clauses:
            clause_satisfied = False
            for var in clause:
                var_index = abs(var) - 1
                # If the clause says this variable should be False
                if var < 0:
                    if assignment[var_index] is False:
                        clause_satisfied = True
                        # We can break out of this clause since we have satisfied at least one of the "or"s
                        break
                # If the clause says this variable should be True
                else:
                    if assignment[var_index]:
                        clause_satisfied = True
                        break
            # Clauses are a series of "or"s, so if none of them are valid, the clause is False
            if not clause_satisfied:
                return False

        return True

    # Given a current assignment that is not valid, find the best variable to flip to
    #   satisfy as many clauses as possible. It breaks ties randomly.
    def get_best_flip(self, assignment, var_list=None):
        best_score = -1
        best_vars = []

        # This will be the case for gsat, but we supply a var_list for walksat
        if not var_list:
            var_list = range(1, len(self.variables))

        for var in var_list:
            score = self.get_score(var, assignment)
            if score > best_score:
                best_score = score
                best_vars = [var]
                continue
            elif score == best_score:
                best_vars.append(var)

        # Return a random variable of the best variables
        #print(best_score, len(best_vars), best_vars)
        return random.choice(best_vars)

    # Given a variable, get how many clauses are True if it is flipped
    # A helper function for the get_best_flip method.
    def get_score(self, var, assignment):
        # Temporarily flip the assignment
        assignment[var - 1] = not assignment[var - 1]
        score = 0
        for clause in self.clauses:
            if self.is_clause_true(clause, assignment):
                score += 1

        # Bring the assignment back to its original state
        assignment[var - 1] = not assignment[var - 1]
        return score

    # Given an assignment, return whether the clause is True or False
    def is_clause_true(self, clause, assignment):
        for var in clause:
            var_index = abs(var) - 1
            if var > 0:
                if assignment[var_index]:
                    return True
            else:
                if not assignment[var_index]:
                    return True
        return False

    # Given a solution, write it to the given file location
    def write_solution(self, solution, file_loc):
        f = open(file_loc, "w")
        for var in range(len(solution)):
            # For reference in self.variables, do to the one-index shift
            var_index = var + 1

            sentence = self.var_sentence_ref[var_index]
            if not solution[var]:
                f.write("-" + sentence + "\n")
            else:
                f.write(sentence + "\n")

        f.close()


if __name__ == "__main__":
    one_cell = SAT("./puzzles/one_cell.cnf")
    # for i in range(100):
    #     print(one_cell.gsat_solver(0.3))
    # print(one_cell.walksat_solver())

    all_cells_no_rules = SAT("./puzzles/all_cells.cnf")
    # print(one_cell.walksat_solver())
    # print(all_cells_no_rules.gsat_solver(0.1))
    print(all_cells_no_rules.walksat_solver())
    # print(len(one_cell.clauses))
    # for clause in one_cell.clauses:
    #     print("clause:", clause)


