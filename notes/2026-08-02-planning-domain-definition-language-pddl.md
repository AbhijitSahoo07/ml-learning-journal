# Planning Domain Definition Language (PDDL)

## Overview
The Planning Domain Definition Language (PDDL) is a standardized language used in Artificial Intelligence (AI) for describing planning problems. Think of it as a blueprint for an AI agent to understand "what needs to be done" and "how things can change" in a specific environment. It doesn't tell the AI *how* to find a solution, but rather provides a clear, formal description of the problem itself, allowing various AI planning algorithms (called "planners") to then search for a sequence of actions to achieve a desired goal.

PDDL separates the description of the world into two main parts:
1.  **Domain File**: Defines the general rules, actions, and properties of an environment that apply to any problem within that domain. For example, in a "robot delivery" domain, it would define actions like `move`, `pickup`, `dropoff`, and properties like `at_location`, `has_package`.
2.  **Problem File**: Describes a specific instance of a planning problem within that domain. It specifies the initial state of the world (e.g., "robot is at warehouse A, package is at warehouse B"), the objects involved (e.g., "robot1", "package1", "warehouseA", "warehouseB"), and the desired goal state (e.g., "package1 is at warehouseA").

By providing this structured description, PDDL enables AI systems to reason about complex tasks, find optimal or near-optimal plans, and adapt to different scenarios without needing to be reprogrammed for each new problem instance.

## What Problem It Solves
PDDL addresses the fundamental challenge of **automated planning** in AI. In many real-world scenarios, an intelligent agent (like a robot, a software agent, or a game character) needs to achieve a specific goal in an environment where its actions have consequences. Manually programming every possible sequence of actions for every possible initial state and goal is practically impossible due to the sheer complexity and combinatorial explosion of possibilities.

PDDL solves this by:

1.  **Bridging the Gap between High-Level Goals and Low-Level Actions**: Instead of telling a robot "move 5 meters forward, then turn left," PDDL allows us to specify a goal like "deliver package to customer." The planning system, using the PDDL domain and problem descriptions, figures out the sequence of `move`, `pickup`, `dropoff` actions required.
2.  **Handling Dynamic and Complex Environments**: Environments are rarely static. Objects move, states change. PDDL provides a formal way to describe these changes through action effects, allowing planners to explore different paths and adapt.
3.  **Enabling General-Purpose Planners**: By standardizing the problem description, PDDL allows researchers and developers to create general-purpose planning algorithms that can solve a wide variety of problems across different domains, as long as they are described in PDDL. This promotes reusability and comparison of planning techniques.
4.  **Managing State Space Complexity**: PDDL helps define the "rules of the game" clearly. A planner uses these rules to explore the vast "state space" (all possible configurations of the world) efficiently, searching for a path from the initial state to the goal state. Without a formal language like PDDL, defining and navigating this space would be incredibly difficult.
5.  **Facilitating Collaboration and Benchmarking**: PDDL serves as a common language for the AI planning community, allowing different research groups to share problems, compare the performance of their planning systems, and build upon each other's work.

In essence, PDDL is needed in machine learning and AI because it provides a powerful, declarative framework for defining complex decision-making problems, allowing AI systems to autonomously generate plans to achieve goals in dynamic environments.

## How It Works
PDDL doesn't "work" in the sense of being an algorithm itself; rather, it's a *description language* that provides the input for a separate AI planning algorithm (a "planner"). Here's how the overall process works:

1.  **Define the Domain (PDDL Domain File)**:
    *   **Types**: You start by defining categories of objects in your world (e.g., `robot`, `package`, `location`). This helps organize your problem.
    *   **Predicates**: These are propositions that describe the state of the world. They are like true/false statements about objects. For example, `(at ?obj ?loc)` could mean that `?obj` is at `?loc`. `?obj` and `?loc` are parameters that will be filled by specific objects.
    *   **Actions (Operators)**: These define what an agent can *do*. Each action has:
        *   **Parameters**: The objects involved in the action (e.g., `(move ?robot ?from ?to)`).
        *   **Preconditions**: A list of predicates that *must be true* for the action to be executed. If any precondition is false, the action cannot happen. For example, for `(move ?robot ?from ?to)`, a precondition might be `(at ?robot ?from)`.
        *   **Effects**: A list of predicates that become true or false *after* the action is executed. These describe how the world changes. Effects are typically represented as `(add ...)` for predicates that become true and `(del ...)` for predicates that become false. For `(move ?robot ?from ?to)`, effects might be `(add (at ?robot ?to))` and `(del (at ?robot ?from))`.

2.  **Define the Problem (PDDL Problem File)**:
    *   **Objects**: You list all the specific instances of the types defined in the domain. For example, `robot1`, `packageA`, `warehouse`, `customer_door`.
    *   **Initial State**: This is a list of all predicates that are true at the very beginning of the problem. For example, `(at robot1 warehouse)`, `(at packageA warehouse)`.
    *   **Goal State**: This is a list of predicates that must be true for the problem to be considered solved. For example, `(at packageA customer_door)`.

3.  **Input to a PDDL Planner**:
    *   Both the PDDL domain file and the PDDL problem file are fed into a specialized AI planning algorithm (a "planner"). Examples of planners include FF (FastForward), LPG, Metric-FF, etc.

4.  **Planner's Internal Mechanism (State Space Search)**:
    *   The planner starts with the `initial state`.
    *   It then looks at all possible `actions` defined in the domain.
    *   For each action, it checks if its `preconditions` are met in the current state.
    *   If an action's preconditions are met, the planner considers executing it. Executing an action means applying its `effects` to the current state, generating a *new state*.
    *   The planner explores this "state space" (the graph of all possible states and transitions between them) using various search algorithms (e.g., A*, Breadth-First Search, Depth-First Search, heuristic search).
    *   The goal of the search is to find a sequence of actions that transforms the `initial state` into a state where all `goal state` predicates are true.

5.  **Output: The Plan**:
    *   If a sequence of actions is found, the planner outputs this sequence as a "plan." The plan is typically a step-by-step list of actions to be executed by the agent.
    *   If no plan can be found (e.g., the goal is unreachable given the available actions and initial state), the planner reports failure.

This modular approach allows the same domain definition to be used with different problem instances, and the same planner to be used across different domains, making AI planning highly flexible and scalable.

## Mathematical Intuition
At its core, PDDL formalizes a planning problem as a **state-transition system**. Let's break down the mathematical intuition:

A planning problem can be formally defined as a tuple $P = (S, A, T, s_0, G)$, where:

*   $S$ is the set of all possible **states**.
*   $A$ is the set of all possible **actions**.
*   $T$ is the **transition function**, which describes how actions change states.
*   $s_0 \in S$ is the **initial state**.
*   $G \subseteq S$ is the set of **goal states**.

Let's elaborate on these components in the context of PDDL:

### 1. States ($S$)
In PDDL, a state is represented by a set of **grounded propositions (or literals)**. A proposition is a predicate with all its parameters replaced by specific objects.
For example, if we have a predicate `(at ?obj ?loc)`, and objects `robot1`, `warehouseA`, then `(at robot1 warehouseA)` is a grounded proposition.

A state $s \in S$ is a finite set of such grounded propositions that are true in that state.
$$s = \{p_1, p_2, \dots, p_k\}$$
where each $p_i$ is a true grounded proposition.
For instance, an initial state might be $s_0 = \{(\text{at robot1 warehouseA}), (\text{has package1 robot1})\}$.

### 2. Actions ($A$)
Each action in PDDL is an **operator** that transforms one state into another. An action $a \in A$ is defined by:
*   **Parameters**: A list of typed variables.
*   **Preconditions**: A logical formula (typically a conjunction of positive literals) that must be true in the current state for the action to be applicable.
*   **Effects**: A set of changes to the state, specified as additions (literals that become true) and deletions (literals that become false).

Let's denote an action $a$ with parameters $\vec{x}$ (e.g., `(move ?robot ?from ?to)`).
The **precondition function** for an action $a$ applied with specific objects $\vec{o}$ (a grounding of $\vec{x}$) is $Pre(a, \vec{o})$. This is a set of grounded propositions that must be true.
The **effect function** for an action $a$ applied with specific objects $\vec{o}$ is $Eff(a, \vec{o})$. This is typically split into:
*   $Eff^+(a, \vec{o})$: Set of grounded propositions to add.
*   $Eff^-(a, \vec{o})$: Set of grounded propositions to delete.

### 3. Transition Function ($T$)
The transition function $T: S \times A \rightarrow S$ describes how an action changes a state.
If an action $a$ with specific objects $\vec{o}$ is applicable in state $s$ (i.e., $Pre(a, \vec{o}) \subseteq s$), then applying $a$ to $s$ results in a new state $s'$:
$$s' = (s \setminus Eff^-(a, \vec{o})) \cup Eff^+(a, \vec{o})$$
This means we remove all propositions specified in $Eff^-(a, \vec{o})$ from $s$ and then add all propositions specified in $Eff^+(a, \vec{o})$. If $Pre(a, \vec{o}) \not\subseteq s$, the action is not applicable, and the state does not change (or is undefined).

### 4. Initial State ($s_0$)
This is the starting point of the planning problem, defined as a set of true grounded propositions.

### 5. Goal States ($G$)
The goal is typically defined as a logical formula (often a conjunction of positive literals) that must be true in the final state. A state $s$ is a goal state if it satisfies the goal formula.
Let $Goal$ be the set of grounded propositions that must be true for the goal to be satisfied. A state $s$ is a goal state if $Goal \subseteq s$.

### The Planning Problem
The planning problem is to find a sequence of applicable actions $\pi = (a_1, a_2, \dots, a_k)$ such that if we start from $s_0$ and apply each action sequentially, the resulting state $s_k$ satisfies the goal.
$$s_0 \xrightarrow{a_1} s_1 \xrightarrow{a_2} \dots \xrightarrow{a_k} s_k$$
where $s_i = (s_{i-1} \setminus Eff^-(a_i, \vec{o}_i)) \cup Eff^+(a_i, \vec{o}_i)$ for $i=1, \dots, k$, and $Goal \subseteq s_k$.

Planners use various search algorithms (like A*, heuristic search, graph search) to explore this state space graph, where nodes are states and edges are actions, to find such a path. The "cost" of a path can be defined by the number of actions, or by numerical costs associated with actions (which PDDL also supports).

## Advantages
*   **Standardization**: PDDL is the de facto standard language for AI planning, promoting interoperability and allowing different planners to be tested on the same problems.
*   **Declarative Nature**: It describes *what* needs to be achieved and *what* actions are possible, rather than *how* to achieve it. This separates problem description from solution strategy.
*   **Modularity**: The separation of domain and problem files allows for high reusability. A single domain definition can be used with many different problem instances.
*   **Expressiveness**: PDDL has evolved over time to include various features like types, negative preconditions, conditional effects, numeric fluents, time, and uncertainty, making it capable of modeling complex real-world scenarios.
*   **Facilitates Research**: Provides a common ground for researchers to compare planning algorithms and advance the field of automated planning.
*   **Human-Readable (to an extent)**: While formal, PDDL syntax is designed to be relatively readable for humans familiar with the structure, aiding in problem definition and debugging.
*   **Abstraction**: Allows modeling problems at a high level of abstraction, focusing on logical relationships and state changes rather than low-level implementation details.

## Disadvantages
*   **Complexity for Large Domains**: As the number of objects, predicates, and actions grows, defining and debugging PDDL domains can become very complex and error-prone.
*   **Requires Expert Knowledge**: Creating effective PDDL models often requires a deep understanding of the problem domain and the nuances of PDDL syntax and semantics. It's not always intuitive for beginners.
*   **Limited Expressiveness for Certain Problems**:
    *   **Continuous Time/States**: While PDDL has extensions for time (PDDL2.1), modeling truly continuous processes or states (e.g., fluid dynamics) is challenging or impossible.
    *   **Uncertainty/Probabilistic Outcomes**: PDDL has extensions for uncertainty (e.g., PPDDL), but the core language is deterministic. Modeling highly stochastic environments can be cumbersome.
    *   **Complex Numerical Reasoning**: PDDL's support for numerical fluents is basic (addition, subtraction, multiplication, division). Complex mathematical optimization or calculus is beyond its scope.
*   **Computational Cost**: Finding plans, especially optimal ones, can be computationally very expensive (NP-hard or even PSPACE-complete in general), leading to long planning times for complex problems.
*   **Lack of Learning**: PDDL itself is a description language; it doesn't inherently learn from experience. The domain and problem must be explicitly defined. While planning can be integrated with learning, PDDL itself doesn't provide this.
*   **Debugging Plans**: When a planner fails to find a plan or finds an unexpected one, debugging the PDDL domain or problem definition to understand why can be difficult.

## Real World Applications
PDDL and automated planning are used in various industries and applications where autonomous decision-making and task sequencing are critical.

1.  **Robotics and Autonomous Systems**:
    *   **Task Planning**: Robots in manufacturing, logistics, or exploration (e.g., Mars rovers) use PDDL to plan sequences of actions to achieve high-level goals like "assemble product X," "navigate to location Y," or "collect rock samples."
    *   **Navigation**: Planning optimal paths and maneuvers for autonomous vehicles or drones, considering obstacles, fuel, and time constraints.
    *   **Human-Robot Collaboration**: Robots planning their actions to assist humans in shared workspaces.

2.  **Logistics and Supply Chain Management**:
    *   **Scheduling and Resource Allocation**: Planning the movement of goods, vehicles, and personnel in complex supply chains to optimize delivery times, minimize costs, or maximize throughput. This includes airline scheduling, freight delivery, and warehouse management.
    *   **Inventory Management**: Planning when and where to move inventory to meet demand while minimizing storage costs.

3.  **Space Exploration and Satellite Operations**:
    *   **Mission Planning**: NASA and other space agencies use planning systems to generate command sequences for spacecraft and rovers (like Curiosity or Perseverance) to perform scientific experiments, navigate terrains, and manage power resources.
    *   **Satellite Constellation Management**: Planning communication schedules, orbital maneuvers, and data collection for large groups of satellites.

4.  **Game AI**:
    *   **Non-Player Character (NPC) Behavior**: Generating intelligent and believable behaviors for NPCs in video games. Instead of scripting every action, PDDL can define an NPC's goals (e.g., "find treasure," "defeat enemy") and available actions, allowing the AI to plan its own sequence of moves.
    *   **Quest Generation**: Dynamically creating quest lines or mission structures based on player actions and game state.

5.  **Manufacturing and Process Control**:
    *   **Assembly Line Planning**: Optimizing the sequence of operations on an assembly line to produce products efficiently, considering machine availability, tool changes, and material flow.
    *   **Chemical Process Control**: Planning sequences of operations in chemical plants to achieve desired product compositions while adhering to safety and efficiency constraints.

## Python Example
PDDL is a language, not a Python library in itself. However, Python can be used to *generate* PDDL files, *call* external PDDL planners, and *parse* their output. For a beginner-friendly example that doesn't require setting up external planners, we can use a Python library like `pddlpy` which allows defining and solving simple PDDL-like problems directly within Python.

Let's create a simple "Blocksworld" problem, a classic AI planning domain, where we want to stack blocks in a specific order.

First, you'd need to install `pddlpy`:
`pip install pddlpy`

```python
import pddlpy

# --- 1. Define the PDDL Domain (using pddlpy's internal representation) ---
# In a real PDDL file, this would be structured with (:domain ...)
# and define types, predicates, and actions.
# pddlpy allows us to define these programmatically.

# Predicates:
# (on ?x ?y) - block ?x is on block ?y
# (ontable ?x) - block ?x is on the table
# (clear ?x) - nothing is on block ?x
# (handempty) - the robot's hand is empty
# (holding ?x) - the robot is holding block ?x

domain_pddl = """
(define (domain blocksworld)
    (:requirements :strips :typing)
    (:types block)
    (:predicates
        (on ?x - block ?y - block)
        (ontable ?x - block)
        (clear ?x - block)
        (handempty)
        (holding ?x - block)
    )

    (:action pick-up
        :parameters (?x - block)
        :precondition (and (clear ?x) (ontable ?x) (handempty))
        :effect (and (not (ontable ?x)) (not (clear ?x)) (not (handempty)) (holding ?x))
    )

    (:action put-down
        :parameters (?x - block)
        :precondition (holding ?x)
        :effect (and (not (holding ?x)) (clear ?x) (ontable ?x) (handempty))
    )

    (:action stack
        :parameters (?x - block ?y - block)
        :precondition (and (holding ?x) (clear ?y))
        :effect (and (not (holding ?x)) (not (clear ?y)) (clear ?x) (on ?x ?y) (handempty))
    )

    (:action unstack
        :parameters (?x - block ?y - block)
        :precondition (and (on ?x ?y) (clear ?x) (handempty))
        :effect (and (not (on ?x ?y)) (not (clear ?x)) (clear ?y) (holding ?x) (not (handempty)))
    )
)
"""

# --- 2. Define the PDDL Problem (using pddlpy's internal representation) ---
# In a real PDDL file, this would be structured with (:problem ...)
# and define objects, initial state, and goal state.

problem_pddl = """
(define (problem simple-blocksworld)
    (:domain blocksworld)
    (:objects a b c - block)
    (:init
        (ontable a)
        (ontable b)
        (ontable c)
        (clear a)
        (clear b)
        (clear c)
        (handempty)
    )
    (:goal (and
        (on a b)
        (on b c)
    ))
)
"""

print("--- PDDL Domain Definition ---")
print(domain_pddl)
print("\n--- PDDL Problem Definition ---")
print(problem_pddl)

# --- 3. Load the PDDL domain and problem using pddlpy ---
# pddlpy.Domain and pddlpy.Problem objects parse the PDDL strings.
try:
    domain = pddlpy.Domain(domain_pddl)
    problem = pddlpy.Problem(domain, problem_pddl)
    print("\nPDDL Domain and Problem loaded successfully.")
except Exception as e:
    print(f"\nError loading PDDL: {e}")
    exit()

# --- 4. Solve the planning problem ---
# pddlpy's planner will search for a sequence of actions.
print("\n--- Attempting to find a plan ---")
plan = problem.solve()

# --- 5. Print the resulting plan ---
if plan:
    print("\nPlan found:")
    for step in plan:
        print(f"- {step}")
else:
    print("\nNo plan found for the given problem.")

print("\n--- Example with a different initial state and goal ---")
problem_pddl_2 = """
(define (problem blocksworld-2)
    (:domain blocksworld)
    (:objects a b c - block)
    (:init
        (ontable c)
        (on b c)
        (on a b)
        (clear a)
        (handempty)
    )
    (:goal (and
        (on c a)
        (on a b)
    ))
)
"""
problem2 = pddlpy.Problem(domain, problem_pddl_2)
plan2 = problem2.solve()

if plan2:
    print("\nPlan 2 found:")
    for step in plan2:
        print(f"- {step}")
else:
    print("\nNo plan found for problem 2.")

```

**Explanation of the Python Example:**

1.  **PDDL Domain Definition (`domain_pddl`)**: This multi-line string contains the PDDL definition for the Blocksworld domain.
    *   `(:domain blocksworld)`: Names the domain.
    *   `(:requirements :strips :typing)`: Specifies features used (STRIPS for basic actions, typing for object categories).
    *   `(:types block)`: Defines a type `block`.
    *   `(:predicates ...)`: Defines the possible facts about the world (e.g., `(on A B)` means block A is on block B).
    *   `(:action ...)`: Defines the four possible actions: `pick-up`, `put-down`, `stack`, `unstack`. Each action has:
        *   `:parameters`: The objects involved in the action.
        *   `:precondition`: What must be true *before* the action can happen.
        *   `:effect`: What changes (adds/deletes) in the world *after* the action happens.

2.  **PDDL Problem Definition (`problem_pddl`)**: This string defines a specific instance of the Blocksworld problem.
    *   `(:problem simple-blocksworld)`: Names the problem.
    *   `(:domain blocksworld)`: Links this problem to the `blocksworld` domain.
    *   `(:objects a b c - block)`: Declares three specific blocks: `a`, `b`, `c`.
    *   `(:init ...)`: Describes the initial state of the world (all blocks on the table, clear, hand empty).
    *   `(:goal ...)`: Describes the desired final state (block A on B, and block B on C).

3.  **Loading with `pddlpy`**:
    *   `pddlpy.Domain(domain_pddl)`: Parses the domain string into a `pddlpy` Domain object.
    *   `pddlpy.Problem(domain, problem_pddl)`: Parses the problem string, associating it with the loaded domain.

4.  **Solving the Problem**:
    *   `problem.solve()`: This is the core planning step. `pddlpy`'s internal planner searches for a sequence of actions that transforms the initial state into the goal state, respecting the action preconditions and effects.

5.  **Printing the Plan**: If `problem.solve()` finds a plan, it returns a list of actions. The code then iterates through and prints each action in the plan.

The second example (`problem_pddl_2`) demonstrates how the same domain can be used with a different initial state and goal to generate a new plan.

This example illustrates how PDDL provides a declarative way to define planning problems, and how a Python library can be used to interact with and solve these problems.

## Interview Questions

1.  **What is PDDL, and what is its primary purpose in AI?**
    *   **Answer**: PDDL (Planning Domain Definition Language) is a standardized, declarative language used in AI for describing planning problems. Its primary purpose is to formally define the characteristics of a planning domain (types of objects, predicates, actions) and a specific problem instance within that domain (initial state, goal state, objects), allowing general-purpose AI planners to find sequences of actions to achieve goals.

2.  **Explain the two main components of a PDDL description.**
    *   **Answer**: The two main components are the **Domain File** and the **Problem File**.
        *   The **Domain File** defines the general rules of an environment: object types, predicates (facts about the world), and actions (operators with preconditions and effects). It's reusable across different specific problems.
        *   The **Problem File** describes a specific instance of a planning problem: the concrete objects involved, the initial state of the world, and the desired goal state. It references a specific domain.

3.  **What are predicates in PDDL, and how are they used?**
    *   **Answer**: Predicates are propositions that describe facts about the world. They are like boolean variables that can be true or false. In PDDL, they are defined with parameters (e.g., `(at ?robot ?location)`). In a specific state, these parameters are "grounded" with actual objects (e.g., `(at robot1 warehouseA)`), making them true or false statements that define the current state of the world. They are used in preconditions to check if an action can be applied and in effects to describe how an action changes the state.

4.  **Describe the role of preconditions and effects in a PDDL action.**
    *   **Answer**:
        *   **Preconditions**: These are a set of predicates that *must be true* in the current state for an action to be considered applicable and executed. If any precondition is false, the action cannot be performed.
        *   **Effects**: These describe how the state of the world changes *after* an action is executed. Effects typically consist of `(add ...)` clauses (predicates that become true) and `(del ...)` clauses (predicates that become false).

5.  **How does PDDL contribute to the reusability of AI planning solutions?**
    *   **Answer**: PDDL promotes reusability by separating the domain definition from the problem definition. A single PDDL domain file (describing the general rules and actions) can be used with multiple different PDDL problem files (describing specific initial states and goals). Furthermore, because PDDL is a standard, different planning algorithms (planners) can be applied to the same PDDL domain and problem definitions.

6.  **What are some limitations of PDDL?**
    *   **Answer**: Some limitations include:
        *   **Complexity for large domains**: Defining and debugging large, intricate domains can be challenging.
        *   **Requires expert knowledge**: Effective modeling often needs a deep understanding of PDDL syntax and planning concepts.
        *   **Limited expressiveness for certain problems**: While PDDL has extensions, the core language struggles with continuous time/states, highly probabilistic outcomes, or complex numerical optimization beyond basic arithmetic.
        *   **Computational cost**: Finding plans can be computationally expensive for complex problems.

7.  **Can PDDL handle numerical values? If so, how?**
    *   **Answer**: Yes, PDDL has extensions (specifically PDDL2.1 and later) that allow for the definition and manipulation of numerical fluents (variables). These fluents can be used in preconditions (e.g., `(> (fuel ?robot) 10)`) and effects (e.g., `(decrease (fuel ?robot) 5)`). This enables modeling resources, costs, and other quantitative aspects of a problem.

8.  **What is the difference between a PDDL domain and a PDDL problem?**
    *   **Answer**: A PDDL **domain** defines the *general rules* of an environment: the types of objects, the possible facts (predicates), and the available actions (operators with preconditions and effects). It's a template. A PDDL **problem** defines a *specific instance* within that domain: the actual objects present, their initial configuration (initial state), and the desired final configuration (goal state). The problem file refers to a specific domain.

9.  **How does an AI planner use PDDL files to generate a plan?**
    *   **Answer**: An AI planner takes the PDDL domain and problem files as input. It starts with the initial state defined in the problem file. It then iteratively explores possible actions defined in the domain file. For each state, it identifies applicable actions (those whose preconditions are met). Executing an action transitions the world to a new state based on its effects. The planner uses search algorithms (e.g., A*, heuristic search) to navigate this "state space" graph, searching for a sequence of actions that leads from the initial state to a state satisfying the goal conditions. The found sequence is the plan.

10. **Provide a simple example of a PDDL action for a "robot delivery" domain.**
    *   **Answer**:
        ```pddl
        (:action move
            :parameters (?robot - robot ?from - location ?to - location)
            :precondition (and
                (at ?robot ?from)
                (connected ?from ?to)
            )
            :effect (and
                (not (at ?robot ?from))
                (at ?robot ?to)
            )
        )
        ```
        This action describes a robot moving from one location to another. Its preconditions are that the robot must be at the starting location (`?from`) and that the two locations must be connected. Its effects are that the robot is no longer at `?from` and is now at `?to`.

## Quiz

1.  What is the primary function of PDDL?
    A) To execute AI planning algorithms.
    B) To describe AI planning problems in a standardized format.
    C) To learn optimal policies from environmental interactions.
    D) To simulate complex physical environments for robots.

2.  Which of the following is typically defined in a PDDL **domain** file?
    A) The initial state of the world.
    B) The specific objects involved in a problem.
    C) The available actions (operators) and their effects.
    D) The desired goal state for a specific problem.

3.  If an action has a precondition `(at ?robot ?location)`, what does this imply?
    A) The robot will move to `?location` after the action.
    B) The robot must be at `?location` for the action to be executed.
    C) The action will make the robot be at `?location`.
    D) The action is only applicable if `?location` is empty.

4.  What is a key advantage of using PDDL for AI planning?
    A) It automatically generates optimal plans without any search.
    B) It allows for the separation of problem description from the planning algorithm.
    C) It can directly handle continuous state spaces and probabilistic outcomes without extensions.
    D) It eliminates the need for defining specific actions, as they are learned.

5.  Which of these is NOT a typical component of a PDDL problem file?
    A) Objects
    B) Initial State
    C) Predicates
    D) Goal State

---

### Answer Key

1.  **B) To describe AI planning problems in a standardized format.**
    *   **Explanation**: PDDL is a descriptive language. It defines the problem, while separate AI planners are responsible for executing algorithms to find solutions.

2.  **C) The available actions (operators) and their effects.**
    *   **Explanation**: The domain file defines the general rules, including types, predicates, and actions. The initial state, specific objects, and goal state are part of the problem file.

3.  **B) The robot must be at `?location` for the action to be executed.**
    *   **Explanation**: A precondition is a condition that must be true *before* an action can be applied. It's a requirement, not an outcome or a future state.

4.  **B) It allows for the separation of problem description from the planning algorithm.**
    *   **Explanation**: This modularity is a core strength of PDDL, enabling reusability and comparison of different planners on the same problem definitions. PDDL's core doesn't automatically handle continuous/probabilistic aspects or learn actions.

5.  **C) Predicates.**
    *   **Explanation**: Predicates are defined in the **domain** file. The problem file then uses these predicates to describe the initial and goal states, and lists the specific objects that instantiate the types defined in the domain.

## Further Reading

1.  **"Artificial Intelligence: A Modern Approach" by Stuart Russell and Peter Norvig**: Chapter 10 (Planning) provides an excellent and comprehensive overview of AI planning, including PDDL. This is a foundational textbook in AI.
    *   [Link to book on Amazon (or search for it online/library)](https://www.amazon.com/Artificial-Intelligence-Modern-Approach-4th/dp/0134610997)

2.  **PDDL.org - The Planning Domain Definition Language Official Website**: This site often hosts the official specifications, tutorials, and resources related to PDDL. It's the authoritative source for the language itself.
    *   [PDDL.org](http://www.pddl.org/) (Note: The site might be intermittently available or redirect to related resources. Searching for "PDDL specification" will yield relevant documents.)

3.  **"Automated Planning and Acting" by Malik Ghallab, Dana Nau, and Paolo Traverso**: A more advanced and specialized textbook dedicated entirely to automated planning, offering deep insights into PDDL and various planning algorithms.
    *   [Link to book on Amazon (or search for it online/library)](https://www.amazon.com/Automated-Planning-Acting-Malik-Ghallab/dp/052119281X)

4.  **International Planning Competition (IPC) Domains**: The IPC provides a rich repository of PDDL domains and problems used for benchmarking planning systems. Exploring these can give practical exposure to various PDDL constructs.
    *   [IPC Website (often hosted by universities, e.g., University of Basel)](https://www.icaps-conference.org/index.php/Main/Competitions) - Look for links to past IPC domains.