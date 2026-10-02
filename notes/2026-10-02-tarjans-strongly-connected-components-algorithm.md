# Tarjan's Strongly Connected Components Algorithm

## Overview
Tarjan's Strongly Connected Components (SCC) Algorithm is a highly efficient and widely used graph algorithm designed to find the strongly connected components of a directed graph. A directed graph consists of nodes (or vertices) and edges that point in a specific direction. A Strongly Connected Component is a maximal subgraph where for any two vertices $u$ and $v$ within that subgraph, there is a path from $u$ to $v$ and a path from $v$ to $u$. In simpler terms, every node in an SCC can reach every other node in the same SCC, and vice versa. Developed by Robert Tarjan in 1972, this algorithm uses a single Depth-First Search (DFS) traversal to identify all SCCs in $O(V+E)$ time, where $V$ is the number of vertices and $E$ is the number of edges, making it remarkably efficient for large graphs.

## What Problem It Solves
Tarjan's algorithm addresses the fundamental problem of identifying "cycles" or "mutually reachable groups" within directed graphs. While a simple cycle detection algorithm might tell you if a cycle exists, Tarjan's algorithm goes further by partitioning the entire graph into its maximal strongly connected subgraphs.

Here's why this is crucial and what problems it solves:

*   **Dependency Cycles:** In many systems, tasks or components have dependencies. If task A depends on B, and B depends on A, they form a cycle. Identifying these cycles is vital in build systems, package managers, or task schedulers to prevent deadlocks or infinite loops. Tarjan's algorithm can pinpoint exactly which tasks are involved in such circular dependencies.
*   **State Machine Analysis:** In finite state machines, SCCs represent sets of states from which all other states within the set are reachable. This can be used to analyze the behavior of a system, identify stable operating regions, or detect unreachable states.
*   **Network Analysis:** In social networks or communication networks, SCCs can represent groups of individuals or entities that have strong mutual influence or communication paths.
*   **Compiler Design:** During control flow analysis, SCCs can help identify loops in program code, which is important for optimization and understanding program structure.
*   **Machine Learning and Graph Neural Networks (GNNs):** While not directly an ML algorithm itself, Tarjan's algorithm can be a preprocessing step or an analytical tool for graph-based ML problems. For instance:
    *   **Graph Simplification:** For very large graphs, identifying SCCs allows for the creation of a "condensation graph" where each SCC is collapsed into a single node. This condensation graph is a Directed Acyclic Graph (DAG), which can simplify subsequent graph processing or feature extraction for GNNs.
    *   **Understanding Information Flow:** In knowledge graphs or causal graphs, SCCs can highlight feedback loops or mutually reinforcing concepts, which might be important features for a learning model.
    *   **Anomaly Detection:** Unusual SCC structures or changes in SCC composition over time could indicate anomalies in dynamic graphs.

## How It Works
Tarjan's algorithm leverages a Depth-First Search (DFS) traversal and maintains two crucial values for each node: `discovery_time` and `low_link_value`, along with a stack to keep track of nodes currently in the DFS path.

Let's break down the mechanism step-by-step:

1.  **Initialization:**
    *   `discovery_time` (or `disc`): An array/dictionary to store the time (order) at which each node is first visited during the DFS. Initialize all to -1 (unvisited).
    *   `low_link_value` (or `low`): An array/dictionary to store the lowest `discovery_time` reachable from the current node `u` (including `u` itself) through the DFS tree edges and at most one back-edge. Initialize all to -1.
    *   `time`: A global counter, initialized to 0, incremented with each node discovery.
    *   `stack`: An empty list (or stack data structure) to store nodes currently in the recursion stack of the DFS and potentially part of an SCC.
    *   `on_stack`: A boolean array/dictionary, initialized to `False` for all nodes, indicating whether a node is currently on the `stack`.
    *   `sccs`: An empty list to store the found Strongly Connected Components.

2.  **DFS Traversal:**
    *   The algorithm iterates through all nodes in the graph. If a node `u` has not been visited (`disc[u] == -1`), it starts a DFS from `u`.
    *   When `dfs(u)` is called:
        *   Set `disc[u] = time` and `low[u] = time`.
        *   Increment `time`.
        *   Push `u` onto the `stack` and set `on_stack[u] = True`.

3.  **Exploring Neighbors:**
    *   For each neighbor `v` of `u`:
        *   **If `v` is unvisited (`disc[v] == -1`):**
            *   Recursively call `dfs(v)`.
            *   After the recursive call returns, update `low[u] = min(low[u], low[v])`. This means that `u` can reach whatever `v` can reach, so `u`'s `low_link_value` might be updated by `v`'s `low_link_value`.
        *   **If `v` is visited AND `v` is currently on the `stack` (`on_stack[v] == True`):**
            *   This indicates a back-edge to an ancestor or a cross-edge to a node in the current DFS tree.
            *   Update `low[u] = min(low[u], disc[v])`. We use `disc[v]` here, not `low[v]`, because `v` is an ancestor (or part of the current component), and its `disc` value represents the earliest point in the current path that `u` can reach through this back-edge.

4.  **Identifying an SCC:**
    *   After visiting all neighbors of `u` and returning from all recursive calls for its children, check if `disc[u] == low[u]`.
    *   If this condition is true, it means `u` is the "root" of an SCC. All nodes from `u` up to the top of the `stack` (until `u` itself is popped) form this SCC.
    *   To extract the SCC:
        *   Create a new empty list for the current SCC.
        *   Pop nodes from the `stack` one by one, add them to the current SCC list, and set their `on_stack` status to `False`, until `u` itself is popped.
        *   Add this newly formed SCC to the `sccs` list.

5.  **Completion:**
    *   The algorithm finishes when all nodes have been visited and processed.

**Example Walkthrough (Conceptual):**
Imagine a graph A -> B, B -> C, C -> A, and C -> D.
1.  Start DFS from A. `disc[A]=0`, `low[A]=0`. Push A. `on_stack[A]=True`.
2.  From A, go to B. `disc[B]=1`, `low[B]=1`. Push B. `on_stack[B]=True`.
3.  From B, go to C. `disc[C]=2`, `low[C]=2`. Push C. `on_stack[C]=True`.
4.  From C, go to A. A is visited (`disc[A]=0`) and `on_stack[A]=True`. This is a back-edge. Update `low[C] = min(low[C], disc[A]) = min(2, 0) = 0`.
5.  From C, go to D. D is unvisited. `disc[D]=3`, `low[D]=3`. Push D. `on_stack[D]=True`.
6.  D has no neighbors. `disc[D]=3`, `low[D]=3`. They are equal. Pop D. SCC: {D}. `on_stack[D]=False`.
7.  Return to C. `low[C]` was 0. Now check `disc[C]=2` vs `low[C]=0`. They are not equal.
8.  C has no more unvisited neighbors. `disc[C]=2`, `low[C]=0`. They are not equal.
9.  Return to B. `low[B]` was 1. Now update `low[B] = min(low[B], low[C]) = min(1, 0) = 0`.
10. B has no more unvisited neighbors. `disc[B]=1`, `low[B]=0`. They are not equal.
11. Return to A. `low[A]` was 0. Now update `low[A] = min(low[A], low[B]) = min(0, 0) = 0`.
12. A has no more unvisited neighbors. `disc[A]=0`, `low[A]=0`. They are equal! Pop nodes from stack until A: C, B, A. SCC: {A, B, C}. `on_stack[A,B,C]=False`.
13. All nodes visited. SCCs: [{D}, {A, B, C}].

## Mathematical Intuition
The core mathematical intuition behind Tarjan's algorithm lies in the properties of Depth-First Search (DFS) trees and the clever use of `discovery_time` and `low_link_value`.

Let's define the key terms more formally:

*   **Discovery Time ($disc[u]$):** For a vertex $u$, $disc[u]$ is the time (an integer counter) at which $u$ is first visited during the DFS traversal. This value is unique for each vertex.
*   **Low-Link Value ($low[u]$):** For a vertex $u$, $low[u]$ is the smallest $disc[v]$ of any vertex $v$ reachable from $u$ (including $u$ itself) through the DFS tree edges and at most one back-edge. A back-edge is an edge $(x, y)$ where $y$ is an ancestor of $x$ in the DFS tree.

The algorithm works by performing a DFS. When we visit a vertex $u$:
1.  We initialize $disc[u]$ and $low[u]$ to the current global `time` counter.
    $$disc[u] \leftarrow \text{time}$$
    $$low[u] \leftarrow \text{time}$$
    $$\text{time} \leftarrow \text{time} + 1$$
    We also push $u$ onto a stack and mark it as `on_stack`.

2.  Then, for each neighbor $v$ of $u$:
    *   **Case 1: $v$ is unvisited ($disc[v]$ is undefined or -1).**
        This means $(u, v)$ is a tree edge. We recursively call DFS on $v$. After the call returns, $v$ has explored all its descendants. The $low[v]$ value will represent the earliest reachable ancestor from $v$'s subtree. Since $u$ can reach $v$, $u$ can also reach whatever $v$ can reach. Therefore, we update $low[u]$:
        $$low[u] \leftarrow \min(low[u], low[v])$$
    *   **Case 2: $v$ is visited AND $v$ is currently on the stack ($on\_stack[v]$ is true).**
        This means $(u, v)$ is a back-edge or a cross-edge to an ancestor in the current DFS tree. Since $v$ is an ancestor (or part of the current component), $u$ can reach $v$. The earliest point $u$ can reach through this edge is $v$'s discovery time. We update $low[u]$:
        $$low[u] \leftarrow \min(low[u], disc[v])$$
        We use $disc[v]$ here, not $low[v]$, because $v$ is an ancestor *in the current DFS path*. Its $disc[v]$ represents the earliest point in that path that $u$ can connect to. Using $low[v]$ might incorrectly pull in information from other branches of $v$'s subtree that are not relevant to the current path from $u$.

3.  **Identifying an SCC Root:**
    After exploring all neighbors of $u$, if $disc[u] == low[u]$, it signifies that $u$ is the "root" of an SCC.
    $$ \text{If } disc[u] == low[u]: $$
    $$ \quad \text{Pop all vertices from the stack until } u \text{ is popped, forming an SCC.} $$
    The condition $disc[u] == low[u]$ means that no vertex reachable from $u$ (including $u$ itself) can reach an ancestor of $u$ (or a node with an earlier discovery time) *that is still on the current DFS stack*. This implies that $u$ and all nodes above it on the stack (until $u$ is popped) form a strongly connected component, as they can all reach $u$, and $u$ can reach them (or they can reach each other through $u$). Once an SCC is identified, its nodes are popped from the stack and marked `on_stack = False` to ensure they are not considered part of any future SCCs.

This process ensures that each node is visited exactly once, and each edge is traversed at most twice (once for each direction if undirected, or once for each direction if directed), leading to an $O(V+E)$ time complexity.

## Advantages
*   **Efficiency:** Tarjan's algorithm runs in $O(V+E)$ time complexity, where $V$ is the number of vertices and $E$ is the number of edges. This is optimal as every vertex and edge must be visited at least once.
*   **Single DFS Pass:** It requires only one Depth-First Search traversal of the graph, making it straightforward to implement and understand once the core concepts are grasped.
*   **Space Efficiency:** The auxiliary space complexity is $O(V+E)$ for storing the graph, plus $O(V)$ for `disc`, `low`, `on_stack` arrays, and the recursion stack.
*   **Robustness:** It correctly identifies all strongly connected components in any directed graph, regardless of its structure (e.g., presence of multiple cycles, self-loops, parallel edges).
*   **Clear Component Identification:** The `disc[u] == low[u]` condition provides a very clear and elegant way to identify the root of an SCC.

## Disadvantages
*   **Recursive Depth:** The algorithm is inherently recursive, which can lead to a stack overflow error for very large graphs with long DFS paths, especially in languages with limited recursion depth (like Python's default). This can often be mitigated by increasing the recursion limit or converting the DFS to an iterative approach using an explicit stack.
*   **Conceptual Complexity:** For beginners, understanding the interplay between `discovery_time`, `low_link_value`, and the auxiliary stack can be challenging. It requires a solid grasp of DFS and graph theory fundamentals.
*   **Implementation Details:** Correctly managing the `on_stack` boolean array/set is crucial and can be a source of bugs if not handled carefully.
*   **Not Intuitive for All:** While elegant, the logic of `low_link_value` propagation and SCC extraction might not be immediately intuitive compared to simpler graph algorithms.

## Real World Applications
1.  **Dependency Management and Build Systems:** In software development, projects often have complex dependencies between modules, libraries, or tasks. If module A depends on B, and B depends on A, this forms a circular dependency. Tarjan's algorithm can detect these cycles, which are critical for preventing deadlocks in build processes (e.g., Maven, Gradle, Makefiles) or ensuring correct package installation order (e.g., `apt`, `pip`). Identifying SCCs helps in breaking these cycles or reorganizing dependencies.
2.  **Social Network Analysis:** In social networks (like Facebook, Twitter, LinkedIn), SCCs can represent groups of individuals who are highly interconnected and mutually influential. For example, if user A follows B, B follows C, and C follows A, they form an SCC. Analyzing these components can reveal tightly-knit communities, echo chambers, or influential cliques within the network, which is valuable for targeted advertising, content recommendation, or understanding information spread.
3.  **Web Crawlers and Link Analysis:** When a web crawler explores the internet, it builds a directed graph where web pages are nodes and hyperlinks are edges. SCCs in this graph can represent clusters of web pages that are highly interlinked. This information can be used to identify authoritative pages (e.g., in PageRank-like algorithms), detect spam farms, or understand the structure of the web for search engine indexing.
4.  **Compiler Optimization and Control Flow Analysis:** In compiler design, the control flow graph (CFG) of a program represents the possible execution paths. SCCs in a CFG correspond to loops or mutually recursive functions. Identifying these loops is crucial for various compiler optimizations, such as loop unrolling, invariant code motion, or parallelization, as well as for static analysis to detect potential infinite loops or unreachable code.
5.  **Biological Networks and Systems Biology:** In biological systems, interactions between genes, proteins, or metabolic pathways can be modeled as directed graphs. SCCs in these networks can represent functional modules or feedback loops that are essential for cellular processes. Analyzing these components helps biologists understand regulatory mechanisms, identify disease pathways, or design interventions.

## Python Example

```python
import collections
import sys

# Increase recursion limit for deep graphs (Python's default is often 1000)
sys.setrecursionlimit(2000)

class TarjanSCC:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        self.graph = collections.defaultdict(list)
        
        # Discovery time of each node
        self.disc = [-1] * num_nodes
        # Low-link value of each node
        self.low = [-1] * num_nodes
        # Boolean array to check if a node is on the stack
        self.on_stack = [False] * num_nodes
        # Stack for DFS traversal
        self.stack = []
        # Global time counter for discovery times
        self.time = 0
        # List to store all found SCCs
        self.sccs = []

    def add_edge(self, u, v):
        """Adds a directed edge from u to v."""
        self.graph[u].append(v)

    def find_sccs(self):
        """
        Main function to find all Strongly Connected Components.
        Iterates through all nodes to ensure all components are found,
        even if the graph is disconnected.
        """
        for i in range(self.num_nodes):
            if self.disc[i] == -1:
                self._dfs(i)
        return self.sccs

    def _dfs(self, u):
        """
        Recursive DFS function to traverse the graph and identify SCCs.
        """
        # Set discovery time and low-link value for node u
        self.disc[u] = self.time
        self.low[u] = self.time
        self.time += 1
        
        # Push u onto the stack and mark it as on_stack
        self.stack.append(u)
        self.on_stack[u] = True

        # Explore neighbors of u
        for v in self.graph[u]:
            if self.disc[v] == -1:
                # If v is not visited, recursively call DFS
                self._dfs(v)
                # After recursive call, update low[u] based on low[v]
                self.low[u] = min(self.low[u], self.low[v])
            elif self.on_stack[v]:
                # If v is visited and on the stack, it's a back-edge
                # Update low[u] based on disc[v]
                self.low[u] = min(self.low[u], self.disc[v])

        # If u is the root of an SCC
        if self.low[u] == self.disc[u]:
            current_scc = []
            while True:
                node = self.stack.pop()
                self.on_stack[node] = False
                current_scc.append(node)
                if node == u:
                    break
            self.sccs.append(current_scc)

# --- Example Usage ---
if __name__ == "__main__":
    # Example 1: Simple graph with one SCC and one isolated node
    print("--- Example 1 ---")
    num_nodes_1 = 5
    tarjan_1 = TarjanSCC(num_nodes_1)
    tarjan_1.add_edge(0, 1)
    tarjan_1.add_edge(1, 2)
    tarjan_1.add_edge(2, 0) # Forms SCC {0, 1, 2}
    tarjan_1.add_edge(2, 3) # Connects to another node
    tarjan_1.add_edge(3, 4) # Node 4 is reachable from 3, but 3 cannot reach 4 back
    
    sccs_1 = tarjan_1.find_sccs()
    print(f"Graph 1 SCCs: {sccs_1}")
    # Expected: [[4], [3], [2, 1, 0]] or similar order, as SCCs are found in reverse topological order.
    # The order of nodes within an SCC might vary based on stack popping.

    # Example 2: Graph with multiple SCCs and a disconnected component
    print("\n--- Example 2 ---")
    num_nodes_2 = 8
    tarjan_2 = TarjanSCC(num_nodes_2)
    tarjan_2.add_edge(0, 1)
    tarjan_2.add_edge(1, 2)
    tarjan_2.add_edge(2, 0) # SCC {0, 1, 2}
    tarjan_2.add_edge(2, 3)
    tarjan_2.add_edge(3, 4)
    tarjan_2.add_edge(4, 5)
    tarjan_2.add_edge(5, 3) # SCC {3, 4, 5}
    tarjan_2.add_edge(6, 7) # Disconnected component
    tarjan_2.add_edge(7, 6) # SCC {6, 7}
    
    sccs_2 = tarjan_2.find_sccs()
    print(f"Graph 2 SCCs: {sccs_2}")
    # Expected: [[7, 6], [5, 4, 3], [2, 1, 0]] or similar order.

    # Example 3: A single node graph
    print("\n--- Example 3 ---")
    num_nodes_3 = 1
    tarjan_3 = TarjanSCC(num_nodes_3)
    # No edges
    sccs_3 = tarjan_3.find_sccs()
    print(f"Graph 3 SCCs: {sccs_3}")
    # Expected: [[0]]

    # Example 4: A graph with no cycles (a DAG)
    print("\n--- Example 4 ---")
    num_nodes_4 = 4
    tarjan_4 = TarjanSCC(num_nodes_4)
    tarjan_4.add_edge(0, 1)
    tarjan_4.add_edge(0, 2)
    tarjan_4.add_edge(1, 3)
    tarjan_4.add_edge(2, 3)
    
    sccs_4 = tarjan_4.find_sccs()
    print(f"Graph 4 SCCs: {sccs_4}")
    # Expected: [[3], [2], [1], [0]] or similar order, each node is its own SCC.
```

## Interview Questions

1.  **What is a Strongly Connected Component (SCC) in a directed graph?**
    *   **Answer:** An SCC is a maximal subgraph of a directed graph such that for any two vertices $u$ and $v$ within the subgraph, there is a path from $u$ to $v$ and a path from $v$ to $u$. In simpler terms, all nodes within an SCC are mutually reachable.

2.  **Explain the core idea behind Tarjan's algorithm for finding SCCs.**
    *   **Answer:** Tarjan's algorithm uses a single Depth-First Search (DFS) traversal. It maintains two values for each node: `discovery_time` (when the node was first visited) and `low_link_value` (the smallest `discovery_time` reachable from the current node, including itself, through tree edges and at most one back-edge). It also uses a stack to keep track of nodes currently in the DFS path. When `discovery_time[u] == low_link_value[u]`, it means `u` is the root of an SCC, and all nodes on the stack from `u` upwards form that SCC.

3.  **What are `discovery_time` and `low_link_value`, and how are they used?**
    *   **Answer:**
        *   `discovery_time[u]` (or `disc[u]`) is the timestamp when node `u` is first visited during the DFS. It's unique for each node.
        *   `low_link_value[u]` (or `low[u]`) is the smallest `discovery_time` of any node reachable from `u` (including `u` itself) through tree edges and at most one back-edge.
        *   They are used to detect cycles. If `low[u] == disc[u]`, it implies that `u` is the root of an SCC because no node reachable from `u` can lead back to an ancestor of `u` (or a node with an earlier `disc` value) that is still part of the current DFS path.

4.  **Why is a stack used in Tarjan's algorithm?**
    *   **Answer:** The stack is used to store nodes that are currently part of the DFS recursion path and are potential members of an SCC. When an SCC root `u` is identified (i.e., `disc[u] == low[u]`), all nodes on the stack from `u` to the top are popped and form that SCC. This ensures that only nodes belonging to the *current* SCC are grouped together.

5.  **What is the role of the `on_stack` array/set?**
    *   **Answer:** The `on_stack` array (or a set) is a boolean flag for each node, indicating whether that node is currently present on the DFS stack. It's crucial for two reasons:
        1.  When exploring a neighbor `v` of `u`, if `v` is already visited (`disc[v] != -1`) AND `on_stack[v]` is true, it means `v` is an ancestor of `u` (or part of the same component currently being explored). In this case, we update `low[u] = min(low[u], disc[v])`.
        2.  It prevents nodes that have already been assigned to an SCC from being considered again in subsequent `low_link_value` updates or SCC formations.

6.  **What is the time and space complexity of Tarjan's algorithm?**
    *   **Answer:**
        *   **Time Complexity:** $O(V+E)$, where $V$ is the number of vertices and $E$ is the number of edges. This is because the algorithm performs a single DFS traversal, visiting each vertex and edge at most a constant number of times.
        *   **Space Complexity:** $O(V+E)$ for storing the graph (adjacency list), plus $O(V)$ for the `disc`, `low`, `on_stack` arrays, and the recursion stack (which can go up to $V$ in the worst case).

7.  **How does Tarjan's algorithm handle disconnected graphs?**
    *   **Answer:** The main `find_sccs` function iterates through all nodes. If a node `i` has not been visited (`disc[i] == -1`), it initiates a DFS from `i`. This ensures that if the graph is disconnected, a DFS will be started for each unvisited component, and all SCCs across all components will be found.

8.  **Compare Tarjan's algorithm with Kosaraju's algorithm for finding SCCs.**
    *   **Answer:** Both algorithms find SCCs in $O(V+E)$ time.
        *   **Tarjan's:** Uses a single DFS traversal, along with `disc`, `low` values, and a stack. It's generally considered more elegant and efficient in practice due to fewer graph traversals.
        *   **Kosaraju's:** Uses two DFS traversals. The first DFS is on the original graph to determine finishing times. Then, the graph is transposed (all edges reversed). A second DFS is performed on the transposed graph in decreasing order of finishing times from the first DFS. Each tree in the second DFS forms an SCC. Kosaraju's is often easier to understand conceptually but involves building a transposed graph.

9.  **Can Tarjan's algorithm detect cycles in a directed graph? If so, how?**
    *   **Answer:** Yes, Tarjan's algorithm inherently detects cycles. Any SCC with more than one node, or a single node with a self-loop, represents a cycle. If an SCC contains nodes $u_1, u_2, \dots, u_k$ where $k > 1$, it means there's a path from $u_i$ to $u_j$ and $u_j$ to $u_i$ for any $i, j$, which implies cycles. If a node forms an SCC by itself, it means it's not part of any larger cycle.

10. **What happens if a node has no outgoing edges? How is it handled by Tarjan's algorithm?**
    *   **Answer:** If a node `u` has no outgoing edges, its DFS will proceed as follows: `disc[u]` and `low[u]` are initialized to `time`. It's pushed onto the stack. Since it has no neighbors, the loop for exploring neighbors won't execute. Immediately after, the condition `low[u] == disc[u]` will be true (as `low[u]` was never updated). Thus, `u` will be popped from the stack, forming an SCC of just `{u}`. This is correct, as a node with no outgoing edges cannot reach any other node, nor can any other node reach it (unless it's part of a larger cycle where it has incoming edges).

## Quiz

1.  What is the primary goal of Tarjan's Strongly Connected Components Algorithm?
    A) To find the shortest path between two nodes in a directed graph.
    B) To identify all maximal subgraphs where every node is mutually reachable.
    C) To detect if a directed graph contains any cycles.
    D) To determine the minimum spanning tree of a directed graph.

2.  Which data structure is crucial for keeping track of nodes currently in the DFS path and potential members of an SCC in Tarjan's algorithm?
    A) Queue
    B) Priority Queue
    C) Stack
    D) Hash Map

3.  In Tarjan's algorithm, what does `low_link_value[u]` represent?
    A) The earliest time a node `u` was discovered.
    B) The number of incoming edges to node `u`.
    C) The smallest discovery time of any node reachable from `u` (including `u`) through tree edges and at most one back-edge.
    D) The total number of nodes in the SCC containing `u`.

4.  When is a node `u` identified as the "root" of a Strongly Connected Component in Tarjan's algorithm?
    A) When `discovery_time[u]` is the smallest among all nodes.
    B) When `low_link_value[u]` is equal to `discovery_time[u]`.
    C) When `u` has no outgoing edges.
    D) When all its neighbors have been visited.

5.  What is the time complexity of Tarjan's algorithm?
    A) $O(V^2)$
    B) $O(E \log V)$
    C) $O(V+E)$
    D) $O(V \cdot E)$

### Answer Key

1.  **B) To identify all maximal subgraphs where every node is mutually reachable.**
    *   **Explanation:** Tarjan's algorithm specifically partitions a directed graph into its Strongly Connected Components, which are maximal subgraphs where all nodes are mutually reachable. Options A and D are for different graph problems, and C is a byproduct, not the primary goal.

2.  **C) Stack**
    *   **Explanation:** The stack is used to store nodes in the current DFS path. When an SCC is identified, nodes are popped from this stack until the root of the SCC is reached, forming the component.

3.  **C) The smallest discovery time of any node reachable from `u` (including `u`) through tree edges and at most one back-edge.**
    *   **Explanation:** This is the precise definition of `low_link_value`. It's a critical component for detecting cycles and identifying SCCs.

4.  **B) When `low_link_value[u]` is equal to `discovery_time[u]`.**
    *   **Explanation:** This condition signifies that node `u` cannot reach any node with an earlier discovery time that is still on the current DFS stack. This means `u` is the highest ancestor in its current DFS tree that is part of an SCC, making it the root.

5.  **C) $O(V+E)$**
    *   **Explanation:** Tarjan's algorithm performs a single Depth-First Search, visiting each vertex and edge a constant number of times. This makes its time complexity linear with respect to the number of vertices ($V$) and edges ($E$).

## Further Reading

1.  **Wikipedia - Tarjan's strongly connected components algorithm:** A good starting point for a concise overview, pseudocode, and visual examples.
    [https://en.wikipedia.org/wiki/Tarjan%27s_strongly_connected_components_algorithm](https://en.wikipedia.org/wiki/Tarjan%27s_strongly_connected_components_algorithm)

2.  **GeeksforGeeks - Tarjan's Algorithm to find Strongly Connected Components:** Provides a detailed explanation with illustrative diagrams and C++/Java implementations.
    [https://www.geeksforgeeks.org/tarjans-algorithm-find-strongly-connected-components/](https://www.geeksforgeeks.org/tarjans-algorithm-find-strongly-connected-components/)

3.  **Introduction to Algorithms (CLRS) - Chapter 22: Elementary Graph Algorithms (specifically 22.5: Strongly Connected Components):** For a rigorous, academic treatment of graph algorithms, including Tarjan's, this textbook is an excellent resource. While it covers Kosaraju's in detail, the principles of DFS and SCCs are universally applicable and provide a strong theoretical foundation. (Note: CLRS primarily details Kosaraju's and a different linear-time algorithm, but the underlying graph theory for SCCs is well-explained and essential for understanding Tarjan's.)
    *   *You might need to search for a specific edition or chapter online if you don't have the book.*