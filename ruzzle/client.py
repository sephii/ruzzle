import Pyro4
import sys
import time
from multiprocessing import Process, Queue

from ruzzle import Grid

def solve(solver_uri, grid, paths_queue):
    solver = Pyro4.Proxy(solver_uri)
    solver.set_grid(grid)

    try:
        while True:
            path = paths_queue.get(timeout=5)

            print("Solver %s, solving %s -> %s" % (solver_uri, path[0], path[1]))
            print(solver.solve(path[0], path[1]))
    except:
        pass

tried = set()

grid = Grid(sys.argv[1])

ns = Pyro4.naming.locateNS()
solvers_uris = ns.list('solver')

paths_queue = Queue()
processes = []
for solver_uri in solvers_uris.values():
    p = Process(target=solve, args=(solver_uri, grid, paths_queue))
    processes.append(p)
    p.start()

start_time = time.time()
print(start_time)
for source in range(0, grid.graph.number_of_nodes()):
    for destination in range(grid.graph.number_of_nodes() - 1, 1, -1):
        if source == destination:
            continue

        #print(solver.solve(source, destination))
        paths_queue.put((source, destination))

for process in processes:
    process.join()

end_time = time.time()
print(end_time)

print(end_time - start_time)

