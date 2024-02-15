# K-Graph-Kit🌐

This project aims to provide a comprehensive library for manipulating and analyzing graphs in Python. It includes various methods for working with both weighted and unweighted graphs, as well as algorithms for finding shortest paths, Krustal algorithm, identifying Eulerian and Hamiltonian cycles, and much more.

## Features 🛠️

* Implementation of the `Graph` class for representing simple graphs, multigraphs, directed, and undirected graphs.
* Methods for calculating vertex degrees.
* Dijkstra's algorithm for finding the shortest paths.
* Support for identifying and working with Eulerian graphs and Hamiltonian cycles.
* Methods for verifying graph connectivity and much more...

## Formalism 📐

This is a model of reprentation of a graph, with some relative methods

    Ex: * Case of graphs with weights

    G = Graph({'A', 'B', 'C'}, {fs({'A', 'B'}): [1, 1], ('A', 'C'): [3.5], fs({'C'}): [4]})

    - {'A', 'B', 'C'} : is the set of vertices of G

    - {fs({'A', 'B'}): [1, 1], ('A', 'C'): [3.5], fs({'C'}): [4]} : is the set of edges of G

    - 'fs({'A', 'B'}): [1, 1]' : means that we have 2 non oriented edges between the edges 'A' et 'B' of weight 1 and 1

    - '('A', 'C'): [3.5]' : means that we have one oriented edge (arc) from 'A' to 'C' of weight 3.5

    - fs({'C'}): [4] : means that we have one edge (loops) of weight 4 which connects 'C' to itself

    NB: - Edges weights are strict positive real numbers

    - Vertices are strings or int

    * Case of graphs without weight

    G = Graph({'A', 'B', 'C'}, {fs({'A', 'B'}): 2, ('A', 'C'): 1, fs({'C'}): 2})

    - {'A', 'B', 'C'} : is the set of vertices of G

    - {fs({'A', 'B'}): 2, ('A', 'C'): 1, fs({'C'}): 2} : is the set of edges of G

    - 'fs({'A', 'B'}): 2' : means that we have 2 non oriented edges between the edges 'A' et 'B'

    - '('A', 'C'): 1' : means that we have one oriented edge (arc) from 'A' to 'C'

    - fs({'C'}): 2 : means that we have 2 edges (loops) which connects 'C' to itself

    NB: - Edges numbers are strict positive integers

    - Vertices are strings or int

## Terminology 📚

    NB: this class uses a little different terminology comparing to the conventionnal one, in terms of the graph theory

    - Arc : oriented edge

    - Chain : an alternative succession of vertices and edges, starting and ending with a vertex, and where each edge is between its starting and ending vertices. Ex: A-(A,B)-B-{B, C}-C

    NB: - In a simple graph, due to the fact that 2 vertices are connected with maximum 1 edge, it is not necessary to mention the edges.

    - Even in multi graph, in general we don't care about the edges, but only about the succession of vertices

    Thus, in most cases, a chain will be just a succession of edges. Ex: [1, 3, 2]

    - Circuit : it is a chain where the starting and the ending vertices are the same

    - Connected graph : graph which has a not oriented version (version where all arcs are replaced by non oriented edges), related.

    - Cycle : it is the equivalent of a circuit in a non oriented graph

    - Edge : link between 2 vertices (in a mixed graph)

    - Loop : edge that connects a vertex to itself

    NB: In convention, a loop is not oriented, due to the fact than an eventual orientation is useless

    - Mixed graph : graph that have can both arcs and not oriented edges

    - Multigraph : graph where we can have loops and even more than 1 edge between 2 vertices

    - Not oriented graph : graph where all edges are not oriented

    - Oriented graph : graph where all edges are arcs

    - Path : it is the equivalent of a chain in a non oriented graph

    - Related graph: a non oriented graph, where it is possible, starting from a given vertex, to reach the others

    Rk: If this condition is possible for a given vertex, it is possible for the others, due to the fact that the graph is not oriented

    - Simple graph : graph without loop, and where there is maximum 1 edge between 2 vertices.

    Rk: a such graph can be oriented or not

    There are some examples of graphs definitions :

- G = Graph({'A', 'B', 'C', 'D', 'E', 'F', 1, 2, 3, 4}, {fs(('C', 'A')): [1], fs({'B', 'D'}): [3], fs({'B', 'F'}): [2, 4], fs({'C', 'D'}): [2], fs({'C', 'E'}): [50], fs({'D', 'E'}): [100], fs({'E'}): [8], fs({'E', 'F'}): [10], (1, 2): [5], fs({1, 3}): [2], (4, 2): [3], (3, 4): [1]})
- G2 = Graph({1, 2, 3, 7, 5, 6}, {fs((1, 2)): [3], fs({1, 7}): [0.5], fs({1, 6}): [1], fs((3, 1)): [4], fs((1, 5)): [1], (3, 2): [3], fs({3, 7}): [1], (5, 6): [3]}, "G2")
- G3 = Graph({1, 2, 3, 4}, {fs((1, 2)): 2, fs((3, 1)): 1, fs((4, 1)): 3, fs((3, 2)): 1, fs((2, 4)): 1, fs((3, 4)): 1}, "G3")

## Usage Examples 📖

### Creating and Manipulating Weighted Graphs

```python
from graph.graph_class import Graph

# Creating a weighted graph with multiple edges and loops
G = Graph({'A', 'B', 'C', 'D', 'E', 'F', 1, 2, 3, 4}, {fs(('C', 'A')): [1], fs({'B', 'D'}): [3], fs({'B', 'F'}): [2, 4], fs({'C', 'D'}): [2], fs({'C', 'E'}): [50], fs({'D', 'E'}): [100], fs({'E'}): [8], fs({'E', 'F'}): [10], (1, 2): [5], fs({1, 3}): [2], (4, 2): [3], (3, 4): [1]})

# Displaying the vertices and edges of the graph
print(G.Vertices) # Outputs {1, 2, 3, 4, 'A', 'B', 'C', 'D', 'E', 'F'}
print(G.Edges) # Outputs {frozenset({'A', 'C'}): [1],
 frozenset({'B', 'D'}): [3],
 frozenset({'B', 'F'}): [2, 4],
 frozenset({'C', 'D'}): [2],
 frozenset({'C', 'E'}): [50],
 frozenset({'D', 'E'}): [100],
 frozenset({'E'}): [8],
 frozenset({'E', 'F'}): [10],
 (1, 2): [5],
 frozenset({1, 3}): [2],
 (4, 2): [3],
 (3, 4): [1]}

# Finding the shortest path from 'A' to 'F' using Dijkstra's algorithm
print(G.Djikstra('A', 'F')) # Outputs the path and cost : (['A', 'C', 'D', 'B', 'F'], 8)
```

### Analyzing Caracteristics

```python
print(G.isConnected()) # Returns False

print(G.isSimple()) # Returns False

```

### ...

### Author ✍️

This project was created by KpihX. You can contact me at kapoivha@gmail.com for any questions or suggestions.

## License 📄

This project is under the MIT license - see the LICENSE file for details.

🔗: https://github.com/KpihX/PyGraphKit
