from math import inf, nan
fs = frozenset
Real = {float, int}

class Graph:
    """This is a model of reprentation of a graph, with some relative methods
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

    Terminology : 
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
    """

    def __init__(self, Vertices:set = set(), Edges:dict = {}, name:str = 'G'):
        self.Vertices = Vertices
        self.Edges = Edges
        self.name = name
        self.isGraph()

    def Adj(self, Vertices:set)-> set:
        """It returns the adjacent vertices to a set of vertices 'Vertices' of a graph self
        A such vertice is directly connected to a vertice of 'Vertices' by an edge
        """
        self.isGraph()
        assert self.Vertices != set(), "The porblematic graph is empty"
        assert Vertices != set() and Vertices <= self.Vertices, f"Vertices = {Vertices} must be a subset of self.Vertices" 
        Adj = set()
        for Edge in self.Edges:
            if type(Edge) == fs:
                Edge = set(Edge)
                Inter = Edge & Vertices
                if len(Inter) == 1:
                    Adj |= Edge-Inter
            if type(Edge) == tuple and Edge[0] in Vertices and Edge[1] not in Vertices:
                Adj.add(Edge[1])
        return Adj  

    def Adj2(self, Vertices:set)-> set:
        """It returns the adjacent edges to a set of vertices 'Vertices' of a graph self
        A such edge connects a vertex of 'Vertices' with another one, not in 'Vertices'
        """
        self.isGraph()
        assert self.Vertices != set(), "The porblematic graph is empty"
        assert Vertices != set() and Vertices <= self.Vertices, f"Vertices = {Vertices} must be a non empty subset of self.Vertices" 
        Adj = set()
        for Edge in self.Edges:
            if type(Edge) == fs:
                Inter = Edge & Vertices
                if len(Inter) == 1 and len(Edge) != 1:
                    Adj.add(Edge)
            if type(Edge) == tuple and Edge[0] in Vertices and Edge[1] not in Vertices:
                Adj.add(Edge)
        return Adj  

    def connectedParts(self)-> list:
        """It returns the indivual connected parts of self in the form of a list
        There are the related parts of the simple version of 'self'"""
        return self.simple().relatedParts()

    def deg(self, vertex)-> int:
        """It returns the degree of vertex in self
        The degree of a vertex in a graph, is the number of edge ends, that arrive at that vertex
        """
        self.isGraph()
        assert self.Vertices != set(), "The porblematic graph is empty"
        assert vertex in self.Vertices, f"vertex = {vertex} must be in self.Vertices"
        if self.isGraphNoWeight(False):
            return int(sum([(vertex in Edge)*2*n/len(Edge) for Edge, n in self.Edges.items()])) #We don't forget the cases of loops
        return int(sum([(vertex in Edge)*2*len(Weights)/len(Edge) for Edge, Weights in self.Edges.items()])) #We don't forget the cases of loops
        
    def degIn(self, vertex)-> int:
        """It returns the ingoing degree of vertex in self
        The ingoing degree of a vertex in a graph, is the number of oriented edges, which arrive to this vertex
        """
        self.isGraph()
        assert self.Vertices != set(), "The porblematic graph is empty"
        assert vertex in self.Vertices, f"vertex = {vertex} must be in self.Vertices"
        if self.isGraphNoWeight(False):
            return sum([(vertex == Edge[1])*n for Edge, n in self.Edges.items() if type(Edge) == tuple])
        return sum([(vertex == Edge[1])*len(Weights) for Edge, Weights in self.Edges.items() if type(Edge) == tuple])

    def degNeu(self, vertex)-> int:
        """It returns the neutral degree of vertex in self
        The neutral degree of a vertex in a graph, is the number of non oriented edge ends, that arrive at that vertex
        """
        self.isGraph()
        assert self.Vertices != set(), "The porblematic graph is empty"
        assert vertex in self.Vertices, f"vertex = {vertex} must be in self.Vertices"
        if self.isGraphNoWeight(False):
            return int(sum([(vertex in Edge)*2*n/len(Edge) for Edge, n in self.Edges.items() if type(Edge) == fs])) #We don't forget the cases of loops
        return int(sum([(vertex in Edge)*2*len(Weights)/len(Edge) for Edge, Weights in self.Edges.items() if type(Edge) == fs])) #We don't forget the cases of loops

    def degOut(self, vertex)-> int:
        """It returns the outgoing degree of vertex in self
        The outgoing degree of a vertex in a graph, is the number of oriented edges starting from this vertex
        """
        self.isGraph()
        assert self.Vertices != set(), "The porblematic graph is empty"
        assert vertex in self.Vertices, f"vertex = {vertex} must be in self.Vertices"
        if self.isGraphNoWeight(False):
            return sum([(vertex == Edge[0])*n for Edge, n in self.Edges.items() if type(Edge) == tuple])
        return sum([(vertex == Edge[0])*len(Weights) for Edge, Weights in self.Edges.items() if type(Edge) == tuple])

    def Djikstra(self, start, end)-> tuple:
        """It returns the path with the smallest total weight going from the vertex 'start' to 'end', using the Djikstra algorithm principle
        The answer is a tuple of the form '[start, ..., end], totalWeight', where the first elt is the successive order of vertices from path to end in the found path, and the 2nd, the total weight going from 'start' to 'end'
        Rq: '(), inf' is returned when there is no possible way from 'start' to 'end' following self edges
        """
        self.isGraphWeight()
        assert {start, end} <= self.Vertices, f"start = {start} and end = {end} must be in self.Vertices"
        if start == end:
            return [start], 0
        Checked = {start: (start, 0)}
        minadj = self.minAdj(Checked)
        while minadj != (nan, nan, inf) and end != minadj[0]:
            Checked[minadj[0]] = (minadj[1], minadj[2])
            minadj = self.minAdj(Checked)
        if end == minadj[0]:
            Path = [end]
            edge = minadj[1]
            while edge != start:
                Path.append(edge)
                edge = Checked[edge][0]
            Path.reverse()
            return [start]+Path, minadj[2]
        else:
            return (), inf #stands for no possible way from start to end

    def EulerCircuit(self)-> tuple:
        """It returns an eventual Euler circuit of self as a tuple
        An Euler circuit is a  graph that we can run through, passing one time by each edge, and where the starting edge is the final edge
        Rk: it is an Euler chain where the starting edge and the final edge are the same
        A graph has an Euler circuit only if it is connected
        """
        assert self.isConnected(), "The problematic graph must be a connected graph in order to give one of its eventual Euler circuits"
        G = self.graphCopy()
        if G.isGraphWeight(False):
            G = G.noWeight()
        G.printGraph()
        StrictEdges = {Edge for Edge in self.Edges if len(Edge) == 2} #We don't consider loops
        for vertex in self.Vertices:
            Paths = {(vertex,): {}} #We'll store there all the eventual paths gradually as keys, and the crossed edges as values.
            CurrentPos = {vertex} #we store there the actual position(s) in the course
            while True:
                for Path, Edges in Paths.copy().items():
                    vertex2 = Path[-1]
                    try:
                        CurrentPos.remove(vertex2)
                    except:
                        pass
                    Paths.pop(Path)
                    #We'll try to update the current path at the current position
                    for Edge in G.Adj2({vertex2}):
                        if type(Edge) == fs:
                            vertex3 = (set(Edge)-{vertex2}).pop()
                        else: #type(edge) == tuple
                            vertex3 = Edge[1]
                        #There, we avoid to pass more than 2 times on a given edge
                        if Edge not in Edges:
                            n = G.Edges[Edge]-1
                        else:
                            if Edges[Edge] == 0:
                                continue
                            else:
                                n = Edges[Edge]-1
                        Paths[Path + (vertex3,)] = Edges | {Edge:n}
                        CurrentPos.add(vertex3)
                        if vertex3 == vertex and set(Paths[Path + (vertex3,)]) == StrictEdges and all([n == 0 for n in Paths[Path + (vertex3,)].values()]):
                            return Path + (vertex3,)
                if CurrentPos == set():
                    break
        return () 

    def EulerChain(self)-> tuple:
        """It returns an eventual Euler chain of self in the form of a tuple
        An Euler chain is a  graph that we can run through, passing one time by each edge
        A graph has an Euler circuit only if it is connected
        """
        assert self.isConnected(), "The problematic graph must be a connected graph in order to give one of its eventual Euler chains"
        G = self.graphCopy()
        if G.isGraphWeight(False):
            G = G.noWeight()
        StrictEdges = {Edge for Edge in self.Edges if len(Edge) == 2} #We don't consider loops
        for vertex in self.Vertices:
            Paths = {(vertex,): {}} #We'll store there all the eventual paths gradually as keys, and the crossed edges as values.
            CurrentPos = {vertex} #we store there the actual position(s) in the course
            while True:
                for Path, Edges in Paths.copy().items():
                    vertex2 = Path[-1]
                    try:
                        CurrentPos.remove(vertex2)
                    except:
                        pass
                    Paths.pop(Path)
                    #We'll try to update the current path at the current position
                    for Edge in G.Adj2({vertex2}):
                        if type(Edge) == fs:
                            vertex3 = (set(Edge)-{vertex2}).pop()
                        else: #type(edge) == tuple
                            vertex3 = Edge[1]
                        #There, we avoid to pass more than 2 times on a given edge
                        if Edge not in Edges:
                            n = G.Edges[Edge]-1
                        else:
                            if Edges[Edge] == 0:
                                continue
                            else:
                                n = Edges[Edge]-1
                        Paths[Path + (vertex3,)] = Edges | {Edge:n}
                        CurrentPos.add(vertex3)
                        if set(Paths[Path + (vertex3,)]) == StrictEdges and all([n == 0 for n in Paths[Path + (vertex3,)].values()]):
                            return Path + (vertex3,)
                if CurrentPos == set():
                    break
        return ()  

    def graphCopy(self):
        """It returns a shallow copy of a graph self"""
        self.isGraph()
        return Graph(self.Vertices.copy(), self.Edges.copy(), f"{self.name}-copy")

    def HamiltonCircuit(self)-> tuple:
        """It return an eventual Hamilton circuit of self in the form of a tuple
        An Hamilton circuit is a  graph that we can run through, passing one time by each vertex, and where the starting edge is the final edge
        An Hamilton circuit is a connected graph, so a non connected graph can't have an hamilton circuit
        """
        assert self.isConnected(), "The problematic graph must be a connected graph in order to give one of its eventual Hamilton circuits"
        G = self.simple(notoriented = False) #Due to the fact that we won't pass more than 1 time by a given vertex, it is more efficient for the course to consider only one of its edges among all its common edges with another vertex
        if G.isGraphWeight(False):
            G = G.noWeight()
        
        for vertex in self.Vertices:
            Paths = [(vertex,)] #We'll store there all the eventual paths gradually
            CurrentPos = {vertex} #we store there the actual position(s) in the course
            while True :
                for Path in Paths:
                    vertex2 = Path[-1]
                    try:
                        CurrentPos.remove(vertex2)
                    except:
                        pass
                    Paths.remove(Path)
                    #We'll try to update the current path at the current position
                    for vertex3 in  G.Adj({vertex2}):
                        if (vertex3 in Path and vertex3 != vertex) or (vertex3 == vertex and set(Path) != self.Vertices):
                            continue
                        CurrentPos.add(vertex3)
                        Paths.append(Path + (vertex3,))
                        #Debug test
                        #print(vertex, vertex2, vertex3, Path, Paths, CurrentPos, sep = '\n\t', end = '\n\n')
                        if vertex == vertex3:
                            return Paths[-1]
                if CurrentPos == set():
                    break
        return () 

    def HamiltonChain(self)-> tuple:
        """It return an eventual Hamilton chain of self in the form of a tuple
        An Hamilton chain is a  graph that we can run through, passing one time by each vertex
        Rk: An Hamilton chain is connected graph, so a non connected graph can't be an hamilton chain
        """
        assert self.isConnected(), "The problematic graph must be a connected graph in order to give one of its eventual Hamilton chains"
        G = self.simple(notoriented = False) #Due to the fact that we won't pass more than 1 time by a given vertex, it is more efficient for the course to consider only one of its edges among all its common edges with another vertex
        if G.isGraphWeight(False):
            G = G.noWeight()

        for vertex in self.Vertices:
            Paths = [(vertex,)] #We'll store there all the eventual paths gradually
            CurrentPos = {vertex} #we store there the actual position(s) in the course
            while True :
                for Path in Paths:
                    vertex2 = Path[-1]
                    try:
                        CurrentPos.remove(vertex2)
                    except:
                        pass
                    Paths.remove(Path)
                    #We'll try to update the current path at the current position
                    for vertex3 in  G.Adj({vertex2}):
                        if (vertex3 in Path and vertex3 != vertex) or (vertex3 == vertex and set(Path) != self.Vertices):
                            continue
                        CurrentPos.add(vertex3)
                        Paths.append(Path + (vertex3,))
                        #Debug test
                        #print(vertex, vertex2, vertex3, Path, Paths, CurrentPos, sep = '\n\t', end = '\n\n')
                        if set(Paths[-1]) == self.Vertices:
                            return Paths[-1]
                if CurrentPos == set():
                    break
        return ()

    def hasEulerCycle(self)-> bool:
        """It checks if self has an Euler cycle
        An Euler cycle is a non oriented graph that we can run through, passing one time by each edge, and where the starting edge is the final edge
        Rk: it is an Euler Path where the starting edge and the final edge are the same
        A graph has an Euler cycle if and only if :
        - it is related
        - and all its vertices are the extremities of an even number of edges 
        """
        return self.isRelated() and sum([self.deg(vertex) % 2 == 1 for vertex in self.Vertices]) == 0

    def hasEulerPath(self)-> bool:
        """It checks if self has an Euler path
        An Euler path is a non oriented graph that we can run through, passing one time by each edge
        A graph has an Euler path if and only if :
        - it is related
        - and it has at most 2 vertices which are each the extremities of an odd number of edges
        """
        return self.isRelated() and sum([self.deg(vertex) % 2 == 1 for vertex in self.Vertices]) in {0, 2}

    def hasHamiltonCircuit(self)-> bool:
        """It checks if self has an Hamilton circuit
        An Hamilton circuit is a  graph that we can run through, passing one time by each vertex, and where the starting edge is the final edge
        Rk: if self is simple and not oriented and for each vertex in self we have deg(vertex) >= len(self.Vertices)/2 (with len(self.Vertices)>=3), then self has an Hamilton circuit (cycle) according to the 'Dirac Theorem'
        An Hamilton circuit is a connected graph, so a non connected graph can't have an hamilton circuit
        """
        if not self.isConnected():
            return False
        l = len(self.Vertices)/2
        if self.isSimple() and self.isNotOriented() and l >= 1.5 and all([self.deg(vertex) >= l for vertex in self.Vertices]):
            return True

        return self.HamiltonCircuit() != ()

    def hasHamiltonChain(self)-> bool:
        """It checks if self has an Hamilton chain
        An Hamilton chain is a  graph that we can run through, passing one time by each vertex
        Rk: if self is simple and non oriented and for each vertex in self we have deg(vertex) >= len(self.Vertices)/2 (with len(self.Vertices)>=3), then self has an Hamilton chain according to the 'Dirac Theorem'
        An Hamilton chain is connected graph, so a non connected graph can't have an hamilton path
        """
        if not self.isConnected():
            return False
        l = len(self.Vertices)/2
        if self.isSimple() and self.isNotOriented() and l >= 1.5 and all([self.deg(vertex) >= l for vertex in self.Vertices]):
            return True

        return self.HamiltonChain() != ()

    def isComplete(self)-> bool:
        """It checks if self is complete or not.
        A complete graph is a non oriented graph where each vertex is connected to the others vertices directly by an edge
        """
        assert self.isNotOriented(), "The problematic graph must be non oriented in order to verify whether it is complete or not."
        return all([fs({vertex, vertex2}) in self.Edges for vertex in self.Vertices for vertex2 in self.Vertices if vertex != vertex2])

    def isConnected(self)-> bool:
        """It verifies if self is a connected graph or not
        A connected graph is a graph where it is possible from any vertex, to reach the other vertices following the edges, in its simple version
        """
        return self.simple().isRelated()

    def isForest(self)-> bool:
        """It verifies whether self is a forest or not
        A graph is a forest if and only if all its related parts are trees
        """
        return all([graph.isTree2() for graph in self.relatedParts()])

    def isGraph(self, error:bool = True):
        """It verifies is a given graph is correct following the modeling format of the class 'Graph'
        It raises an error if error == True and just return a bool, else.
        """
        bool1 = all([type(vertex) in {int, str} for vertex in self.Vertices])
        boolWeight = all([type(Edge) in {fs, tuple} and len(Edge) in {1, 2} and type(Weights) == list and Weights != []  and all([type(weight) in Real and weight > 0 for weight in Weights]) and all([vertex in self.Vertices for vertex in Edge]) and len(set(Edge)) == len(Edge) for Edge, Weights in self.Edges.items()])
        boolNoWeight = all([type(Edge) in {fs, tuple} and len(Edge) in {1, 2} and type(n) == int and n > 0 and all([vertex in self.Vertices for vertex in Edge]) and len(set(Edge)) == len(Edge) for Edge, n in self.Edges.items()])
        bool2 = boolWeight or boolNoWeight
        if error == False:
            return bool1 and bool2
        assert bool1, f"The structure '{self.Vertices}', containing the vertices of the problematic graph has at least one vertex which is neither an int nor a string\n\tRefer to the help of the 'Graph' class"
        assert bool2, f"At least one of the edge of the problematic graph is not well defined in '{self.Edges}'\n\tRefer to the help of the 'Graph' class"

    def isGraphWeight(self, error:bool = True)-> bool:
        """It verifies is a given graph is a correct graph with weights following the modeling format of the class 'Graph'
        It raises an error if error == True and just return a bool, else.
        """
        bool1 = all([type(vertex) in {int, str} for vertex in self.Vertices])
        bool2 = all([type(Edge) in {fs, tuple} and len(Edge) in {1, 2} and type(Weights) == list and Weights != []  and all([type(weight) in Real and weight > 0 for weight in Weights]) and all([vertex in self.Vertices for vertex in Edge]) and len(set(Edge)) == len(Edge) for Edge, Weights in self.Edges.items()])
        if error == False:
            return bool1 and bool2
        assert bool1, f"The structure '{self.Vertices}', containing the vertices of the problematic graph (with weights) has at least one vertex which is neither an int nor a string\n\tRefer to the help of the 'Graph' class"
        assert bool2, f"At least one of the edge of the problematic graph is not well defined in '{self.Edges}'\n\tRefer to the help of the 'Graph' class"

    def isGraphNoWeight(self, error:bool = True)-> bool:
        """It verifies is a given graph is a correct graph without weight following the modeling format of the class 'Graph'
        It raises an error if error == True and just return a bool, else.
        """
        bool1 = all([type(vertex) in {int, str} for vertex in self.Vertices])
        bool2 = all([type(Edge) in {fs, tuple} and len(Edge) in {1, 2} and type(n) == int and n > 0 and all([vertex in self.Vertices for vertex in Edge]) and len(set(Edge)) == len(Edge) for Edge, n in self.Edges.items()])
        if error == False:
            return bool1 and bool2
        assert bool1, f"The structure '{self.Vertices}', containing the vertices of the problematic graph (with weights) has at least one vertex which is neither an int nor a string\n\tRefer to the help of the 'Graph' class"
        assert bool2, f"At least one of the edge of the problematic graph (without weights) is not well defined in '{self.Edges}'\n\tRefer to the help of the 'Graph' class"

    def isNotOriented(self)-> bool:
        """It verifies wheter the graph 'self' is not oriented or not
        A graph is not oriented when all its edges aren't arcs. In this case, its edges are frozensets
        """
        self.isGraph()
        assert self.Vertices != set(), "The porblematic graph is empty"
        return all([type(Edge) == fs for Edge in self.Edges if len(Edge) == 2])

    def isOriented(self)-> bool:
        """It verifies wheter the graph 'self' is oriented or not
        A graph is oriented when all its edges are arcs. In this case, its edges are tuples
        """
        self.isGraph()
        assert self.Vertices != set(), "The porblematic graph is empty"
        return all([type(Edge) == tuple for Edge in self.Edges if len(Edge) == 2])

    def isRelated(self)-> bool:
        """It verifies if self is a related graph or not
        A related graph is a non oriented graph where it is possible from any vertex, to reach the other vertices following the edges.
        """
        assert  self.isNotOriented(), "The problematic graph must be not oriented in order to verify whether it is related or not."
        self = self.simple()
        start = self.Vertices.pop()
        Tested = {start}
        self.Vertices.add(start)
        ToTest = self.Adj(Tested)
        while ToTest != set():
            Tested.update(ToTest)
            ToTest = self.Adj(Tested)
        if Tested == self.Vertices:
            return True
        return False

    def isSimple(self)-> bool:
        """It verifies wheter the graph 'self' is simple or not
        A graph is simple if there is at most one edge between 2 vertices, and no edge that connects a given vertex to itself (loop)
        """
        self.isGraph()
        assert self.Vertices != set(), "The porblematic graph is empty"
        if self.isGraphNoWeight(False):
            for Edge in self.Edges:
                if self.Edges[Edge] > 1 or len(Edge) == 1:
                    return False
            return True 
        for Edge in self.Edges:
            if len(self.Edges[Edge]) > 1 or len(Edge) == 1:
                return False
        return True

    def isStronglyRelated(self)-> bool:
        """It verifies if self is a strongly related graph or not
        A strongly related graph is a graph where it is possible from any vertex, to reach the other vertices following the edges.
        """
        assert self.Vertices != set(), "The porblematic graph is empty"
        self = self.simple(notoriented = False)
        for edge in self.Vertices:
            Tested = {edge}
            ToTest = self.Adj(Tested)
            while ToTest != set():
                Tested.update(ToTest)
                ToTest = self.Adj(Tested)
            if Tested != self.Vertices:
                return False
        return True

    def isTree(self)-> bool:
        """It checks if self is a tree or not
        A tree is a simple related graph without cycle
        """
        assert self.isSimple() and self.isRelated(), "The problematic graph must be a related and simple graph in order to verify whether it is a tree or not."
        Edges = self.Edges.copy()
        start = self.Vertices.pop()
        Tested = {start}
        self.Vertices.add(start)
        l = len(self.Vertices)
        while len(Tested) < l:
            for Edge in Edges.copy().items():
                Edge1 = set(Edge)
                Inter = Edge1 & Tested
                if len(Inter) == 2:
                    return False
                if len(Inter) == 1: 
                    Tested.update(Edge1-Inter)
                    Edges.pop(Edge)
        return True
            
    def isTree2(self)-> bool:
        """It checks if self is a tree or not
        A tree is a simple related graph without cycle
        Rk: this function is more efficent than self.istree(), because it uses the equivalence : 'a graph G of n vertices is a tree if and only if G is related and has n-1 edges 
        """
        assert self.isSimple() and self.isRelated(), "The problematic graph must be a related and simple graph in order to verify whether it is a tree or not."
        return len(self.Vertices) == len(self.Edges)+1
    
    def Krustal(self):
        """It returns a minimum spanning tree of a graph of weights 'self' using the Krustal algorithm principle
        NB: self must be related and should be simple
        """
        self.isGraphWeight()
        assert self.isRelated(), "The problematic graph must be a related graph"
        G = Graph(set(), {})
        InvEdges = [(min(Weights), Edge) for Edge, Weights in self.Edges.items() if len(Edge) == 2]
        InvEdges.sort()
        i = 1
        l = len(self.Vertices) 
        while i < len(self.Vertices):
            weight, Edge = InvEdges[0][0], InvEdges[0][1]
            InvEdges.pop(0)
            try:
                G.Vertices.update(set(Edge))
                G.Edges[Edge] = [weight]
                assert G.isForest() == True
                i += 1
            except  AssertionError:
                G.Edges.pop(Edge)
        G.name = f"{self.name}-Krustal"
        return G

    def minAdj(self, Vertices:dict)-> tuple:
        """It returns the nearest adjacent vertex to a set of vertices 'Vertices' in a graph of weights 'self'
        A such vertex has among the vertices in self but not in Vertices, the smallest total weight from the first added vertex in 'Vertices', which is 'start' in self.Djikstra()
        Rk: The first added vertex in 'Vertices' has the with 0 as 2nd parameter and itself as first parameter. Ex: 'A':('A', 0)
        Also elt of vertex are in the form vertex:(vertex2, dist) where dist is a positive real number.
        """
        self.isGraphWeight()
        assert self.Vertices != set(), "The porblematic graph is empty"
        assert len(Vertices) != 0 and all([vertex in self.Vertices and val[0] in self.Vertices and type(val[1]) in Real and val[1] >= 0 for vertex, val in Vertices.items()]), f"Vertices = {Vertices} must be a non empty subset of self.Vertices, with elts in the form vertex:(vertex2, dist) where dist is a positive real number."
        minadj = nan, nan, inf
        for Edge, Weights in self.Edges.items():
            if len(Edge) == 1:
                continue
            if type(Edge) == fs:
                Edge = set(Edge)
                Inter = Edge & Vertices.keys()
                if len(Inter) == 1:
                    prev = Inter.pop()
                    dist = Vertices[prev][1] + min(Weights)
                    if dist < minadj[2]:
                        minadj = (Edge - {prev}).pop(), prev, dist
            if type(Edge) == tuple and Edge[0] in Vertices and Edge[1] not in Vertices:
                dist = Vertices[Edge[0]][1] + min(Weights)
                if dist < minadj[2]:
                    minadj = Edge[1], Edge[0], dist
        return minadj

    def noWeight(self):
        """It returns a version of a graph of weights where weights are removed"""
        self.isGraphWeight()
        return Graph(self.Vertices.copy(), {Edge: len(Weights) for Edge, Weights in self.Edges.items()}, f"{self.name}-noWeight")

    def printGraph(self, indent:int = 4):
        """It prints in the terminal the essential information of the graph self with indentation of 'indent'"""
        self.isGraph()
        assert type(indent) == int and indent >= 1, f"indent = {indent} must be a strict positive integer"
        print(f'Graph {self.name} :\n\tVertices = {self.Vertices}\n\tEdges ='.expandtabs(indent), '{', end = '')
        i = 1
        l = len(self.Edges)
        for Edge, Weights in self.Edges.items():
            if i != l:
                Sep = ', '
            else:
                Sep = ''
            if type(Edge) == tuple:
                print(f"{Edge}: {Weights}", Sep, end = '')
            else:
                Edge = set(Edge)
                if len(Edge) == 2:
                    print("{'", Edge.pop(), "', '", Edge.pop(), "'}: ", Weights, Sep, sep = '', end = '')
                else:
                    print("{", Edge.pop(), "}: ", Weights, Sep, sep = '', end = '')
            i += 1
        print('}')

    def relatedParts(self)-> list:
        """It returns the indivual related parts of a non oriented graph 'self' in the form of a list
        A related part of self is a related subgraph of self, not contained in another related subgraph of self
        """
        assert self.isNotOriented(), "The problematic graph must be not oriented in order to return its related parts."
        i = 1
        l = len(self.Vertices)
        Parts = []
        Vertices = self.Vertices.copy()
        j = 1
        while i < l:
            Tested = {Vertices.pop()}
            ToTest = self.Adj(Tested)
            while ToTest != set():
                Tested.update(ToTest)
                ToTest = self.Adj(Tested)
            G = self.subGraph(Tested)
            G.name = f"{self.name}-{j}"
            Parts.append(G)
            Vertices -= Tested 
            j += 1
            i += len(Tested)
        return Parts

    def simple(self, loop:bool = False, notoriented:bool = True, multi:bool = False):
        """It returns the simple version of self following the principle of self.isSimple()
        NB: if there are more than 1 edge between 2 vertices, only the one with the smallest weight will be conserved
        if notoriented = False, the fubction doesn't bother about the oriented character of self
        In the opposite case, all arcs are transformed into non oriented edges
        """
        self.isGraph()
        assert self.Vertices != set(), "The porblematic graph is empty"
        assert type(loop) == bool and type(notoriented) == bool and type(multi) == bool
        G = self.graphCopy()
        G.name = f"{self.name}-simple"
        if not notoriented and multi and loop:
            return G
        if notoriented:
            for Edge, val in self.Edges.items():
                if type(Edge) == fs:
                    continue
                Edge2 = fs(Edge)
                if Edge2 not in G.Edges:
                    G.Edges[Edge2] = val
                else:
                    if self.isGraphNoWeight(False):
                        G.Edges[Edge2] += val
                    else:
                        G.Edges[Edge2].extend(val)
                G.Edges.pop(Edge)
        if not multi:
            for Edge, val in G.Edges.copy().items():
                if self.isGraphNoWeight(False):
                    G.Edges[Edge] = 1
                else:
                    G.Edges[Edge] = [min(val)]
        if not loop:
            for Edge in G.Edges.copy():
                if len(Edge) == 1:
                    G.Edges.pop(Edge)
        return G

    def subGraph(self, Vertices:set):
        """It returns a subgraph of self with 'Vertices' as vertices
        Rq: Only the edges that connect vertices of 'Vertices' will be conserved
        """
        self.isGraph()
        assert self.Vertices != set(), "The porblematic graph is empty"
        assert Vertices <= self.Vertices and Vertices != {}, f"Vertices = {Vertices} must be a non empty subset of self.Vertices"
        G = Graph(Vertices.copy(), {}, name = f"{self.name}-subGraph")
        G.Edges = {Edge:val for Edge, val in self.Edges.items() if all([vertex in Vertices for vertex in Edge])}
        return G

if __name__ == "__main__":
    import graph_class
    print("'Graph' is a module full of methods, to easily manipulate and extract information from graphs. Here are some detailed help :")      
    help(graph_class)
    input("Glad to have served you!")
