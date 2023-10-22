import random
assignment = [(True if random.random() < 0.5 else False) for i in range(10)]

print(assignment)