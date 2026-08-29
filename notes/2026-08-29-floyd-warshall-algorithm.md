# Floyd-Warshall Algorithm

## Overview
The Floyd-Warshall Algorithm is a powerful and elegant algorithm used to find the shortest paths between *all pairs* of vertices in a weighted graph. It's a prime example of dynamic programming, where a complex problem is broken down into simpler subproblems, and their solutions are combined to solve the larger problem. Unlike algorithms like Dijkstra's or Bellman-Ford, which find the shortest paths from a *single source* to all other vertices, Floyd-Warshall computes the shortest path for every possible source-destination pair simultaneously. It can handle graphs with both positive and negative edge weights, but it cannot handle graphs containing negative cycles (a cycle where the sum of edge weights is negative), as such cycles would lead to infinitely decreasing path lengths.

## What Problem It Solves
The Floyd-Warshall Algorithm primarily solves the **All-Pairs Shortest Path (APSP)** problem. This problem asks: "What is the shortest path from every vertex $u$ to every other vertex $v$ in a given graph?"

Why is this needed in machine learning?
*   **Graph-based Machine Learning**: Many machine learning problems can be modeled as graphs. For instance, in social networks, we might want to find the shortest "connection" path between any two users. In knowledge graphs, finding relationships between entities often involves pathfinding.
*   **Clustering and Similarity**: Shortest path distances can be used as a measure of similarity or dissimilarity between nodes. If two nodes are "close" in terms of shortest path, they might belong to the same cluster or share similar properties.
*   **Network Analysis**: In recommendation systems or anomaly detection, understanding the shortest paths between different items or users can reveal underlying structures or unusual behaviors.
*   **Transitive Closure**: A related problem is finding the transitive closure of a graph, which determines if there's *any* path (not necessarily shortest) between all pairs of vertices. Floyd-Warshall can be adapted for this.
*   **Reinforcement Learning**: In some grid-world or state-space problems, finding optimal paths between all states can be a pre-computation step for policy evaluation.

While other algorithms like running Dijkstra's from every node can also solve APSP (if no negative weights), Floyd-Warshall offers a clean dynamic programming approach that naturally handles negative weights (without negative cycles) and is often simpler to implement for dense graphs.

## How It Works
The Floyd-Warshall algorithm works by iteratively improving estimates of the shortest path between all pairs of vertices. It considers each vertex in the graph as a potential "intermediate" vertex on the path between any two other vertices.

Let's break down the mechanism step-by-step:

1.  **Initialization**:
    *   Create a distance matrix, let's call it `dist`, of size $V \times V$, where $V$ is the number of vertices in the graph.
    *   Initialize `dist[i][j]` with the direct edge weight from vertex $i$ to vertex $j$.
    *   If there is no direct edge between $i$ and $j$, set `dist[i][j]` to infinity ($\infty$).
    *   Set `dist[i][i]` to 0 for all vertices $i$ (the distance from a vertex to itself is zero).

2.  **Iteration through Intermediate Vertices**:
    *   The core of the algorithm involves three nested loops. The outermost loop iterates through each vertex $k$ from $0$ to $V-1$. This vertex $k$ is considered as a potential *intermediate* vertex.
    *   For each such $k$, the algorithm then iterates through every possible pair of source vertices $i$ (from $0$ to $V-1$) and destination vertices $j$ (from $0$ to $V-1$).

3.  **Path Relaxation (Update Rule)**:
    *   Inside the innermost loop, for each pair $(i, j)$, the algorithm checks if the path from $i$ to $j$ can be shortened by going through the current intermediate vertex $k$.
    *   The update rule is: `dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])`.
    *   This means: the shortest path from $i$ to $j$ is either the path we already found (without using $k$ as an intermediate vertex) OR the path that goes from $i$ to $k$ and then from $k$ to $j$. We take the minimum of these two options.

4.  **Final Result**:
    *   After iterating through all possible intermediate vertices $k$, the `dist` matrix will contain the shortest path distances between all pairs of vertices.

**Example Walkthrough Idea:**
Imagine you have three cities A, B, C.
*   Initially, you know direct routes: A to B is 5, B to C is 2, A to C is 10.
*   **k = A**: Can A be an intermediate? No, because we're looking for paths *through* A, not starting or ending at A. (This is a slight simplification for intuition; in the algorithm, $k$ is just an intermediate node, not necessarily the start/end).
*   **k = B**:
    *   Consider path A to C. Current `dist[A][C]` is 10.
    *   Is `dist[A][B] + dist[B][C]` shorter? $5 + 2 = 7$.
    *   Since $7 < 10$, update `dist[A][C]` to 7.
*   **k = C**:
    *   Consider path A to B. Current `dist[A][B]` is 5.
    *   Is `dist[A][C] + dist[C][B]` shorter? (Assume C to B is 3). $7 + 3 = 10$.
    *   Since $10 > 5$, `dist[A][B]` remains 5.

This iterative process ensures that by the time all vertices have been considered as intermediate nodes, the `dist[i][j]` value will hold the true shortest path between $i$ and $j$.

## Mathematical Intuition
The Floyd-Warshall algorithm is a classic example of dynamic programming. Let's define the state and recurrence relation.

Let $V$ be the number of vertices in the graph, indexed from $0$ to $V-1$.
Let $w(i, j)$ be the weight of the direct edge from vertex $i$ to vertex $j$. If there is no direct edge, $w(i, j) = \infty$. If $i=j$, $w(i, j) = 0$.

We define $D_k(i, j)$ as the shortest path distance from vertex $i$ to vertex $j$ such that all intermediate vertices on the path are chosen from the set $\{0, 1, \dots, k-1\}$.

**Base Case:**
For $k=0$, $D_0(i, j)$ represents the shortest path from $i$ to $j$ using no intermediate vertices. This means it's either the direct edge weight or infinity if no direct edge exists.
$$D_0(i, j) = w(i, j)$$
This initializes our distance matrix.

**Recurrence Relation:**
Now, consider how to compute $D_k(i, j)$ from $D_{k-1}(i, j)$. When we consider vertex $k$ as a potential intermediate vertex, there are two possibilities for the shortest path from $i$ to $j$ using intermediate vertices from $\{0, 1, \dots, k-1\}$:

1.  The shortest path from $i$ to $j$ does *not* use vertex $k$ as an intermediate vertex. In this case, the shortest path distance is simply $D_{k-1}(i, j)$.
2.  The shortest path from $i$ to $j$ *does* use vertex $k$ as an intermediate vertex. If it does, then this path can be broken down into two segments:
    *   A shortest path from $i$ to $k$ using intermediate vertices from $\{0, 1, \dots, k-1\}$. The length of this path is $D_{k-1}(i, k)$.
    *   A shortest path from $k$ to $j$ using intermediate vertices from $\{0, 1, \dots, k-1\}$. The length of this path is $D_{k-1}(k, j)$.
    The total length of this path would be $D_{k-1}(i, k) + D_{k-1}(k, j)$.

Combining these two possibilities, the shortest path $D_k(i, j)$ is the minimum of these two options:
$$D_k(i, j) = \min(D_{k-1}(i, j), D_{k-1}(i, k) + D_{k-1}(k, j))$$

This recurrence relation is applied for all $k$ from $0$ to $V-1$, and for all pairs $(i, j)$.
After the outermost loop completes (i.e., after $k$ reaches $V-1$), $D_V(i, j)$ will contain the shortest path distance from $i$ to $j$ using any vertex from $\{0, 1, \dots, V-1\}$ as an intermediate vertex. This means $D_V(i, j)$ is the true all-pairs shortest path distance.

**Negative Cycle Detection:**
The algorithm can also detect negative cycles. If, after all iterations, any $D_V(i, i)$ (distance from a vertex to itself) is found to be negative, it implies that there is a negative cycle reachable from $i$ and $i$ is part of it. This is because a path from $i$ to $i$ should ideally be 0. If it's negative, it means we can keep traversing the cycle to get an arbitrarily small (large negative) path length, which is undefined for shortest path problems.

## Advantages
*   **All-Pairs Shortest Path**: It efficiently computes the shortest paths between all pairs of vertices in a single run.
*   **Handles Negative Edge Weights**: Unlike Dijkstra's algorithm, Floyd-Warshall can correctly find shortest paths in graphs with negative edge weights, as long as there are no negative cycles.
*   **Simplicity**: The algorithm is relatively straightforward to understand and implement due to its simple triple-nested loop structure.
*   **Dynamic Programming**: It leverages dynamic programming principles, building up solutions to larger problems from solutions to smaller subproblems.
*   **Detects Negative Cycles**: It can detect the presence of negative cycles in the graph, which is crucial for understanding graph properties.

## Disadvantages
*   **High Time Complexity**: The time complexity is $O(V^3)$, where $V$ is the number of vertices. This makes it unsuitable for very large graphs. For sparse graphs, running a single-source shortest path algorithm (like Dijkstra's with a Fibonacci heap) from each vertex might be faster ($O(V(E + V \log V))$ or $O(VE \log V)$).
*   **High Space Complexity**: The space complexity is $O(V^2)$ to store the distance matrix. For very large graphs, this can be a significant memory requirement.
*   **Cannot Handle Negative Cycles Correctly**: While it can *detect* negative cycles, it cannot provide meaningful shortest path distances if negative cycles exist, as path lengths could become infinitely negative.
*   **Dense Graph Preference**: It performs best on dense graphs (graphs with many edges) where $E \approx V^2$. For sparse graphs, other algorithms might be more efficient.
*   **No Path Reconstruction (Directly)**: The basic algorithm only computes the shortest distances. To reconstruct the actual paths, an additional predecessor matrix needs to be maintained, increasing complexity slightly.

## Real World Applications
1.  **Route Planning and GPS Navigation**:
    *   **Application**: Finding the shortest driving distance or travel time between any two locations in a city or region.
    *   **How it's used**: Cities and roads can be modeled as a graph where intersections are vertices and roads are edges with weights representing distance or time. Floyd-Warshall can pre-compute the shortest paths between all major intersections, allowing for quick query responses in navigation systems.
2.  **Network Routing**:
    *   **Application**: Determining the most efficient path for data packets to travel across a computer network (e.g., the internet, local area networks).
    *   **How it's used**: Routers are vertices, and network links are edges with weights representing latency, bandwidth, or cost. Floyd-Warshall can help routers build routing tables that specify the optimal next hop for any destination, minimizing packet travel time or maximizing throughput.
3.  **Transitive Closure of Graphs**:
    *   **Application**: In databases or knowledge graphs, determining reachability between entities. For example, "Is A related to C through any chain of relationships?"
    *   **How it's used**: By modifying the Floyd-Warshall algorithm to use boolean operations (AND for addition, OR for minimum), it can compute the transitive closure. If `dist[i][j]` becomes `True`, it means there is a path from $i$ to $j$. This is useful in dependency analysis, access control, or inferring relationships.
4.  **Computational Biology (Sequence Alignment)**:
    *   **Application**: Finding similarities between DNA or protein sequences.
    *   **How it's used**: While more complex algorithms like Smith-Waterman are often used, the underlying dynamic programming principles are similar to Floyd-Warshall. In some simplified models, finding optimal alignments can be framed as finding shortest paths in a specially constructed graph where nodes represent states in the alignment process and edge weights represent penalties or scores for matches/mismatches.
5.  **Social Network Analysis**:
    *   **Application**: Understanding influence, centrality, or information flow in social networks.
    *   **How it's used**: Users are vertices, and connections are edges. Floyd-Warshall can compute the shortest path (e.g., "degrees of separation") between any two users. This information can be used to identify influential users (those with short paths to many others), community structures, or how information might spread.

## Python Example

This example demonstrates the Floyd-Warshall algorithm using a simple adjacency matrix representation for a graph.

```python
import numpy as np

def floyd_warshall(graph):
    """
    Implements the Floyd-Warshall algorithm to find all-pairs shortest paths.

    Args:
        graph (list of lists): An adjacency matrix representation of the graph.
                               graph[i][j] is the weight of the edge from i to j.
                               Use float('inf') for no direct edge, and 0 for i to i.

    Returns:
        numpy.ndarray: A matrix where result[i][j] is the shortest path distance
                       from vertex i to vertex j.
                       Returns None if a negative cycle is detected.
    """
    num_vertices = len(graph)
    
    # Initialize the distance matrix with the given graph weights
    # We use a copy to avoid modifying the original graph
    dist = np.array(graph, dtype=float) 

    # Main loop: Iterate through all possible intermediate vertices 'k'
    # k represents the intermediate vertex in the path from i to j
    for k in range(num_vertices):
        # Iterate through all possible source vertices 'i'
        for i in range(num_vertices):
            # Iterate through all possible destination vertices 'j'
            for j in range(num_vertices):
                # If vertex k is on the shortest path from i to j, then update the value of dist[i][j]
                # dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
                if dist[i][k] != float('inf') and dist[k][j] != float('inf'): # Avoid overflow with infinity
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    
    # Check for negative cycles
    # If dist[i][i] is negative for any i, then a negative cycle exists
    for i in range(num_vertices):
        if dist[i][i] < 0:
            print(f"Negative cycle detected involving vertex {i}. Shortest paths are undefined.")
            return None # Or raise an error, depending on desired behavior

    return dist

# --- Example Usage ---
if __name__ == "__main__":
    # Define a graph as an adjacency matrix
    # float('inf') represents no direct edge
    # 0 represents distance from a node to itself
    
    # Example 1: Simple graph with positive weights
    graph1 = [
        [0,   3,   float('inf'), 7],
        [8,   0,   2,   float('inf')],
        [5,   float('inf'), 0,   1],
        [2,   float('inf'), float('inf'), 0]
    ]
    
    print("--- Graph 1 (Positive Weights) ---")
    print("Initial Adjacency Matrix:")
    for row in graph1:
        print([f"{x if x != float('inf') else 'inf':<5}" for x in row])

    shortest_paths1 = floyd_warshall(graph1)
    if shortest_paths1 is not None:
        print("\nAll-Pairs Shortest Paths Matrix:")
        for row in shortest_paths1:
            print([f"{x if x != float('inf') else 'inf':<5.1f}" for x in row])
    print("-" * 40)

    # Example 2: Graph with negative weights (no negative cycle)
    graph2 = [
        [0,   1,   float('inf'), float('inf')],
        [float('inf'), 0,   -1,  float('inf')],
        [float('inf'), float('inf'), 0,   -1],
        [-1,  float('inf'), float('inf'), 0]
    ]

    print("\n--- Graph 2 (Negative Weights, No Negative Cycle) ---")
    print("Initial Adjacency Matrix:")
    for row in graph2:
        print([f"{x if x != float('inf') else 'inf':<5}" for x in row])

    shortest_paths2 = floyd_warshall(graph2)
    if shortest_paths2 is not None:
        print("\nAll-Pairs Shortest Paths Matrix:")
        for row in shortest_paths2:
            print([f"{x if x != float('inf') else 'inf':<5.1f}" for x in row])
    print("-" * 40)

    # Example 3: Graph with a negative cycle
    graph3 = [
        [0,   1,   float('inf')],
        [float('inf'), 0,   -2],
        [-1,  float('inf'), 0]
    ]

    print("\n--- Graph 3 (With Negative Cycle) ---")
    print("Initial Adjacency Matrix:")
    for row in graph3:
        print([f"{x if x != float('inf') else 'inf':<5}" for x in row])

    shortest_paths3 = floyd_warshall(graph3)
    if shortest_paths3 is not None:
        print("\nAll-Pairs Shortest Paths Matrix:")
        for row in shortest_paths3:
            print([f"{x if x != float('inf') else 'inf':<5.1f}" for x in row])
    print("-" * 40)
```

**Explanation of the Code:**
1.  **`floyd_warshall(graph)` function**:
    *   Takes an adjacency matrix `graph` as input. `graph[i][j]` is the direct weight from `i` to `j`. `float('inf')` signifies no direct edge, and `0` for `i` to `i`.
    *   `num_vertices` is determined from the size of the input matrix.
    *   `dist = np.array(graph, dtype=float)`: A NumPy array `dist` is initialized as a copy of the input graph. This matrix will store the shortest path distances. Using `float` ensures `inf` values are handled correctly.
    *   **Outer loop (`for k in range(num_vertices)`)**: This loop iterates through each vertex `k`, considering it as an intermediate vertex.
    *   **Middle loop (`for i in range(num_vertices)`)**: This loop iterates through all possible source vertices `i`.
    *   **Inner loop (`for j in range(num_vertices)`)**: This loop iterates through all possible destination vertices `j`.
    *   **`if dist[i][k] != float('inf') and dist[k][j] != float('inf')`**: This check is crucial to prevent `float('inf') + x` from potentially becoming `float('inf')` and then being compared to a finite number, or to prevent `inf + (-inf)` which results in `nan`. We only consider paths through `k` if both segments (`i` to `k` and `k` to `j`) are reachable.
    *   **`dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])`**: This is the core dynamic programming step. It updates the shortest path from `i` to `j` if a shorter path is found by going through `k`.
    *   **Negative Cycle Detection**: After all iterations, the algorithm checks if `dist[i][i]` is less than 0 for any vertex `i`. If it is, a negative cycle exists, and the function prints a message and returns `None`.
    *   Finally, the `dist` matrix containing all-pairs shortest paths is returned.
2.  **Example Usage (`if __name__ == "__main__":`)**:
    *   Three example graphs are provided: one with positive weights, one with negative weights but no negative cycle, and one with a negative cycle.
    *   The initial adjacency matrix and the resulting shortest path matrix (or negative cycle detection message) are printed for each example.

## Interview Questions

1.  **What is the Floyd-Warshall Algorithm, and what problem does it solve?**
    *   **Answer**: The Floyd-Warshall Algorithm is a dynamic programming algorithm used to find the shortest paths between *all pairs* of vertices in a weighted graph. It solves the All-Pairs Shortest Path (APSP) problem.

2.  **Explain the core idea behind Floyd-Warshall using dynamic programming.**
    *   **Answer**: The core idea is to build up the solution iteratively. It defines $D_k(i, j)$ as the shortest path from $i$ to $j$ using only intermediate vertices from the set $\{0, 1, \dots, k-1\}$. The recurrence relation is $D_k(i, j) = \min(D_{k-1}(i, j), D_{k-1}(i, k) + D_{k-1}(k, j))$. This means the shortest path from $i$ to $j$ either doesn't use $k$ as an intermediate vertex (and thus is $D_{k-1}(i, j)$) or it does use $k$ (and thus is $D_{k-1}(i, k) + D_{k-1}(k, j)$). By iterating $k$ from $0$ to $V-1$, we eventually consider all possible intermediate vertices.

3.  **What are the time and space complexities of the Floyd-Warshall Algorithm?**
    *   **Answer**:
        *   **Time Complexity**: $O(V^3)$, where $V$ is the number of vertices. This is due to the three nested loops, each iterating $V$ times.
        *   **Space Complexity**: $O(V^2)$ to store the distance matrix. An additional $O(V^2)$ might be needed to store a predecessor matrix for path reconstruction.

4.  **Can Floyd-Warshall handle negative edge weights? What about negative cycles?**
    *   **Answer**: Yes, Floyd-Warshall can handle negative edge weights correctly. However, it cannot handle graphs that contain negative cycles. If a negative cycle exists, the shortest path becomes undefined (infinitely negative). The algorithm can detect negative cycles if, after all iterations, the distance from a vertex to itself ($D_V(i, i)$) is found to be negative.

5.  **How does Floyd-Warshall compare to running Dijkstra's algorithm from every vertex to solve the All-Pairs Shortest Path problem?**
    *   **Answer**:
        *   **Dijkstra's (repeatedly)**: If all edge weights are non-negative, running Dijkstra's from each vertex takes $V \times O(E \log V)$ with a binary heap or $V \times O(E + V \log V)$ with a Fibonacci heap. This can be faster for sparse graphs ($E \ll V^2$). It cannot handle negative weights.
        *   **Floyd-Warshall**: Has a fixed $O(V^3)$ complexity, regardless of graph sparsity. It can handle negative weights (without negative cycles). For dense graphs ($E \approx V^2$), $O(V^3)$ might be comparable or even better than repeated Dijkstra's.

6.  **How does Floyd-Warshall detect negative cycles?**
    *   **Answer**: After the algorithm completes all $V$ iterations (i.e., after considering all vertices as intermediate nodes), if the shortest path distance from any vertex $i$ to itself (`dist[i][i]`) is found to be negative, it indicates the presence of a negative cycle that includes vertex $i$. A path from a vertex to itself should ideally be 0; a negative value implies that traversing a cycle can reduce the path length indefinitely.

7.  **Can the Floyd-Warshall algorithm be modified to reconstruct the actual shortest paths, not just their lengths? If so, how?**
    *   **Answer**: Yes, it can. To reconstruct paths, an additional $V \times V$ `predecessor` matrix (or `path` matrix) is maintained. `predecessor[i][j]` stores the vertex that comes *before* $j$ on the shortest path from $i$. When `dist[i][j]` is updated via `k` (i.e., `dist[i][k] + dist[k][j]` is shorter), `predecessor[i][j]` is updated to `predecessor[k][j]`. The path can then be reconstructed by backtracking from the destination to the source using this predecessor matrix.

8.  **In what scenarios would you prefer Floyd-Warshall over other shortest path algorithms like Bellman-Ford or Dijkstra's?**
    *   **Answer**:
        *   When you need to find shortest paths between *all pairs* of vertices.
        *   When the graph contains negative edge weights (but no negative cycles).
        *   For dense graphs where $V^3$ complexity is acceptable or competitive.
        *   When simplicity of implementation is a priority.

9.  **What are the main limitations of the Floyd-Warshall algorithm?**
    *   **Answer**: Its primary limitations are its high time complexity ($O(V^3)$) and space complexity ($O(V^2)$), making it impractical for very large graphs. It also cannot provide meaningful shortest paths in the presence of negative cycles, only detect them.

10. **Describe a real-world application where Floyd-Warshall would be suitable.**
    *   **Answer**: A classic application is in **GPS navigation systems** for route planning. If we model cities as vertices and roads as edges with weights representing travel time or distance, Floyd-Warshall can pre-compute the shortest paths between all major intersections or points of interest. This allows the navigation system to quickly retrieve the optimal route between any two user-specified locations without re-calculating paths on the fly, especially useful for systems with fixed road networks.

## Quiz

1.  The Floyd-Warshall algorithm is used to solve which problem?
    A) Single-Source Shortest Path
    B) Minimum Spanning Tree
    C) All-Pairs Shortest Path
    D) Maximum Flow

2.  What is the time complexity of the Floyd-Warshall algorithm for a graph with $V$ vertices?
    A) $O(V^2)$
    B) $O(V \log V)$
    C) $O(V^3)$
    D) $O(E + V \log V)$

3.  Which of the following statements about Floyd-Warshall and negative edge weights is true?
    A) It cannot handle negative edge weights at all.
    B) It can handle negative edge weights but not negative cycles.
    C) It can handle negative cycles by finding the shortest path through them.
    D) It only works for graphs with strictly positive edge weights.

4.  The core dynamic programming recurrence relation for Floyd-Warshall is $D_k(i, j) = \min(D_{k-1}(i, j), \dots)$. What completes this relation?
    A) $D_{k-1}(i, j) + D_{k-1}(k, j)$
    B) $D_{k-1}(i, k) + D_{k-1}(k, j)$
    C) $D_{k}(i, k) + D_{k}(k, j)$
    D) $D_{k-1}(i, k) \times D_{k-1}(k, j)$

5.  How does the Floyd-Warshall algorithm detect a negative cycle?
    A) By checking if any edge weight is negative.
    B) By checking if the total number of edges is less than $V-1$.
    C) By checking if `dist[i][i]` is negative for any vertex `i` after all iterations.
    D) It cannot detect negative cycles; it will loop indefinitely.

---

### Answer Key

1.  **C) All-Pairs Shortest Path**
    *   **Explanation**: Floyd-Warshall is specifically designed to find the shortest paths between every possible pair of vertices in a graph.

2.  **C) $O(V^3)$**
    *   **Explanation**: The algorithm consists of three nested loops, each iterating $V$ times (for intermediate vertex $k$, source vertex $i$, and destination vertex $j$), leading to a cubic time complexity.

3.  **B) It can handle negative edge weights but not negative cycles.**
    *   **Explanation**: Floyd-Warshall correctly computes shortest paths even with negative edge weights. However, if a negative cycle exists, the shortest path becomes undefined, and the algorithm will detect its presence but cannot provide a meaningful shortest path.

4.  **B) $D_{k-1}(i, k) + D_{k-1}(k, j)$**
    *   **Explanation**: The recurrence states that the shortest path from $i$ to $j$ using intermediate vertices up to $k$ is either the path that doesn't use $k$ ($D_{k-1}(i, j)$) or the path that goes from $i$ to $k$ and then from $k$ to $j$, where both segments use intermediate vertices up to $k-1$.

5.  **C) By checking if `dist[i][i]` is negative for any vertex `i` after all iterations.**
    *   **Explanation**: A path from a vertex to itself should have a length of 0. If, after considering all possible intermediate vertices, the calculated shortest path from a vertex to itself is negative, it implies that a negative cycle exists through that vertex, allowing for infinitely decreasing path lengths.

## Further Reading

1.  **Introduction to Algorithms (CLRS)**: Chapter 25, "All-Pairs Shortest Paths." This is the definitive textbook for algorithms. The section on Floyd-Warshall provides a rigorous mathematical treatment and proofs.
    *   *Resource Type*: Textbook Chapter
    *   *Link (General Reference)*: You would typically find this in a physical or digital copy of "Introduction to Algorithms" by Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein.

2.  **GeeksforGeeks - Floyd Warshall Algorithm**: A popular online resource that provides clear explanations, pseudocode, and Python implementations. Excellent for beginners.
    *   *Resource Type*: Online Tutorial/Article
    *   *Link*: [https://www.geeksforgeeks.org/floyd-warshall-algorithm-dp-16/](https://www.geeksforgeeks.org/floyd-warshall-algorithm-dp-16/)

3.  **Wikipedia - Floyd-Warshall Algorithm**: Offers a concise overview, historical context, and mathematical formulation. Good for quick reference and understanding the core concepts.
    *   *Resource Type*: Encyclopedia Article
    *   *Link*: [https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm](https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm)