"""
Rewritten on python mpi program
Source: https://computing.llnl.gov/tutorials/mpi/samples/C/mpi_hello.c
"""
from mpi4py import MPI

MASTER = 0


def main():
    comm = MPI.COMM_WORLD
    number_of_tasks = comm.size
    task_id = comm.rank
    host_name = comm.name

    print(f'Hello from task {task_id} on {host_name}')
    if task_id == MASTER:
        print(f'MASTER: Number of MPI tasks is: {number_of_tasks}')


if __name__ == '__main__':
    main()
