# Prim's Algorithm

## Overview
Prim's Algorithm is a greedy algorithm used to find a Minimum Spanning Tree (MST) for a weighted, undirected graph. Imagine you have a set of cities (nodes) and roads connecting them (edges), each road having a certain length (weight). A "spanning tree" is a subset of these roads that connects all cities without forming any loops (cycles). A "minimum spanning tree" is a spanning tree where the total length of all selected roads is as small as possible. Prim's Algorithm helps you find exactly that – the most economical way to connect all cities. It starts from an arbitrary node and iteratively adds the cheapest edge that connects a node already in the MST to a node outside the MST, until all nodes are included.

## What Problem It Solves
Prim's Algorithm primarily solves the **Minimum Spanning Tree (MST) problem**. Given a connected, undirected graph with weighted edges, the goal is to find a subgraph that:
1.  Is a tree (no cycles).
2.  Connects all the vertices in the original graph (it's "spanning").
3.  Has the minimum possible total sum of edge weights.

**Why is it needed in machine learning?**
While Prim's Algorithm isn't a core machine learning algorithm itself, the concept of Minimum Spanning Trees (MSTs) and graph theory, in general, has applications or serves as a foundational concept in several areas relevant to machine learning:

*   **Clustering:** Some clustering algorithms, particularly hierarchical clustering methods like single-linkage clustering, can be conceptualized or even implemented using MSTs. The MST can reveal the underlying structure of data points, where clusters are formed by dense regions connected by short edges.
*   **Feature Selection:** In some cases, an MST can be used to understand the relationships between features. If features are nodes in a graph and edge weights represent some measure of similarity or dependency, an MST can help identify a minimal set of features that still capture the essential relationships.
*   **Image Segmentation:** MSTs can be used to segment images by treating pixels as nodes and edge weights as dissimilarity measures between adjacent pixels. Cutting the "weakest" edges in the MST can separate regions.
*   **Network Analysis:** In graph-based machine learning (e.g., Graph Neural Networks), understanding the fundamental structure of a graph, such as its MST, can be crucial for tasks like community detection, anomaly detection, or efficient message passing.
*   **Dimensionality Reduction:** MSTs can sometimes be used to construct low-dimensional representations of high-dimensional data, preserving the intrinsic connectivity.

Essentially, Prim's Algorithm provides an efficient way to find the most "economical" way to connect all components in a system, which is a problem that arises in various forms across different domains, including those that intersect with machine learning.

## How It Works
Prim's Algorithm builds the MST incrementally, starting from a single vertex and growing the tree one edge at a time. Here's a step-by-step breakdown:

1.  **Initialization:**
    *   Choose an arbitrary starting vertex (node) from the graph. Add it to your MST.
    *   Keep track of all vertices already included in the MST (let's call this set `MST_nodes`). Initially, it only contains the starting vertex.
    *   Maintain a way to efficiently find the minimum weight edge connecting a node in `MST_nodes` to a node *not* in `MST_nodes`. A **priority queue** is ideal for this.

2.  **Iteration (Growing the MST):**
    *   Repeat the following steps until all vertices in the graph are included in `MST_nodes`:
        a.  **Find the "Cheapest" Edge:** Look at all edges that connect a vertex in `MST_nodes` to a vertex *not* in `MST_nodes`. From these "candidate" edges, select the one with the smallest weight.
        b.  **Add to MST:** Add this selected edge to your MST.
        c.  **Update `MST_nodes`:** Add the new vertex (the one that was *not* in `MST_nodes` but is now connected by the chosen edge) to `MST_nodes`.
        d.  **Update Candidate Edges:** For the newly added vertex, examine all its outgoing edges to vertices *not* yet in `MST_nodes`. If any of these edges offer a cheaper way to connect an unvisited vertex to the growing MST, update their priority in your priority queue.

3.  **Termination:**
    *   The algorithm stops when `MST_nodes` contains all vertices from the original graph. At this point, the set of edges you've added forms the Minimum Spanning Tree.

**Analogy:**
Imagine you're building a network of roads to connect all towns in a region, and you want to minimize the total length of roads.
1.  Pick any town to start your network.
2.  From this town, look at all roads leading to other towns not yet in your network. Pick the shortest one.
3.  Add that road and the new town it connects to your network.
4.  Now, from *all* towns currently in your network, look at all roads leading to towns *not yet* in your network. Again, pick the shortest one.
5.  Repeat until all towns are connected.

This greedy approach works because of a fundamental property of MSTs (the "cut property"), which ensures that at each step, picking the locally optimal (cheapest) edge leads to a globally optimal solution.

## Mathematical Intuition
Let's formalize the concepts behind Prim's Algorithm.

A **graph** $G$ is defined as a pair $G = (V, E)$, where $V$ is a set of vertices (nodes) and $E$ is a set of edges connecting pairs of vertices. Each edge $(u, v) \in E$ has a non-negative weight $w(u, v)$.

A **spanning tree** $T$ of a connected graph $G$ is a subgraph that is a tree and connects all vertices in $V$. If $G$ has $N$ vertices, any spanning tree $T$ will have exactly $N-1$ edges.

A **Minimum Spanning Tree (MST)** is a spanning tree $T^*$ such that the sum of its edge weights is minimized:
$$ \sum_{(u, v) \in T^*} w(u, v) \le \sum_{(u, v) \in T} w(u, v) $$
for any other spanning tree $T$ of $G$.

The core mathematical principle that justifies Prim's (and Kruskal's) greedy approach is the **Cut Property (or Bridge Property)**.

**Definition of a Cut:** A **cut** in a connected graph $G=(V, E)$ is a partition of the vertices $V$ into two non-empty, disjoint sets, $S$ and $V \setminus S$. An edge $(u, v)$ is said to **cross the cut** if one endpoint ($u$) is in $S$ and the other endpoint ($v$) is in $V \setminus S$.

**Cut Property Theorem:** If for any cut $(S, V \setminus S)$ in a connected, weighted graph $G$, an edge $(u, v)$ is the unique minimum-weight edge crossing that cut, then $(u, v)$ must be part of *every* MST of $G$. If there are multiple minimum-weight edges crossing the cut, then at least one of them must be part of *some* MST.

**How Prim's Algorithm uses the Cut Property:**
Prim's Algorithm iteratively builds an MST. At each step, it maintains a set of vertices $S$ that are already included in the growing MST, and the remaining vertices $V \setminus S$ are outside it. The algorithm then considers the cut $(S, V \setminus S)$. It finds the edge $(u, v)$ with the minimum weight such that $u \in S$ and $v \in V \setminus S$. By the Cut Property, this minimum-weight edge must be part of *some* MST. Prim's algorithm adds this edge and vertex $v$ to its growing tree, effectively expanding $S$ to include $v$. This process continues until $S$ includes all vertices in $V$.

The greedy choice at each step (picking the minimum weight edge crossing the current cut) is guaranteed to be safe and leads to a global optimum because of this fundamental property. The algorithm ensures that no cycles are formed because it always adds an edge that connects a vertex *outside* the current tree to a vertex *inside* it.

## Advantages
*   **Guaranteed Optimality:** Prim's Algorithm is guaranteed to find a Minimum Spanning Tree for any connected, weighted, undirected graph.
*   **Simplicity:** The underlying concept of growing a tree from a single starting node by always picking the cheapest connecting edge is intuitive and relatively easy to understand.
*   **Works well for Dense Graphs:** When the number of edges is close to the maximum possible ($|E| \approx |V|^2$), Prim's Algorithm implemented with an adjacency matrix and a simple array for `min_cost` can be efficient. With a Fibonacci heap, it's very efficient for dense graphs.
*   **Single Component Growth:** It builds the MST as a single connected component, which can be advantageous in certain applications where a connected structure is desired from the outset.
*   **Can Start Anywhere:** The algorithm can start from any arbitrary vertex in the graph and will still find an MST.

## Disadvantages
*   **Requires a Connected Graph:** Prim's Algorithm only works on connected graphs. If the graph is disconnected, it will only find an MST for the connected component containing the starting vertex.
*   **Less Efficient for Sparse Graphs:** For very sparse graphs (where $|E|$ is much smaller than $|V|^2$), Kruskal's Algorithm often performs better. Prim's algorithm, especially with a basic array implementation, can be slower for sparse graphs.
*   **Does Not Handle Negative Edge Weights (in the context of MST definition):** While the algorithm itself can technically run with negative weights, the concept of an MST usually implies non-negative weights. If negative cycles exist, the MST problem is ill-defined. If only negative edge weights exist but no negative cycles, Prim's will still find an MST, but the interpretation might be different from typical "cost minimization."
*   **Implementation Complexity:** While conceptually simple, an efficient implementation of Prim's Algorithm typically requires a priority queue (like a min-heap), which adds a layer of complexity compared to a naive array-based approach.

## Real World Applications
1.  **Network Design (Telecommunications, Computer Networks):** This is perhaps the most classic application. When designing a new communication network (e.g., laying fiber optic cables, connecting computer servers), Prim's Algorithm can determine the most cost-effective way to connect all nodes (cities, servers) with the minimum total cable length or installation cost, ensuring connectivity without redundant connections.
2.  **Circuit Board Design:** In the design of printed circuit boards (PCBs), components need to be connected by traces. Prim's Algorithm can be used to find the shortest possible total length of traces required to connect all necessary pins, minimizing material usage and signal latency.
3.  **Clustering Analysis:** While not a direct ML algorithm, the MST concept is fundamental in some clustering techniques. For instance, single-linkage hierarchical clustering can be visualized as building an MST. The "cuts" in the MST (removing the longest edges) can reveal natural clusters in data points, where edge weights represent distances or dissimilarities between points.
4.  **Image Segmentation:** In computer vision, images can be represented as graphs where pixels are vertices and edge weights represent the dissimilarity between adjacent pixels (e.g., difference in color or intensity). Prim's Algorithm can be used to construct an MST, and then by removing edges with high weights, the image can be segmented into regions with similar characteristics.
5.  **Road Network Planning:** For urban planners, Prim's Algorithm can help design efficient road networks, utility lines (water, gas, electricity), or railway systems. By treating intersections or service points as nodes and potential connections as edges with associated costs (distance, construction cost), the algorithm can find the most economical way to connect all points.

## Python Example

This example demonstrates Prim's Algorithm using a min-priority queue (`heapq`) to efficiently find the minimum weight edge at each step. We'll represent the graph using an adjacency list.

```python
import heapq

def prim_algorithm(graph, start_node):
    """
    Implements Prim's Algorithm to find the Minimum Spanning Tree (MST).

    Args:
        graph (dict): An adjacency list representation of the graph.
                      Keys are nodes, values are lists of (neighbor, weight) tuples.
                      Example: {
                          'A': [('B', 2), ('C', 3)],
                          'B': [('A', 2), ('C', 1), ('D', 1)],
                          ...
                      }
        start_node: The node from which to start building the MST.

    Returns:
        tuple: A tuple containing:
               - list: The edges of the MST, represented as (u, v, weight) tuples.
               - int: The total weight of the MST.
    """
    if not graph:
        return [], 0

    # Set to keep track of nodes already included in the MST
    mst_nodes = set()
    
    # Priority queue to store candidate edges.
    # Each element is (weight, u, v), where (u, v) is an edge.
    # We use u as the source node already in MST, and v as the target node not yet in MST.
    min_heap = []

    # List to store the edges of the MST
    mst_edges = []
    
    # Total weight of the MST
    total_mst_weight = 0

    # Start with the given start_node
    mst_nodes.add(start_node)

    # Add all edges connected to the start_node to the priority queue
    for neighbor, weight in graph.get(start_node, []):
        heapq.heappush(min_heap, (weight, start_node, neighbor))

    # Loop until all nodes are included in the MST or the heap is empty
    # (meaning no more connections can be made)
    while min_heap and len(mst_nodes) < len(graph):
        # Pop the edge with the smallest weight
        weight, u, v = heapq.heappop(min_heap)

        # If the target node 'v' is already in the MST, skip this edge
        # (it would form a cycle or is redundant)
        if v in mst_nodes:
            continue

        # Add the new node 'v' to the MST
        mst_nodes.add(v)
        
        # Add the edge to our MST edges list
        mst_edges.append((u, v, weight))
        
        # Add its weight to the total MST weight
        total_mst_weight += weight

        # Now, add all edges connected to the newly added node 'v'
        # to the priority queue, but only if the neighbor is not yet in the MST
        for neighbor_of_v, weight_to_neighbor in graph.get(v, []):
            if neighbor_of_v not in mst_nodes:
                heapq.heappush(min_heap, (weight_to_neighbor, v, neighbor_of_v))
                
    # Check if the graph was connected and we found an MST for all nodes
    if len(mst_nodes) != len(graph):
        print("Warning: The graph is disconnected. MST found for the component containing the start node.")
        
    return mst_edges, total_mst_weight

# --- Dummy Dataset (Graph) ---
# Representing a graph using an adjacency list
# Each key is a node, and its value is a list of (neighbor, weight) tuples.
# This graph is undirected, so edges are added in both directions.
graph_data = {
    'A': [('B', 2), ('C', 3)],
    'B': [('A', 2), ('C', 1), ('D', 1), ('E', 4)],
    'C': [('A', 3), ('B', 1), ('F', 5)],
    'D': [('B', 1), ('E', 1)],
    'E': [('B', 4), ('D', 1), ('F', 1)],
    'F': [('C', 5), ('E', 1)]
}

print("--- Running Prim's Algorithm ---")
start_node = 'A'
mst_edges, total_weight = prim_algorithm(graph_data, start_node)

print(f"\nStarting node for Prim's: {start_node}")
print("\nEdges in the Minimum Spanning Tree:")
for u, v, weight in mst_edges:
    print(f"  {u} --({weight})-- {v}")

print(f"\nTotal weight of the MST: {total_weight}")

# Example with a disconnected graph (to show the warning)
disconnected_graph = {
    'A': [('B', 1)],
    'B': [('A', 1)],
    'C': [('D', 2)],
    'D': [('C', 2)]
}

print("\n--- Running Prim's Algorithm on a Disconnected Graph ---")
start_node_disconnected = 'A'
mst_edges_disc, total_weight_disc = prim_algorithm(disconnected_graph, start_node_disconnected)

print(f"\nStarting node for Prim's: {start_node_disconnected}")
print("\nEdges in the Minimum Spanning Tree (for component):")
for u, v, weight in mst_edges_disc:
    print(f"  {u} --({weight})-- {v}")

print(f"\nTotal weight of the MST (for component): {total_weight_disc}")

```

**Explanation of the Python Code:**

1.  **`prim_algorithm(graph, start_node)` function:**
    *   Takes `graph` (adjacency list) and a `start_node` as input.
    *   `mst_nodes`: A `set` to keep track of all vertices that have been added to our MST.
    *   `min_heap`: A `heapq` (min-priority queue) is used to store candidate edges. Each element is a tuple `(weight, u, v)`. The `heapq` automatically ensures that `heapq.heappop()` always returns the edge with the smallest `weight`.
    *   `mst_edges`: A list to store the edges that form the MST.
    *   `total_mst_weight`: Accumulates the sum of weights of edges in the MST.
    *   **Initialization:** The `start_node` is added to `mst_nodes`. All edges connected to `start_node` are pushed into the `min_heap`.
    *   **Main Loop:** The `while` loop continues as long as there are candidate edges in the `min_heap` and not all nodes have been added to the `mst_nodes`.
        *   `heapq.heappop(min_heap)`: Retrieves the edge with the smallest weight.
        *   **Cycle Check:** `if v in mst_nodes: continue`: This is crucial. If the target node `v` is already in `mst_nodes`, adding this edge would create a cycle, so we skip it.
        *   **Add to MST:** If `v` is not in `mst_nodes`, it means we've found the cheapest way to connect a new node to our growing MST. We add `v` to `mst_nodes`, record the edge `(u, v, weight)`, and update `total_mst_weight`.
        *   **Explore New Node's Edges:** For the newly added node `v`, we iterate through all its neighbors. If a neighbor `neighbor_of_v` is *not* yet in `mst_nodes`, we add the edge `(weight_to_neighbor, v, neighbor_of_v)` to the `min_heap` as a new candidate.
    *   **Disconnected Graph Check:** After the loop, if `len(mst_nodes)` is less than `len(graph)`, it means the graph was disconnected, and Prim's only found the MST for the component reachable from the `start_node`.
    *   Returns the list of MST edges and the total weight.

2.  **`graph_data`:** A sample graph is defined as an adjacency list. Since it's an undirected graph, each edge (e.g., A-B with weight 2) is represented in both A's and B's adjacency lists.

3.  **Output:** The code prints the edges that form the MST and their total combined weight. It also includes an example of a disconnected graph to show how the algorithm handles it.

## Interview Questions

1.  **What is Prim's Algorithm, and what problem does it solve?**
    *   **Answer:** Prim's Algorithm is a greedy algorithm used to find a Minimum Spanning Tree (MST) for a connected, weighted, undirected graph. The problem it solves is to find a subset of the edges that connects all the vertices together, without any cycles, and with the minimum possible total edge weight.

2.  **How does Prim's Algorithm work step-by-step?**
    *   **Answer:** It starts with an arbitrary vertex and grows the MST one edge at a time. It maintains a set of vertices already included in the MST. In each step, it finds the minimum-weight edge that connects a vertex in the MST to a vertex outside the MST. This edge and the new vertex are then added to the MST. This process continues until all vertices are included.

3.  **What is the time complexity of Prim's Algorithm, and how does it depend on the data structures used?**
    *   **Answer:**
        *   **With an Adjacency Matrix and a simple array to find min-edge:** $O(V^2)$, where $V$ is the number of vertices. This is because in each of the $V$ iterations, it scans $V$ edges to find the minimum.
        *   **With an Adjacency List and a Binary Min-Heap (Priority Queue):** $O(E \log V)$ or $O(E \log E)$, which simplifies to $O(E \log V)$ since $E \le V^2$. Each edge insertion/deletion into the heap takes $O(\log E)$ time, and there are $E$ such operations in the worst case.
        *   **With an Adjacency List and a Fibonacci Heap:** $O(E + V \log V)$. This is the theoretically most efficient for dense graphs but is complex to implement.

4.  **How does Prim's Algorithm differ from Kruskal's Algorithm?**
    *   **Answer:** Both find MSTs but use different greedy strategies:
        *   **Prim's:** Grows a single tree from a starting vertex. It focuses on connecting the current MST to the closest outside vertex. It's "vertex-centric."
        *   **Kruskal's:** Grows a forest of trees (multiple components) that are eventually merged. It sorts all edges by weight and adds the cheapest edge if it doesn't form a cycle. It's "edge-centric."
        *   **Best Use Cases:** Prim's is generally better for dense graphs, while Kruskal's is often preferred for sparse graphs.

5.  **Can Prim's Algorithm handle disconnected graphs? What happens if it encounters one?**
    *   **Answer:** No, Prim's Algorithm, in its standard form, assumes a connected graph. If the graph is disconnected, it will only find an MST for the connected component that contains the starting vertex. It will not be able to reach or connect to other components.

6.  **Explain the "cut property" and how it relates to Prim's Algorithm.**
    *   **Answer:** The cut property states that for any cut (a partition of vertices into two sets $S$ and $V \setminus S$) in a connected, weighted graph, if an edge $(u, v)$ is the minimum-weight edge crossing that cut (with $u \in S$ and $v \in V \setminus S$), then $(u, v)$ must be part of *some* MST. Prim's Algorithm leverages this by always selecting the minimum-weight edge that connects a vertex in its growing MST ($S$) to a vertex outside it ($V \setminus S$), thus guaranteeing that each chosen edge is part of an MST.

7.  **Is Prim's Algorithm a greedy algorithm? Justify your answer.**
    *   **Answer:** Yes, Prim's Algorithm is a greedy algorithm. At each step, it makes a locally optimal choice by selecting the minimum-weight edge that connects a vertex in the current MST to a vertex outside it. This local optimal choice, thanks to the cut property, leads to a globally optimal solution (the MST).

8.  **What data structures are typically used for an efficient implementation of Prim's Algorithm?**
    *   **Answer:**
        *   **Adjacency List:** To represent the graph, allowing efficient iteration over neighbors of a vertex.
        *   **Min-Priority Queue (Min-Heap):** To efficiently retrieve the minimum-weight edge connecting a vertex in the MST to a vertex outside it. This is crucial for achieving better time complexity than $O(V^2)$.
        *   **Set/Boolean Array:** To keep track of which vertices have already been included in the MST.

9.  **What happens if there are multiple edges with the same minimum weight when Prim's Algorithm is selecting an edge?**
    *   **Answer:** If there are multiple edges with the same minimum weight crossing the cut, Prim's Algorithm can pick any one of them. The choice might lead to a different set of edges in the MST, but the total weight of the MST will remain the same. This means an MST is not necessarily unique in terms of its edge composition, but its total weight is unique.

10. **In what real-world scenarios would you prefer Prim's Algorithm over Kruskal's?**
    *   **Answer:** Prim's Algorithm is generally preferred for **dense graphs** (graphs with many edges, close to $V^2$). Its $O(V^2)$ or $O(E + V \log V)$ complexity can be more efficient than Kruskal's $O(E \log E)$ when $E$ is large. It's also useful when you need to grow the MST from a specific starting point or when the graph is represented by an adjacency matrix, making it easy to query all edges from a vertex. Examples include network design where all nodes are potentially connected, or certain image processing tasks.

## Quiz

1.  **What problem does Prim's Algorithm solve?**
    A) Shortest path between two nodes
    B) Maximum flow in a network
    C) Minimum Spanning Tree
    D) Traveling Salesperson Problem

2.  **Which of the following best describes the approach of Prim's Algorithm?**
    A) It sorts all edges by weight and adds them if they don't form a cycle.
    B) It iteratively adds the cheapest edge connecting a vertex in the current MST to a vertex outside it.
    C) It explores all possible paths to find the shortest one.
    D) It divides the graph into subproblems and combines their solutions.

3.  **What is a typical time complexity for Prim's Algorithm when implemented with an adjacency list and a binary min-heap?**
    A) $O(V^2)$
    B) $O(E \log V)$
    C) $O(V + E)$
    D) $O(E^2)$

4.  **Prim's Algorithm is generally more efficient than Kruskal's Algorithm for which type of graphs?**
    A) Sparse graphs
    B) Disconnected graphs
    C) Dense graphs
    D) Directed graphs

5.  **Which property is fundamental to the correctness of Prim's Algorithm?**
    A) Triangle Inequality
    B) Bellman-Ford Property
    C) Cut Property
    D) Transitivity Property

---

### Answer Key

1.  **C) Minimum Spanning Tree**
    *   **Explanation:** Prim's Algorithm is specifically designed to find the Minimum Spanning Tree of a weighted, undirected graph.

2.  **B) It iteratively adds the cheapest edge connecting a vertex in the current MST to a vertex outside it.**
    *   **Explanation:** This describes the greedy, vertex-centric approach of Prim's Algorithm, where it grows a single tree by always picking the minimum-weight edge that expands the tree to a new vertex.

3.  **B) $O(E \log V)$**
    *   **Explanation:** With an adjacency list (for graph representation) and a binary min-heap (for efficient edge selection), Prim's Algorithm achieves a time complexity of $O(E \log V)$, where $E$ is the number of edges and $V$ is the number of vertices.

4.  **C) Dense graphs**
    *   **Explanation:** Prim's Algorithm, especially with efficient heap implementations, tends to perform better on dense graphs (where the number of edges $E$ is close to $V^2$) compared to Kruskal's Algorithm.

5.  **C) Cut Property**
    *   **Explanation:** The Cut Property is the mathematical principle that guarantees the correctness of Prim's (and Kruskal's) greedy choices, ensuring that selecting the minimum-weight edge crossing a cut will always lead to an MST.

## Further Reading

1.  **Introduction to Algorithms (CLRS) - Chapter 23: Minimum Spanning Trees:** This is a classic textbook for algorithms. Chapter 23 provides a rigorous and detailed explanation of Prim's Algorithm, including its proof of correctness and various implementations.
    *   *Resource Type:* Textbook Chapter (available in most university libraries or online through academic subscriptions).
    *   *Search Term:* "Cormen Leiserson Rivest Stein Introduction to Algorithms Prim's Algorithm"

2.  **GeeksforGeeks - Prim's Algorithm:** A highly accessible online resource that provides clear explanations, pseudocode, and Python/Java/C++ implementations of Prim's Algorithm. Excellent for beginners.
    *   *Link:* [https://www.geeksforgeeks.org/prims-minimum-spanning-tree-mst-greedy-algo-5/](https://www.geeksforgeeks.org/prims-minimum-spanning-tree-mst-greedy-algo-5/)

3.  **Wikipedia - Prim's Algorithm:** Offers a concise overview, historical context, pseudocode, and a discussion of its complexity and relationship to other MST algorithms.
    *   *Link:* [https://en.wikipedia.org/wiki/Prim%27s_algorithm](https://en.wikipedia.org/wiki/Prim%27s_algorithm)