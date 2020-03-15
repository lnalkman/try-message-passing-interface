"""
Rewritten on python mpi program
Source: https://computing.llnl.gov/tutorials/mpi/samples/C/mpi_pi_reduce.c
"""
from random import random

from mpi4py import MPI

MASTER = 0

NUMBER_OF_THROWS = 50000
ROUNDS = 100


def dboard(darts):
    score = 0

    for _ in range(darts):
        x_coord = 2 * random() - 1
        y_coord = 2 * random() - 1

        is_dot_inside_circle = x_coord**2 + y_coord**2 <= 1
        if is_dot_inside_circle:
            score += 1

    pi = 4 * score / darts
    return pi


def main():
    comm = MPI.COMM_WORLD
    number_of_tasks = comm.size
    task_id = comm.rank

    avg_pi = 0
    for i in range(ROUNDS):
        # Local PI value for task
        local_pi = dboard(NUMBER_OF_THROWS)

        pi_sum = comm.allreduce(local_pi)

        if task_id == MASTER:
            pi = pi_sum / number_of_tasks
            avg_pi = (avg_pi * i + pi) / (i + 1)
            print(f"   After {i:<3} rounds, average value of pi = {avg_pi}")

    if task_id == MASTER:
        print("Real value of PI: 3.1415926535897")


if __name__ == '__main__':
    main()
