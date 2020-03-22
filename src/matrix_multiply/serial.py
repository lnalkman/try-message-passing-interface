from pprint import pprint

# Number of rows in matrix A
NRA = 62

# Number of columns in matrix A
NCA = 15

# Number of rows in matrix B equals number of columns matrix A
NRB = NRA

# Number of columns in matrix B
NCB = 7


def main():

    a_matrix = [
        [row + column for column in range(NCA)]
        for row in range(NRA)
    ]

    b_matrix = [
        [row * column for column in range(NCB)]
        for row in range(NRB)
    ]

    c_matrix = [
        [0 for _ in range(NCB)]
        for _ in range(NRA)
    ]

    for i in range(NRA):
        for j in range(NCB):
            for k in range(NCA):
                c_matrix[i][j] += a_matrix[i][k] * b_matrix[k][j]

    pprint(c_matrix)


if __name__ == '__main__':
    main()