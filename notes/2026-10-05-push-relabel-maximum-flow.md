# Push-Relabel Maximum Flow

## Overview

The Push-Relabel algorithm is one of the most efficient and sophisticated methods for solving the **Maximum Flow problem** in a network. Imagine a network of pipes, where each pipe has a maximum capacity for water flow. You have a source where water enters and a sink where it exits. The Maximum Flow problem asks: what is the maximum amount of water that can flow from the source to the sink without exceeding any pipe's capacity?

Unlike augmenting path algorithms (like Edmonds-Karp or Dinic's), which find paths from source to sink and push flow along them, Push-Relabel takes a different approach. It's a **preflow-push algorithm**. This means it first "pushes" as much flow as possible out of the source, potentially creating "excess flow" at intermediate nodes. Then, it systematically moves this excess flow towards the sink using two primary operations: `Push` and `Relabel`. The algorithm maintains a "height" or "label" for each node, which guides the flow in a downhill manner towards the sink, ensuring that flow always moves from higher-height nodes to lower-height nodes. This local, distributed approach often makes it very fast in practice, especially for dense graphs.

## What Problem It Solves

Push-Relabel Maximum Flow solves the **Maximum Flow Problem**. This fundamental problem in graph theory can be formally stated as:

Given a directed graph $G = (V, E)$ with a source node $s \in V$, a sink node $t \in V$, and a capacity function $c: E \to \mathbb{R}^+$ for each edge $(u,v) \in E$, find a flow function $f: E \to \mathbb{R}^+$ such that:

1.  **Capacity Constraint**: For every edge $(u,v) \in E$, $0 \le f(u,v) \le c(u,v)$. (The flow through an edge cannot exceed its capacity).
2.  **Skew Symmetry**: For every edge $(u,v) \in E$, $f(u,v) = -f(v,u)$. (Flow from $u$ to $v$ is the negative of flow from $v$ to $u$, useful for residual graphs).
3.  **Flow Conservation**: For every node $u \in V \setminus \{s, t\}$, the total flow entering $u$ must equal the total flow leaving $u$. That is, $\sum_{v \in V} f(v,u) = \sum_{v \in V} f(u,v)$. (No flow is lost or gained at intermediate nodes).

The objective is to maximize the total flow leaving the source (or entering the sink), which is defined as $\sum_{v \in V} f(s,v)$.

**Why is it needed in machine learning?**

The Maximum Flow problem, and by extension Push-Relabel, is a powerful tool in machine learning and computer vision due to its close relationship with the **Minimum Cut problem** (Max-Flow Min-Cut Theorem). Many problems can be formulated as finding a minimum cut in a graph, which then can be solved by finding a maximum flow.

Here are a few examples:

*   **Image Segmentation**: A common technique for segmenting objects from an image involves constructing a graph where pixels are nodes. Edges connect adjacent pixels and also connect pixels to "source" (foreground) and "sink" (background) nodes. Edge capacities are defined based on pixel similarities and likelihood of being foreground/background. A minimum cut in this graph separates the pixels into two sets, corresponding to the foreground object and the background, effectively segmenting the image.
*   **Clustering**: Graph-cut based clustering algorithms can use max-flow min-cut to partition data points into clusters.
*   **Object Tracking**: In video analysis, tracking objects can sometimes be formulated as finding optimal paths or segmentations over time, which can involve max-flow min-cut.
*   **Energy Minimization**: Many problems in computer vision (e.g., stereo matching, image denoising) can be cast as energy minimization problems, which are often equivalent to finding a minimum cut in a specially constructed graph.

## How It Works

The Push-Relabel algorithm operates on the concept of a "preflow" and "heights" (or labels) for each vertex. A preflow is a flow that satisfies capacity constraints and skew symmetry, but *not necessarily* flow conservation for intermediate nodes. Instead, intermediate nodes can have "excess flow" – more flow entering than leaving. The algorithm's goal is to move all excess flow from intermediate nodes to the sink.

Here's a step-by-step breakdown:

1.  **Initialization**:
    *   Set the flow $f(u,v) = 0$ for all edges $(u,v)$.
    *   Initialize the `excess flow` $e(u) = 0$ for all nodes $u$.
    *   Initialize the `height` $h(u) = 0$ for all nodes $u$.
    *   For the source node $s$: Set its height $h(s) = |V|$ (where $|V|$ is the number of nodes in the graph). This makes the source "tallest" so flow can initially push out.
    *   Push as much flow as possible from the source $s$ to all its neighbors. For each edge $(s,v)$:
        *   Set $f(s,v) = c(s,v)$.
        *   Update $e(v) = e(v) + c(s,v)$.
        *   Update $e(s) = e(s) - c(s,v)$.
    *   All other nodes initially have $h(u)=0$ and $e(u)=0$.

2.  **Main Loop**:
    The algorithm continues as long as there is an **active vertex**. An active vertex is any vertex $u \in V \setminus \{s, t\}$ such that its excess flow $e(u) > 0$.

    Inside the loop, for an active vertex $u$, one of two operations is performed: `Push` or `Relabel`. The choice depends on whether $u$ can push flow to a "lower" neighbor.

3.  **Operations**:

    *   **`Push(u, v)`**:
        This operation moves flow from an active vertex $u$ to an adjacent vertex $v$. It can only be performed if:
        1.  $u$ has excess flow ($e(u) > 0$).
        2.  There is residual capacity on the edge $(u,v)$ (meaning $f(u,v) < c(u,v)$).
        3.  The height of $u$ is exactly one greater than the height of $v$ ($h(u) = h(v) + 1$). This ensures flow moves "downhill".

        If these conditions are met, flow is pushed:
        *   Calculate the amount of flow to push: $\Delta f = \min(e(u), c(u,v) - f(u,v))$.
        *   Increase flow on $(u,v)$: $f(u,v) = f(u,v) + \Delta f$.
        *   Decrease flow on $(v,u)$ (residual graph concept): $f(v,u) = f(v,u) - \Delta f$.
        *   Update excess flows: $e(u) = e(u) - \Delta f$ and $e(v) = e(v) + \Delta f$.

    *   **`Relabel(u)`**:
        This operation increases the height of an active vertex $u$. It is performed if:
        1.  $u$ has excess flow ($e(u) > 0$).
        2.  $u$ cannot push flow to any adjacent vertex $v$ with residual capacity because the height condition ($h(u) = h(v) + 1$) is not met for any such $v$. In other words, for all neighbors $v$ reachable from $u$ with residual capacity, $h(u) \le h(v)$.

        If these conditions are met, $u$'s height is increased:
        *   Set $h(u) = 1 + \min \{h(v) \mid (u,v) \text{ has residual capacity}\}$. This effectively raises $u$'s height just enough to allow it to push flow to its "lowest" neighbor with residual capacity, or to move it further away from the sink if all neighbors are "too high".

4.  **Termination**:
    The algorithm terminates when there are no more active vertices (i.e., all intermediate nodes have $e(u) = 0$). At this point, all excess flow has either reached the sink or returned to the source. The total flow into the sink $t$ (or out of the source $s$) is the maximum flow.

The key idea is that heights act like potential energy, guiding flow from higher potential to lower potential. The `Push` operation moves flow, and the `Relabel` operation increases potential when flow gets "stuck," allowing it to find new paths towards the sink. The algorithm guarantees that flow only moves towards the sink because $h(s) = |V|$ and $h(t) = 0$, and pushes always go from $h(u)$ to $h(v)$ where $h(u) = h(v) + 1$.

## Mathematical Intuition

The Push-Relabel algorithm relies on maintaining two crucial properties: a **preflow** and a **valid labeling (height function)**.

1.  **Preflow**:
    A preflow $f$ is a function that satisfies:
    *   **Capacity Constraint**: $f(u,v) \le c(u,v)$ for all $(u,v) \in E$.
    *   **Skew Symmetry**: $f(u,v) = -f(v,u)$ for all $(u,v) \in E$.
    *   **Excess Flow**: For any vertex $u \in V \setminus \{s\}$, the net flow into $u$ can be positive. This is called the excess flow at $u$, denoted $e(u)$.
        $$e(u) = \sum_{v \in V} f(v,u)$$
        Note that for the source $s$, $e(s)$ can be negative, representing flow leaving the source. For the sink $t$, $e(t)$ represents the total flow entering the sink.

2.  **Residual Graph and Residual Capacity**:
    The algorithm operates on a residual graph $G_f = (V, E_f)$, where $E_f$ contains edges $(u,v)$ if flow can still be pushed from $u$ to $v$.
    The **residual capacity** $c_f(u,v)$ for an edge $(u,v)$ is defined as:
    *   If $(u,v) \in E$: $c_f(u,v) = c(u,v) - f(u,v)$. This is the remaining capacity on the original edge.
    *   If $(v,u) \in E$: $c_f(u,v) = f(v,u)$. This allows "pushing back" flow, which is equivalent to reducing flow on the original edge $(v,u)$.
    An edge $(u,v)$ exists in $E_f$ if $c_f(u,v) > 0$.

3.  **Height Function (Labeling)**:
    A height function $h: V \to \mathbb{N}_0$ is a mapping from vertices to non-negative integers. It is considered **valid** if:
    *   $h(s) = |V|$ (or any value $\ge |V|$).
    *   $h(t) = 0$.
    *   For every edge $(u,v)$ in the residual graph $G_f$ (i.e., $c_f(u,v) > 0$), we must have $h(u) \le h(v) + 1$. This is the **admissibility condition**.

    The height function essentially represents a "distance" from the sink in the residual graph, but in a specific way. The condition $h(u) \le h(v) + 1$ implies that if you can push flow from $u$ to $v$, $v$ should not be "too far" below $u$.

    *   **`Push` Operation**:
        A `Push` operation from $u$ to $v$ is only allowed if $e(u) > 0$, $c_f(u,v) > 0$, AND $h(u) = h(v) + 1$.
        This condition ensures that flow is always pushed "downhill" by exactly one unit of height. This is crucial for the algorithm's correctness and termination. When flow is pushed, the residual capacities change, potentially creating new residual edges or removing existing ones.

    *   **`Relabel` Operation**:
        A `Relabel` operation on $u$ is performed when $e(u) > 0$ but $u$ cannot push flow to any neighbor $v$ because the condition $h(u) = h(v) + 1$ is not met for any $v$ with $c_f(u,v) > 0$.
        In this case, $u$ is "stuck". To allow it to push flow again, its height is increased:
        $$h(u) \leftarrow 1 + \min \{h(v) \mid c_f(u,v) > 0\}$$
        This new height makes $u$ exactly one unit taller than the "lowest" neighbor it can push to, thus enabling future `Push` operations. If $u$ cannot push to any neighbor (all neighbors are "taller" or have no residual capacity), its height will increase significantly, effectively moving it further away from the sink until it can find a path.

The algorithm terminates when all excess flow $e(u)$ for $u \in V \setminus \{s, t\}$ is zero. At this point, the preflow becomes a valid flow, and its value (total flow into $t$) is the maximum flow. The validity of the height function and the specific conditions for `Push` and `Relabel` ensure that no flow cycles are created and that flow eventually reaches the sink or returns to the source, leading to a maximum flow.

## Advantages

*   **Efficiency**: Push-Relabel algorithms, especially optimized versions (e.g., using a highest-label selection rule), are among the most efficient known algorithms for the maximum flow problem. Their theoretical worst-case time complexity is $O(V^2 E)$ or $O(V^3)$ for dense graphs, and $O(V^2 \sqrt{E})$ or $O(V^2 \log U)$ (where $U$ is max capacity) for specific implementations, which can be better than augmenting path algorithms for certain graph structures.
*   **Local Operations**: The algorithm operates locally, focusing on individual nodes with excess flow. This can make it suitable for parallelization, though practical parallel implementations are complex.
*   **No Augmenting Paths**: Unlike Edmonds-Karp or Dinic's, Push-Relabel does not explicitly search for augmenting paths. This can be an advantage as path finding can be computationally expensive.
*   **Handles Large Graphs**: Due to its efficiency, it's well-suited for solving maximum flow problems on large graphs that arise in real-world applications like image processing or network design.
*   **Preflow Concept**: The concept of preflow allows for a more flexible and less constrained approach initially, pushing flow without strict conservation, then resolving excesses.

## Disadvantages

*   **Complexity of Implementation**: Push-Relabel is generally more complex to implement correctly compared to simpler augmenting path algorithms like Edmonds-Karp. Managing residual capacities, excess flows, and heights, along with the specific conditions for `Push` and `Relabel`, requires careful coding.
*   **Not Intuitive for Tracing Flow**: While efficient, the flow path is not always clear or intuitive during the execution, as flow can be pushed back and forth, and excess flow moves around. This makes debugging or understanding the flow dynamics harder than path-based methods.
*   **Memory Usage**: It requires additional memory to store height labels and excess flow for each vertex, which can be significant for very large graphs.
*   **Worst-Case Performance**: While often fast in practice, certain graph structures can still lead to its theoretical worst-case performance, which might be slower than some highly optimized augmenting path algorithms (like Dinic's for specific graph types).
*   **No Direct Min-Cut**: While it finds the max flow, identifying the min-cut requires an additional step after the algorithm terminates (e.g., finding all nodes reachable from the source in the residual graph).

## Real World Applications

1.  **Image Segmentation (Graph Cuts)**: This is perhaps one of the most prominent applications in machine learning and computer vision. Given an image, the goal is to separate a foreground object from its background. A graph is constructed where pixels are nodes. Edges connect adjacent pixels (with capacities reflecting pixel similarity) and also connect pixels to a "source" (representing foreground) and a "sink" (representing background), with capacities reflecting the likelihood of a pixel belonging to foreground or background. A minimum cut in this graph corresponds to an optimal segmentation, and by the Max-Flow Min-Cut theorem, this can be found by computing the maximum flow.

2.  **Project Selection Problem**: In project management, you might have a set of potential projects, each with a cost and a revenue. Some projects might be prerequisites for others. The goal is to select a subset of projects to maximize total profit. This can be modeled as a maximum flow problem. A source connects to revenue-generating projects, a sink connects to cost-incurring projects, and prerequisite relationships are modeled with infinite capacity edges. A minimum cut in this graph reveals the optimal project selection.

3.  **Network Reliability and Design**: In telecommunications or transportation networks, maximum flow can be used to determine the maximum data throughput or traffic capacity between two points. This helps in designing robust networks, identifying bottlenecks, and assessing network reliability under various failure scenarios. For instance, if certain links fail, what is the maximum remaining capacity?

4.  **Bipartite Matching**: Finding a maximum bipartite matching (e.g., assigning workers to tasks, students to projects) can be reduced to a maximum flow problem. A source connects to one set of nodes (e.g., workers), which connect to the other set of nodes (e.g., tasks), which then connect to a sink. All capacities are 1. The maximum flow in this network gives the maximum number of pairings.

5.  **Supply Chain Optimization**: Companies can use maximum flow to optimize the flow of goods from factories (sources) through warehouses (intermediate nodes) to retail stores (sinks). Edge capacities represent transportation limits or warehouse storage capacities. The maximum flow determines the maximum amount of goods that can be moved through the supply chain, helping to identify bottlenecks and improve logistics.

## Python Example

Since popular machine learning libraries like `scikit-learn` do not directly implement graph algorithms like Push-Relabel Maximum Flow, we will provide a custom, standalone Python implementation to demonstrate its core mechanics.

```python
import collections

class PushRelabelMaxFlow:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        # Adjacency list: graph[u] = [(v, capacity)]
        self.graph = collections.defaultdict(list)
        # Residual graph: stores current flow and remaining capacity
        # residual_graph[u][v] = current_flow_on_u_v
        self.residual_graph = collections.defaultdict(lambda: collections.defaultdict(int))
        self.excess = [0] * num_nodes # Excess flow at each node
        self.height = [0] * num_nodes # Height label for each node

    def add_edge(self, u, v, capacity):
        """Adds a directed edge with a given capacity."""
        self.graph[u].append((v, capacity))
        # Initialize residual capacity for forward edge
        self.residual_graph[u][v] = capacity
        # Initialize residual capacity for backward edge (for pushing back flow)
        self.residual_graph[v][u] = 0 # Initially no flow, so 0 backward capacity

    def _push(self, u, v):
        """
        Pushes flow from u to v if conditions are met.
        Conditions: u has excess, residual capacity (u,v) > 0, h[u] == h[v] + 1
        """
        if self.excess[u] > 0 and self.residual_graph[u][v] > 0 and self.height[u] == self.height[v] + 1:
            # Amount of flow to push
            flow_amount = min(self.excess[u], self.residual_graph[u][v])

            # Update residual capacities
            self.residual_graph[u][v] -= flow_amount
            self.residual_graph[v][u] += flow_amount # Add to backward edge

            # Update excess flows
            self.excess[u] -= flow_amount
            self.excess[v] += flow_amount
            return True
        return False

    def _relabel(self, u):
        """
        Relabels node u if it has excess but cannot push to any lower neighbor.
        """
        if self.excess[u] > 0:
            min_neighbor_height = float('inf')
            can_push_anywhere = False

            # Find the minimum height of neighbors with residual capacity
            for v_neighbor in range(self.num_nodes):
                if self.residual_graph[u][v_neighbor] > 0:
                    if self.height[u] == self.height[v_neighbor] + 1:
                        can_push_anywhere = True # Can push, so no relabel needed yet
                        break
                    min_neighbor_height = min(min_neighbor_height, self.height[v_neighbor])
            
            # If cannot push to any lower neighbor, relabel
            if not can_push_anywhere and min_neighbor_height != float('inf'):
                self.height[u] = min_neighbor_height + 1
                return True
        return False

    def get_active_vertex(self, source, sink):
        """
        Returns an active vertex (has excess flow, not source/sink).
        Could be optimized with a queue or list of active vertices.
        """
        for u in range(self.num_nodes):
            if u != source and u != sink and self.excess[u] > 0:
                return u
        return -1 # No active vertex found

    def find_max_flow(self, source, sink):
        """
        Main Push-Relabel algorithm.
        """
        # 1. Initialization
        self.height[source] = self.num_nodes # Source height is N
        
        # Push initial flow from source to its neighbors
        for v_neighbor, capacity in self.graph[source]:
            flow_amount = capacity # Push full capacity from source
            
            self.residual_graph[source][v_neighbor] -= flow_amount
            self.residual_graph[v_neighbor][source] += flow_amount # Add to backward edge

            self.excess[source] -= flow_amount
            self.excess[v_neighbor] += flow_amount

        # 2. Main Loop: While there's an active vertex
        while True:
            u = self.get_active_vertex(source, sink)
            if u == -1: # No active vertex, algorithm terminates
                break

            # Try to push flow from u
            pushed = False
            for v_neighbor in range(self.num_nodes):
                if self._push(u, v_neighbor):
                    pushed = True
                    break # After a successful push, re-evaluate u or find next active vertex

            # If no push was possible, relabel u
            if not pushed:
                self._relabel(u)
        
        # 3. Termination: Max flow is the total excess at the sink
        return self.excess[sink]

# --- Example Usage ---
if __name__ == "__main__":
    # Example 1: Simple graph
    print("--- Example 1: Simple Graph ---")
    num_nodes_1 = 4
    source_1 = 0
    sink_1 = 3
    pr_flow_1 = PushRelabelMaxFlow(num_nodes_1)

    # Edges: (u, v, capacity)
    pr_flow_1.add_edge(0, 1, 10)
    pr_flow_1.add_edge(0, 2, 10)
    pr_flow_1.add_edge(1, 2, 2)
    pr_flow_1.add_edge(1, 3, 8)
    pr_flow_1.add_edge(2, 3, 10)

    max_flow_1 = pr_flow_1.find_max_flow(source_1, sink_1)
    print(f"Max Flow (Example 1): {max_flow_1}") # Expected: 18

    # Example 2: More complex graph (from CLRS textbook example)
    print("\n--- Example 2: CLRS Example ---")
    num_nodes_2 = 6 # s=0, o=1, p=2, q=3, r=4, t=5
    source_2 = 0
    sink_2 = 5
    pr_flow_2 = PushRelabelMaxFlow(num_nodes_2)

    pr_flow_2.add_edge(0, 1, 16) # s -> o
    pr_flow_2.add_edge(0, 2, 13) # s -> p
    pr_flow_2.add_edge(1, 3, 12) # o -> q
    pr_flow_2.add_edge(2, 1, 4)  # p -> o
    pr_flow_2.add_edge(2, 4, 14) # p -> r
    pr_flow_2.add_edge(3, 2, 9)  # q -> p
    pr_flow_2.add_edge(3, 5, 20) # q -> t
    pr_flow_2.add_edge(4, 3, 7)  # r -> q
    pr_flow_2.add_edge(4, 5, 4)  # r -> t

    max_flow_2 = pr_flow_2.find_max_flow(source_2, sink_2)
    print(f"Max Flow (Example 2): {max_flow_2}") # Expected: 23

    # Example 3: Graph with zero capacity edges (should be handled)
    print("\n--- Example 3: Zero Capacity Edge ---")
    num_nodes_3 = 3
    source_3 = 0
    sink_3 = 2
    pr_flow_3 = PushRelabelMaxFlow(num_nodes_3)

    pr_flow_3.add_edge(0, 1, 5)
    pr_flow_3.add_edge(1, 2, 0) # Zero capacity
    pr_flow_3.add_edge(0, 2, 3)

    max_flow_3 = pr_flow_3.find_max_flow(source_3, sink_3)
    print(f"Max Flow (Example 3): {max_flow_3}") # Expected: 3
```

**Explanation of the Python Code:**

1.  **`PushRelabelMaxFlow` Class**:
    *   `__init__(self, num_nodes)`: Initializes the graph with `num_nodes`.
        *   `self.graph`: An adjacency list to store the original graph structure and capacities.
        *   `self.residual_graph`: A dictionary of dictionaries to store the current residual capacities. `self.residual_graph[u][v]` represents the remaining capacity from `u` to `v`. This is crucial for both forward and backward flow.
        *   `self.excess`: A list to store the excess flow `e(u)` for each node `u`.
        *   `self.height`: A list to store the height `h(u)` for each node `u`.
    *   `add_edge(self, u, v, capacity)`: Adds a directed edge from `u` to `v` with a given `capacity`. It also initializes the residual capacities.
        *   `self.residual_graph[u][v] = capacity`: Sets the forward capacity.
        *   `self.residual_graph[v][u] = 0`: Initializes the backward capacity to 0, as no flow has been pushed yet.

2.  **`_push(self, u, v)` Method**:
    *   This method attempts to push flow from node `u` to node `v`.
    *   It checks the three conditions for a valid push: `u` has excess, there's residual capacity on `(u,v)`, and `h(u) == h(v) + 1`.
    *   If conditions are met, it calculates `flow_amount` (the minimum of `u`'s excess and `(u,v)`'s residual capacity).
    *   It updates `residual_graph` for both `(u,v)` (decreasing capacity) and `(v,u)` (increasing capacity, representing flow that can be pushed back).
    *   It updates `excess` for both `u` (decreasing) and `v` (increasing).

3.  **`_relabel(self, u)` Method**:
    *   This method attempts to relabel node `u`.
    *   It first checks if `u` has excess flow.
    *   It then iterates through all potential neighbors `v_neighbor` to see if `u` can push flow to any of them. If it can, `relabel` is not needed yet.
    *   If `u` cannot push to any neighbor (because `h(u) != h(v_neighbor) + 1` for all neighbors with residual capacity), it finds the minimum height among all neighbors `v_neighbor` that `u` *could* push to (i.e., `residual_graph[u][v_neighbor] > 0`).
    *   `u`'s height is then set to `min_neighbor_height + 1`.

4.  **`get_active_vertex(self, source, sink)` Method**:
    *   This helper method simply iterates through all nodes (excluding source and sink) and returns the first one it finds with `excess[u] > 0`. In a more optimized implementation, a queue or list of active vertices would be maintained for faster access.

5.  **`find_max_flow(self, source, sink)` Method**:
    *   **Initialization**:
        *   `self.height[source] = self.num_nodes`: Sets the source's height to `N`.
        *   It then performs the initial push from the source to all its direct neighbors, filling their capacities and creating initial excess at those neighbors.
    *   **Main Loop**:
        *   It repeatedly calls `get_active_vertex` to find a node `u` that has excess flow and is not the source or sink.
        *   If no active vertex is found, the loop breaks, and the algorithm terminates.
        *   Inside the loop, it first tries to `_push` flow from `u` to any of its neighbors. If a push is successful, it means `u` might still have excess or a new neighbor might have excess, so it continues the loop.
        *   If no `_push` was possible from `u` (meaning `u` is "stuck"), it calls `_relabel(u)` to increase `u`'s height, allowing it to potentially push flow in a future iteration.
    *   **Termination**: Once the loop finishes, all excess flow has either reached the sink or returned to the source. The total flow into the sink is simply `self.excess[sink]`.

The example demonstrates the algorithm with a few simple graphs, showing how to set up the graph and retrieve the maximum flow.

## Interview Questions

1.  **What is the core idea behind the Push-Relabel algorithm, and how does it differ from augmenting path algorithms like Edmonds-Karp?**
    *   **Answer**: The core idea of Push-Relabel is to maintain a "preflow" (where nodes can have excess incoming flow) and a "height function" for each node. It works by locally pushing excess flow from higher-height nodes to lower-height neighbors and relabeling (increasing height) nodes that are "stuck" until they can push flow. It differs from augmenting path algorithms (like Edmonds-Karp or Dinic's) because it doesn't explicitly search for paths from source to sink. Instead, it moves flow locally, potentially creating excess flow at intermediate nodes, and then systematically drains this excess towards the sink.

2.  **Define "excess flow" and "height label" in the context of Push-Relabel. How do they guide the algorithm?**
    *   **Answer**:
        *   **Excess Flow ($e(u)$)**: For any node $u$ (except the source), it's the net amount of flow that has entered $u$ minus the amount that has left $u$. If $e(u) > 0$, the node has excess flow that needs to be pushed towards the sink.
        *   **Height Label ($h(u)$)**: An integer value assigned to each node, representing its "distance" from the sink in a conceptual sense. The source typically has the highest label, and the sink has the lowest (0).
    *   **Guidance**: Excess flow identifies active nodes that need processing. Height labels guide the flow: flow is only pushed from a node $u$ to a node $v$ if $h(u) = h(v) + 1$, ensuring flow moves "downhill" towards the sink. If a node with excess cannot push flow downhill, its height is increased (relabel) to allow it to find new downhill paths.

3.  **Explain the two main operations: `Push` and `Relabel`. What are the conditions for each?**
    *   **Answer**:
        *   **`Push(u, v)`**: Moves flow from node $u$ to node $v$.
            *   **Conditions**:
                1.  $u$ has excess flow ($e(u) > 0$).
                2.  There is residual capacity on the edge $(u,v)$ ($c_f(u,v) > 0$).
                3.  The height of $u$ is exactly one greater than the height of $v$ ($h(u) = h(v) + 1$).
        *   **`Relabel(u)`**: Increases the height of node $u$.
            *   **Conditions**:
                1.  $u$ has excess flow ($e(u) > 0$).
                2.  $u$ cannot perform a `Push` operation to any neighbor $v$ with residual capacity (i.e., for all $v$ such that $c_f(u,v) > 0$, $h(u) \le h(v)$).
            *   **Action**: $h(u)$ is updated to $1 + \min \{h(v) \mid c_f(u,v) > 0\}$.

4.  **What is the significance of setting the source's initial height to $|V|$ (number of nodes)?**
    *   **Answer**: Setting $h(s) = |V|$ (or any sufficiently large value, typically $\ge |V|$) ensures that the source is initially "taller" than all other nodes (which start at height 0). This allows the initial `Push` operations from the source to its neighbors to occur, as $h(s)$ will be greater than $h(v)+1$ for any neighbor $v$ with $h(v)=0$. It establishes a high "potential" at the source, enabling flow to start moving.

5.  **How does the algorithm guarantee termination and correctness (finding the maximum flow)?**
    *   **Answer**:
        *   **Termination**: Each `Push` operation either moves flow towards the sink or back towards the source, reducing excess at some node. Each `Relabel` operation strictly increases a node's height. A node's height can increase at most $2|V|-1$ times (from 0 to $2|V|-2$). Since there are $|V|$ nodes, the total number of relabels is bounded. The total number of pushes is also bounded. These bounds ensure the algorithm terminates.
        *   **Correctness**: The algorithm maintains the invariant that for any edge $(u,v)$ with residual capacity, $h(u) \le h(v) + 1$. When the algorithm terminates, all excess flow has been pushed to the sink or returned to the source. This means the preflow becomes a valid flow. At termination, if there were any augmenting paths from source to sink, there would be an active node. Since there are no active nodes, no such path exists, implying a maximum flow (by the Max-Flow Min-Cut theorem).

6.  **What is the time complexity of the Push-Relabel algorithm? Are there different variants?**
    *   **Answer**: The basic Push-Relabel algorithm has a worst-case time complexity of $O(V^2 E)$. However, there are optimized variants:
        *   **Highest-Label Push-Relabel**: Always selecting an active vertex with the highest height label. This variant has a complexity of $O(V^3)$.
        *   **FIFO Push-Relabel**: Using a queue to manage active vertices (first-in, first-out). This variant has a complexity of $O(V^3)$.
        *   **Relabel-to-Front**: A specific implementation that uses a list of vertices and processes them in order, relabeling and pushing until a vertex becomes inactive, then moving it to the front. This variant achieves $O(V^3)$ or $O(V^2 \sqrt{E})$ for simple networks.
        *   For dense graphs, $O(V^3)$ is often better than $O(V^2 E)$.

7.  **How would you extract the minimum cut from the final state of the Push-Relabel algorithm?**
    *   **Answer**: After the Push-Relabel algorithm terminates, the maximum flow has been found. According to the Max-Flow Min-Cut theorem, the value of the maximum flow is equal to the capacity of the minimum cut. To find the actual cut $(S, T)$, where $S$ is the set of nodes reachable from the source and $T$ is the rest:
        1.  Perform a Breadth-First Search (BFS) or Depth-First Search (DFS) starting from the source $s$ in the *residual graph* using only edges with *positive residual capacity*.
        2.  All nodes reachable from $s$ in this residual graph form the set $S$.
        3.  The remaining nodes form the set $T = V \setminus S$.
        4.  The minimum cut consists of all original edges $(u,v)$ such that $u \in S$ and $v \in T$. The sum of their original capacities will equal the maximum flow.

8.  **Can Push-Relabel handle graphs with negative capacities? Why or why not?**
    *   **Answer**: No, standard Push-Relabel (and indeed, the Maximum Flow problem itself) assumes non-negative capacities. The concept of "flow" and "capacity" inherently implies non-negative values. If negative capacities were allowed, the problem could become ill-defined (e.g., infinite flow could be generated through cycles with negative capacity) or transform into a minimum cost flow problem, which is a different class of problem.

9.  **In what real-world scenarios would you prefer Push-Relabel over other max-flow algorithms?**
    *   **Answer**: Push-Relabel is often preferred in scenarios involving large, dense graphs, or when the graph structure is complex and augmenting path searches might be inefficient.
        *   **Image Segmentation**: Where graphs can be very large (pixels as nodes) and dense.
        *   **Computer Vision Problems**: Many energy minimization problems in vision map to min-cut, which benefits from efficient max-flow solvers.
        *   **General-purpose Max-Flow Libraries**: Many highly optimized max-flow libraries use Push-Relabel or its variants as their core algorithm due to its practical speed.

10. **What is a "preflow" and why is it allowed in Push-Relabel, whereas traditional flow algorithms require strict flow conservation at all intermediate nodes?**
    *   **Answer**: A "preflow" is a function that satisfies capacity constraints and skew symmetry, but *not necessarily* flow conservation for intermediate nodes. This means an intermediate node $u$ can have $e(u) > 0$, where more flow enters $u$ than leaves it.
    *   **Why allowed**: Push-Relabel's strategy is to first "saturate" the network by pushing as much flow as possible out of the source, creating these excesses. The algorithm then systematically "drains" these excesses towards the sink using `Push` and `Relabel` operations. This allows for a more aggressive, local approach to moving flow, rather than strictly maintaining conservation at every step. The algorithm ensures that by the time it terminates, all excesses at intermediate nodes are resolved, and the preflow becomes a valid flow.

## Quiz

1.  Which of the following is NOT a core component of the Push-Relabel algorithm?
    A) Excess flow
    B) Height labels
    C) Augmenting paths
    D) Residual graph

2.  What is the primary condition for a `Push` operation from node $u$ to node $v$?
    A) $h(u) < h(v)$
    B) $h(u) = h(v)$
    C) $h(u) = h(v) + 1$
    D) $h(u) > h(v) + 1$

3.  When does a `Relabel` operation occur for a node $u$?
    A) When $u$ has no excess flow.
    B) When $u$ can push flow to a neighbor $v$ where $h(u) = h(v) + 1$.
    C) When $u$ has excess flow but cannot push to any neighbor $v$ satisfying the height condition.
    D) When $u$ is the source node.

4.  If the Push-Relabel algorithm terminates, what does the excess flow at the sink node ($e(t)$) represent?
    A) The total capacity of the graph.
    B) The minimum cut value.
    C) The maximum flow value.
    D) The number of active nodes.

5.  Which of these problems can be solved using a Maximum Flow algorithm like Push-Relabel?
    A) Finding the shortest path in a graph.
    B) Image segmentation using graph cuts.
    C) Sorting a list of numbers.
    D) Calculating the determinant of a matrix.

---

### Answer Key

1.  **C) Augmenting paths**
    *   **Explanation**: Push-Relabel is a preflow-push algorithm that operates locally using excess flow and height labels. It does not explicitly search for augmenting paths from source to sink, which is characteristic of algorithms like Edmonds-Karp or Dinic's.

2.  **C) $h(u) = h(v) + 1$**
    *   **Explanation**: The `Push` operation is only allowed if the height of the source node $u$ is exactly one greater than the height of the destination node $v$. This ensures flow moves "downhill" by a single height unit.

3.  **C) When $u$ has excess flow but cannot push to any neighbor $v$ satisfying the height condition.**
    *   **Explanation**: A `Relabel` operation is performed when an active node $u$ (with excess flow) is "stuck" because it cannot find any adjacent node $v$ with residual capacity such that $h(u) = h(v) + 1$. Its height is then increased to allow future pushes.

4.  **C) The maximum flow value.**
    *   **Explanation**: Upon termination, all excess flow from intermediate nodes has been pushed either to the sink or back to the source. Therefore, the total excess flow accumulated at the sink represents the maximum amount of flow that could be sent from the source to the sink.

5.  **B) Image segmentation using graph cuts.**
    *   **Explanation**: Image segmentation is a classic application where the problem is formulated as finding a minimum cut in a graph, which by the Max-Flow Min-Cut theorem, is equivalent to finding the maximum flow. Shortest path, sorting, and matrix determinants are unrelated problems.

## Further Reading

1.  **"Introduction to Algorithms" by Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein (CLRS)**: Chapter 26, "Maximum Flow". This is the definitive textbook for algorithms and provides a detailed, rigorous explanation of Push-Relabel and other max-flow algorithms.
    *   *Link (search for the book)*: [https://mitpress.mit.edu/books/introduction-algorithms](https://mitpress.mit.edu/books/introduction-algorithms)

2.  **TopCoder Tutorial on Max Flow (includes Push-Relabel)**: TopCoder often has excellent competitive programming tutorials that explain algorithms clearly with practical insights.
    *   *Link*: [https://www.topcoder.com/thrive/articles/Max%20Flow%20-%20Part%202](https://www.topcoder.com/thrive/articles/Max%20Flow%20-%20Part%202) (Part 2 specifically covers Push-Relabel)

3.  **"Network Flows: Theory, Algorithms, and Applications" by Ravindra K. Ahuja, Thomas L. Magnanti, and James B. Orlin**: A comprehensive textbook dedicated entirely to network flow problems, including in-depth coverage of Push-Relabel and its advanced variants.
    *   *Link (search for the book)*: [https://www.pearson.com/us/higher-education/program/Ahuja-Network-Flows-Theory-Algorithms-and-Applications/PGM10842.html](https://www.pearson.com/us/higher-education/program/Ahuja-Network-Flows-Theory-Algorithms-and-Applications/PGM10842.html)