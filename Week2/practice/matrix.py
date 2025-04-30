a = [[1, 2, 3,4,5],
    [5,6,7,8,9],
    [10,11,12,13,14]]

sum = []

for i in range(len(a) - 2):
    for j in range(len(a[0]) - 2):
        center = a[i+1] [j+1]
        top = a[i][j+1]
        left = a[i+1][j]
        right = a[i+1][j+2]
        bottom = a[i+2][j+1]

        sums = center + top + left + right + bottom
        sum.append(sums)
print(sum)


