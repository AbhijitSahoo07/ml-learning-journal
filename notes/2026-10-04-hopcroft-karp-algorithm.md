# Hopcroft-Karp Algorithm

## Overview
The Hopcroft-Karp algorithm is a highly efficient algorithm used to find a **maximum cardinality matching** in a **bipartite graph**. Developed by John Hopcroft and Richard Karp in 1973, it significantly improved upon previous algorithms by achieving a better time complexity. While other algorithms like Ford-Fulkerson can also solve this problem by transforming it into a maximum flow problem, Hopcroft-Karp is specifically optimized for bipartite matching, making it a go-to choice for this particular task. It operates by repeatedly finding a maximal set of shortest augmenting paths.

## What Problem It Solves
The Hopcroft-Karp algorithm addresses the problem of finding a **Maximum Cardinality Bipartite Matching**. Let's break down what that means:

1.  **Bipartite Graph**: A graph where the vertices can be divided into two disjoint sets, say `U` and `V`, such that every edge connects a vertex in `U` to one in `V`. There are no edges within `U` or within `V`. Think of it like two distinct groups, and connections only happen *between* the groups, not *within* them.

2.  **Matching**: In a graph, a matching is a set of edges where no two edges share a common vertex. If an edge `(u, v)` is in the matching, then `u` and `v` are said to be "matched."

3.  **Cardinality**: This refers to the number of edges in the matching.

4.  **Maximum Cardinality Matching**: The goal is to find a matching that contains the largest possible number of edges. This means we want to pair up as many vertices as possible without any vertex being part of more than one pair.

For example, if you have a set of job applicants (U) and a set of available jobs (V), and an edge exists if an applicant is qualified for a job, a maximum cardinality matching would pair the maximum number of applicants with jobs such that each applicant gets at most one job and each job is filled by at most one applicant.

## How It Works
The Hopcroft-Karp algorithm works in phases, iteratively improving the current matching until a maximum matching is found. Each phase consists of two main steps:

1.  **Breadth-First Search (BFS) for Layering**:
    *   Starting from all unmatched vertices in set `U`, a BFS is performed.
    *   The BFS explores alternating paths: unmatched edges, then matched edges, then unmatched edges, and so on.
    *   The goal is to build "layers" of vertices, where each layer represents the shortest distance from an unmatched vertex in `U` to other vertices, considering the alternating path structure.
    *   This BFS stops when it finds the first unmatched vertex in set `V` (or if no such vertex is reachable). The paths found up to this point are the "shortest augmenting paths." An augmenting path is a path that starts and ends with unmatched vertices and alternates between unmatched and matched edges.

2.  **Depth-First Search (DFS) for Augmenting Paths**:
    *   Once the layers are established by BFS, a series of DFS traversals are performed.
    *   The DFS starts from unmatched vertices in `U` and tries to find *disjoint* augmenting paths using only edges that follow the layering established by the BFS (i.e., paths of the shortest possible length).
    *   "Disjoint" here means vertex-disjoint paths.
    *   For each augmenting path found, the matching is updated by "flipping" the edges along the path: matched edges become unmatched, and unmatched edges become matched. This increases the size of the matching by one.
    *   This DFS step continues until no more disjoint shortest augmenting paths can be found within the current layers.

These two steps (BFS and DFS) constitute one phase. The algorithm repeats these phases. A crucial property is that in each subsequent phase, the length of the shortest augmenting path found will be strictly greater than in the previous phase. This property ensures that the algorithm terminates quickly.

## Mathematical Intuition
The core mathematical intuition behind Hopcroft-Karp lies in the concept of **augmenting paths** and their lengths.

Let $M$ be a matching in a bipartite graph $G = (U \cup V, E)$. An **augmenting path** with respect to $M$ is a path that starts and ends at unmatched vertices and alternates between edges not in $M$ and edges in $M$. If we "flip" the edges along an augmenting path (i.e., remove matched edges and add unmatched edges), the size of the matching increases by one.

The algorithm's efficiency comes from finding a **maximal set of shortest augmenting paths** in each phase.
Let $k$ be the length of the shortest augmenting path in a given phase.
The algorithm guarantees that all augmenting paths found in a single phase are of length $k$.
After a phase, the length of the shortest augmenting path in the residual graph (with respect to the new matching) will be strictly greater than $k$.

The time complexity of Hopcroft-Karp is $O(E\sqrt{V})$, where $V$ is the number of vertices and $E$ is the number of edges. This is derived from:
*   There are at most $2\sqrt{V}$ phases. This is a key theoretical result by Hopcroft and Karp.
*   Each phase involves one BFS ($O(E+V)$) and multiple DFS traversals. The total work for DFS in one phase is also $O(E+V)$ because each edge and vertex is visited a constant number of times across all DFS calls within that phase.
*   Thus, the total time complexity is $O(\sqrt{V} \cdot (E+V))$. Since $E$ can be up to $V^2$, and $V$ is typically less than $E$ in connected graphs, this simplifies to $O(E\sqrt{V})$.

## Advantages
*   **Optimal Time Complexity**: For general bipartite graphs, Hopcroft-Karp's $O(E\sqrt{V})$ time complexity is asymptotically optimal, making it one of the fastest known algorithms for this problem.
*   **Efficiency in Practice**: Despite its theoretical complexity, it performs very well in practice for many types of graphs.
*   **Specific Optimization**: It is specifically designed for bipartite matching, unlike general max-flow algorithms which can be overkill for this particular problem.

## Disadvantages
*   **Complexity of Implementation**: Compared to simpler augmenting path algorithms (like those based on Ford-Fulkerson on a flow network), Hopcroft-Karp is more complex to implement due to the layered BFS and multiple DFS traversals per phase.
*   **Not Always the Fastest for Sparse Graphs**: For very sparse graphs, a simpler DFS-based augmenting path algorithm might perform comparably or even faster in practice due to lower constant factors, though its worst-case complexity is higher.
*   **Limited Scope**: It is specialized for bipartite graphs. For general graphs, other algorithms like Edmonds' blossom algorithm are required for maximum matching.

## Real World Applications
1.  **Job Assignment/Resource Allocation**: Matching employees to tasks, students to projects, or resources to demands, where each entity can only be assigned once. For instance, assigning a set of interns (U) to a set of available projects (V) based on their skills and project requirements.
2.  **DNA Sequencing and Genomics**: In bioinformatics, finding overlaps between DNA fragments (reads) to reconstruct a longer DNA sequence can sometimes be modeled as a matching problem, particularly in scenarios involving paired-end reads.
3.  **Image Processing (Stereo Matching)**: In computer vision, finding correspondences between pixels in two images taken from slightly different viewpoints (stereo images) to reconstruct 3D information. This can be formulated as a matching problem on a grid-like bipartite graph.

## Python Example
Here's a simplified Python implementation of the Hopcroft-Karp algorithm. Note that a full, robust implementation can be quite involved. This example focuses on the core BFS and DFS logic.

```python
class HopcroftKarp:
    def __init__(self, graph_u_to_v):
        """
        Initializes the Hopcroft-Karp algorithm.
        graph_u_to_v: A dictionary representing the bipartite graph.
                      Keys are vertices in set U, values are lists of adjacent vertices in set V.
        """
        self.graph = graph_u_to_v
        self.U = list(graph_u_to_v.keys())
        self.V = []
        for u in self.U:
            for v in self.graph[u]:
                if v not in self.V:
                    self.V.append(v)
        
        self.matchU = {} # Stores matching for U: matchU[u] = v
        self.matchV = {} # Stores matching for V: matchV[v] = u
        self.dist = {}   # Stores distances for BFS layering

    def bfs(self):
        """
        Performs BFS to build layers and find shortest augmenting paths.
        Returns True if an augmenting path is found, False otherwise.
        """
        queue = []
        for u in self.U:
            if u not in self.matchU: # If u is unmatched
                self.dist[u] = 0
                queue.append(u)
            else:
                self.dist[u] = float('inf')
        
        self.dist[None] = float('inf') # Sentinel for V-side unmatched vertices

        head = 0
        while head < len(queue):
            u = queue[head]
            head += 1

            if self.dist[u] < self.dist[None]:
                for v in self.graph[u]:
                    if v not in self.matchV: # v is unmatched
                        if self.dist[None] == float('inf'): # First time we reach an unmatched V
                            self.dist[None] = self.dist[u] + 1
                    elif self.dist.get(self.matchV[v], float('inf')) == float('inf'):
                        # If matchV[v] (the U-vertex matched with v) hasn't been visited
                        self.dist[self.matchV[v]] = self.dist[u] + 1
                        queue.append(self.matchV[v])
        
        return self.dist[None] != float('inf')

    def dfs(self, u):
        """
        Performs DFS to find an augmenting path starting from u.
        Returns True if an augmenting path is found and matching is updated, False otherwise.
        """
        if u is None:
            return True
        
        for v in self.graph[u]:
            # Check if v is part of a shortest augmenting path layer
            # If v is unmatched, or if matchV[v] is in the next layer
            if (v not in self.matchV and self.dist[None] == self.dist[u] + 1) or \
               (v in self.matchV and self.dist.get(self.matchV[v], float('inf')) == self.dist[u] + 1):
                
                # If we can find an augmenting path from matchV[v]
                if self.dfs(self.matchV.get(v, None)):
                    self.matchV[v] = u
                    self.matchU[u] = v
                    return True
        
        self.dist[u] = float('inf') # Mark u as visited for this DFS phase
        return False

    def find_max_matching(self):
        """
        Main function to find the maximum cardinality bipartite matching.
        """
        matching_size = 0
        while self.bfs(): # While there are shortest augmenting paths
            for u in self.U:
                if u not in self.matchU: # If u is unmatched
                    if self.dfs(u):
                        matching_size += 1
        return matching_size, self.matchU

# Example Usage:
# Graph: U = {A, B, C}, V = {1, 2, 3}
# A connects to 1, 2
# B connects to 1
# C connects to 2, 3
graph = {
    'A': ['1', '2'],
    'B': ['1'],
    'C': ['2', '3']
}

hk = HopcroftKarp(graph)
max_matching_size, matching = hk.find_max_matching()

print(f"Maximum Matching Size: {max_matching_size}")
print("Matching:")
for u, v in matching.items():
    print(f"  {u} -- {v}")

# Expected Output:
# Maximum Matching Size: 3
# Matching:
#   A -- 1 (or A -- 2, depending on path choice)
#   B -- ? (if A--1, then B cannot match 1)
#   C -- ?
# Let's trace:
# Initial: M = {}
# Phase 1:
# BFS from A, B, C.
# dist[A]=0, dist[B]=0, dist[C]=0
# A->1, A->2
# B->1
# C->2, C->3
# Shortest augmenting paths of length 1 (e.g., A-1, B-1, C-2, C-3)
# DFS:
# Try A: A-1. Match A-1. M = {A-1}
# Try B: B is unmatched. B-1 is not possible (1 is matched to A).
# Try C: C is unmatched. C-2. Match C-2. M = {A-1, C-2}
# Try C: C-3. Match C-3. M = {A-1, C-3} (if C-2 was not taken)
# This is where the disjoint paths logic is crucial.
# Let's assume A-1, C-2 are found. Matching size = 2.
# Phase 2:
# BFS from B (unmatched).
# B->1 (matched). matchV[1] = A. dist[A] = dist[B]+1.
# A->2 (matched). matchV[2] = C. dist[C] = dist[A]+1.
# C->3 (unmatched). dist[None] = dist[C]+1.
# Shortest augmenting path: B-1-A-2-C-3 (length 5).
# DFS:
# Try B: B-1-A-2-C-3. Flip. M = {B-1, A-2, C-3}. Matching size = 3.
# No more augmenting paths.
# Final matching: {B-1, A-2, C-3} (or similar permutation)
```

## Interview Questions
1.  **What is the time complexity of Hopcroft-Karp, and why is it considered an improvement over a general max-flow algorithm for bipartite matching?**
    *   **Answer**: The time complexity of Hopcroft-Karp is $O(E\sqrt{V})$. It's an improvement because a general max-flow algorithm (like Edmonds-Karp) on a constructed flow network for bipartite matching would have a complexity of $O(VE^2)$ or $O(V^2E)$ depending on implementation, which is generally worse than $O(E\sqrt{V})$. Hopcroft-Karp is specifically optimized for the bipartite structure, allowing it to find augmenting paths more efficiently in phases.

2.  **Explain the concept of "phases" in the Hopcroft-Karp algorithm. What is the significance of finding "shortest" augmenting paths?**
    *   **Answer**: A "phase" in Hopcroft-Karp consists of two steps: a BFS to find layers of vertices representing shortest augmenting paths, followed by multiple DFS traversals to find a maximal set of vertex-disjoint augmenting paths within those layers. The significance of finding *shortest* augmenting paths is crucial for the algorithm's efficiency. By only considering shortest paths in each phase, the algorithm guarantees that the length of the shortest augmenting path strictly increases in successive phases. This property limits the total number of phases to $O(\sqrt{V})$, which is key to its optimal time complexity.

3.  **How does Hopcroft-Karp guarantee finding a maximum matching, not just any matching?**
    *   **Answer**: Hopcroft-Karp guarantees a maximum matching based on Berge's Lemma, which states that a matching $M$ is maximum if and only if there are no $M$-augmenting paths. The algorithm iteratively finds and applies augmenting paths. Each time an augmenting path is found and "flipped," the size of the matching increases by one. The algorithm continues this process until no more augmenting paths can be found (i.e., the `bfs` function returns `False`). At this point, by Berge's Lemma, the current matching must be a maximum cardinality matching.

## Quiz
1.  The Hopcroft-Karp algorithm is primarily used to find a maximum cardinality matching in what type of graph?
    a) Directed Acyclic Graph (DAG)
    b) Weighted Graph
    c) Bipartite Graph
    d) Complete Graph

    **Answer**: c) Bipartite Graph

2.  What is the typical time complexity of the Hopcroft-Karp algorithm for a graph with $V$ vertices and $E$ edges?
    a) $O(V^3)$
    b) $O(E \log V)$
    c) $O(E\sqrt{V})$
    d) $O(V+E)$

    **Answer**: c) $O(E\sqrt{V})$

## Further Reading
1.  **Wikipedia - Hopcroft-Karp algorithm**: [https://en.wikipedia.org/wiki/Hopcroft%E2%80%93Karp_algorithm](https://en.wikipedia.org/wiki/Hopcroft%E2%80%93Karp_algorithm)
2.  **GeeksforGeeks - Hopcroft-Karp Algorithm for Maximum Matching**: [https://www.geeksforgeeks.org/hopcroft-karp-algorithm-for-maximum-matching/](https://www.geeksforgeeks.org/hopcroft-karp-algorithm-for-maximum-matching/)
3.  **Introduction to Algorithms (CLRS)**: Chapter on Maximum Bipartite Matching (often found in the Network Flow section). This textbook provides a rigorous mathematical treatment.