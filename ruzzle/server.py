import Pyro4
import time
import socket
from ruzzle import Dictionary, Solver, Grid

d = Dictionary('fr.wl')

daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()
uri = daemon.register(Solver(d))
ns.register("solver-%s-%s" % (socket.gethostname(), time.time()), uri)
daemon.requestLoop()
