import networkx as nx
import sys

def add_edges(graph, table, col, row):
    for i in range(-1, 2):
        for j in range(-1, 2):
            destination = (col + j, row + i)

            if i == 0 and j == 0:
                continue

            if destination[0] < 0 or destination[1] < 0:
                continue

            if destination[0] > 3 or destination[1] > 3:
                continue

            graph.add_edge(row * 4 + col, destination[1] * 4 + destination[0])

words = set()
tried = set()
table = []

g = nx.Graph()

with open('fr.wl') as f:
    for line in f:
        line = line.strip()
        words.add(line.lower())

line = 0
for (i, letter) in enumerate(sys.argv[1]):
    g.add_node(i, letter=letter)

    if len(table) < line + 1:
        table.append([])

    table[line].append(letter)

    if (i + 1) % 4 == 0 and i > 0:
        line += 1

for i in range(0, 4):
    for j in range(0, 4):
        add_edges(g, table, j, i)

for source in range(0, g.number_of_nodes()):
    for destination in range(g.number_of_nodes() - 1, 1, -1):
        if source == destination:
            continue

        for path in nx.all_simple_paths(g, source, destination):
            buffer = ''
            for node in path:
                buffer += g.node[node]['letter']

            if buffer in words and len(buffer) > 3 and buffer not in tried:
                tried.add(buffer)

                if len(buffer) > 5:
                    print('*** %s' % buffer)
                else:
                    print(buffer)
