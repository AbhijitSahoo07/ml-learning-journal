# Topological Sorting (Kahn's Algorithm)

## Overview
Topological Sorting is an algorithm used to order the vertices of a Directed Acyclic Graph (DAG) in such a way that for every directed edge $u \to v$, vertex $u$ comes before vertex $v$ in the ordering. Think of it as finding a valid sequence of tasks where some tasks must be completed before others. It's like creating a "to-do list" where you respect all prerequisites.

Kahn's Algorithm is one of the two primary algorithms for performing topological sorting (the other being based on Depth-First Search). It's particularly intuitive because it directly models the idea of "tasks with no pending prerequisites." It works by repeatedly finding nodes that have no incoming edges (i.e., no prerequisites) and adding them to the sorted list, then removing them and their outgoing edges from the graph, which in turn might make other nodes have no incoming edges. This process continues until all nodes are sorted or a cycle is detected.

## What Problem It Solves
Topological Sorting, and specifically Kahn's Algorithm, addresses problems where there's a set of items or tasks with dependencies, and you need to find a valid linear ordering of these items. The key constraint is that these dependencies must not form a cycle (i.e., you can't have Task A depend on Task B, and Task B depend on Task A, directly or indirectly).

In machine learning and related fields, this is crucial for:
*   **Dependency Resolution**: Many ML workflows involve a sequence of steps: data loading, preprocessing, feature engineering, model training, evaluation, deployment. Some steps depend on the completion of others (e.g., you can't train a model before preprocessing the data). Topological sorting helps define a valid execution order for these steps.
*   **Build Systems**: Compiling code or building complex ML models often involves many files and libraries with interdependencies. A build system uses topological sorting to determine the correct order in which to compile or link components.
*   **Task Scheduling**: In distributed ML systems or data pipelines (like Apache Airflow or Kubeflow), tasks often have dependencies. Topological sorting helps schedule these tasks efficiently, ensuring prerequisites are met before a task is executed.
*   **Course Scheduling**: In academic settings, courses often have prerequisites. Topological sorting can help determine a valid sequence of courses a student can take.
*   **Data Flow Analysis**: In compilers or data processing engines, understanding the flow of data and operations often involves directed graphs, and topological sorting can help optimize execution.

Essentially, whenever you have a "precedes" or "depends on" relationship that forms a DAG, topological sorting is the tool to find a valid sequential order.

## How It Works
Kahn's Algorithm operates on the principle of identifying nodes that have no incoming dependencies and processing them first. Here's a step-by-step breakdown:

1.  **Calculate In-Degrees**: For every node in the graph, determine its "in-degree." The in-degree of a node is the number of incoming edges it has. These represent the number of prerequisites that must be met before this node can be processed.

2.  **Initialize Queue**: Create a queue (e.g., a `collections.deque` in Python) and add all nodes that have an in-degree of 0 to this queue. These are the nodes that have no prerequisites and can be processed first.

3.  **Process Nodes**: While the queue is not empty:
    a.  **Dequeue Node**: Remove a node, let's call it `u`, from the front of the queue.
    b.  **Add to Result**: Add `u` to your topological sort result list.
    c.  **Update Neighbors**: For each neighbor `v` of `u` (i.e., for every edge $u \to v$):
        i.  Decrement the in-degree of `v` by 1. This signifies that one of `v`'s prerequisites (`u`) has now been met.
        ii. If the in-degree of `v` becomes 0, it means all of `v`'s prerequisites have now been met. Add `v` to the queue.

4.  **Check for Cycles**: After the loop finishes, compare the number of nodes in your topological sort result list with the total number of nodes in the graph.
    *   If they are equal, it means all nodes were successfully sorted, and the graph is a DAG.
    *   If they are not equal, it means there's a cycle in the graph, and a topological sort is not possible. The remaining nodes in the graph are part of this cycle.

**Example Walkthrough:**

Consider a graph: A -> B, A -> C, B -> D, C -> D, D -> E

1.  **In-Degrees**:
    *   A: 0
    *   B: 1 (from A)
    *   C: 1 (from A)
    *   D: 2 (from B, C)
    *   E: 1 (from D)

2.  **Initialize Queue**: Queue = [A] (since A has in-degree 0)
    Result = []

3.  **Process Nodes**:
    *   **Iteration 1**:
        *   Dequeue A. Result = [A]
        *   Neighbors of A: B, C.
        *   Decrement in-degree of B (now 0). Add B to queue. Queue = [B]
        *   Decrement in-degree of C (now 0). Add C to queue. Queue = [B, C]
    *   **Iteration 2**:
        *   Dequeue B. Result = [A, B]
        *   Neighbors of B: D.
        *   Decrement in-degree of D (now 1). Queue = [C]
    *   **Iteration 3**:
        *   Dequeue C. Result = [A, B, C]
        *   Neighbors of C: D.
        *   Decrement in-degree of D (now 0). Add D to queue. Queue = [D]
    *   **Iteration 4**:
        *   Dequeue D. Result = [A, B, C, D]
        *   Neighbors of D: E.
        *   Decrement in-degree of E (now 0). Add E to queue. Queue = [E]
    *   **Iteration 5**:
        *   Dequeue E. Result = [A, B, C, D, E]
        *   Neighbors of E: None. Queue = []

4.  **Check for Cycles**: Result length (5) == Total nodes (5). No cycle.
    Final Topological Sort: [A, B, C, D, E] (or [A, C, B, D, E] if C was dequeued before B in step 1, as both had in-degree 0 at that point).

## Mathematical Intuition
The mathematical intuition behind Kahn's Algorithm is rooted in graph theory, specifically the properties of Directed Acyclic Graphs (DAGs).

1.  **Directed Acyclic Graph (DAG)**: A topological sort is only possible for a DAG. A directed graph $G = (V, E)$ consists of a set of vertices $V$ and a set of directed edges $E$. An edge $(u, v) \in E$ means there's a dependency where $u$ must precede $v$. "Acyclic" means there are no cycles; you can't start at a vertex, follow a sequence of directed edges, and return to the same vertex. If a cycle exists, a topological sort is impossible because there's a circular dependency (e.g., A depends on B, B depends on C, and C depends on A).

2.  **In-Degree**: The core concept is the in-degree of a vertex. For a vertex $v \in V$, its in-degree, denoted as $indegree(v)$, is the number of incoming edges to $v$. Mathematically,
    $$indegree(v) = \sum_{(u,v) \in E} 1$$
    A vertex with an in-degree of 0 has no prerequisites. It can be the first task to be executed.

3.  **Iterative Dependency Removal**: Kahn's algorithm works by iteratively finding and "removing" these prerequisite-free vertices.
    *   When a vertex $u$ with $indegree(u) = 0$ is selected, it means all its prerequisites (which are none) have been met.
    *   By adding $u$ to the topological sort and then conceptually "removing" it from the graph (along with its outgoing edges), we are essentially saying that $u$ has been processed.
    *   For every neighbor $v$ of $u$ (i.e., for every edge $u \to v$), decrementing $indegree(v)$ by 1 reflects that one of $v$'s prerequisites ($u$) has now been satisfied.
    *   If $indegree(v)$ becomes 0, it implies that all of $v$'s prerequisites have now been met, making $v$ eligible to be processed next. This process continues, effectively "unraveling" the dependencies layer by layer.

4.  **Existence of a Source**: In any non-empty DAG, there must be at least one vertex with an in-degree of 0. This is a fundamental property that guarantees Kahn's algorithm can always start. If there were no such vertex, it would imply that every vertex has at least one incoming edge, which would inevitably lead to a cycle in a finite graph.

The algorithm's correctness relies on the fact that by always picking nodes with no outstanding prerequisites, we maintain a valid ordering. If a cycle exists, the algorithm will eventually run out of nodes with an in-degree of 0 before processing all nodes, thus correctly identifying the cycle.

## Advantages
*   **Simple and Intuitive**: The logic of finding nodes with no prerequisites and processing them is very straightforward to understand and implement.
*   **Detects Cycles**: Kahn's algorithm naturally detects if a graph contains a cycle. If the final topological sort list does not contain all the graph's vertices, a cycle exists.
*   **Guaranteed to Find a Solution (if one exists)**: For any DAG, Kahn's algorithm will produce a valid topological sort.
*   **Efficient**: The time complexity is $O(V + E)$, where $V$ is the number of vertices and $E$ is the number of edges. This is optimal for graph traversal algorithms, as it visits each vertex and edge at most a constant number of times.
*   **Multiple Solutions**: If multiple topological sorts are possible (which is common), Kahn's algorithm can produce different valid sorts depending on the order in which nodes are dequeued from the queue when multiple nodes have an in-degree of 0.

## Disadvantages
*   **Only for DAGs**: The most significant limitation is that it only works for Directed Acyclic Graphs. If the graph contains a cycle, it cannot produce a complete topological sort.
*   **Space Complexity**: Requires additional space to store in-degrees for all vertices ($O(V)$) and an adjacency list for the graph ($O(V+E)$), as well as the queue ($O(V)$ in the worst case).
*   **Not Unique**: For many DAGs, there can be multiple valid topological sorts. Kahn's algorithm produces one such valid sort, but not necessarily a unique one or one that satisfies additional criteria (e.g., shortest path, earliest completion time).
*   **Requires Graph Representation**: Needs the graph to be explicitly represented (e.g., adjacency list) to efficiently calculate in-degrees and iterate through neighbors.

## Real World Applications
1.  **Task Scheduling and Project Management**:
    *   **Use Case**: In project management software or build systems (like `make` or `Gradle`), tasks often have dependencies. For example, "compile module A" must happen before "link executable B," and "run tests" must happen after "link executable B."
    *   **Application**: Kahn's algorithm can determine a valid order to execute these tasks, ensuring all prerequisites are met. If a circular dependency is detected (e.g., Task A depends on B, B depends on C, and C depends on A), the system can flag it as an error.

2.  **Course Prerequisite Systems**:
    *   **Use Case**: Universities have course catalogs where certain courses are prerequisites for others (e.g., "Calculus I" before "Calculus II," "Introduction to Programming" before "Data Structures").
    *   **Application**: A student's academic plan can be modeled as a DAG. Topological sorting can generate a valid sequence of courses a student can take to fulfill their degree requirements, respecting all prerequisites.

3.  **Compiler Optimization and Instruction Scheduling**:
    *   **Use Case**: In compilers, when optimizing code, instructions often have data dependencies (e.g., instruction B uses the result of instruction A). To maximize parallel execution on multi-core processors, instructions need to be scheduled in an order that respects these dependencies.
    *   **Application**: The instructions and their dependencies form a DAG. Topological sorting can provide a valid execution order for instructions, which can then be further optimized for parallel execution while maintaining correctness.

4.  **Data Processing Pipelines (e.g., Apache Airflow, Kubeflow)**:
    *   **Use Case**: Modern machine learning and data engineering workflows involve complex pipelines with many interconnected steps: data ingestion, cleaning, transformation, feature engineering, model training, evaluation, deployment. These steps often depend on the successful completion of previous ones.
    *   **Application**: These pipelines are naturally represented as DAGs. Kahn's algorithm is used internally by orchestrators like Apache Airflow to determine the execution order of tasks, ensuring data readiness and proper sequencing.

5.  **Dependency Resolution in Package Managers**:
    *   **Use Case**: When you install software packages (e.g., using `pip` for Python, `npm` for Node.js, `apt` for Debian), packages often depend on other packages.
    *   **Application**: The package dependencies form a DAG. Topological sorting helps determine the correct order in which to install packages, ensuring that all dependencies of a package are installed before the package itself.

## Python Example

This example demonstrates Kahn's Algorithm to perform a topological sort on a given Directed Acyclic Graph (DAG). We'll represent the graph using an adjacency list.

```python
import collections

def kahn_topological_sort(num_vertices, edges):
    """
    Performs topological sorting using Kahn's Algorithm.

    Args:
        num_vertices (int): The total number of vertices in the graph.
        edges (list of tuples): A list of (u, v) tuples representing directed edges
                                from u to v. Vertices are 0-indexed.

    Returns:
        list: A list representing one possible topological sort of the graph.
              Returns an empty list if a cycle is detected.
    """
    
    # 1. Initialize data structures
    # Adjacency list to store the graph
    adj = collections.defaultdict(list)
    # In-degree array to store the number of incoming edges for each vertex
    in_degree = [0] * num_vertices

    # 2. Build the graph and calculate initial in-degrees
    for u, v in edges:
        adj[u].append(v)
        in_degree[v] += 1

    # 3. Initialize the queue with all vertices having an in-degree of 0
    queue = collections.deque()
    for i in range(num_vertices):
        if in_degree[i] == 0:
            queue.append(i)

    # List to store the topological sort result
    topological_order = []
    
    # Counter for visited nodes to detect cycles
    visited_nodes_count = 0

    # 4. Process nodes from the queue
    while queue:
        u = queue.popleft()
        topological_order.append(u)
        visited_nodes_count += 1

        # For each neighbor v of u
        for v in adj[u]:
            in_degree[v] -= 1  # Decrement in-degree of v
            # If v's in-degree becomes 0, add it to the queue
            if in_degree[v] == 0:
                queue.append(v)

    # 5. Check for cycles
    if visited_nodes_count != num_vertices:
        print("Error: The graph contains a cycle. Topological sort is not possible.")
        return [] # Return empty list to indicate a cycle
    else:
        return topological_order

# --- Example Usage ---

# Example 1: A simple DAG
print("--- Example 1: Simple DAG ---")
num_vertices_1 = 6 # Vertices 0, 1, 2, 3, 4, 5
edges_1 = [
    (5, 2),
    (5, 0),
    (4, 0),
    (4, 1),
    (2, 3),
    (3, 1)
]
# Expected output: one possible order could be [4, 5, 0, 2, 3, 1] or [5, 4, 0, 2, 3, 1] etc.
# Visual representation:
# 5 -> 2 -> 3 -> 1
# ^    ^
# |    |
# 4 -> 0

sorted_order_1 = kahn_topological_sort(num_vertices_1, edges_1)
if sorted_order_1:
    print(f"Topological Sort Order: {sorted_order_1}")
else:
    print("No topological sort found for Example 1.")

print("\n--- Example 2: Another DAG (Course Prerequisites) ---")
# Courses: 0: Intro, 1: Algebra, 2: Calc I, 3: Calc II, 4: Diff Eq, 5: Linear Alg
# Dependencies:
# Intro -> Algebra
# Intro -> Calc I
# Algebra -> Calc II
# Calc I -> Calc II
# Calc II -> Diff Eq
# Calc II -> Linear Alg
num_vertices_2 = 6
edges_2 = [
    (0, 1), # Intro -> Algebra
    (0, 2), # Intro -> Calc I
    (1, 3), # Algebra -> Calc II
    (2, 3), # Calc I -> Calc II
    (3, 4), # Calc II -> Diff Eq
    (3, 5)  # Calc II -> Linear Alg
]

sorted_order_2 = kahn_topological_sort(num_vertices_2, edges_2)
if sorted_order_2:
    print(f"Topological Sort Order: {sorted_order_2}")
else:
    print("No topological sort found for Example 2.")

print("\n--- Example 3: Graph with a Cycle ---")
num_vertices_3 = 3
edges_3 = [
    (0, 1),
    (1, 2),
    (2, 0) # This creates a cycle: 0 -> 1 -> 2 -> 0
]

sorted_order_3 = kahn_topological_sort(num_vertices_3, edges_3)
if sorted_order_3:
    print(f"Topological Sort Order: {sorted_order_3}")
else:
    print("No topological sort found for Example 3 (as expected due to cycle).")

```

**Explanation of the Python Code:**

1.  **`kahn_topological_sort(num_vertices, edges)` function**:
    *   Takes `num_vertices` (total nodes) and `edges` (list of `(u, v)` tuples) as input.
    *   `collections.defaultdict(list)`: Used for `adj` (adjacency list). `adj[u]` will store a list of all vertices `v` such that there's an edge `u -> v`.
    *   `in_degree = [0] * num_vertices`: An array to store the in-degree for each vertex. `in_degree[i]` will be the count of incoming edges to vertex `i`.

2.  **Building Graph and In-Degrees**:
    *   It iterates through all `(u, v)` edges.
    *   `adj[u].append(v)`: Adds `v` to the list of neighbors for `u`.
    *   `in_degree[v] += 1`: Increments the in-degree of `v` because there's an incoming edge from `u` to `v`.

3.  **Initializing Queue**:
    *   `queue = collections.deque()`: A double-ended queue is efficient for `append` and `popleft` operations.
    *   It iterates through all vertices. If a vertex `i` has `in_degree[i] == 0`, it means it has no prerequisites, so it's added to the `queue`.

4.  **Processing Nodes**:
    *   The `while queue:` loop continues as long as there are nodes to process.
    *   `u = queue.popleft()`: Removes a node `u` from the front of the queue. This `u` is now considered processed.
    *   `topological_order.append(u)`: Adds `u` to our result list.
    *   `visited_nodes_count += 1`: Keeps track of how many nodes we've successfully added to the sort.
    *   **Updating Neighbors**: For each `v` that `u` points to (`for v in adj[u]`):
        *   `in_degree[v] -= 1`: We decrement `v`'s in-degree because `u` (one of its prerequisites) has now been processed.
        *   `if in_degree[v] == 0: queue.append(v)`: If `v`'s in-degree becomes 0, it means all its prerequisites are now met, so `v` is ready to be processed and is added to the queue.

5.  **Cycle Detection**:
    *   After the loop, if `visited_nodes_count` is not equal to `num_vertices`, it implies that some nodes were never added to the `topological_order` list. This can only happen if those remaining nodes are part of a cycle, as they would never reach an in-degree of 0. In this case, the function prints an error and returns an empty list.
    *   Otherwise, it returns the `topological_order`.

The examples demonstrate how it works for a simple DAG, a more complex DAG (course prerequisites), and a graph containing a cycle.

## Interview Questions

1.  **What is Topological Sorting, and what kind of graphs can it be applied to?**
    *   **Answer**: Topological Sorting is an algorithm for ordering the vertices of a Directed Acyclic Graph (DAG) such that for every directed edge $u \to v$, vertex $u$ comes before vertex $v$ in the ordering. It can only be applied to Directed Acyclic Graphs (DAGs) because if a cycle exists, there's a circular dependency, making a linear ordering impossible.

2.  **Explain the core idea behind Kahn's Algorithm for Topological Sorting.**
    *   **Answer**: Kahn's Algorithm works by iteratively finding and processing nodes that have no incoming edges (i.e., an in-degree of 0). These nodes have no prerequisites and can be placed first in the topological order. Once such a node is processed, it's conceptually removed from the graph, and its outgoing edges are also removed. This reduction might cause other nodes to now have an in-degree of 0, making them eligible for processing. This process continues until all nodes are processed or a cycle is detected.

3.  **How does Kahn's Algorithm detect cycles in a graph?**
    *   **Answer**: Kahn's Algorithm detects cycles by keeping track of the number of nodes added to the topological sort. If, after the algorithm finishes, the total number of nodes in the topological sort list is less than the total number of vertices in the graph, it means that some nodes were never able to reach an in-degree of 0. These unvisited nodes must be part of a cycle, as they always have at least one incoming edge that prevents their in-degree from becoming zero.

4.  **What is the time and space complexity of Kahn's Algorithm?**
    *   **Answer**:
        *   **Time Complexity**: $O(V + E)$, where $V$ is the number of vertices and $E$ is the number of edges. This is because each vertex and each edge is visited and processed a constant number of times (e.g., calculating in-degrees, iterating through neighbors).
        *   **Space Complexity**: $O(V + E)$. This is primarily for storing the adjacency list (graph representation) and the in-degree array. The queue can also hold up to $O(V)$ vertices in the worst case.

5.  **Compare Kahn's Algorithm with the DFS-based approach for Topological Sorting.**
    *   **Answer**:
        *   **Kahn's Algorithm (BFS-based)**: Uses a queue, starts with nodes of in-degree 0, and iteratively removes dependencies. Naturally detects cycles by counting processed nodes.
        *   **DFS-based Algorithm**: Uses recursion (or an explicit stack), starts a DFS from an unvisited node, and adds nodes to the topological order *after* all their descendants have been visited. Detects cycles by checking for back-edges to nodes currently in the recursion stack.
        *   Both have $O(V+E)$ time and space complexity. Kahn's is often considered more intuitive for dependency resolution, while DFS is more common for general graph traversal.

6.  **Can a graph have multiple valid topological sorts? If so, how does Kahn's Algorithm handle this?**
    *   **Answer**: Yes, a graph can have multiple valid topological sorts if, at any point, there are multiple nodes with an in-degree of 0. Kahn's Algorithm will produce one of these valid sorts. The specific order depends on which node is dequeued first when multiple nodes are available in the queue. The algorithm doesn't guarantee a unique sort, nor does it try to find all possible sorts.

7.  **In what real-world scenarios would you prefer Kahn's Algorithm over a DFS-based topological sort?**
    *   **Answer**: Kahn's Algorithm is often preferred in scenarios where:
        *   **Dependency resolution is explicit**: The concept of "no prerequisites" maps directly to in-degree 0, making it very intuitive for task scheduling, build systems, or course prerequisites.
        *   **Cycle detection is a primary concern**: Its cycle detection mechanism (comparing processed nodes to total nodes) is straightforward.
        *   **Breadth-first processing is beneficial**: If there's a preference for processing "layers" of dependencies (e.g., all tasks with no prerequisites, then all tasks whose prerequisites are now met, and so on), Kahn's algorithm naturally provides this.

8.  **What happens if you try to run Kahn's Algorithm on a graph that is not directed?**
    *   **Answer**: Kahn's Algorithm is specifically designed for directed graphs. If applied to an undirected graph, the concept of "in-degree" would need to be reinterpreted (e.g., as just "degree"). However, an undirected graph with edges can always be considered to have cycles (e.g., $A-B$ implies $A \to B$ and $B \to A$ if treated as directed edges), making a topological sort impossible in the traditional sense. The algorithm would likely detect cycles or produce an arbitrary ordering that doesn't hold the "precedes" property.

9.  **How would you modify Kahn's Algorithm to find *all* possible topological sorts?**
    *   **Answer**: To find all possible topological sorts, Kahn's Algorithm would need to be adapted into a recursive backtracking algorithm. Instead of simply `popleft()` from the queue, at each step, if there are multiple nodes with an in-degree of 0, we would recursively explore each choice. For each choice:
        1.  Add the chosen node to the current path.
        2.  Decrement in-degrees of its neighbors.
        3.  Recursively call the function with the updated graph state.
        4.  **Backtrack**: Increment in-degrees of neighbors and remove the node from the current path to explore other choices.
    *   This approach would be significantly more complex and computationally expensive, as the number of topological sorts can grow factorially.

10. **Can Kahn's Algorithm be used to find the critical path in a project schedule?**
    *   **Answer**: No, Kahn's Algorithm by itself cannot find the critical path. A critical path involves finding the longest path in a DAG, often when edges have weights representing task durations. While topological sorting provides a valid order, it doesn't inherently consider path lengths or durations. Algorithms like the Bellman-Ford algorithm (adapted for DAGs) or dynamic programming approaches are typically used for critical path analysis. However, a topological sort can be a *pre-processing step* for such algorithms, as it provides a valid order to process nodes for calculating longest/shortest paths efficiently.

## Quiz

1.  Which type of graph is required for Topological Sorting?
    A) Undirected Graph
    B) Directed Graph with cycles
    C) Directed Acyclic Graph (DAG)
    D) Weighted Graph

2.  What is the primary data structure used in Kahn's Algorithm to manage nodes ready for processing?
    A) Stack
    B) Priority Queue
    C) Queue
    D) Hash Map

3.  What does the "in-degree" of a vertex represent in the context of Kahn's Algorithm?
    A) The number of outgoing edges from the vertex.
    B) The number of incoming edges to the vertex.
    C) The total number of edges connected to the vertex.
    D) The weight of the vertex.

4.  How does Kahn's Algorithm detect the presence of a cycle in a graph?
    A) By checking if any node is visited twice during the process.
    B) By comparing the length of the topological sort result with the total number of vertices.
    C) By encountering a negative edge weight.
    D) By using a separate Depth-First Search.

5.  What is the time complexity of Kahn's Algorithm for a graph with $V$ vertices and $E$ edges?
    A) $O(V^2)$
    B) $O(E \log V)$
    C) $O(V + E)$
    D) $O(V \cdot E)$

---

### Answer Key

1.  **C) Directed Acyclic Graph (DAG)**
    *   **Explanation**: Topological sorting is only possible on Directed Acyclic Graphs because it requires a linear ordering of tasks without circular dependencies.

2.  **C) Queue**
    *   **Explanation**: Kahn's Algorithm uses a queue to store all vertices that currently have an in-degree of 0, representing tasks that are ready to be processed.

3.  **B) The number of incoming edges to the vertex.**
    *   **Explanation**: The in-degree of a vertex counts its prerequisites. A vertex with an in-degree of 0 has no outstanding prerequisites.

4.  **B) By comparing the length of the topological sort result with the total number of vertices.**
    *   **Explanation**: If the number of nodes successfully added to the topological sort list is less than the total number of vertices in the graph, it implies that the remaining nodes are part of a cycle and could never reach an in-degree of 0.

5.  **C) $O(V + E)$**
    *   **Explanation**: Kahn's Algorithm visits each vertex and each edge a constant number of times (for calculating in-degrees, adding to queue, and processing neighbors), leading to an optimal time complexity for graph traversal.

## Further Reading

1.  **GeeksforGeeks - Topological Sort (Kahn's algorithm)**: A classic resource for algorithm explanations with clear examples and code.
    *   [https://www.geeksforgeeks.org/topological-sort-using-kahn-algorithm/](https://www.geeksforgeeks.org/topological-sort-using-kahn-algorithm/)

2.  **Introduction to Algorithms (CLRS) - Chapter 22: Elementary Graph Algorithms**: This textbook provides a rigorous and detailed explanation of topological sort, including both Kahn's algorithm and the DFS-based approach, along with proofs of correctness. (Specific page numbers vary by edition, but look for the section on Topological Sort in Chapter 22).
    *   *Note: This is a textbook, not a direct link. You'd need to access the book.*

3.  **Khan Academy - Topological sort algorithm**: Offers an interactive and visual explanation of topological sorting, which can be very helpful for beginners.
    *   [https://www.khanacademy.org/computing/computer-science/algorithms/topological-sort/a/topological-sort](https://www.khanacademy.org/computing/computer-science/algorithms/topological-sort/a/topological-sort)