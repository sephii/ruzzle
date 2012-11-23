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

        letter_position = 0
        for (i, letter) in enumerate(letters):
            if letter.isdigit():
                letter = int(letter)

                if letter == 1:
                    self.graph.node[letter_position - 1]['letter_modifier'] = 2
                elif letter == 2:
                    self.graph.node[letter_position - 1]['letter_modifier'] = 3
                elif letter == 3:
                    self.graph.node[letter_position - 1]['word_modifier'] = 2
                elif letter == 4:
                    self.graph.node[letter_position - 1]['word_modifier'] = 3

                continue

            self.graph.add_node(letter_position, letter=letter, letter_modifier=1,
                    word_modifier=1)

            if len(self.table) < line + 1:
                self.table.append([])

            self.table[line].append(letter)

            if (letter_position + 1) % 4 == 0 and letter_position > 0:
                line += 1

            letter_position += 1

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

    def get_letter_score(self, letter):
        scores = {
                'd': 2, 'l': 2, 'p': 3, 'h': 4, 'q': 8, 'b': 3, 'v': 5,
        }

        if letter in scores:
            return scores[letter]

        return 1

    def get_length_score(self, length):
        if length >= 5:
            return 5 + (5 * (length - 5))

        return 0

    def solve(self, source, destination):
        solutions = set()

        for path in nx.all_simple_paths(self.grid.graph, source, destination):
            buffer = ''
            score = 0
            word_modifier = 1
            for node_id in path:
                node = self.grid.graph.node[node_id]
                score += self.get_letter_score(node['letter']) * node['letter_modifier']
                buffer += node['letter']

                if node['word_modifier'] > word_modifier:
                    word_modifier = node['word_modifier']

            if buffer in self.dictionary.words:
                score *= word_modifier
                score += self.get_length_score(len(buffer))
                solutions.add((score, buffer))

        return list(solutions)
