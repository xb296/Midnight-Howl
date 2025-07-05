grid = []
for i in range(2):
    for j in range(2):
        for k in range(2):
            grid.append(pow(-1, i) * 10 / pow(2, 1) + pow(-1, j) * 10 / pow(2, 2) + pow(-1, k) * 10 / pow(2, 3))

print(grid)