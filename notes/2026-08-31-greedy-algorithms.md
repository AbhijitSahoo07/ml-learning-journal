# Greedy Algorithms

## Overview
Greedy algorithms are a class of algorithms that make locally optimal choices at each step with the hope of finding a global optimum. Imagine you're trying to climb a hill, and at every step, you choose to move in the direction that takes you highest, right now. You don't look ahead to see if there's a slightly lower path that eventually leads to a much taller peak; you just focus on the immediate gain.

This "greedy" approach is often simple, intuitive, and computationally efficient. However, the critical challenge with greedy algorithms is that a sequence of locally optimal choices does not always lead to a globally optimal solution. They work best for problems that exhibit two key properties: "greedy choice property" and "optimal substructure."

## What Problem It Solves
Greedy algorithms are primarily used to solve **optimization problems**. These are problems where we need to find the "best" solution among a set of possible solutions, often meaning maximizing a certain value (e.g., profit, efficiency) or minimizing another (e.g., cost, time, number of items).

Specifically, greedy algorithms address problems where:
1.  **A sequence of choices needs to be made:** The final solution is built up by making a series of decisions.
2.  **Each choice contributes to the overall solution:** Every decision impacts the final outcome.
3.  **There's a clear criterion for what constitutes the "best" immediate choice:** At any given step, we can identify the most promising option without considering future consequences too deeply.

**Why is it needed in machine learning?**
While not a core machine learning model type itself, greedy algorithms are fundamental building blocks and strategies used *within* various machine learning contexts:
*   **Feature Selection:** In high-dimensional datasets, selecting the most relevant features can improve model performance and reduce complexity. Greedy approaches like "forward selection" (add the best feature at each step) or "backward elimination" (remove the worst feature at each step) are common.
*   **Decision Tree Construction:** Algorithms like CART (Classification and Regression Trees) build decision trees by greedily selecting the best split point (feature and threshold) at each node to maximize information gain or minimize impurity.
*   **Clustering:** Some clustering algorithms, especially those involving iterative refinement, might use greedy heuristics to assign points to clusters or update cluster centroids.
*   **Resource Allocation/Scheduling:** In scenarios like allocating computational resources or scheduling tasks for training ML models, greedy strategies can be used to optimize throughput or minimize latency.
*   **Approximation Algorithms:** For NP-hard optimization problems in ML (e.g., certain types of graph problems or set cover problems), greedy algorithms are often used to find good, though not necessarily optimal, approximate solutions efficiently.

## How It Works
The mechanism of a greedy algorithm can be broken down into a few simple steps:

1.  **Identify the Optimization Problem:** First, clearly define what you are trying to maximize or minimize. For example, minimize the number of coins, maximize the number of activities scheduled, etc.

2.  **Define the "Greedy Choice":** Determine what constitutes the "best" immediate decision at any given step. This is the core of the greedy strategy. This choice must be locally optimal, meaning it looks like the best option right now, without considering its impact on future choices.

3.  **Make the Greedy Choice:** Select the option that satisfies your greedy criterion. This choice is made without backtracking or reconsidering previous decisions.

4.  **Reduce the Problem:** After making a choice, the original problem is typically reduced to a smaller subproblem. The chosen item/action is removed or accounted for, and the remaining problem needs to be solved.

5.  **Repeat:** Continue steps 2-4 until the problem is completely solved or no further choices can be made. The sequence of greedy choices forms the final solution.

**Example: Coin Change Problem (with standard denominations)**
Suppose you want to make change for 63 cents using the fewest number of coins, with denominations: {25 cents, 10 cents, 5 cents, 1 cent}.

*   **Step 1 (Problem):** Minimize the number of coins to make 63 cents.
*   **Step 2 (Greedy Choice):** Always pick the largest coin denomination that is less than or equal to the remaining amount.
*   **Step 3 & 4 (Make Choice & Reduce):**
    *   Remaining amount: 63 cents. Largest coin $\le 63$ is 25 cents.
    *   Choose one 25-cent coin. Remaining amount: $63 - 25 = 38$ cents.
    *   Remaining amount: 38 cents. Largest coin $\le 38$ is 25 cents.
    *   Choose one 25-cent coin. Remaining amount: $38 - 25 = 13$ cents.
    *   Remaining amount: 13 cents. Largest coin $\le 13$ is 10 cents.
    *   Choose one 10-cent coin. Remaining amount: $13 - 10 = 3$ cents.
    *   Remaining amount: 3 cents. Largest coin $\le 3$ is 1 cent.
    *   Choose one 1-cent coin. Remaining amount: $3 - 1 = 2$ cents.
    *   Remaining amount: 2 cents. Largest coin $\le 2$ is 1 cent.
    *   Choose one 1-cent coin. Remaining amount: $2 - 1 = 1$ cent.
    *   Remaining amount: 1 cent. Largest coin $\le 1$ is 1 cent.
    *   Choose one 1-cent coin. Remaining amount: $1 - 1 = 0$ cents.
*   **Step 5 (Repeat until solved):** The amount is 0. The solution is: two 25-cent coins, one 10-cent coin, and three 1-cent coins, totaling 6 coins. This is indeed the optimal solution for standard US coin denominations.

## Mathematical Intuition
The mathematical intuition behind greedy algorithms revolves around two key properties that, if present in a problem, often guarantee that a greedy approach will yield an optimal solution:

1.  **Greedy Choice Property:** This property states that a globally optimal solution can be reached by making a locally optimal (greedy) choice. In other words, at each step, making the choice that seems best *right now* will not prevent you from finding the overall best solution later. There's always an optimal solution that begins with the greedy choice.

    Let's consider the Coin Change Problem again. Suppose we want to make change for an amount $A$ using a set of coin denominations $C = \{c_1, c_2, \dots, c_k\}$, where $c_1 > c_2 > \dots > c_k$. The greedy choice is to pick the largest coin $c_i$ such that $c_i \le A$.
    
    The greedy choice property for this problem (with standard US denominations) implies that if there's an optimal solution for amount $A$, there's also an optimal solution for $A$ that includes the largest possible coin $c_i \le A$.
    
    Mathematically, if $S^*$ is an optimal set of coins for amount $A$, and $c_{max}$ is the largest coin in $C$ such that $c_{max} \le A$, then there exists an optimal solution $S'$ for $A$ such that $c_{max} \in S'$. This means we can safely pick $c_{max}$ and then solve the subproblem for $A - c_{max}$.

2.  **Optimal Substructure:** This property means that an optimal solution to the overall problem contains optimal solutions to its subproblems. If you remove the greedy choice from an optimal solution, the remaining part must be an optimal solution to the remaining subproblem.

    Continuing with the Coin Change example: If $S^*$ is an optimal solution for amount $A$, and we remove one instance of the largest coin $c_{max}$ from $S^*$, then the remaining coins $S^* \setminus \{c_{max}\}$ must form an optimal solution for the amount $A - c_{max}$.
    
    This can be expressed as:
    Let $A$ be the total amount.
    Let $C = \{c_1, c_2, \dots, c_k\}$ be the set of available coin denominations, sorted in descending order ($c_1 > c_2 > \dots > c_k$).
    We want to find $n_1, n_2, \dots, n_k$ such that:
    $$ \sum_{i=1}^k n_i c_i = A $$
    and the total number of coins $\sum_{i=1}^k n_i$ is minimized.

    The greedy algorithm proceeds as follows:
    For the current amount $A_{current}$:
    1. Find the largest coin $c_j \in C$ such that $c_j \le A_{current}$.
    2. Take $n_j = \lfloor A_{current} / c_j \rfloor$ coins of denomination $c_j$.
    3. Update the remaining amount: $A_{current} \leftarrow A_{current} - n_j c_j$.
    4. Repeat until $A_{current} = 0$.

    This iterative process relies on the assumption that the greedy choice at each step (taking as many of the largest possible coin as possible) is consistent with an overall optimal solution. This assumption holds for standard coin systems but fails for others (e.g., denominations {1, 3, 4} and target 6; greedy gives 4+1+1=3 coins, optimal is 3+3=2 coins).

The mathematical rigor for proving a greedy algorithm's correctness often involves an "exchange argument" or "proof by contradiction," demonstrating that if an optimal solution doesn't make the greedy choice, it can be modified to include the greedy choice without increasing its cost (or decreasing its value), thus showing that an optimal solution *can* always start with the greedy choice.

## Advantages
*   **Simplicity:** Greedy algorithms are often straightforward to understand and implement. The logic for making a choice at each step is usually simple.
*   **Efficiency:** They are typically very fast and have lower time complexity compared to other optimization techniques like dynamic programming or brute-force search, as they don't explore all possible paths.
*   **Intuitive:** The "take the best available option" approach often aligns with human intuition for problem-solving.
*   **Memory Efficient:** They usually require less memory because they don't need to store results of subproblems for future use (unlike dynamic programming).

## Disadvantages
*   **Not Always Optimal:** The biggest drawback is that a greedy algorithm does not guarantee a globally optimal solution for all problems. It can get stuck in a "local optimum," which is the best solution in its immediate vicinity but not the best overall.
*   **Problem-Specific:** Whether a greedy approach works optimally depends heavily on the specific problem's structure and properties (greedy choice property and optimal substructure).
*   **Difficulty in Proving Correctness:** For problems where it *does* work optimally, proving its correctness can sometimes be complex, requiring formal mathematical arguments like exchange proofs.
*   **No Backtracking:** Once a greedy choice is made, it's final. There's no mechanism to backtrack and explore alternative paths if the current path turns out to be suboptimal later.

## Real World Applications
1.  **Minimum Spanning Tree (MST) Algorithms (Prim's and Kruskal's):**
    *   **Application:** Used in network design (e.g., laying out electrical grids, telecommunication networks, or water pipes) to connect all points with the minimum total cable/pipe length.
    *   **Greedy Aspect:** Prim's algorithm greedily adds the cheapest edge connecting a vertex in the MST to a vertex outside the MST. Kruskal's algorithm greedily adds the cheapest edge that does not form a cycle. Both make locally optimal choices to build a globally minimal spanning tree.

2.  **Dijkstra's Algorithm:**
    *   **Application:** Finds the shortest path between a starting node and all other nodes in a graph with non-negative edge weights. Used extensively in GPS navigation systems, network routing protocols (like OSPF), and finding optimal routes in various logistics problems.
    *   **Greedy Aspect:** At each step, Dijkstra's algorithm greedily selects the unvisited node with the smallest known distance from the source node, assuming this path is part of the shortest path.

3.  **Huffman Coding:**
    *   **Application:** A widely used data compression technique (lossless compression). It's used in formats like JPEG, MP3, and various file compression utilities (e.g., `zip`).
    *   **Greedy Aspect:** It builds a binary tree by repeatedly merging the two nodes with the smallest frequencies (or probabilities) until only one node remains. This greedy merging strategy creates a prefix code that minimizes the average code length.

4.  **Activity Selection Problem:**
    *   **Application:** Scheduling tasks or meetings in a conference room, allocating CPU time to processes, or managing resources where multiple activities compete for a single resource over time.
    *   **Greedy Aspect:** Given a set of activities with start and finish times, the greedy strategy is to always select the activity that finishes earliest among the compatible activities. This leaves the maximum amount of time available for subsequent activities.

5.  **Change-making Problem (with standard coin denominations):**
    *   **Application:** Cash registers, vending machines, and financial systems need to dispense change using the fewest possible coins.
    *   **Greedy Aspect:** As demonstrated earlier, for standard coin systems (like USD or EUR), repeatedly taking the largest possible coin denomination that is less than or equal to the remaining amount provides the optimal solution.

## Python Example

Let's demonstrate a greedy algorithm using the **Coin Change Problem**. We'll implement a function that calculates the minimum number of coins needed to make a given amount, assuming standard US coin denominations (25, 10, 5, 1 cents).

```python
import numpy as np

def greedy_coin_change(amount, denominations):
    """
    Calculates the minimum number of coins to make a given amount using a greedy approach.
    
    Args:
        amount (int): The total amount for which to make change.
        denominations (list): A list of available coin denominations, sorted in descending order.
                              Example: [25, 10, 5, 1] for US coins.
                                       For this greedy approach to be optimal, the denominations
                                       must satisfy certain properties (e.g., standard US coins).
                                       It might not work for arbitrary denominations.
                                       
    Returns:
        dict: A dictionary where keys are coin denominations and values are the count of each coin.
        int: The total number of coins used.
    """
    if amount < 0:
        raise ValueError("Amount cannot be negative.")
    if not denominations or any(d <= 0 for d in denominations):
        raise ValueError("Denominations must be positive and non-empty.")
    
    # Ensure denominations are sorted in descending order for the greedy choice
    denominations = sorted(denominations, reverse=True)
    
    coins_used = {}
    total_coins = 0
    remaining_amount = amount
    
    print(f"Making change for: {amount} cents with denominations: {denominations}")
    
    for coin in denominations:
        if remaining_amount == 0:
            break
        
        # Greedy choice: Take as many of the current largest coin as possible
        num_coins = remaining_amount // coin
        
        if num_coins > 0:
            coins_used[coin] = num_coins
            total_coins += num_coins
            remaining_amount -= num_coins * coin
            print(f"  Used {num_coins} x {coin}-cent coin(s). Remaining: {remaining_amount} cents.")
            
    if remaining_amount > 0:
        print(f"  Warning: Could not make exact change. {remaining_amount} cents remaining.")
        
    return coins_used, total_coins

# --- Example Usage ---

# Define standard US coin denominations (sorted descending is good practice for greedy)
us_denominations = [25, 10, 5, 1]

# Test Case 1: A common amount
target_amount_1 = 63
print(f"\n--- Test Case 1: Amount = {target_amount_1} ---")
result_coins_1, total_count_1 = greedy_coin_change(target_amount_1, us_denominations)
print(f"Result for {target_amount_1} cents: {result_coins_1}")
print(f"Total coins used: {total_count_1}")

# Test Case 2: A smaller amount
target_amount_2 = 17
print(f"\n--- Test Case 2: Amount = {target_amount_2} ---")
result_coins_2, total_count_2 = greedy_coin_change(target_amount_2, us_denominations)
print(f"Result for {target_amount_2} cents: {result_coins_2}")
print(f"Total coins used: {total_count_2}")

# Test Case 3: An amount that requires only one type of coin
target_amount_3 = 75
print(f"\n--- Test Case 3: Amount = {target_amount_3} ---")
result_coins_3, total_count_3 = greedy_coin_change(target_amount_3, us_denominations)
print(f"Result for {target_amount_3} cents: {result_coins_3}")
print(f"Total coins used: {total_count_3}")

# Test Case 4: An amount that is 0
target_amount_4 = 0
print(f"\n--- Test Case 4: Amount = {target_amount_4} ---")
result_coins_4, total_count_4 = greedy_coin_change(target_amount_4, us_denominations)
print(f"Result for {target_amount_4} cents: {result_coins_4}")
print(f"Total coins used: {total_count_4}")

# --- Example where greedy fails (for non-standard denominations) ---
# Denominations: {1, 3, 4}
# Target Amount: 6
# Greedy would pick: 4, then 1, then 1 (total 3 coins)
# Optimal would pick: 3, then 3 (total 2 coins)
non_standard_denominations = [4, 3, 1]
target_amount_fail = 6
print(f"\n--- Test Case 5: Greedy Fails Example (Amount = {target_amount_fail}) ---")
print(f"Denominations: {non_standard_denominations}")
result_coins_fail, total_count_fail = greedy_coin_change(target_amount_fail, non_standard_denominations)
print(f"Greedy Result for {target_amount_fail} cents: {result_coins_fail}")
print(f"Greedy Total coins used: {total_count_fail}")
print("  Note: The optimal solution for 6 cents with {1, 3, 4} is two 3-cent coins (2 coins total).")
print("  This demonstrates where a greedy approach does not yield the global optimum.")
```

**Explanation of the Python Code:**

1.  **`greedy_coin_change(amount, denominations)` function:**
    *   Takes `amount` (the target sum) and `denominations` (a list of coin values) as input.
    *   **Input Validation:** Checks for negative amounts or invalid denominations.
    *   **Sorting Denominations:** It's crucial that `denominations` are sorted in *descending* order. The greedy strategy relies on trying the largest possible coin first. `sorted(denominations, reverse=True)` ensures this.
    *   **Initialization:** `coins_used` dictionary stores the count of each coin, `total_coins` tracks the total number of coins, and `remaining_amount` starts with the target `amount`.
    *   **Iterating through Denominations:** The code loops through each coin denomination from largest to smallest.
    *   **Greedy Choice:** `num_coins = remaining_amount // coin` calculates how many times the current `coin` can fit into the `remaining_amount`. This is the greedy choice: take as many of the largest possible coin as you can.
    *   **Update:** If `num_coins` is greater than 0, it means we used some of this coin. We update `coins_used`, `total_coins`, and `remaining_amount`.
    *   **Early Exit:** If `remaining_amount` becomes 0, we've made exact change and can stop.
    *   **Warning:** If `remaining_amount` is still greater than 0 after checking all denominations, it means exact change couldn't be made with the given coins.
    *   **Return Value:** Returns the dictionary of coins used and the total count.

2.  **Example Usage:**
    *   We define `us_denominations` as `[25, 10, 5, 1]`.
    *   Several test cases demonstrate how the algorithm works for different amounts, including one where the greedy approach for non-standard denominations fails to find the optimal solution, highlighting its limitation.

## Interview Questions

1.  **What is a Greedy Algorithm?**
    *   **Answer:** A greedy algorithm is an algorithmic paradigm that makes the locally optimal choice at each stage with the hope of finding a global optimum. It never reconsiders its choices. It's often simple and efficient but doesn't always guarantee the best overall solution.

2.  **When is a greedy algorithm guaranteed to find the optimal solution?**
    *   **Answer:** A greedy algorithm is guaranteed to find the optimal solution for problems that exhibit two key properties:
        *   **Greedy Choice Property:** A globally optimal solution can be reached by making a locally optimal (greedy) choice.
        *   **Optimal Substructure:** An optimal solution to the overall problem contains optimal solutions to its subproblems.

3.  **Give an example where a greedy algorithm fails to find the optimal solution.**
    *   **Answer:** The classic example is the Coin Change Problem with non-standard denominations. Consider denominations {1, 3, 4} and a target amount of 6.
        *   **Greedy approach:** Pick 4 (remaining 2), then 1 (remaining 1), then 1 (remaining 0). Total coins: 3 (4, 1, 1).
        *   **Optimal solution:** Pick 3, then 3. Total coins: 2 (3, 3).
        *   Here, the greedy choice of picking 4 first prevents finding the optimal solution.

4.  **Compare Greedy Algorithms with Dynamic Programming.**
    *   **Answer:**
        *   **Greedy:** Makes locally optimal choices without reconsidering. It's generally faster and simpler but doesn't always guarantee global optimality. It builds a solution step-by-step, never looking back.
        *   **Dynamic Programming:** Solves subproblems and stores their solutions to avoid recomputing them (memoization or tabulation). It explores all possible paths to ensure global optimality. It's typically more complex and slower than greedy but guarantees the optimal solution for problems with optimal substructure and overlapping subproblems.
        *   Both rely on optimal substructure, but dynamic programming also requires overlapping subproblems, and it explores more options to ensure optimality.

5.  **What are the key properties a problem must have for a greedy approach to work optimally?**
    *   **Answer:** The two main properties are the **Greedy Choice Property** (a global optimum can be achieved by making local optimums) and **Optimal Substructure** (an optimal solution to the problem contains optimal solutions to its subproblems). Without both, a greedy approach might not yield the global optimum.

6.  **Name some common greedy algorithms and their applications.**
    *   **Answer:**
        *   **Prim's and Kruskal's Algorithms:** For finding Minimum Spanning Trees (network design).
        *   **Dijkstra's Algorithm:** For finding the shortest path in a graph with non-negative edge weights (GPS, network routing).
        *   **Huffman Coding:** For data compression.
        *   **Activity Selection Problem:** For scheduling non-overlapping activities.
        *   **Fractional Knapsack Problem:** For maximizing value when items can be broken.

7.  **How would you apply a greedy approach to the Activity Selection Problem?**
    *   **Answer:** The Activity Selection Problem involves selecting the maximum number of non-overlapping activities from a given set, each with a start and finish time. The greedy strategy is to:
        1.  Sort all activities by their **finish times** in ascending order.
        2.  Select the first activity (the one that finishes earliest).
        3.  Then, iteratively select the next activity from the remaining ones that starts *after* the previously selected activity finishes.
        This works because choosing an activity that finishes earliest leaves the maximum amount of time available for subsequent activities.

8.  **What are the advantages and disadvantages of using greedy algorithms?**
    *   **Answer:**
        *   **Advantages:** Simplicity, efficiency (often fast with low time complexity), intuitive, and generally memory-efficient.
        *   **Disadvantages:** Does not always find the global optimum (can get stuck in local optima), correctness is highly problem-dependent, and proving correctness can be challenging.

9.  **Can greedy algorithms be used in machine learning? If so, where?**
    *   **Answer:** Yes, they are used as components or strategies within ML algorithms:
        *   **Feature Selection:** Forward selection (greedily add best feature) or backward elimination (greedily remove worst feature).
        *   **Decision Tree Construction:** Algorithms like CART greedily select the best split (feature and threshold) at each node to maximize information gain or minimize impurity.
        *   **Clustering:** Some iterative clustering algorithms might use greedy heuristics for initial assignments or centroid updates.
        *   **Resource Allocation/Scheduling:** Optimizing task scheduling for ML model training.

10. **Explain the concept of "local optimum" vs. "global optimum" in the context of greedy algorithms.**
    *   **Answer:**
        *   **Local Optimum:** The best solution within a restricted or immediate neighborhood of choices. A greedy algorithm always aims for the local optimum at each step.
        *   **Global Optimum:** The absolute best solution among all possible solutions for the entire problem.
        *   The challenge with greedy algorithms is that a sequence of locally optimal choices does not always guarantee reaching the global optimum. The algorithm might make a choice that seems best at the moment but leads to a suboptimal overall solution because it doesn't consider the long-term consequences.

## Quiz

1.  Which of the following best describes a greedy algorithm?
    A) An algorithm that explores all possible solutions to find the optimal one.
    B) An algorithm that makes the best possible choice at each step, hoping to find a global optimum.
    C) An algorithm that breaks down a problem into overlapping subproblems and solves each subproblem only once.
    D) An algorithm that uses randomness to find an approximate solution.

2.  For a greedy algorithm to guarantee an optimal solution, which property is essential?
    A) Overlapping subproblems
    B) Memoization
    C) Greedy Choice Property
    D) Exponential time complexity

3.  Which of these problems is typically solved using a greedy algorithm?
    A) Traveling Salesperson Problem
    B) 0/1 Knapsack Problem
    C) Huffman Coding
    D) Longest Common Subsequence

4.  What is a common disadvantage of greedy algorithms?
    A) They are always very slow.
    B) They require a lot of memory.
    C) They do not always find the globally optimal solution.
    D) They are difficult to implement.

5.  In the context of machine learning, where might a greedy approach be applied?
    A) Training a Support Vector Machine (SVM) kernel.
    B) Optimizing the learning rate for a neural network.
    C) Feature selection in a high-dimensional dataset.
    D) Calculating the gradient in gradient descent.

---

### Answer Key

1.  **B) An algorithm that makes the best possible choice at each step, hoping to find a global optimum.**
    *   **Explanation:** This accurately defines the core principle of a greedy algorithm: making locally optimal decisions. Option A describes brute-force, C describes dynamic programming, and D describes randomized algorithms.

2.  **C) Greedy Choice Property**
    *   **Explanation:** The Greedy Choice Property, along with Optimal Substructure, is crucial for a greedy algorithm to guarantee an optimal solution. Overlapping subproblems and memoization are characteristic of dynamic programming.

3.  **C) Huffman Coding**
    *   **Explanation:** Huffman Coding is a classic example of a greedy algorithm used for data compression. The Traveling Salesperson Problem and 0/1 Knapsack are typically solved with dynamic programming or approximation algorithms, and Longest Common Subsequence is solved with dynamic programming.

4.  **C) They do not always find the globally optimal solution.**
    *   **Explanation:** This is the most significant limitation of greedy algorithms. While they are often simple and efficient, their local choices don't always lead to the best overall outcome.

5.  **C) Feature selection in a high-dimensional dataset.**
    *   **Explanation:** Greedy strategies like forward selection or backward elimination are commonly used in feature selection to iteratively add or remove features based on their immediate impact on model performance. The other options are related to different aspects of ML model training and optimization, not typically direct applications of a greedy algorithm.

## Further Reading

1.  **"Introduction to Algorithms" by Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein (CLRS)**
    *   **Chapter 16: Greedy Algorithms:** This is the definitive textbook chapter for understanding greedy algorithms, their properties, and proofs of correctness. It covers classic examples like activity selection, Huffman codes, and fractional knapsack.
    *   *Note: This is a textbook, so you'd look for the specific chapter.*

2.  **GeeksforGeeks - Greedy Algorithms Tutorial**
    *   **Link:** `https://www.geeksforgeeks.org/greedy-algorithms/`
    *   **Description:** A comprehensive online resource with detailed explanations, examples, and code implementations for various greedy algorithms. It's an excellent starting point for beginners and provides practical insights.

3.  **MIT OpenCourseware - Introduction to Algorithms (Lecture on Greedy Algorithms)**
    *   **Link:** `https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/resources/lecture-15-greedy-algorithms/` (or search for similar lectures from other years)
    *   **Description:** Video lectures and accompanying notes from MIT's renowned algorithms course. These resources offer a deep dive into the theoretical foundations and practical applications of greedy algorithms, often with clear visual explanations.