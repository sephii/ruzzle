import Pyro4
import sys
import time
from Queue import PriorityQueue, Empty
from multiprocessing import Process, Queue

from ruzzle import Grid

class bcolors:
    RED = '\033[31m'
    BLUE = '\033[34m'
    GREEN = '\033[32m'
    CYAN = '\033[36m'
    PURPLE = '\033[35m'
    YELLOW = '\033[33m'
    WHITE = '\033[37m'
    ENDC = '\033[0m'

def solve(solver_uri, grid, paths_queue, solutions_queue):
    solver = Pyro4.Proxy(solver_uri)
    solver.set_grid(grid)

    try:
        while True:
            path = paths_queue.get(timeout=5)

            #print("Solver %s, solving %s -> %s" % (solver_uri, path[0], path[1]))
            solutions = solver.solve(path[0], path[1])

            for solution in solutions:
                solutions_queue.put(solution)
    except Empty:
        print('Paths queue is empty')
    except KeyboardInterrupt:
        pass

def print_solution(score, solution):
    colors = [
        (150, bcolors.RED),
        (100, bcolors.PURPLE),
        (75, bcolors.YELLOW),
        (50, bcolors.GREEN),
        (25, bcolors.CYAN),
        (0, bcolors.WHITE),
    ]

    for (s, c) in colors:
        if score >= s:
            color = c
            break

    print('%s%s: %s%s' % (color, score, solution, bcolors.ENDC))

def consume_solution_queue(q):
    priority_queue = PriorityQueue()
    proposed_solutions = set()

    try:
        while True:
            fetch = True
            while fetch:
                try:
                    item = q.get_nowait()

                    if item[1] not in proposed_solutions:
                        priorized_item = (-1 * (item[0] / len(item[1])), item[0], item[1])
                        priority_queue.put(priorized_item)
                        proposed_solutions.add(item[1])
                except Empty:
                    fetch = False

            try:
                solution = priority_queue.get_nowait()
                print_solution(solution[1], solution[2])
            except Empty:
                pass

            time.sleep(2)
    except KeyboardInterrupt:
        pass

tried = set()

sys.excepthook=Pyro4.util.excepthook
grid = Grid(sys.argv[1])

ns = Pyro4.naming.locateNS()
solvers_uris = ns.list('solver')

solutions_queue = Queue()
paths_queue = Queue()
processes = []
nodes_queue = []

for solver_uri in solvers_uris.values():
    p = Process(target=solve, args=(solver_uri, grid, paths_queue,
                solutions_queue))
    processes.append(p)
    p.start()

for node in grid.graph.nodes():
    priority = grid.graph.node[node]['letter_score'] + ((grid.graph.node[node]['word_modifier'] - 1) * 20)
    nodes_queue.append((-1 * priority, node))

nodes_queue = sorted(nodes_queue)

for (priority, source) in nodes_queue:
    for destination in range(grid.graph.number_of_nodes() - 1, -1, -1):
        if source == destination:
            continue

        paths_queue.put((source, destination))

p = Process(target=consume_solution_queue, args=(solutions_queue,))
p.start()

try:
    for process in processes:
        process.join()
except KeyboardInterrupt:
    pass
