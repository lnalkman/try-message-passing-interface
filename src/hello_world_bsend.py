"""
Rewritten on python mpi program
Source: https://computing.llnl.gov/tutorials/mpi/samples/C/mpi_helloBsend.c
"""
from mpi4py import MPI

MASTER = 0


def main():
    comm = MPI.COMM_WORLD
    number_of_tasks = comm.size
    task_id = comm.rank
    host_name = comm.name

    if number_of_tasks % 2:
        print(
            f'Quitting. Need an even number of tasks: '
            f'numtasks={number_of_tasks}'
        )
        return

    if task_id == MASTER:
        print(f'MASTER: Number of MPI tasks is: {number_of_tasks}')

    print(f'Hello from task {task_id} on {host_name}')

    message = None
    if task_id < number_of_tasks / 2:
        partner = int(number_of_tasks / 2 + task_id)
        comm.send(task_id, dest=partner)
        message = comm.recv(source=partner)
    elif task_id >= number_of_tasks / 2:
        partner = int(task_id - number_of_tasks / 2)
        message = comm.recv(source=partner)
        comm.send(task_id, dest=partner)

    print(f'Task {task_id} is partner with {message}')


if __name__ == '__main__':
    main()
