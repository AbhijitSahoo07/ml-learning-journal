# Median of Medians

## Overview
The Median of Medians algorithm is a clever and powerful selection algorithm used to find the $k$-th smallest element in an unsorted list or array. It's a deterministic algorithm, meaning its performance is predictable and doesn't rely on randomness. What makes it particularly significant is its *guaranteed* linear time complexity, $O(n)$, even in the worst-case scenario. This stands in contrast to algorithms like Quickselect, which also finds the $k$-th smallest element in average linear time but can degrade to $O(n^2)$ in the worst case. The Median of Medians achieves this robust performance by carefully selecting a "good" pivot element, ensuring that the partitions created are never too imbalanced.

## What Problem It Solves
The Median of Medians algorithm primarily solves the **selection problem**, which is the task of finding the $k$-th smallest (or largest) element in an unsorted collection of items. This is also known as finding the $k$-th order statistic.

Here's why this problem is important and why Median of Medians is needed:

1.  **Efficiency for Order Statistics**: Often, we don't need to sort an entire dataset to find a specific order statistic like the median, quartiles, or percentiles. Sorting takes $O(n \log n)$ time. If we only need the median, sorting is overkill. Selection algorithms aim to do this faster.

2.  **Worst-Case Performance Guarantees**:
    *   **Quickselect**: A common algorithm for the selection problem is Quickselect, which is a variant of Quicksort. On average, Quickselect runs in $O(n)$ time. However, if a "bad" pivot is chosen repeatedly (e.g., always the smallest or largest element), Quickselect's performance can degrade to $O(n^2)$ in the worst case. This makes it unsuitable for applications where predictable performance is critical, such as real-time systems or security-sensitive contexts where an adversary might intentionally provide inputs that trigger worst-case behavior.
    *   **Median of Medians**: This algorithm guarantees $O(n)$ time complexity in *all* cases, including the worst case. It achieves this by employing a sophisticated pivot selection strategy that ensures the chosen pivot is "good enough" to prevent highly skewed partitions.

3.  **Robustness in Machine Learning**: In machine learning, finding medians or other quantiles is crucial for robust statistics (less sensitive to outliers than means), data preprocessing (e.g., median imputation), and certain algorithms that rely on order statistics. While Quickselect is often used due to its simpler implementation and good average performance, Median of Medians provides a theoretical foundation and a practical alternative when worst-case guarantees are paramount.

In essence, Median of Medians provides a deterministic, worst-case linear time solution to the selection problem, offering a strong guarantee that other simpler selection algorithms cannot always provide.

## How It Works
The Median of Medians algorithm works by recursively finding a "good" pivot element that guarantees balanced partitions, leading to its $O(n)$ worst-case time complexity. Here's a step-by-step breakdown:

Let's say we want to find the $k$-th smallest element in an array `arr` of size $n$.

1.  **Divide into Groups**:
    *   Divide the $n$ elements of the input array `arr` into groups of 5 elements each.
    *   If $n$ is not a multiple of 5, the last group will have fewer than 5 elements.

2.  **Find Medians of Groups**:
    *   For each of these small groups (of size 5 or less), find its median. Since each group is very small, you can simply sort each group and pick the middle element. This takes constant time for each group (e.g., sorting 5 elements takes a fixed small number of comparisons).
    *   Collect all these medians into a new list, let's call it `medians_list`.

3.  **Find the Median of Medians (Recursive Step for Pivot)**:
    *   Recursively call the Median of Medians algorithm on `medians_list` to find its median. This median of medians will be our chosen pivot element, let's call it `pivot`.
    *   This is the core recursive step that ensures the pivot is "good".

4.  **Partition the Array**:
    *   Partition the original array `arr` around the `pivot`. This means rearranging `arr` such that:
        *   All elements less than `pivot` are placed to its left.
        *   All elements greater than `pivot` are placed to its right.
        *   Elements equal to `pivot` can be placed in either partition or in a separate "equal" partition.
    *   Let $L$ be the list of elements less than `pivot`, $E$ be the list of elements equal to `pivot`, and $G$ be the list of elements greater than `pivot`.

5.  **Recurse on the Correct Partition**:
    *   Compare $k$ with the sizes of $L$ and $E$:
        *   If $k \le |L|$ (where $|L|$ is the number of elements in $L$), the $k$-th smallest element must be in $L$. Recursively call Median of Medians on $L$ to find the $k$-th smallest element.
        *   If $k > |L|$ and $k \le |L| + |E|$, the $k$-th smallest element is the `pivot` itself (or any element in $E$).
        *   If $k > |L| + |E|$, the $k$-th smallest element must be in $G$. Recursively call Median of Medians on $G$ to find the $(k - |L| - |E|)$-th smallest element. (We subtract the elements already accounted for in $L$ and $E$).

**Base Case**:
*   If the input array `arr` has 5 or fewer elements, simply sort it and return the $k$-th element directly. This is because for such small arrays, sorting is very fast (constant time).

The choice of groups of 5 is crucial. If groups were smaller (e.g., 3), the recurrence relation wouldn't guarantee linear time. If they were much larger, the constant factor for finding medians of groups would increase, making it less efficient in practice. Groups of 5 strike a balance.

## Mathematical Intuition
The mathematical intuition behind Median of Medians revolves around ensuring that the chosen pivot element is "good enough" to divide the array into two partitions of roughly comparable size. This prevents the worst-case $O(n^2)$ behavior seen in Quickselect.

Let's break down the key ideas:

1.  **The "Good" Pivot Guarantee**:
    *   When we divide the array into groups of 5 and find the median of each group, we get $\lceil n/5 \rceil$ medians.
    *   Let $M$ be the set of these medians.
    *   We then find the median of $M$, which we call `pivot`.
    *   Consider the elements relative to this `pivot`. At least half of the medians in $M$ are less than or equal to `pivot`. Let's say there are $m = \lceil n/5 \rceil$ medians. So, at least $\lceil m/2 \rceil = \lceil (\lceil n/5 \rceil)/2 \rceil$ medians are $\le$ `pivot`.
    *   Each of these medians comes from a group of 5. In each group, the median is greater than or equal to 3 elements (including itself).
    *   Therefore, for each median $m_i \le \text{pivot}$, there are at least 3 elements in its original group that are $\le m_i \le \text{pivot}$.
    *   So, the total number of elements less than or equal to `pivot` is at least $3 \times \lceil (\lceil n/5 \rceil)/2 \rceil$.
    *   A more precise lower bound for elements $\le \text{pivot}$ is $3 \left( \frac{1}{2} \left\lceil \frac{n}{5} \right\rceil - 2 \right) \approx \frac{3n}{10}$. (The "-2" accounts for edge cases with small $n$ and rounding).
    *   Similarly, at least $3n/10$ elements are greater than or equal to `pivot`.
    *   This means that the `pivot` is guaranteed to be within the 30th and 70th percentile of the data. In other words, the smallest partition will contain at least $3n/10$ elements, and the largest partition will contain at most $7n/10$ elements.

2.  **Recurrence Relation for Time Complexity**:
    Let $T(n)$ be the time complexity to find the $k$-th smallest element in an array of size $n$.

    *   **Step 1 & 2 (Divide into groups and find medians)**:
        *   Dividing into groups takes $O(n)$ time.
        *   Finding the median of each group of 5 (by sorting) takes constant time, say $C_1$. There are $\lceil n/5 \rceil$ such groups. So, this step takes $O(n)$ time.
        *   Total for these steps: $O(n)$.

    *   **Step 3 (Find Median of Medians)**:
        *   This is a recursive call on the list of medians, which has size $\lceil n/5 \rceil$.
        *   Time taken: $T(\lceil n/5 \rceil)$.

    *   **Step 4 (Partition the array)**:
        *   Partitioning around the `pivot` takes $O(n)$ time.

    *   **Step 5 (Recurse on the correct partition)**:
        *   As established, the largest partition will have at most $7n/10$ elements.
        *   Time taken: $T(7n/10)$.

    Combining these, the recurrence relation for the worst-case time complexity is:
    $$T(n) \le T(\lceil n/5 \rceil) + T(7n/10) + O(n)$$

3.  **Solving the Recurrence**:
    We can solve this recurrence using the Master Theorem or by substitution. Let's assume $T(n) \le cn$ for some constant $c$.
    $$cn \ge c \lceil n/5 \rceil + c (7n/10) + An$$
    For large $n$, $\lceil n/5 \rceil \approx n/5$.
    $$cn \ge c(n/5) + c(7n/10) + An$$
    $$cn \ge c(2n/10) + c(7n/10) + An$$
    $$cn \ge c(9n/10) + An$$
    $$cn - c(9n/10) \ge An$$
    $$c(n/10) \ge An$$
    $$c/10 \ge A$$
    This inequality holds if we choose $c \ge 10A$. Since $A$ is a positive constant (from the $O(n)$ work), we can always find such a $c$.
    Therefore, the time complexity $T(n)$ is indeed $O(n)$.

This mathematical guarantee is what makes Median of Medians a theoretically important algorithm, ensuring linear time performance regardless of the input data distribution.

## Advantages
*   **Guaranteed Linear Time Complexity**: The most significant advantage is its worst-case time complexity of $O(n)$, which is deterministic. Unlike Quickselect, it never degrades to $O(n^2)$.
*   **Robustness**: It is robust against adversarial inputs that might try to force worst-case behavior by consistently choosing bad pivots.
*   **Theoretical Importance**: It provides a strong theoretical guarantee for the selection problem, demonstrating that order statistics can be found in linear time without relying on randomness.
*   **Foundation for Other Algorithms**: The pivot selection strategy can be adapted for other algorithms, such as a deterministic linear-time Quicksort (though this is rarely used in practice due to high constant factors).

## Disadvantages
*   **Higher Constant Factor**: While asymptotically $O(n)$, the constant factor hidden by the big-O notation is significantly larger than that of Quickselect. This means that for most practical inputs, Quickselect (which has an average-case $O(n)$) will run faster.
*   **Complexity of Implementation**: The algorithm is considerably more complex to implement correctly compared to Quickselect, involving multiple recursive calls and careful handling of partitions.
*   **Not Widely Used in Practice**: Due to its higher constant factor and implementation complexity, Median of Medians is rarely used in practical applications where Quickselect (or even sorting for smaller datasets) is sufficient and often faster on average. Its primary value is theoretical.
*   **Overhead for Small Datasets**: For small arrays, the overhead of dividing into groups, finding medians, and recursive calls makes it slower than simple sorting or Quickselect.

## Real World Applications
While not as commonly implemented as Quickselect due to its complexity, the Median of Medians algorithm and its underlying principles have applications in scenarios where worst-case performance guarantees are critical or where order statistics are fundamental:

1.  **Quantile and Percentile Calculation**: In statistical analysis, data science, and machine learning, calculating medians, quartiles, or arbitrary percentiles is a common task. For instance, finding the 25th, 50th (median), and 75th percentiles of a dataset. While `numpy.percentile` or `pandas.quantile` often use optimized C implementations that might leverage Quickselect or partial sorting, the theoretical guarantee of Median of Medians ensures that these operations can always be performed efficiently, even on maliciously structured data.

2.  **Robust Statistics and Outlier Detection**: The median is a robust statistic, meaning it's less sensitive to outliers than the mean. Algorithms that rely on robust statistics (e.g., RANSAC for model fitting, certain clustering algorithms) might theoretically benefit from a guaranteed linear-time median finding algorithm, especially in environments where data quality is uncertain or adversarial.

3.  **Database Systems and Query Optimization**: Database management systems often need to find specific order statistics (e.g., the $k$-th largest salary, the median age) to answer queries or for internal optimization strategies. While highly optimized internal algorithms are used, the principles of efficient selection are crucial. A deterministic linear-time algorithm could be a component in ensuring predictable query performance.

4.  **Competitive Programming and Algorithm Design**: In competitive programming, where strict time limits and worst-case scenarios are common, understanding and being able to implement Median of Medians can be a valuable tool for solving problems that require finding order statistics with guaranteed efficiency. It also serves as a foundational concept for designing other complex algorithms with strong performance guarantees.

5.  **Theoretical Basis for Deterministic Quicksort**: Although not directly used to implement Quicksort, the pivot selection strategy of Median of Medians can be incorporated into Quicksort to create a deterministic $O(n \log n)$ worst-case sorting algorithm. This is a significant theoretical result, even if the practical overhead makes it less appealing than randomized Quicksort.

## Python Example

This Python example demonstrates the Median of Medians algorithm to find the $k$-th smallest element in a list. We'll implement the algorithm from scratch and then verify its correctness.

```python
import random
import numpy as np

def find_median_of_five(arr):
    """
    Finds the median of a list with 5 or fewer elements.
    This is a base case for the median-of-medians pivot selection.
    """
    arr.sort() # Simple sort for small arrays
    return arr[len(arr) // 2]

def partition(arr, pivot):
    """
    Partitions the array into three lists:
    elements less than pivot, elements equal to pivot, elements greater than pivot.
    """
    less = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    greater = [x for x in arr if x > pivot]
    return less, equal, greater

def median_of_medians(arr, k):
    """
    Finds the k-th smallest element in arr using the Median of Medians algorithm.
    k is 1-indexed.
    """
    n = len(arr)

    # Base case: If the array is small, sort and return the k-th element
    if n <= 5:
        arr.sort()
        return arr[k - 1]

    # 1. Divide arr into groups of 5 and find medians of each group
    medians = []
    for i in range(0, n, 5):
        group = arr[i:min(i + 5, n)] # Handle the last group which might have < 5 elements
        medians.append(find_median_of_five(group))

    # 2. Recursively find the median of these medians (the "pivot")
    # The k for medians_list is (len(medians) // 2) + 1 to get the actual median
    pivot = median_of_medians(medians, (len(medians) // 2) + 1)

    # 3. Partition the original array around the pivot
    less, equal, greater = partition(arr, pivot)

    # 4. Recurse on the correct partition
    if k <= len(less):
        return median_of_medians(less, k)
    elif k <= len(less) + len(equal):
        # The k-th element is the pivot itself (or any element in the 'equal' partition)
        return pivot
    else:
        # Adjust k for the elements in 'less' and 'equal' partitions
        return median_of_medians(greater, k - len(less) - len(equal))

# --- Demonstration ---
if __name__ == "__main__":
    # Generate a dummy dataset
    data_size = 100
    random_data = [random.randint(1, 1000) for _ in range(data_size)]
    print(f"Original data (first 10 elements): {random_data[:10]}...")
    print(f"Data size: {len(random_data)}")

    # Test cases for k
    test_ks = [1, data_size // 4, data_size // 2, 3 * data_size // 4, data_size]

    print("\n--- Testing Median of Medians ---")
    for k_val in test_ks:
        # Make a copy as the algorithm modifies the list in place for base cases
        data_copy = list(random_data)
        
        # Find k-th smallest using Median of Medians
        result_mom = median_of_medians(data_copy, k_val)

        # Verify using Python's built-in sort (for correctness check)
        sorted_data = sorted(random_data)
        expected_result = sorted_data[k_val - 1] # k is 1-indexed

        print(f"For k = {k_val}:")
        print(f"  Median of Medians result: {result_mom}")
        print(f"  Expected result (from sorted): {expected_result}")
        print(f"  Match: {result_mom == expected_result}")
        assert result_mom == expected_result, f"Mismatch for k={k_val}! Got {result_mom}, expected {expected_result}"
        print("-" * 30)

    # Example: Finding the actual median (k = n/2)
    data_size_median = 101 # Odd number for clear median
    random_data_median = [random.randint(1, 1000) for _ in range(data_size_median)]
    k_median = (data_size_median // 2) + 1 # For 1-indexed median

    print(f"\n--- Finding the actual Median (k={k_median}) ---")
    data_copy_median = list(random_data_median)
    result_actual_median = median_of_medians(data_copy_median, k_median)
    sorted_data_median = sorted(random_data_median)
    expected_actual_median = sorted_data_median[k_median - 1]

    print(f"  Data size: {data_size_median}")
    print(f"  Median of Medians result: {result_actual_median}")
    print(f"  Expected median: {expected_actual_median}")
    print(f"  Match: {result_actual_median == expected_actual_median}")
    assert result_actual_median == expected_actual_median, "Mismatch for actual median!"
    print("-" * 30)

    # Example with duplicate values
    data_with_duplicates = [10, 5, 20, 5, 15, 20, 10, 25, 30, 5]
    k_dup = 3 # Find the 3rd smallest
    print(f"\n--- Testing with duplicates (k={k_dup}) ---")
    print(f"  Data: {data_with_duplicates}")
    result_dup = median_of_medians(list(data_with_duplicates), k_dup)
    expected_dup = sorted(data_with_duplicates)[k_dup - 1]
    print(f"  Median of Medians result: {result_dup}")
    print(f"  Expected result: {expected_dup}")
    print(f"  Match: {result_dup == expected_dup}")
    assert result_dup == expected_dup, "Mismatch with duplicates!"
    print("-" * 30)
```

**Explanation of the Code:**

1.  **`find_median_of_five(arr)`**: This helper function is used for the base case of finding the median of a very small list (5 or fewer elements). It simply sorts the small list and returns the middle element.
2.  **`partition(arr, pivot)`**: This function takes an array and a pivot, then divides the array into three new lists: `less` (elements smaller than pivot), `equal` (elements equal to pivot), and `greater` (elements larger than pivot). This is a standard partitioning step.
3.  **`median_of_medians(arr, k)`**:
    *   **Base Case**: If the input `arr` has 5 or fewer elements, it's small enough to just sort and pick the `k-1`-th index element (since `k` is 1-indexed).
    *   **Group Medians**: It iterates through the array in chunks of 5, calls `find_median_of_five` for each chunk, and collects these medians into the `medians` list.
    *   **Recursive Pivot Selection**: It then recursively calls `median_of_medians` on the `medians` list itself to find *its* median. This result becomes our `pivot`. The `k` for this recursive call is `(len(medians) // 2) + 1` to correctly find the median of the `medians` list.
    *   **Partitioning**: The original `arr` is partitioned using the `pivot`.
    *   **Recursive Search**: Based on the size of the `less` and `equal` partitions, the algorithm determines which partition the `k`-th element must be in and makes a recursive call on that partition, adjusting `k` if necessary.
4.  **Demonstration (`if __name__ == "__main__":`)**:
    *   Generates a random list of numbers.
    *   Tests the `median_of_medians` function for various `k` values (smallest, quartiles, median, largest).
    *   Compares the result with Python's built-in `sorted()` function to verify correctness.
    *   Includes specific tests for finding the actual median and handling duplicate values.

## Interview Questions

1.  **What is the primary problem that Median of Medians solves?**
    *   **Answer:** It solves the selection problem, which is finding the $k$-th smallest (or largest) element in an unsorted list or array. This is also known as finding the $k$-th order statistic.

2.  **What is the worst-case time complexity of Median of Medians, and why is this significant?**
    *   **Answer:** The worst-case time complexity is $O(n)$, where $n$ is the number of elements in the array. This is significant because it provides a *guaranteed* linear time performance, unlike Quickselect which has an average-case $O(n)$ but a worst-case $O(n^2)$. This makes it robust against adversarial inputs.

3.  **How does Median of Medians guarantee a good pivot, unlike Quickselect?**
    *   **Answer:** It guarantees a good pivot by recursively finding the median of a set of medians. Specifically, it divides the array into groups of 5, finds the median of each group, and then recursively finds the median of *these* medians. This "median of medians" is chosen as the pivot. This strategy ensures that the pivot is always within the 30th to 70th percentile of the data, preventing highly skewed partitions.

4.  **Why are groups of 5 typically used in the Median of Medians algorithm? What would happen if groups of 3 or 7 were used?**
    *   **Answer:** Groups of 5 are chosen because they strike a balance. If groups of 3 were used, the recurrence relation $T(n) = T(n/3) + T(2n/3) + O(n)$ would not guarantee linear time (it would be $O(n \log n)$). If groups of 7 were used, the recurrence $T(n) = T(n/7) + T(5n/7) + O(n)$ would still yield $O(n)$, but the constant factor for finding medians of 7 elements would be higher, making it less efficient in practice. Groups of 5 are the smallest size that allows for the $O(n)$ worst-case guarantee.

5.  **Explain the recurrence relation for the time complexity of Median of Medians.**
    *   **Answer:** The recurrence relation is $T(n) \le T(\lceil n/5 \rceil) + T(7n/10) + O(n)$.
        *   $T(\lceil n/5 \rceil)$: Time to recursively find the median of medians (the pivot). There are $\lceil n/5 \rceil$ medians.
        *   $T(7n/10)$: Time to recursively search in the larger partition. The pivot selection guarantees that the largest partition will have at most $7n/10$ elements.
        *   $O(n)$: Time for dividing into groups, finding medians of groups, and partitioning the array.
    This recurrence solves to $O(n)$.

6.  **What are the main disadvantages of Median of Medians compared to Quickselect?**
    *   **Answer:**
        1.  **Higher Constant Factor:** While $O(n)$ asymptotically, its constant factor is significantly larger than Quickselect's, making it slower in practice for most inputs.
        2.  **Implementation Complexity:** It is much more complex to implement correctly due to its nested recursive structure and careful pivot selection.
        3.  **Not Widely Used:** Due to the above, it's rarely used in practical applications where Quickselect's average-case performance is sufficient.

7.  **In what scenarios would you prefer Median of Medians over Quickselect?**
    *   **Answer:** You would prefer Median of Medians in scenarios where:
        1.  **Worst-case performance guarantees are critical:** E.g., real-time systems, safety-critical applications, or security-sensitive contexts where an adversary might craft inputs to degrade performance.
        2.  **Theoretical robustness is paramount:** When proving strong performance bounds for an algorithm.
        3.  **Competitive programming:** Where strict time limits and worst-case inputs are common.

8.  **Can Median of Medians be used as a pivot selection strategy for Quicksort? What would be the implications?**
    *   **Answer:** Yes, it can. If Median of Medians is used to select the pivot for Quicksort, it would guarantee an $O(n \log n)$ worst-case time complexity for Quicksort. The implication is a Quicksort that is robust against worst-case inputs, but at the cost of a significantly higher constant factor due to the overhead of finding the median-of-medians pivot in each step. This makes it generally impractical compared to randomized Quicksort, which has $O(n \log n)$ average-case performance and a much lower constant factor.

9.  **What is the base case for the Median of Medians algorithm?**
    *   **Answer:** The base case is when the input array has a very small number of elements (typically 5 or fewer, matching the group size). In this scenario, the algorithm simply sorts the small array and returns the $k$-th element directly, as sorting a tiny array is a constant-time operation.

10. **How does the partitioning step work in Median of Medians, and why is it crucial?**
    *   **Answer:** After selecting the median-of-medians as the pivot, the array is partitioned into three sub-arrays: elements strictly less than the pivot, elements equal to the pivot, and elements strictly greater than the pivot. This step is crucial because it reduces the problem size. By knowing the sizes of these partitions, the algorithm can determine which sub-array contains the $k$-th element and recursively search only within that sub-array, effectively discarding a significant portion of the data in each step.

## Quiz

1.  What is the worst-case time complexity of the Median of Medians algorithm?
    A) $O(n^2)$
    B) $O(n \log n)$
    C) $O(n)$
    D) $O(\log n)$

2.  The Median of Medians algorithm is primarily used to solve which problem?
    A) Sorting an array
    B) Finding the shortest path in a graph
    C) Finding the $k$-th smallest element in an unsorted array
    D) Matrix multiplication

3.  Why does Median of Medians typically divide the array into groups of 5?
    A) It's an arbitrary choice with no specific mathematical reason.
    B) It's the largest group size that guarantees $O(n)$ complexity.
    C) It's the smallest group size that guarantees $O(n)$ complexity.
    D) It simplifies the implementation significantly.

4.  Which of the following is a major disadvantage of Median of Medians compared to Quickselect?
    A) It has a worse worst-case time complexity.
    B) It is a randomized algorithm, making its performance unpredictable.
    C) It has a higher constant factor, making it slower in practice for most inputs.
    D) It cannot handle duplicate values in the array.

5.  If the Median of Medians algorithm partitions an array of size $n$ around its chosen pivot, what is the maximum size of the larger sub-problem it will recurse on?
    A) $n/2$
    B) $n/5$
    C) $7n/10$
    D) $3n/10$

---

### Answer Key

1.  **C) $O(n)$**
    *   **Explanation:** Median of Medians is specifically designed to guarantee linear time complexity in the worst case, making it robust against adversarial inputs.

2.  **C) Finding the $k$-th smallest element in an unsorted array**
    *   **Explanation:** This is known as the selection problem or finding the $k$-th order statistic, which is the core problem Median of Medians addresses.

3.  **C) It's the smallest group size that guarantees $O(n)$ complexity.**
    *   **Explanation:** Groups of 3 would lead to $O(n \log n)$, while groups of 5 are the minimum size that allows the recurrence relation to resolve to $O(n)$. Larger groups would also work but increase the constant factor.

4.  **C) It has a higher constant factor, making it slower in practice for most inputs.**
    *   **Explanation:** While Median of Medians has a better worst-case guarantee ($O(n)$ vs. Quickselect's $O(n^2)$), its more complex pivot selection mechanism introduces a larger constant factor, meaning Quickselect is typically faster on average.

5.  **C) $7n/10$**
    *   **Explanation:** The pivot selection strategy of Median of Medians guarantees that at least $3n/10$ elements are smaller than or equal to the pivot, and at least $3n/10$ elements are greater than or equal to the pivot. This means the largest partition will contain at most $n - 3n/10 = 7n/10$ elements.

## Further Reading

1.  **"Introduction to Algorithms" by Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein (CLRS)**: Chapter 9, "Medians and Order Statistics," provides a detailed explanation of the selection problem, Quickselect, and the Median of Medians algorithm, including its mathematical proof. This is a foundational textbook for algorithms.
    *   *Link (example, may vary by edition/publisher):* Search for "CLRS Chapter 9 Medians and Order Statistics"

2.  **Wikipedia - Selection Algorithm (Median of Medians)**: The Wikipedia page offers a concise yet comprehensive overview, including the algorithm steps, complexity analysis, and comparisons with other selection algorithms.
    *   *Link:* [https://en.wikipedia.org/wiki/Selection_algorithm#Linear_general_selection_algorithm_-_Median_of_Medians_algorithm](https://en.wikipedia.org/wiki/Selection_algorithm#Linear_general_selection_algorithm_-_Median_of_Medians_algorithm)

3.  **GeeksforGeeks - Kth Smallest/Largest Element in Unsorted Array | Set 5 (Median of Medians Algorithm)**: This article provides a good explanation with code examples, often breaking down the concepts in an accessible way for beginners.
    *   *Link:* [https://www.geeksforgeeks.org/kth-smallestlargest-element-unsorted-array-set-5-median-of-medians-algorithm/](https://www.geeksforgeeks.org/kth-smallestlargest-element-unsorted-array-set-5-median-of-medians-algorithm/)