import random


def build_matrix(n):
    arr = [i + 1 for i in range(n * n)]
    random.shuffle(arr)

    # build a matrix from the array
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            matrix[i][j] = arr.pop()

    return matrix


def print_matrix_to_console(matrix):
    """print the matrix like a table to console use | to separate the numbers"""
    # print the edge
    print("-" * (len(matrix) * 4 - 1))
    # print the matrix
    for row in matrix:
        print("|", end="")
        print("|".join(map(str, row)), end="|\n")
    # print the edge
    print("-" * (len(matrix) * 4 - 1))


def print_matrix_to_file(matrix, filename):
    """print the matrix to file use | to separate the numbers"""
    with open(filename, "w") as f:
        # print the edge
        f.write("-" * (len(matrix) * 4 - 1) + "\n")
        # print the matrix
        for row in matrix:
            f.write("|" + "|".join(map(str, row)) + "|\n")
        # print the edge
        f.write("-" * (len(matrix) * 4 - 1) + "\n")


mat = build_matrix(5)
print_matrix_to_console(mat)
# print_matrix_to_file(mat, "matrix.txt")
