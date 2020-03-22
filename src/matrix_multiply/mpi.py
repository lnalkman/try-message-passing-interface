"""
Rewritten on python mpi program
Source: https://computing.llnl.gov/tutorials/mpi/samples/C/mpi_mm.c
"""

from mpi4py import MPI

MASTER = 0

# Number of rows in matrix A
NRA = 500

# Number of columns in matrix A
NCA = 500

# Number of rows in matrix B equals number of columns matrix A
NRB = NRA

# Number of columns in matrix B
NCB = 500


def main():
    comm = MPI.COMM_WORLD
    number_of_tasks = comm.size
    task_id = comm.rank

    if number_of_tasks < 2:
        print('Need at least two MPI tasks. Quitting...')
        return

    number_of_workers = number_of_tasks - 1

    c_matrix = [
        [0 for _ in range(NCB)]
        for _ in range(NRA)
    ]

    # *** master task ***
    if task_id == MASTER:
        a_matrix = [
            [row + column for column in range(NCA)]
            for row in range(NRA)
        ]
        b_matrix = [
            [row * column for column in range(NCB)]
            for row in range(NRB)
        ]

        # Send matrix data to the worker tasks
        ave_row = int(NRA / number_of_workers)
        extra = NRA % number_of_workers
        offset = 0
        for dest in range(1, number_of_workers + 1):
            rows = ave_row + 1 if dest <= extra else ave_row
            print(f'Sending {rows} rows to task {dest} offset={offset}')
            comm.send(offset, dest=dest)
            comm.send(rows, dest=dest)
            comm.send(a_matrix, dest=dest)
            comm.send(b_matrix, dest=dest)
            offset = offset + rows

        # Receive results from worker tasks
        for worker_id in range(1, number_of_workers + 1):
            offset = comm.recv(source=worker_id)
            rows = comm.recv(source=worker_id)
            worker_c_matrix = comm.recv(source=worker_id)
            for row in range(offset, offset + rows):
                c_matrix[row] = worker_c_matrix[row]
            print(f'Received results from task {worker_id}')

        print('*********')
        print('Result matrix: \n')
        # for row in c_matrix:
        #     print(' '.join(str(elem).rjust(6) for elem in row))
        print('*********')
        print('Done.\n')

    # *** worker task ***
    if task_id > MASTER:
        offset = comm.recv(source=MASTER)
        rows = comm.recv(source=MASTER)
        a_matrix = comm.recv(source=MASTER)
        b_matrix = comm.recv(source=MASTER)

        for k in range(NCB):
            for i in range(offset, offset + rows):
                for j in range(NCA):
                    c_matrix[i][k] = (
                        c_matrix[i][k]
                        + a_matrix[i][j]
                        * b_matrix[j][k]
                    )

        comm.send(offset, dest=MASTER)
        comm.send(rows, dest=MASTER)
        comm.send(c_matrix, dest=MASTER)


if __name__ == '__main__':
    main()
