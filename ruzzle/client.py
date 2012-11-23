import Pyro4
import sys
import time
from Queue import PriorityQueue, Empty
from multiprocessing import Process, Queue

from ruzzle import Grid

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

def consume_solution_queue(q):
    priority_queue = PriorityQueue()
    proposed_solutions = set()

    while True:
        fetch = True
        while fetch:
            try:
                item = q.get_nowait()

                if item[1] not in proposed_solutions:
                    item = (-1 * item[0], item[1])
                    priority_queue.put(item)
                    proposed_solutions.add(item[1])
            except Empty:
                fetch = False

        try:
            solution = priority_queue.get_nowait()
            print('%s: %s' % (-1 * solution[0], solution[1]))
        except Empty:
            pass

        time.sleep(3)

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
    priority = grid.graph.node[node]['letter_score'] * grid.graph.node[node]['word_modifier']
    nodes_queue.append((-1 * priority, node))

nodes_queue = sorted(nodes_queue)

for (priority, source) in nodes_queue:
    for destination in range(grid.graph.number_of_nodes() - 1, -1, -1):
        if source == destination:
            continue

        paths_queue.put((source, destination))

p = Process(target=consume_solution_queue, args=(solutions_queue,))
p.start()

for process in processes:
    process.join()

#p.terminate()
