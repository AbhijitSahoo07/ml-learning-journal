# Selection Sort

## Overview
Selection Sort is one of the simplest and most intuitive sorting algorithms. Imagine you have a messy pile of items (like numbers or names) and you want to arrange them in order, say from smallest to largest. Selection Sort tackles this by repeatedly finding the smallest (or largest) element from the unsorted part of the list and moving it to the beginning (or end) of the sorted part. It's like picking the absolute smallest item from your pile, putting it aside, then picking the smallest from the *remaining* pile, and so on, until all items are sorted. It's a comparison-based, in-place sorting algorithm, meaning it sorts elements by comparing them and doesn't require extra memory proportional to the input size.

## What Problem It Solves
The core problem Selection Sort solves is **ordering a collection of items**. In the world of machine learning and data science, sorting is a fundamental operation that appears in various contexts, even if not always explicitly using Selection Sort itself:

1.  **Data Preprocessing**: Before feeding data into a machine learning model, it often needs to be cleaned and organized. Sorting can be crucial for:
    *   **Time-series data**: Sorting by timestamp ensures chronological order, which is vital for many sequence models.
    *   **Ranking and Top-K problems**: If you need to find the top N most relevant items, sorting can help identify them after calculating relevance scores.
    *   **Data Visualization and Analysis**: Sorted data is much easier to analyze, spot trends, or visualize effectively (e.g., sorting features by importance).
    *   **Median/Quantile Calculation**: To find the median or other quantiles, data must first be sorted.
2.  **Algorithm Efficiency**: Some algorithms perform better or require sorted input. For example, binary search, a very efficient search algorithm, *requires* the data to be sorted. While Selection Sort might not be the fastest way to sort for large datasets, understanding its mechanism is foundational to understanding more complex sorting algorithms.
3.  **Educational Tool**: Selection Sort's simplicity makes it an excellent algorithm for beginners to understand the core concepts of sorting, algorithm design, and complexity analysis before moving on to more advanced techniques.

While Selection Sort is rarely the algorithm of choice for large datasets in production ML systems due to its inefficiency, its conceptual simplicity makes it a valuable stepping stone for understanding more complex data manipulation techniques.

## How It Works
Selection Sort works by dividing the input list into two parts: a sorted sublist and an unsorted sublist. Initially, the sorted sublist is empty, and the unsorted sublist contains all elements. The algorithm then repeatedly "selects" the smallest (or largest) element from the unsorted sublist and swaps it with the leftmost element of the unsorted sublist, effectively moving it to the sorted sublist.

Let's break down the step-by-step mechanism for sorting in ascending order:

1.  **Initialization**: Start with an unsorted list of $n$ elements.
2.  **First Pass (Finding the Smallest)**:
    *   Assume the first element of the unsorted list is the minimum.
    *   Iterate through the *rest* of the unsorted list (from the second element to the last).
    *   If you find an element smaller than your current minimum, update your minimum to that new element's value and remember its position (index).
    *   After checking all elements in the unsorted part, you will have identified the absolute smallest element and its index.
3.  **Swap**: Swap the smallest element found with the element at the current starting position of the unsorted sublist. This moves the smallest element to its correct sorted position at the beginning of the list.
4.  **Shrink Unsorted Sublist**: The element that was just swapped is now considered part of the sorted sublist. The unsorted sublist effectively shrinks by one element from its left side.
5.  **Repeat**: Increment the starting position of the unsorted sublist by one. Repeat steps 2-4 for the new unsorted sublist. Continue this process until the entire list is sorted (i.e., the unsorted sublist becomes empty, or only contains one element, which is by definition sorted).

**Example Walkthrough (Ascending Order):**

Let's sort the list `[64, 25, 12, 22, 11]`

*   **Initial List**: `[64, 25, 12, 22, 11]`

*   **Pass 1 (i=0)**:
    *   Unsorted part: `[64, 25, 12, 22, 11]`
    *   Assume `64` (at index 0) is min.
    *   Compare `64` with `25`. `25` is smaller. New min is `25` (at index 1).
    *   Compare `25` with `12`. `12` is smaller. New min is `12` (at index 2).
    *   Compare `12` with `22`. `12` is still min.
    *   Compare `12` with `11`. `11` is smaller. New min is `11` (at index 4).
    *   Smallest element found is `11` at index `4`.
    *   Swap `64` (at index 0) with `11` (at index 4).
    *   List becomes: `[11, 25, 12, 22, 64]`
    *   Sorted part: `[11]` | Unsorted part: `[25, 12, 22, 64]`

*   **Pass 2 (i=1)**:
    *   Unsorted part: `[25, 12, 22, 64]` (starting from index 1)
    *   Assume `25` (at index 1) is min.
    *   Compare `25` with `12`. `12` is smaller. New min is `12` (at index 2).
    *   Compare `12` with `22`. `12` is still min.
    *   Compare `12` with `64`. `12` is still min.
    *   Smallest element found is `12` at index `2`.
    *   Swap `25` (at index 1) with `12` (at index 2).
    *   List becomes: `[11, 12, 25, 22, 64]`
    *   Sorted part: `[11, 12]` | Unsorted part: `[25, 22, 64]`

*   **Pass 3 (i=2)**:
    *   Unsorted part: `[25, 22, 64]` (starting from index 2)
    *   Assume `25` (at index 2) is min.
    *   Compare `25` with `22`. `22` is smaller. New min is `22` (at index 3).
    *   Compare `22` with `64`. `22` is still min.
    *   Smallest element found is `22` at index `3`.
    *   Swap `25` (at index 2) with `22` (at index 3).
    *   List becomes: `[11, 12, 22, 25, 64]`
    *   Sorted part: `[11, 12, 22]` | Unsorted part: `[25, 64]`

*   **Pass 4 (i=3)**:
    *   Unsorted part: `[25, 64]` (starting from index 3)
    *   Assume `25` (at index 3) is min.
    *   Compare `25` with `64`. `25` is still min.
    *   Smallest element found is `25` at index `3`.
    *   Swap `25` (at index 3) with `25` (at index 3). (No actual change, but conceptually a swap occurs).
    *   List becomes: `[11, 12, 22, 25, 64]`
    *   Sorted part: `[11, 12, 22, 25]` | Unsorted part: `[64]`

*   **Pass 5 (i=4)**:
    *   Unsorted part: `[64]` (starting from index 4)
    *   Only one element left, it's already in its correct place. No comparisons or swaps needed.
    *   List becomes: `[11, 12, 22, 25, 64]`
    *   Sorted part: `[11, 12, 22, 25, 64]` | Unsorted part: `[]`

The list is now fully sorted!

## Mathematical Intuition

The mathematical intuition behind Selection Sort primarily revolves around its **time complexity** (how many operations it takes as the input size grows) and **space complexity** (how much extra memory it uses).

Let $n$ be the number of elements in the list we want to sort.

### Time Complexity

Selection Sort involves nested loops.
*   The **outer loop** iterates $n-1$ times (from the first element up to the second-to-last, as the last element will be in place automatically). This loop determines the position where the next smallest element will be placed.
*   The **inner loop** iterates through the unsorted portion of the list to find the minimum element.

Let's analyze the number of comparisons:

*   **First pass (outer loop $i=0$)**: The inner loop compares the element at index 0 with $n-1$ other elements to find the minimum. This is $n-1$ comparisons.
*   **Second pass (outer loop $i=1$)**: The inner loop compares the element at index 1 with $n-2$ other elements (the remaining unsorted part). This is $n-2$ comparisons.
*   ...
*   **Last pass (outer loop $i=n-2$)**: The inner loop compares the element at index $n-2$ with $1$ other element. This is $1$ comparison.

The total number of comparisons is the sum of an arithmetic series:
$$ (n-1) + (n-2) + \dots + 1 $$
This sum can be calculated using the formula for the sum of the first $k$ integers, which is $\frac{k(k+1)}{2}$. Here, $k = n-1$.
So, the total number of comparisons is:
$$ \frac{(n-1)((n-1)+1)}{2} = \frac{(n-1)n}{2} = \frac{n^2 - n}{2} $$
As $n$ becomes very large, the $n^2$ term dominates. Therefore, the number of comparisons is approximately proportional to $n^2$.

Now, let's analyze the number of swaps:
In each pass of the outer loop, exactly one swap is performed (to place the found minimum element into its correct position). Since the outer loop runs $n-1$ times, there are exactly $n-1$ swaps.

Combining these, the dominant factor for time complexity is the number of comparisons, which is $O(n^2)$.
*   **Best Case Time Complexity**: $O(n^2)$ (even if the list is already sorted, it still performs all comparisons).
*   **Worst Case Time Complexity**: $O(n^2)$ (e.g., if the list is sorted in reverse order).
*   **Average Case Time Complexity**: $O(n^2)$

This means that if you double the number of elements in your list, the time it takes to sort will roughly quadruple. For very large datasets, an $O(n^2)$ algorithm becomes very slow.

### Space Complexity

Space complexity refers to the amount of extra memory an algorithm needs to run.
Selection Sort is an **in-place** sorting algorithm. This means it sorts the elements within the original array without requiring a significant amount of additional memory. It only needs a few temporary variables to store the minimum element's value and its index during a pass, and for swapping elements.
This constant amount of extra space, regardless of the input size $n$, is denoted as $O(1)$.

In summary:
*   **Time Complexity**: $O(n^2)$
*   **Space Complexity**: $O(1)$

## Advantages
*   **Simplicity**: Selection Sort is one of the easiest sorting algorithms to understand and implement. Its logic is straightforward.
*   **In-Place Sorting**: It requires a minimal amount of additional memory ($O(1)$ space complexity) because it sorts the array by swapping elements within the original array itself. This is beneficial for systems with limited memory.
*   **Minimal Swaps**: Unlike some other quadratic sorting algorithms (like Bubble Sort), Selection Sort performs at most $n-1$ swaps. This can be an advantage in scenarios where writing to memory (swapping elements) is a very expensive operation compared to reading (comparing elements).
*   **Good for Small Lists**: For very small lists, the overhead of more complex algorithms might outweigh the benefits of their better asymptotic complexity, making Selection Sort a reasonable choice due to its simplicity.

## Disadvantages
*   **Inefficiency for Large Datasets**: Its $O(n^2)$ time complexity makes it highly inefficient for large lists. As the number of elements grows, the execution time increases quadratically, making it impractical for big data.
*   **Not Adaptive**: Selection Sort performs the same number of comparisons regardless of the initial order of the elements. Even if the list is already sorted, it will still go through all $O(n^2)$ comparisons.
*   **Not Stable**: A sorting algorithm is "stable" if it preserves the relative order of equal elements. Selection Sort is generally not stable. For example, if you have `[5a, 8, 5b]` and `5a` appears before `5b`, after sorting, `5b` might appear before `5a` if `5b` was chosen as the minimum and swapped.
*   **Performance in all cases**: Best, worst, and average case time complexity are all $O(n^2)$, meaning its performance doesn't improve even with partially sorted data.

## Real World Applications
While Selection Sort is not typically used for large-scale, performance-critical applications due to its $O(n^2)$ time complexity, its simplicity and minimal swap count can make it suitable for specific niche scenarios:

1.  **Educational Purposes**: Selection Sort is frequently taught as one of the first sorting algorithms in computer science courses. Its straightforward logic makes it an excellent tool for beginners to grasp fundamental concepts like loops, comparisons, swaps, and algorithm complexity analysis.
2.  **Small Data Sets or Embedded Systems**: In environments with very limited memory or where the datasets are guaranteed to be small (e.g., a few dozen elements), the simplicity of Selection Sort might be preferred over more complex algorithms. The overhead of setting up more advanced sorts could outweigh the performance benefits for tiny inputs. Embedded systems often prioritize simple, predictable code.
3.  **Situations Where Swaps are Costly**: In very specific scenarios where memory writes (swaps) are significantly more expensive than memory reads (comparisons) – for instance, if elements are very large objects that take a long time to copy – Selection Sort's minimal number of swaps ($O(n)$ swaps compared to $O(n^2)$ comparisons) could be an advantage over algorithms like Bubble Sort.
4.  **Internal Sorting in Hybrid Algorithms**: Sometimes, more advanced sorting algorithms (like Introsort, which is a hybrid of QuickSort, HeapSort, and InsertionSort) might switch to a simpler algorithm like Insertion Sort or Selection Sort for very small sub-arrays to reduce overhead. While Insertion Sort is more common for this, Selection Sort could theoretically be used.
5.  **Demonstrating Algorithm Visualization**: Due to its predictable and clear step-by-step process, Selection Sort is often used in algorithm visualization tools to clearly illustrate how sorting works, making it easier for learners to follow the process.

## Python Example

Here's a complete, standalone Python code snippet demonstrating Selection Sort. We'll use a standard Python list for simplicity, as `numpy` arrays don't fundamentally change the sorting logic for this algorithm.

```python
import random
import time

def selection_sort(arr):
    """
    Sorts a list of numbers in ascending order using the Selection Sort algorithm.

    Args:
        arr (list): The list of numbers to be sorted.

    Returns:
        list: The sorted list.
    """
    n = len(arr)

    # Traverse through all array elements
    for i in range(n):
        # Find the minimum element in remaining unsorted array
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j

        # Swap the found minimum element with the first element of the unsorted part
        # This places the smallest element at its correct sorted position
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    
    return arr

# --- Demonstration ---

print("--- Selection Sort Demonstration ---")

# 1. Generate a dummy dataset
# Let's create a list of 10 random integers for a clear demonstration
data_size = 10
dummy_data = [random.randint(1, 100) for _ in range(data_size)]

print(f"\nOriginal list ({data_size} elements):")
print(dummy_data)

# 2. Apply the Selection Sort operation
print("\nSorting the list using Selection Sort...")
start_time = time.time()
sorted_data = selection_sort(list(dummy_data)) # Pass a copy to preserve original if needed
end_time = time.time()

# 3. Print the results
print("\nSorted list:")
print(sorted_data)

# 4. Basic evaluation/verification
is_sorted = all(sorted_data[k] <= sorted_data[k+1] for k in range(len(sorted_data) - 1))
print(f"\nIs the list correctly sorted? {is_sorted}")
print(f"Time taken for sorting: {end_time - start_time:.6f} seconds")

# --- Another example with a smaller, custom list ---
print("\n--- Custom List Example ---")
custom_list = [64, 25, 12, 22, 11]
print(f"Original custom list: {custom_list}")
sorted_custom_list = selection_sort(custom_list)
print(f"Sorted custom list: {sorted_custom_list}")

# --- Example with duplicate values ---
print("\n--- Duplicate Values Example ---")
duplicates_list = [5, 2, 8, 2, 5, 1]
print(f"Original list with duplicates: {duplicates_list}")
sorted_duplicates_list = selection_sort(duplicates_list)
print(f"Sorted list with duplicates: {sorted_duplicates_list}")
```

**Explanation of the Code:**

1.  **`selection_sort(arr)` function**:
    *   `n = len(arr)`: Gets the total number of elements in the list.
    *   **Outer loop (`for i in range(n)`):** This loop iterates from the first element to the last. `i` represents the current position where we want to place the smallest element found in the *remaining unsorted part*.
    *   **`min_idx = i`**: We initially assume that the element at the current position `i` is the minimum in the unsorted part.
    *   **Inner loop (`for j in range(i + 1, n)`):** This loop iterates through the rest of the unsorted part of the list (from `i + 1` to the end). Its purpose is to find the *actual* minimum element in this unsorted segment.
    *   **`if arr[j] < arr[min_idx]: min_idx = j`**: If an element `arr[j]` is found that is smaller than the current minimum (`arr[min_idx]`), then `min_idx` is updated to `j`.
    *   **`arr[i], arr[min_idx] = arr[min_idx], arr[i]`**: After the inner loop completes, `min_idx` holds the index of the smallest element in the unsorted part. This line performs a swap: the smallest element is moved to position `i`, and the element originally at `i` is moved to `min_idx`. This effectively places the smallest element into its correct sorted position.
    *   The function returns the modified (sorted) list.

2.  **Demonstration Section**:
    *   A list `dummy_data` of 10 random integers is generated to serve as our input.
    *   The `selection_sort` function is called on a copy of `dummy_data` (to keep the original list intact for comparison, though `selection_sort` modifies in-place).
    *   The original and sorted lists are printed.
    *   A simple check `is_sorted` verifies if the list is indeed sorted correctly.
    *   The time taken for sorting is measured using `time.time()` to give an idea of performance (though for 10 elements, it will be very fast).
    *   Additional examples with a custom list and a list with duplicate values are provided to show its behavior.

## Interview Questions

Here are some common interview questions about Selection Sort, along with detailed answers:

1.  **What is Selection Sort? Explain its basic principle.**
    *   **Answer:** Selection Sort is a simple, in-place, comparison-based sorting algorithm. Its basic principle is to repeatedly find the minimum (or maximum) element from the unsorted part of the list and swap it with the element at the current beginning (or end) of the unsorted part. This effectively builds the sorted list one element at a time from the beginning.

2.  **Describe the step-by-step process of Selection Sort.**
    *   **Answer:**
        1.  Start with an unsorted list of $n$ elements.
        2.  Initialize an outer loop that iterates from the first element to the second-to-last element (index `0` to `n-2`). This `i` represents the current position where the smallest element will be placed.
        3.  Inside the outer loop, assume the element at index `i` is the minimum. Store its index as `min_idx`.
        4.  Start an inner loop from `i+1` to `n-1`. Compare each element `arr[j]` with `arr[min_idx]`. If `arr[j]` is smaller, update `min_idx` to `j`.
        5.  After the inner loop completes, `min_idx` will hold the index of the smallest element in the unsorted portion `arr[i...n-1]`.
        6.  Swap the element at `arr[i]` with the element at `arr[min_idx]`. This places the smallest element into its correct sorted position.
        7.  The outer loop continues, effectively shrinking the unsorted portion of the list by one element from the left.

3.  **What is the time complexity of Selection Sort in the best, worst, and average cases?**
    *   **Answer:** Selection Sort has a time complexity of $O(n^2)$ in all cases (best, worst, and average). This is because it always performs $O(n^2)$ comparisons, regardless of the initial arrangement of the elements. The outer loop runs $n-1$ times, and the inner loop runs approximately $n$, $n-1$, ..., $1$ times, leading to $\frac{n(n-1)}{2}$ comparisons.

4.  **What is the space complexity of Selection Sort?**
    *   **Answer:** Selection Sort has a space complexity of $O(1)$. It is an in-place sorting algorithm, meaning it sorts the elements within the original array and only requires a constant amount of extra memory for temporary variables (like `min_idx` and for swapping).

5.  **Is Selection Sort a stable sorting algorithm? Why or why not?**
    *   **Answer:** No, Selection Sort is generally not a stable sorting algorithm. A stable sort preserves the relative order of equal elements. Selection Sort can disrupt this order because it performs swaps over arbitrary distances. For example, if you have `[5a, 8, 5b]` (where `5a` and `5b` are equal but distinct elements), and `5b` is found to be the minimum in a later pass and swapped with an element that was originally before `5a`, the relative order of `5a` and `5b` might change.

6.  **When would you choose to use Selection Sort over other sorting algorithms?**
    *   **Answer:** Selection Sort is rarely the optimal choice for large datasets due to its $O(n^2)$ time complexity. However, it might be chosen in specific scenarios:
        *   **Educational purposes**: Its simplicity makes it great for teaching fundamental sorting concepts.
        *   **Very small datasets**: For lists with a handful of elements, its simplicity might outweigh the performance benefits of more complex algorithms.
        *   **When memory writes (swaps) are very expensive**: Selection Sort performs a minimal number of swaps (exactly $n-1$ swaps), which can be an advantage if writing to memory is a much costlier operation than reading/comparing.
        *   **Embedded systems with limited resources**: Its simple implementation and $O(1)$ space complexity can be appealing.

7.  **Compare Selection Sort with Bubble Sort.**
    *   **Answer:** Both Selection Sort and Bubble Sort are simple, $O(n^2)$ comparison-based sorting algorithms.
        *   **Comparisons**: Both perform $O(n^2)$ comparisons.
        *   **Swaps**: Selection Sort performs a maximum of $n-1$ swaps, making it efficient in terms of writes. Bubble Sort, in its basic form, can perform up to $O(n^2)$ swaps.
        *   **Stability**: Neither is inherently stable, though Bubble Sort can be made stable with a slight modification.
        *   **Performance**: Selection Sort generally outperforms Bubble Sort slightly in practice due to fewer swaps, especially when element swapping is expensive.

8.  **Compare Selection Sort with Insertion Sort.**
    *   **Answer:**
        *   **Time Complexity**: Both are $O(n^2)$ in the worst and average cases. However, Insertion Sort has a best-case time complexity of $O(n)$ if the list is already sorted, making it adaptive. Selection Sort is always $O(n^2)$.
        *   **Swaps/Shifts**: Selection Sort performs $O(n)$ swaps. Insertion Sort performs $O(n^2)$ shifts (which are similar to swaps in cost).
        *   **Stability**: Insertion Sort is a stable sorting algorithm, while Selection Sort is not.
        *   **Practicality**: Insertion Sort is generally preferred over Selection Sort for small arrays or nearly sorted arrays due to its adaptiveness and stability.

9.  **Can Selection Sort be implemented recursively?**
    *   **Answer:** Yes, Selection Sort can be implemented recursively, although it's less common and generally less efficient than the iterative approach due to function call overhead. A recursive implementation would involve:
        1.  Base case: If the list has 0 or 1 element, it's already sorted.
        2.  Recursive step: Find the minimum element in the current sub-array, swap it with the first element of that sub-array, and then recursively call the sort function on the remaining sub-array (excluding the first element).

10. **What is the primary disadvantage of Selection Sort for large datasets?**
    *   **Answer:** The primary disadvantage is its quadratic time complexity, $O(n^2)$. This means that as the size of the dataset ($n$) increases, the execution time grows proportionally to the square of $n$. For large datasets, this leads to significantly longer processing times compared to more efficient algorithms like Merge Sort or Quick Sort, which have $O(n \log n)$ complexity.

## Quiz

1.  **Which of the following best describes the core mechanism of Selection Sort?**
    A) It repeatedly swaps adjacent elements if they are in the wrong order.
    B) It divides the list into halves, sorts each half, and then merges them.
    C) It repeatedly finds the minimum element from the unsorted part and puts it at the beginning of the sorted part.
    D) It picks an element as a pivot and partitions the array around the pivot.

2.  **What is the time complexity of Selection Sort in the worst-case scenario?**
    A) $O(n \log n)$
    B) $O(n)$
    C) $O(n^2)$
    D) $O(\log n)$

3.  **What is the space complexity of Selection Sort?**
    A) $O(n)$
    B) $O(n \log n)$
    C) $O(1)$
    D) $O(n^2)$

4.  **Is Selection Sort a stable sorting algorithm?**
    A) Yes, always.
    B) No, never.
    C) It depends on the implementation.
    D) Only for already sorted lists.

5.  **Which of the following is an advantage of Selection Sort?**
    A) It is very fast for large datasets.
    B) It is an adaptive algorithm, performing better on nearly sorted data.
    C) It performs a minimal number of swaps.
    D) It is a stable sorting algorithm.

---

### Answer Key

1.  **C) It repeatedly finds the minimum element from the unsorted part and puts it at the beginning of the sorted part.**
    *   **Explanation:** This accurately describes the fundamental operation of Selection Sort. Option A describes Bubble Sort, B describes Merge Sort, and D describes Quick Sort.

2.  **C) $O(n^2)$**
    *   **Explanation:** Selection Sort always performs approximately $n^2/2$ comparisons, regardless of the initial order of elements, making its time complexity $O(n^2)$ in all cases (best, worst, and average).

3.  **C) $O(1)$**
    *   **Explanation:** Selection Sort is an in-place algorithm, meaning it sorts the array by swapping elements within the original array and only requires a constant amount of extra memory for temporary variables.

4.  **B) No, never.**
    *   **Explanation:** Selection Sort is generally not stable because it can swap elements over arbitrary distances, potentially changing the relative order of equal elements.

5.  **C) It performs a minimal number of swaps.**
    *   **Explanation:** Selection Sort performs exactly $n-1$ swaps in total, which is a minimal number compared to its $O(n^2)$ comparisons. This can be an advantage in scenarios where memory writes are costly. Options A, B, and D are incorrect as Selection Sort is slow for large datasets, not adaptive, and not stable.

## Further Reading

1.  **GeeksforGeeks - Selection Sort**: A comprehensive resource with detailed explanations, animations, and code examples in multiple languages.
    *   [https://www.geeksforgeeks.org/selection-sort/](https://www.geeksforgeeks.org/selection-sort/)

2.  **Programiz - Selection Sort Algorithm**: Another excellent beginner-friendly guide with clear diagrams and step-by-step explanations.
    *   [https://www.programiz.com/dsa/selection-sort](https://www.programiz.com/dsa/selection-sort)

3.  **Khan Academy - Selection Sort (Video & Article)**: A great visual and conceptual explanation, often helpful for understanding the algorithm's flow.
    *   [https://www.khanacademy.org/computing/computer-science/algorithms/selection-sort/a/overview-of-selection-sort](https://www.khanacademy.org/computing/computer-science/algorithms/selection-sort/a/overview-of-selection-sort)