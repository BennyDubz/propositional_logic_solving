# Boolean Satisfiability (SAT) Solving
### Ben Williams '25, October 2023

## Problem Representation

We consider all SAT problems in conjunctive normal form (CNF). Our .cnf files have can have any variable names they want (be it `112` or `BLUE`), except that a variable being false is represented with a `-` in front. Each line in the .cnf is a clause, where spaces between variables represent "or" operators. 

For example, the line `-111 112 -113`, indicates that `112` is False or `112` is True or `113` is False.

The goal is to find an assignment to all the variables such that all the clauses are satisfied, if it exists. All the algorithms here are generic and can solve any SAT problem with the above formatting (with the `-` for False, otherwise True).

### Sudoku

The main SAT problem that we solve here is Sudoku. We can explicitly define sudoku with boolean variables in the format `rcn` where `r` is the row, `c` is the column, and `n` is the number. Sudoku problems have 729 variables (9 rows * 9 columns * 9 numbers) and usually have about ~3000 clauses. 

## GSAT Solver

The GSAT algorithm is very simple. We do the following:

1) Generate a random assignment
2) If the assignment satisfies all clauses, return the assignment
3) With some probability h, flip a random variable in the assignment and return to step 2
4) Otherwise, flip the variable that would cause the most clauses to be satisfied (break ties randomly). Return to step 2

This algorithm can run infinitely if the problem is unsatisfiable. Our implementation has a `max_steps` parameter that forces the algorithm to break out of the algorithm after that many steps have occurred without success.

### Scoring - Picking the best variable

For GSAT, the process of finding the best variable to flip is incredibly slow. We loop through each variable, temporarily flip its value in the assignment, and count how many clauses are satisfied. 

For example, if we had 500 variables and 2000 clauses, this step would loop through about 1,000,000 times just to flip a single variable.

### Discussion - Randomness

Allowing variables to be flipped randomly can push us out of local minima in the solution space, but also has the chance to slow us down significantly (by pushing us farther from a solution). Keeping a low `h` value balances this appropriately, but matters more in the Walksat as we will see later. The `h` value used for the GSAT testing was 0.2.

### Results

GSAT is able to fill in all the cells of sudoku with numbers, do so following the row rules. More complex cnfs (such as the rows and columns combined) take too long for GSAT to complete

All-Cells - 330 steps (does not follow any rules)
```
4 5 2 | 4 4 6 | 7 3 5 
7 2 1 | 4 8 9 | 8 9 2 
8 2 2 | 6 8 2 | 1 5 9 
---------------------
5 2 3 | 7 8 5 | 2 7 5 
3 3 6 | 8 3 1 | 6 3 3 
7 1 8 | 7 6 2 | 1 4 6 
---------------------
2 4 3 | 3 5 1 | 1 7 5 
7 1 2 | 5 7 8 | 7 1 9 
8 2 3 | 9 6 7 | 9 8 8 
```

Rows - 418 Steps
```
3 1 9 | 2 6 4 | 5 8 7 
3 2 1 | 5 8 9 | 7 4 6 
7 4 2 | 1 8 3 | 6 5 9 
---------------------
3 9 7 | 4 8 5 | 2 6 1 
7 3 9 | 6 4 2 | 1 5 8 
4 1 5 | 8 9 3 | 2 7 6 
---------------------
3 7 4 | 1 5 6 | 2 8 9 
7 5 8 | 2 9 6 | 3 1 4 
3 8 6 | 4 5 7 | 9 2 1 
```

## Walksat

Walksat is very similar to GSAT, except that it takes a more refined approach for deciding which variables to score and which variables it might randomly flip. Walksat chooses an unsatisfied clause at random. Then with probability `h` it flips a random variable within that unsatisfied clause, otherwise it flips the variable within the unsatisfied clause that causes the most clauses to be True (the same scoring as GSAT).

Walksat is much faster because rather than looping through _all_ variables, it only has to look at the variables in a single clause. Therefore, the speed of Walksat is partially determined by the average clause size. In Sudoku, most clauses are only 2 variables long, and the longest ones are only 9 variables long. Compared to looping through 729 * `num_clauses`, this is a major improvement. Nevertheless, Walksat still runs into the issue of local minima. We try to mitigate this with the random variable flipping. More about this in the below discussion.

### Results

We are able to solve much more complex problems with the Walksat. While we still show the number of steps taken, note that each step in Walksat is much faster than each step in GSAT. 

### Discussion - Randomness (again)

The randomness for the Walksat is especially important as we are more likely to run into local minima here. Experimentally in the Sudoku examples, we frequently get stuck with having 82 variables as True, where we should only have 81 in the final answer. We end up here quickly, but can take thousands (or tens of thousands) of steps to escape and finally find a solution. 

For the `puzzle_bonus`, having an `h=0.3` caused the program to reach the `max_steps` breakpoint at both 100,000 and 200,000 steps respectively. However, trying a `h=0.5`, which is a bit more extreme, allowed the problem to be solved in ~50,000 steps. This leads me to believe that what made `puzzle_bonus` difficult is the presence of __many local minima__ in the solution space, though it is hard to say for certain.

Puzzle bonus solution:
```
5 3 4 | 6 7 8 | 9 1 2 
6 7 2 | 1 9 5 | 3 4 8 
1 9 8 | 3 4 2 | 5 6 7 
---------------------
8 5 9 | 7 6 1 | 4 2 3 
4 2 6 | 8 5 3 | 7 9 1 
7 1 3 | 9 2 4 | 8 5 6 
---------------------
9 6 1 | 5 3 7 | 2 8 4 
2 8 7 | 4 1 9 | 6 3 5 
3 4 5 | 2 8 6 | 1 7 9 
```

## Walksat Modified - Constants

### Only explicitly defined constants

### All constants

### Results

### Discussion