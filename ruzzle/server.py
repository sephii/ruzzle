import Pyro4
import multiprocessing
import sys
import time
import socket
from ruzzle import Dictionary, Solver, Grid
import uuid

def server_process(dictionary):
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = daemon.register(Solver(dictionary))
    ns.register("solver-%s-%s" % (socket.gethostname(), uuid.uuid1()), uri)
    daemon.requestLoop()

d = Dictionary('fr.wl')

if len(sys.argv) > 1:
    nb_processes = int(sys.argv[1])
else:
    nb_processes = 1

processes = []
for i in range(0, nb_processes):
    p = multiprocessing.Process(target=server_process, args=(d,))
    processes.append(p)
    p.start()

for process in processes:
    process.join()
