# Problem Solving for Agents

## Overview
In the fascinating world of Artificial Intelligence, an "agent" is anything that can perceive its environment through sensors and act upon that environment through effectors. Think of a self-driving car perceiving the road with cameras and lidar, and acting by steering, accelerating, or braking. Or a recommendation system perceiving your past purchases and acting by suggesting new products.

For an agent to be truly intelligent and autonomous, it needs to be able to figure out *what to do* to achieve its goals. This is where "Problem Solving for Agents" comes into play. It's a fundamental area of AI that equips agents with the ability to plan a sequence of actions to reach a desired state from an initial state. It's essentially about finding a path through a maze of possibilities, where each turn or step represents an action the agent can take. This field provides the algorithms and frameworks that allow agents to reason about their environment, anticipate outcomes, and make informed decisions to achieve their objectives efficiently and effectively.

## What Problem It Solves
Problem Solving for Agents addresses several core challenges that arise when designing intelligent systems:

1.  **Autonomy and Decision Making:** Agents need to operate independently without constant human intervention. Problem-solving techniques enable them to make their own decisions about which actions to take to achieve a goal, rather than following a predefined script for every possible situation.
2.  **Goal Achievement in Complex Environments:** Real-world environments are often dynamic, uncertain, and complex, with many possible states and actions. Agents need a systematic way to navigate this complexity to reach specific goals, such as a robot finding its way to a charging station, or a game character completing a quest.
3.  **Handling Uncertainty and Incomplete Information:** While basic problem-solving often assumes a known environment, advanced techniques extend to situations where the agent might not have complete information or where actions have uncertain outcomes. It provides frameworks to reason under these conditions.
4.  **Efficiency and Optimality:** There might be multiple ways to achieve a goal. Problem-solving aims not just to find *any* solution, but often the *best* solution – one that is optimal in terms of cost (e.g., shortest path, least energy consumption, fewest steps) or time.
5.  **Adaptability:** Environments can change. An agent equipped with problem-solving capabilities can adapt its plans if the environment changes or if its initial plan fails, by re-evaluating its situation and formulating a new plan.

In essence, it's needed in machine learning to move beyond simple pattern recognition and prediction towards intelligent behavior, where systems can actively strategize and plan their actions to achieve desired outcomes in a goal-directed manner.

## How It Works
The process of problem-solving for an agent typically involves several key steps:

1.  **Goal Formulation:**
    *   First, the agent needs to understand *what* it's trying to achieve. This involves defining a clear goal state. For example, if a robot is delivering a package, the goal state might be "package is at destination X."
    *   The goal must be precise enough for the agent to recognize when it has been achieved.

2.  **Problem Formulation:**
    *   Once the goal is set, the agent needs to define the "problem" in a structured way that it can understand and process. This involves:
        *   **Initial State:** Where the agent starts. (e.g., robot at warehouse, package at origin).
        *   **Actions (Operators):** A set of possible actions the agent can take. Each action has a precondition (what must be true to perform it) and an effect (how it changes the state). (e.g., `Move(location_A, location_B)`, `PickUp(package)`, `DropOff(package)`).
        *   **Transition Model:** A description of what state results from performing an action in a particular state. This defines the "rules" of the environment.
        *   **Goal Test:** A function that determines whether a given state is the goal state.
        *   **Path Cost Function:** A function that assigns a numerical cost to each path (sequence of actions). This allows the agent to compare different solutions and find the most efficient one. (e.g., distance traveled, time taken, energy consumed).

3.  **Search:**
    *   This is the core of problem-solving. The agent explores the "state space" – a graph where nodes are states and edges are actions – to find a sequence of actions (a path) from the initial state to a goal state.
    *   **Search Algorithms:** Various algorithms are used:
        *   **Uninformed Search (Blind Search):** These algorithms don't use any domain-specific knowledge about the problem beyond the structure of the state space. Examples include:
            *   **Breadth-First Search (BFS):** Explores all nodes at the current depth level before moving to the next level. Guarantees finding the shortest path in terms of number of actions if edge costs are uniform.
            *   **Depth-First Search (DFS):** Explores as far as possible along each branch before backtracking. Can find a solution quickly if one exists along a deep path, but not guaranteed to be optimal.
            *   **Uniform-Cost Search (UCS):** Similar to BFS but expands the node with the lowest path cost so far. Guarantees finding the cheapest path.
        *   **Informed Search (Heuristic Search):** These algorithms use "heuristic functions" – estimates of how close a state is to the goal – to guide the search and make it more efficient. Examples include:
            *   **Greedy Best-First Search:** Expands the node that appears closest to the goal based on a heuristic function. Fast, but not guaranteed to be optimal or complete.
            *   **A* Search:** Combines Uniform-Cost Search and Greedy Best-First Search. It expands the node with the lowest value of $f(n) = g(n) + h(n)$, where $g(n)$ is the cost from the start state to node $n$, and $h(n)$ is the estimated cost from node $n$ to the goal. A* is optimal and complete if the heuristic is admissible (never overestimates the cost to the goal) and consistent.

4.  **Execution:**
    *   Once a solution (a sequence of actions) is found by the search algorithm, the agent executes these actions in the environment.
    *   In dynamic or uncertain environments, the agent might need to monitor its progress and re-plan if its actions don't have the expected outcomes (e.g., a path is blocked, an object moves). This leads to interleaved planning and execution.

This structured approach allows agents to tackle complex tasks by breaking them down into manageable components and systematically exploring potential solutions.

## Mathematical Intuition
The mathematical intuition behind problem-solving for agents primarily revolves around graph theory and optimization.

Let's consider a problem as a **state space graph** $G = (V, E)$, where:
*   $V$ is the set of all possible states the agent can be in.
*   $E$ is the set of possible transitions (actions) between states. An edge $(u, v) \in E$ exists if there's an action that takes the agent from state $u$ to state $v$.

Each edge $(u, v)$ typically has an associated **cost** $c(u, v)$, representing the cost of performing the action that transitions from $u$ to $v$. This cost could be distance, time, energy, etc.

The goal is to find a path (a sequence of states and actions) from an **initial state** $S_0 \in V$ to a **goal state** $S_G \in V$ such that the total cost of the path is minimized.

For a path $P = (S_0, S_1, \dots, S_k)$, the **path cost** is given by:
$$g(P) = \sum_{i=0}^{k-1} c(S_i, S_{i+1})$$

In **Uniform-Cost Search (UCS)**, the algorithm explores nodes by always expanding the node $n$ with the lowest $g(n)$ value, where $g(n)$ is the cost of the path found so far from $S_0$ to $n$. This guarantees finding the path with the minimum total cost.

For **Informed Search algorithms** like A*, we introduce a **heuristic function**, denoted as $h(n)$.
*   $h(n)$ is an estimated cost from state $n$ to the goal state $S_G$. It's a "guess" or an "informed estimate" of how far $n$ is from the goal.
*   The quality of $h(n)$ is crucial. An **admissible heuristic** is one that never overestimates the true cost to reach the goal. That is, for any state $n$:
    $$h(n) \le h^*(n)$$
    where $h^*(n)$ is the true cost from $n$ to $S_G$.

**A* Search** combines the actual cost from the start state $g(n)$ with the estimated cost to the goal $h(n)$ to evaluate each node $n$. It uses an evaluation function $f(n)$:
$$f(n) = g(n) + h(n)$$
A* expands the node $n$ that has the lowest $f(n)$ value.
*   $g(n)$: The cost of the path from the initial state to $n$. This is the "backward cost."
*   $h(n)$: The estimated cost of the cheapest path from $n$ to the goal. This is the "forward cost."

By minimizing $f(n)$, A* aims to find a path that is both cheap to reach from the start and appears cheap to reach the goal from its current position. If $h(n)$ is admissible, A* is guaranteed to find an optimal (cheapest) path. If $h(n)$ is also **consistent** (or monotonic), meaning that for every node $n$ and every successor $n'$ of $n$ generated by action $a$:
$$h(n) \le c(n, n') + h(n')$$
then A* is even more efficient and can avoid re-expanding nodes.

The mathematical foundation ensures that these algorithms can systematically explore the vast possibilities of a state space, guided by cost functions and heuristics, to arrive at optimal or near-optimal solutions for complex problems.

## Advantages
*   **Goal-Directed Behavior:** Enables agents to pursue specific objectives, making them purposeful and intelligent.
*   **Autonomy:** Allows agents to make independent decisions and plan actions without constant human intervention.
*   **Optimality (with certain algorithms):** Algorithms like A* search can guarantee finding the shortest or cheapest path to a goal if an admissible heuristic is used.
*   **Completeness (with certain algorithms):** Algorithms like BFS and A* are guaranteed to find a solution if one exists.
*   **Flexibility and Adaptability:** Agents can adapt to changing environments by re-planning when initial plans fail or conditions change.
*   **Systematic Exploration:** Provides a structured way to explore the vast possibilities of a state space, ensuring that solutions are not missed.
*   **Foundation for Advanced AI:** Forms the basis for more complex AI tasks like planning, scheduling, and reinforcement learning.

## Disadvantages
*   **State Space Explosion:** The number of possible states can grow exponentially with the complexity of the environment, making search computationally intractable for large problems. This is a major challenge.
*   **Computational Complexity:** Even with heuristics, searching large state spaces can require significant memory and processing power.
*   **Perfect Information Assumption:** Many classical search algorithms assume a fully observable, deterministic environment, which is often not true in the real world.
*   **Heuristic Design:** Designing effective and admissible heuristic functions can be challenging and domain-specific. A poor heuristic can lead to inefficient search or non-optimal solutions.
*   **Local Optima:** Some search strategies (e.g., greedy approaches) can get stuck in local optima, failing to find the globally best solution.
*   **Dynamic Environments:** Re-planning in highly dynamic environments can be computationally expensive and time-consuming, potentially making the agent slow to react.
*   **Action Uncertainty:** Dealing with actions that have uncertain outcomes (stochastic environments) requires more complex probabilistic planning methods, moving beyond basic search.

## Real World Applications
1.  **Robotics and Autonomous Vehicles:**
    *   **Pathfinding and Navigation:** Robots (e.g., factory robots, Mars rovers) and self-driving cars use problem-solving to find optimal paths from their current location to a destination while avoiding obstacles. Algorithms like A* are crucial for real-time navigation in complex, dynamic environments.
    *   **Task Planning:** Robots need to plan sequences of actions to complete tasks, such as assembling products, picking up objects, or performing surgery.

2.  **Game AI:**
    *   **Non-Player Character (NPC) Movement:** NPCs in video games use pathfinding algorithms to navigate game worlds, find targets, or patrol areas. For example, an enemy character might use A* to find the shortest path to the player.
    *   **Strategic Planning:** AI opponents in strategy games (e.g., chess, Go, real-time strategy games) use search algorithms (like Minimax with Alpha-Beta Pruning) to explore possible moves and counter-moves to achieve victory.

3.  **Logistics and Supply Chain Management:**
    *   **Route Optimization:** Companies like FedEx or Amazon use problem-solving techniques to optimize delivery routes for their fleets, minimizing fuel consumption, travel time, and operational costs. This often involves solving variants of the Traveling Salesperson Problem.
    *   **Scheduling:** Scheduling tasks in factories, flights for airlines, or appointments for services can be formulated as search problems to find optimal arrangements that meet constraints and minimize costs.

4.  **Web Crawling and Information Retrieval:**
    *   **Web Crawlers:** Search engines use agents (crawlers) that "solve the problem" of finding new web pages and updating their index. They navigate the web graph, deciding which links to follow to efficiently discover content.
    *   **Recommendation Systems:** While often using machine learning, the underlying goal of finding "best" items for a user can be seen as a search problem in a vast item space, optimizing for user satisfaction.

5.  **Drug Discovery and Chemical Synthesis:**
    *   **Molecular Design:** AI agents can search through vast chemical spaces to identify molecules with desired properties for drug discovery. This involves planning synthesis pathways or exploring molecular structures.
    *   **Retrosynthesis:** Planning the steps to synthesize a complex chemical compound from simpler precursors is a classic problem-solving task, often tackled with graph search techniques.

## Python Example
Let's implement a simple Breadth-First Search (BFS) algorithm to find the shortest path in a grid (maze). BFS is a good choice for a beginner-friendly example as it's conceptually straightforward and guarantees the shortest path in terms of steps.

```python
import collections

def solve_maze_bfs(maze, start, end):
    """
    Solves a maze using Breadth-First Search (BFS).

    Args:
        maze (list of list of int): A 2D grid representing the maze.
                                    0 = path, 1 = wall.
        start (tuple): (row, col) coordinates of the starting point.
        end (tuple): (row, col) coordinates of the ending point.

    Returns:
        list of tuple: The shortest path from start to end as a list of (row, col)
                       coordinates, or None if no path exists.
    """
    rows, cols = len(maze), len(maze[0])
    
    # Queue for BFS: stores (row, col, path_so_far)
    # path_so_far is a list of coordinates from start to current
    queue = collections.deque([(start[0], start[1], [start])])
    
    # Set to keep track of visited cells to avoid cycles and redundant processing
    visited = set([(start[0], start[1])])
    
    # Define possible movements (up, down, left, right)
    # dr = delta row, dc = delta column
    dr = [-1, 1, 0, 0] # Up, Down
    dc = [0, 0, -1, 1] # Left, Right

    while queue:
        r, c, path = queue.popleft()

        # If we reached the end, return the path
        if (r, c) == end:
            return path

        # Explore neighbors
        for i in range(4):
            nr, nc = r + dr[i], c + dc[i] # New row, new column

            # Check if the new position is valid:
            # 1. Within grid boundaries
            # 2. Not a wall (maze[nr][nc] == 0)
            # 3. Not already visited
            if (0 <= nr < rows and 0 <= nc < cols and
                maze[nr][nc] == 0 and (nr, nc) not in visited):
                
                visited.add((nr, nc))
                # Add the new position and updated path to the queue
                queue.append((nr, nc, path + [(nr, nc)]))
                
    # If the queue becomes empty and the end was not reached, no path exists
    return None

def print_maze_with_path(maze, path):
    """
    Prints the maze with the found path marked.
    """
    if path is None:
        print("No path found.")
        return

    display_maze = [row[:] for row in maze] # Create a copy to modify
    for r, c in path:
        if (r, c) == path[0]:
            display_maze[r][c] = 'S' # Start
        elif (r, c) == path[-1]:
            display_maze[r][c] = 'E' # End
        else:
            display_maze[r][c] = '*' # Path

    for row in display_maze:
        print(" ".join(map(str, row)))

# --- Example Usage ---
if __name__ == "__main__":
    # Define a sample maze (0 = path, 1 = wall)
    # S = Start, E = End
    # 0 0 0 1 0
    # 1 1 0 1 0
    # 0 0 0 0 0
    # 0 1 1 1 0
    # 0 0 0 0 0
    maze = [
        [0, 0, 0, 1, 0],
        [1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0]
    ]

    start_point = (0, 0)
    end_point = (4, 4)

    print("Original Maze:")
    for row in maze:
        print(" ".join(map(str, row)))
    print(f"\nSearching path from {start_point} to {end_point}...\n")

    shortest_path = solve_maze_bfs(maze, start_point, end_point)

    print("Maze with Shortest Path:")
    print_maze_with_path(maze, shortest_path)

    if shortest_path:
        print(f"\nPath found with {len(shortest_path) - 1} steps:")
        print(shortest_path)
    else:
        print("\nNo path could be found.")

    # Example with no path
    print("\n--- Example with No Path ---")
    maze_no_path = [
        [0, 0, 0, 1, 0],
        [1, 1, 1, 1, 0], # Wall blocking path
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0]
    ]
    start_point_no_path = (0, 0)
    end_point_no_path = (4, 4)

    print("Original Maze (No Path):")
    for row in maze_no_path:
        print(" ".join(map(str, row)))
    print(f"\nSearching path from {start_point_no_path} to {end_point_no_path}...\n")

    shortest_path_no_path = solve_maze_bfs(maze_no_path, start_point_no_path, end_point_no_path)
    print_maze_with_path(maze_no_path, shortest_path_no_path)
```

**Explanation:**

1.  **`solve_maze_bfs(maze, start, end)` function:**
    *   Takes the `maze` (a 2D list), `start` coordinates, and `end` coordinates as input.
    *   `collections.deque` is used as a queue, which is efficient for `popleft()` operations. Each item in the queue is a tuple `(row, col, path_so_far)`. `path_so_far` stores the sequence of coordinates taken to reach the current `(row, col)`.
    *   `visited` is a `set` to keep track of cells that have already been added to the queue or processed. This prevents infinite loops in mazes with cycles and ensures we find the shortest path by not re-exploring longer paths to the same cell.
    *   `dr` and `dc` arrays define the relative movements for up, down, left, and right.
    *   The `while queue` loop continues as long as there are cells to explore.
    *   In each iteration, it `popleft()`s a cell `(r, c)` and its `path`.
    *   If `(r, c)` is the `end` point, the `path` is returned.
    *   Otherwise, it iterates through the four possible neighbors. For each neighbor `(nr, nc)`:
        *   It checks if `(nr, nc)` is within the maze boundaries, is not a wall (`maze[nr][nc] == 0`), and has not been `visited` yet.
        *   If all conditions are met, the neighbor is marked as `visited`, and `(nr, nc)` along with the `path` extended by `(nr, nc)` is added to the `queue`.
    *   If the queue becomes empty and the `end` was never reached, it means no path exists, and `None` is returned.

2.  **`print_maze_with_path(maze, path)` function:**
    *   This helper function visualizes the maze and the found path.
    *   'S' marks the start, 'E' marks the end, and '*' marks intermediate path steps.

3.  **Example Usage (`if __name__ == "__main__":`)**
    *   A sample `maze` is defined.
    *   `start_point` and `end_point` are set.
    *   The `solve_maze_bfs` function is called.
    *   The original maze and the maze with the path are printed, along with the path coordinates and number of steps.
    *   A second example demonstrates a maze where no path exists.

This example clearly demonstrates how an agent (represented by the search algorithm) can "solve a problem" (find a path) by systematically exploring its environment (the maze) to achieve a goal (reach the end point).

## Interview Questions

1.  **What is an "agent" in the context of AI, and how does problem-solving relate to it?**
    *   **Answer:** An agent is anything that can perceive its environment through sensors and act upon that environment through effectors. Problem-solving is a core capability for intelligent agents, enabling them to determine a sequence of actions to take from an initial state to reach a desired goal state. It provides the intelligence for autonomous decision-making and goal achievement.

2.  **Describe the key components of problem formulation for an agent.**
    *   **Answer:** Problem formulation involves defining:
        *   **Initial State:** The starting point of the agent.
        *   **Actions (Operators):** A set of possible actions the agent can perform, each with preconditions and effects.
        *   **Transition Model:** Describes the resulting state after an action is performed in a given state.
        *   **Goal Test:** A function to determine if a given state is the desired goal state.
        *   **Path Cost Function:** A function that assigns a numerical cost to a sequence of actions (a path).

3.  **Differentiate between uninformed and informed search algorithms. Give an example of each.**
    *   **Answer:**
        *   **Uninformed Search (Blind Search):** These algorithms do not use any domain-specific knowledge or heuristics to guide the search. They explore the state space systematically without knowing how "close" a state is to the goal. Examples include Breadth-First Search (BFS), Depth-First Search (DFS), and Uniform-Cost Search (UCS).
        *   **Informed Search (Heuristic Search):** These algorithms use a heuristic function, which is an estimate of the cost from the current state to the goal, to guide the search towards promising paths. Examples include Greedy Best-First Search and A* Search.

4.  **Explain the A* search algorithm. What are its key components, and when is it optimal?**
    *   **Answer:** A* search is an informed search algorithm that finds the shortest path between a start and a goal node in a graph. It evaluates each node $n$ using an evaluation function $f(n) = g(n) + h(n)$.
        *   $g(n)$: The actual cost from the start node to node $n$.
        *   $h(n)$: The estimated cost (heuristic) from node $n$ to the goal node.
    *   A* is optimal (guaranteed to find the shortest path) and complete (guaranteed to find a path if one exists) if the heuristic function $h(n)$ is **admissible** (i.e., it never overestimates the true cost to reach the goal). It is also more efficient if the heuristic is **consistent** (monotonic).

5.  **What is a heuristic function, and what makes a good one?**
    *   **Answer:** A heuristic function $h(n)$ is an estimate of the cost from a given state $n$ to the goal state. It provides domain-specific knowledge to guide informed search algorithms. A good heuristic is:
        *   **Admissible:** It never overestimates the true cost to the goal ($h(n) \le h^*(n)$). This is crucial for A* optimality.
        *   **Consistent (Monotonic):** For every node $n$ and every successor $n'$ of $n$, $h(n) \le c(n, n') + h(n')$. This is a stronger condition than admissibility and helps A* avoid re-expanding nodes.
        *   **Informative:** It should be as close as possible to the true cost without overestimating, as a more informative heuristic leads to a more efficient search (fewer nodes expanded).
        *   **Easy to compute:** The computational cost of calculating $h(n)$ should not outweigh the benefits of guiding the search.

6.  **What is the "state space explosion" problem, and how does it impact problem-solving for agents?**
    *   **Answer:** State space explosion refers to the phenomenon where the number of possible states in a problem grows exponentially with the number of variables or components in the system. For example, if each of $N$ binary variables can be 0 or 1, there are $2^N$ states. This makes it computationally intractable to explore the entire state space, even for moderately complex problems, leading to excessive memory and time requirements for search algorithms.

7.  **Compare Breadth-First Search (BFS) and Depth-First Search (DFS) in terms of completeness, optimality, and space/time complexity.**
    *   **Answer:**
        *   **BFS:**
            *   **Completeness:** Yes, if a solution exists.
            *   **Optimality:** Yes, for unweighted graphs (shortest path in terms of number of edges). For weighted graphs, Uniform-Cost Search is needed for optimality.
            *   **Time Complexity:** $O(b^d)$, where $b$ is branching factor, $d$ is depth of shallowest solution.
            *   **Space Complexity:** $O(b^d)$, as it stores all nodes at the current depth level. Can be very high.
        *   **DFS:**
            *   **Completeness:** No, can get stuck in infinite loops or deep paths without a solution if not modified (e.g., Iterative Deepening DFS).
            *   **Optimality:** No, it finds the first solution it encounters, which may not be the shortest or cheapest.
            *   **Time Complexity:** $O(b^m)$, where $m$ is the maximum depth of the search space.
            *   **Space Complexity:** $O(bm)$, much less than BFS, as it only stores the current path.

8.  **In what real-world scenarios would you prefer an uninformed search over an informed search, and vice-versa?**
    *   **Answer:**
        *   **Uninformed Search (e.g., BFS, UCS) preferred when:**
            *   No reliable heuristic is available or can be easily computed.
            *   The state space is relatively small.
            *   Optimality (shortest path in terms of steps or cost) is strictly required, and the graph is unweighted (BFS) or edge costs are known (UCS).
        *   **Informed Search (e.g., A*) preferred when:**
            *   The state space is large, and a good heuristic can significantly prune the search space.
            *   Efficiency is critical, and a good heuristic can drastically speed up finding a solution.
            *   Near-optimal solutions are acceptable if an admissible heuristic is hard to find, or if a non-admissible heuristic is used for speed.

9.  **How do agents handle uncertainty in problem-solving?**
    *   **Answer:** Basic search assumes a deterministic environment. To handle uncertainty (e.g., actions have probabilistic outcomes, partial observability), agents move to more advanced planning techniques:
        *   **Stochastic Planning:** Uses Markov Decision Processes (MDPs) or Partially Observable MDPs (POMDPs) where actions lead to a probability distribution over next states. The agent aims to find a policy (a mapping from states to actions) that maximizes expected utility.
        *   **Contingency Planning:** Generates a plan that includes branches for different possible outcomes of uncertain actions.
        *   **Sensor Models:** For partial observability, agents use sensor models to update their belief state (a probability distribution over possible actual states) based on observations.
        *   **Interleaved Planning and Execution:** The agent plans a few steps, executes them, observes the environment, and then re-plans based on the new observations, adapting to unexpected changes.

10. **What is the difference between a "plan" and a "policy" in the context of agent problem-solving?**
    *   **Answer:**
        *   A **plan** is a sequence of actions designed to achieve a specific goal from a specific initial state in a *deterministic* environment. It's a fixed path. For example, "Go to X, then pick up Y, then go to Z."
        *   A **policy** is a mapping from *every possible state* to an action. It tells the agent what to do in *any* state it might find itself in. Policies are used in *stochastic* or *partially observable* environments where the exact sequence of states cannot be guaranteed. A policy allows the agent to react appropriately to unexpected outcomes or changes in the environment.

## Quiz

1.  Which of the following is NOT a core component of problem formulation for an agent?
    A) Initial State
    B) Action Set
    C) Sensor Model
    D) Goal Test

2.  An admissible heuristic function $h(n)$ for A* search must satisfy which condition?
    A) $h(n) = 0$ for all states $n$.
    B) $h(n) \ge h^*(n)$, where $h^*(n)$ is the true cost to the goal.
    C) $h(n) \le h^*(n)$, where $h^*(n)$ is the true cost to the goal.
    D) $h(n)$ must always be greater than $g(n)$.

3.  Which search algorithm guarantees finding the shortest path in terms of the number of steps in an unweighted graph?
    A) Depth-First Search (DFS)
    B) Greedy Best-First Search
    C) Breadth-First Search (BFS)
    D) Hill Climbing

4.  The "state space explosion" problem primarily refers to:
    A) An agent's memory running out due to too many actions.
    B) The exponential growth in the number of possible states in a problem.
    C) The agent getting stuck in a local optimum.
    D) The environment changing too rapidly for the agent to plan.

5.  What is the primary advantage of using an informed search algorithm like A* over an uninformed search algorithm like BFS for large state spaces?
    A) A* is always faster regardless of the heuristic.
    B) A* guarantees optimality even with a non-admissible heuristic.
    C) A* uses a heuristic function to guide the search, making it more efficient.
    D) A* requires less memory than BFS.

---

### Answer Key

1.  **C) Sensor Model**
    *   **Explanation:** While a sensor model is crucial for an agent's perception in real-world environments, it's typically part of the agent's architecture or environment model, not a direct component of the *problem formulation* itself, which focuses on defining the search space (states, actions, goal, costs).

2.  **C) $h(n) \le h^*(n)$, where $h^*(n)$ is the true cost to the goal.**
    *   **Explanation:** An admissible heuristic never overestimates the true cost to the goal. This property is essential for A* search to guarantee finding an optimal path.

3.  **C) Breadth-First Search (BFS)**
    *   **Explanation:** BFS explores the state space level by level, ensuring that it finds all nodes at a given depth before moving to the next. Therefore, the first path it finds to the goal will always be the one with the fewest steps.

4.  **B) The exponential growth in the number of possible states in a problem.**
    *   **Explanation:** State space explosion is the challenge where the number of possible configurations or states of a system becomes astronomically large, making exhaustive search impractical or impossible.

5.  **C) A* uses a heuristic function to guide the search, making it more efficient.**
    *   **Explanation:** The main power of informed search algorithms like A* comes from their ability to use domain-specific knowledge (heuristics) to intelligently prune the search space and focus on promising paths, leading to significantly faster solutions for large problems compared to blind search.

## Further Reading

1.  **"Artificial Intelligence: A Modern Approach" by Stuart Russell and Peter Norvig:**
    *   This is the definitive textbook in AI. Chapters 3 and 4 specifically cover "Solving Problems by Searching" and "Beyond Classical Search," providing comprehensive details on agents, problem formulation, and various search algorithms.
    *   [Official Website (often has resources/errata)](http://aima.cs.berkeley.edu/) - Look for chapters on "Problem-solving agents" and "Search algorithms."

2.  **MIT OpenCourseware - Introduction to Artificial Intelligence:**
    *   MIT offers free course materials, including lectures and notes, on AI topics. Their sections on search algorithms are excellent for beginners.
    *   [MIT OpenCourseware - 6.034 Artificial Intelligence](https://ocw.mit.edu/courses/6-034-artificial-intelligence-fall-2010/resources/) - Look for lecture notes and assignments related to "Search" or "Problem Solving."

3.  **Stanford CS221 - Artificial Intelligence: Principles and Techniques:**
    *   Similar to MIT, Stanford provides excellent course materials. Their lectures and notes on state-space search and heuristic search are highly recommended.
    *   [Stanford CS221 Course Website](http://cs221.stanford.edu/) - Navigate to the "Lectures" or "Notes" section and find topics like "State-Space Search," "Heuristic Search," and "A* Search."