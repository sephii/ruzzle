import networkx as nx
import sys

class Dictionary(object):
    def __init__(self, file):
        self.words = set()

        with open(file) as f:
            for line in f:
                line = line.strip()
                self.words.add(line.lower())

class Grid(object):
    def __init__(self, letters):
        line = 0
        self.graph = nx.Graph()
        self.table = []

        for (i, letter) in enumerate(letters):
            self.graph.add_node(i, letter=letter)

            if len(self.table) < line + 1:
                self.table.append([])

            self.table[line].append(letter)

            if (i + 1) % 4 == 0 and i > 0:
                line += 1

        for i in range(0, 4):
            for j in range(0, 4):
                self.add_edges(j, i)

    def add_edges(self, col, row):
        for i in range(-1, 2):
            for j in range(-1, 2):
                destination = (col + j, row + i)

                if i == 0 and j == 0:
                    continue

                if destination[0] < 0 or destination[1] < 0:
                    continue

                if destination[0] > 3 or destination[1] > 3:
                    continue

                self.graph.add_edge(row * 4 + col, destination[1] * 4 + destination[0])

class Solver(object):
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def set_grid(self, grid):
        self.grid = grid

    def solve(self, source, destination):
        solutions = set()

        for path in nx.all_simple_paths(self.grid.graph, source, destination):
            buffer = ''
            for node in path:
                buffer += self.grid.graph.node[node]['letter']

            if buffer in self.dictionary.words:
                solutions.add(buffer)

        return solutions
