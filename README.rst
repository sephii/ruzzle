Installation
============

To install it::

    git clone https://github.com/sephii/ruzzle
    cd ruzzle
    virtualenv .
    source bin/activate
    pip install -r requirements.txt

Usage
=====

This program uses Pyro4 to add parallelism to grid resolution. It means you can
run servers on multiple computers and they will process the grid in parallel.
First you must run the Pyro name server::

    python -m Pyro4.naming

Then run one or more servers (set nb_processes to start more than 1 process at
the same time, useful if you don't want to manually start several servers on the
same server)::

    python ruzzle/server.py <nb_processes>

Now run the client::

    python ruzzle/client.py <grid>

The grid is a 16 letter string, line by line, starting from top left to bottom
right. You can set letter/word multipliers by postfixing the letters with
characters 1 (double letter), 2 (triple letter), 3 (double word) and 4 (triple
word).

Consider the following grid, with the first E having a "double letter"
multiplier, the first S having a "triple letter" multiplier, the last A having a
"double word" multiplier and the last R having a "triple word" multiplier::

    E E A S
    R I G H
    P U R T
    A I E R

To solve it, run::

    python ruzzle/client.py e1eas2righpurta3ier4
