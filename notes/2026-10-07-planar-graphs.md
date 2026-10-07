# Planar Graphs

## Overview
A **Planar Graph** is a graph that can be drawn on a two-dimensional plane (like a piece of paper) in such a way that no two edges cross each other, except possibly at their shared vertices. If such a drawing exists, the graph is said to be *planar*. It's important to note that a graph is planar based on its *structure*, not just a particular drawing. If even one drawing exists without edge crossings, the graph is planar.

## What Problem It Solves
Planar graphs primarily address problems related to **layout, visualization, and physical realization** where avoiding intersections is crucial.
*   **Clarity and Readability**: In data visualization, a planar drawing makes complex networks easier to understand by eliminating confusing edge crossings.
*   **Physical Constraints**: In engineering and design, such as circuit board layout or pipeline routing, physical components cannot cross each other. Planar graphs help determine if a design can be realized without such intersections.
*   **Efficiency and Optimization**: Many graph algorithms (e.g., shortest path, max flow) can be solved more efficiently on planar graphs due to their simpler structure.
*   **Resource Management**: In network design, avoiding crossings can prevent signal interference or optimize resource allocation.

## How It Works
The core idea of a planar graph is its ability to be "embedded" in a plane. This means finding a specific geometric arrangement of its vertices and edges such that:
1.  Each vertex is represented by a distinct point.
2.  Each edge is represented by a continuous curve connecting its two endpoints.
3.  These curves (edges) only intersect at their common endpoints (vertices).

If such an embedding can be found, the graph is planar. The regions enclosed by the edges in a planar drawing are called **faces** (or regions), including the unbounded outer region. The existence of such a drawing is a fundamental property of the graph itself, not just a characteristic of one particular drawing.

## Mathematical Intuition
Two fundamental theorems provide the mathematical backbone for understanding planar graphs:

1.  **Euler's Formula for Planar Graphs**:
    For any *connected* planar graph, the number of vertices ($V$), edges ($E$), and faces ($F$) are related by the formula:
    $$V - E + F = 2$$
    This formula is incredibly powerful as it provides a simple relationship between the structural components of any connected planar graph. For example, if you know the number of vertices and edges, you can deduce the number of faces.

2.  **Kuratowski's Theorem**:
    This theorem provides a definitive characterization of planar graphs. It states that a finite graph is planar if and only if it does not contain a subgraph that is a subdivision of $K_5$ or $K_{3,3}$.
    *   $K_5$ is the **complete graph on 5 vertices**, meaning every pair of distinct vertices is connected by a unique edge. It has 5 vertices and 10 edges.
    *   $K_{3,3}$ is the **complete bipartite graph** where vertices are divided into two sets of 3, and every vertex in the first set is connected to every vertex in the second set. It has 6 vertices and 9 edges.
    *   A "subdivision" of a graph means a graph obtained by adding new vertices into the middle of existing edges (e.g., replacing an edge $u-v$ with $u-w-v$).
    Essentially, Kuratowski's Theorem says that these two graphs ($K_5$ and $K_{3,3}$) are the "minimal non-planar graphs," and any graph containing them (or their subdivisions) as a structural component cannot be drawn without crossings.

## Advantages
*   **Improved Readability and Visualization**: Planar drawings are inherently clearer and easier to interpret, especially for complex networks.
*   **Physical Realizability**: Essential for designing physical systems like integrated circuits, printed circuit boards (PCBs), and utility networks where components cannot physically cross.
*   **Efficient Algorithms**: Many graph problems (e.g., shortest path, maximum flow, minimum spanning tree) can be solved more efficiently on planar graphs than on general graphs.
*   **Theoretical Foundation**: Provides a strong theoretical basis for graph theory, leading to important theorems like the Four Color Theorem.

## Disadvantages
*   **Limited Scope**: Not all graphs are planar. Many real-world networks (e.g., social networks, the internet) are inherently non-planar, meaning planar graph theory cannot directly apply to their full structure.
*   **Complexity of Planarity Testing**: While algorithms exist to test planarity, they can still be computationally intensive for very large graphs.
*   **Embedding Uniqueness**: A planar graph can have multiple distinct planar embeddings, which can complicate certain applications.
*   **Drawing Algorithms**: Finding an aesthetically pleasing planar drawing can be a complex algorithmic challenge, even if the graph is known to be planar.

## Real World Applications
1.  **Circuit Board Design (PCBs)**: One of the most prominent applications. Traces on a PCB must not cross each other to prevent short circuits. Planar graph theory helps engineers design multi-layered boards or route traces efficiently to avoid intersections.
2.  **Map Coloring**: The famous Four Color Theorem states that any planar map can be colored with at most four colors such that no two adjacent regions have the same color. This is directly applicable to geographical maps, where countries or states are represented as faces of a planar graph.
3.  **Network Visualization and Layout**: Used in visualizing transportation networks, utility grids (water, gas, electricity), or even organizational charts to create clear, uncluttered diagrams that are easy to understand and navigate.

## Python Example
We can use the `networkx` library in Python to check if a graph is planar. `networkx` provides a function `is_planar()` which implements a planarity test.

```python
import networkx as nx
import matplotlib.pyplot as plt

# --- Example 1: A Planar Graph (Cycle Graph C4) ---
G_planar = nx.cycle_graph(4) # A square, clearly planar
print(f"Is G_planar (C4) planar? {nx.is_planar(G_planar)}")

# --- Example 2: A Non-Planar Graph (Kuratowski's K3,3) ---
# K3,3 is a complete bipartite graph with 3 vertices in each partition
G_non_planar_k33 = nx.complete_bipartite_graph(3, 3)
print(f"Is G_non_planar_k33 (K3,3) planar? {nx.is_planar(G_non_planar_k33)}")

# --- Example 3: Another Non-Planar Graph (Kuratowski's K5) ---
# K5 is a complete graph on 5 vertices
G_non_planar_k5 = nx.complete_graph(5)
print(f"Is G_non_planar_k5 (K5) planar? {nx.is_planar(G_non_planar_k5)}")

# Optional: Visualize a planar graph
plt.figure(figsize=(4, 4))
nx.draw_circular(G_planar, with_labels=True, node_color='lightblue', node_size=700, font_weight='bold')
plt.title("Planar Graph (C4)")
plt.show()

# Optional: Visualize a non-planar graph (it will still draw, but edges will cross)
plt.figure(figsize=(4, 4))
nx.draw_circular(G_non_planar_k33, with_labels=True, node_color='lightcoral', node_size=700, font_weight='bold')
plt.title("Non-Planar Graph (K3,3)")
plt.show()
```

## Interview Questions
1.  **Define a planar graph and provide an example of a graph that is planar and one that is not.**
    *   **Answer**: A planar graph is a graph that can be drawn on a plane without any edges crossing each other except at their vertices. An example of a planar graph is a simple cycle graph (e.g., a square or a triangle). An example of a non-planar graph is $K_5$ (the complete graph on 5 vertices) or $K_{3,3}$ (the complete bipartite graph with 3 vertices in each partition).

2.  **State Euler's formula for planar graphs and explain its significance.**
    *   **Answer**: Euler's formula states that for any connected planar graph, $V - E + F = 2$, where $V$ is the number of vertices, $E$ is the number of edges, and $F$ is the number of faces (regions, including the outer unbounded region). Its significance lies in providing a fundamental topological invariant for planar graphs, relating their basic structural components. It can be used to prove properties about planar graphs, such as bounds on the number of edges.

3.  **What is Kuratowski's Theorem, and how is it used to determine if a graph is planar?**
    *   **Answer**: Kuratowski's Theorem states that a finite graph is planar if and only if it does not contain a subgraph that is a subdivision of $K_5$ (the complete graph on 5 vertices) or $K_{3,3}$ (the complete bipartite graph with 3 vertices in each partition). To determine if a graph is planar using this theorem, one would look for the presence of these specific non-planar "forbidden minors" (or their subdivisions) within the graph. If neither is found, the graph is planar; otherwise, it is not.

## Quiz
1.  For a connected planar graph with 10 vertices and 15 edges, how many faces does it have according to Euler's formula?
    a) 5
    b) 7
    c) 9
    d) 12
    *   **Answer**: b) 7 ($V - E + F = 2 \Rightarrow 10 - 15 + F = 2 \Rightarrow -5 + F = 2 \Rightarrow F = 7$)

2.  Which of the following graphs is *always* non-planar according to Kuratowski's Theorem?
    a) A tree
    b) A cycle graph $C_n$ for any $n \ge 3$
    c) $K_5$ (complete graph on 5 vertices)
    d) A path graph
    *   **Answer**: c) $K_5$

## Further Reading
1.  **Wikipedia - Planar Graph**: [https://en.wikipedia.org/wiki/Planar_graph](https://en.wikipedia.org/wiki/Planar_graph)
2.  **NetworkX Documentation - Planarity Testing**: [https://networkx.org/documentation/stable/reference/algorithms/planarity.html](https://networkx.org/documentation/stable/reference/algorithms/planarity.html)
3.  **Graph Theory by Reinhard Diestel (Chapter 4: Planar Graphs)**: A comprehensive textbook for deeper mathematical understanding.