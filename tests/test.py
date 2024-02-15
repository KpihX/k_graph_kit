#!/usr/bin/env python3
# -*-coding:UTF-8 -*

from k_graph_kit import *

# Creating a weighted graph with multiple edges and loops
G = Graph({'A', 'B', 'C', 'D', 'E', 'F', 1, 2, 3, 4}, {fs(('C', 'A')): [1], fs({'B', 'D'}): [3], fs({'B', 'F'}): [2, 4], fs({'C', 'D'}): [2], fs({'C', 'E'}): [50], fs({'D', 'E'}): [100], fs({'E'}): [8], fs({'E', 'F'}): [10], (1, 2): [5], fs({1, 3}): [2], (4, 2): [3], (3, 4): [1]})

# Displaying the vertices and edges of the graph
print(G.Vertices) # Outputs {1, 2, 3, 4, 'A', 'B', 'C', 'D', 'E', 'F'}
print(G.Edges) #Outputs {frozenset({'A', 'C'}): [1], frozenset({'B', 'D'}): [3], frozenset({'B', 'F'}): [2, 4], frozenset({'C', 'D'}): [2], frozenset({'C', 'E'}): [50], frozenset({'D', 'E'}): [100], frozenset({'E'}): [8], frozenset({'E', 'F'}): [10], (1, 2): [5], frozenset({1, 3}): [2], (4, 2): [3], (3, 4): [1]}

# Finding the shortest path from 'A' to 'F' using Dijkstra's algorithm
print(G.Djikstra('A', 'F')) # Outputs the path and cost : (['A', 'C', 'D', 'B', 'F'], 8)

print(G.isConnected()) # Returns False

print(G.isSimple()) # Returns False


"""Some examples of graphs for tests
G = Graph({'A', 'B', 'C', 'D', 'E', 'F', 1, 2, 3, 4}, {fs(('C', 'A')): [1], fs({'B', 'D'}): [3], fs({'B', 'F'}): [2, 4], fs({'C', 'D'}): [2], fs({'C', 'E'}): [50], fs({'D', 'E'}): [100], fs({'E'}): [8], fs({'E', 'F'}): [10], (1, 2): [5], fs({1, 3}): [2], (4, 2): [3], (3, 4): [1]})

G2 = Graph({1, 2, 3, 7, 5, 6}, {fs((1, 2)): [3], fs({1, 7}): [0.5], fs({1, 6}): [1], fs((3, 1)): [4], fs((1, 5)): [1], (3, 2): [3], fs({3, 7}): [1], (5, 6): [3]}, "G2")

G3 = Graph({1, 2, 3, 4}, {fs((1, 2)): 2, fs((3, 1)): 1, fs((4, 1)): 3, fs((3, 2)): 1, fs((2, 4)): 1, fs((3, 4)): 1}, "G3")
"""

input("Glad to have served you! Press 'Enter' to quit.")

