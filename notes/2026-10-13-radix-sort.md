# Radix Sort

## Overview
Radix Sort is a non-comparative integer sorting algorithm that sorts data with integer keys by processing individual digits. Unlike comparison-based sorting algorithms (like Merge Sort or Quick Sort) that compare elements directly, Radix Sort distributes elements into buckets based on their digit values, then collects them, repeating this process for each digit position. It's particularly efficient for sorting integers or strings of fixed length.

## What Problem It Solves
Radix Sort primarily solves the problem of efficiently sorting large lists of integers or fixed-length strings. It offers an alternative to comparison-based sorts, which have a theoretical lower bound of $\Omega(N \log N)$ comparisons. For specific data types like integers, Radix Sort can achieve linear time complexity, making it faster than comparison sorts under certain conditions. It's ideal when the range of numbers is known, or when numbers have a limited number of digits.

## How It Works
Radix Sort typically works using the Least Significant Digit (LSD) approach, meaning it starts sorting from the rightmost (least significant) digit and moves towards the leftmost (most significant) digit.

Here's a step-by-step breakdown:

1.  **Determine Maximum Digits:** Find the maximum number of digits in the largest number in the input array. This determines how many passes the algorithm will make.
2.  **Iterate by Digit Position:**
    *   Start with the least significant digit (units place, `exp = 1`).
    *   For each digit position, perform a stable sort on the entire array based *only* on the value of that digit. A stable sorting algorithm (like Counting Sort) is crucial here, as it preserves the relative order of elements that have the same digit value.
    *   After sorting by the current digit, all elements with the same digit value will be grouped together, and their original relative order will be maintained.
    *   Move to the next significant digit (tens place, `exp = 10`, then hundreds place, `exp = 100`, and so on).
3.  **Repeat:** Continue this process until all digit positions (up to the most significant digit) have been processed. After the last pass, the array will be fully sorted.

**Example Trace:** Let's sort `[170, 45, 75, 90, 802, 24, 2, 66]`

*   **Original Array:** `[170, 45, 75, 90, 802, 24, 2, 66]`
*   **Pass 1 (Units Digit - `exp = 1`):**
    *   Sort based on `0, 5, 5, 0, 2, 4, 2, 6`.
    *   Using Counting Sort (stable): `[170, 90, 802, 2, 24, 45, 75, 66]`
*   **Pass 2 (Tens Digit - `exp = 10`):**
    *   Sort based on `7, 4, 7, 9, 0, 2, 0, 6` (for 2, 802, we consider 0 as the tens digit).
    *   Using Counting Sort (stable): `[802, 2, 24, 45, 66, 170, 75, 90]`
*   **Pass 3 (Hundreds Digit - `exp = 100`):**
    *   Sort based on `8, 0, 0, 0, 0, 1, 0, 0` (for 2, 24, 45, 66, 75, 90, we consider 0 as the hundreds digit).
    *   Using Counting Sort (stable): `[2, 24, 45, 66, 75, 90, 170, 802]`
*   **Final Sorted Array:** `[2, 24, 45, 66, 75, 90, 170, 802]`

## Mathematical Intuition
The efficiency of Radix Sort comes from its non-comparative nature. Instead of comparing elements, it uses digit values as indices into "buckets."

Let:
*   $N$ be the number of elements to be sorted.
*   $d$ be the maximum number of digits in any element (or maximum key length).
*   $k$ be the base (radix) of the numbers (e.g., 10 for decimal numbers, 256 for bytes).

Each pass of Radix Sort involves a stable sorting algorithm (like Counting Sort) that processes $N$ elements based on a single digit. Counting Sort has a time complexity of $O(N + k)$ for each pass.

Since there are $d$ passes (one for each digit position), the total time complexity of Radix Sort is:
$$O(d \cdot (N + k))$$

For integers up to a maximum value $M$, the number of digits $d$ can be expressed as $\log_k M$. So, the complexity can also be written as:
$$O(N \log_k M)$$

When $k$ is a constant (e.g., 10 for decimal numbers, or 256 for byte-sized digits), and $d$ is relatively small compared to $N$, Radix Sort approaches a linear time complexity of $O(N)$. This is its primary advantage over comparison sorts.

The space complexity is $O(N + k)$ due to the auxiliary array used by Counting Sort and the buckets for digit distribution.

## Advantages
*   **Faster than Comparison Sorts:** For certain data distributions (e.g., integers within a limited range, fixed-length strings), Radix Sort can achieve linear time complexity $O(N)$, outperforming the $O(N \log N)$ lower bound of comparison-based sorts.
*   **Stable:** If the underlying digit-sorting algorithm (e.g., Counting Sort) is stable, Radix Sort itself is stable. This means elements with equal values maintain their relative order in the sorted output.
*   **Non-Comparative:** It doesn't rely on comparisons, making it immune to the comparison-based sorting lower bound.
*   **Parallelizable:** Each pass of Radix Sort can be parallelized, especially the counting and distribution steps, which can lead to performance gains on multi-core processors.

## Disadvantages
*   **Not General Purpose:** Radix Sort is typically limited to integers or data that can be represented as integers (like strings or floating-point numbers with specific transformations). It cannot directly sort arbitrary data types.
*   **Requires Fixed-Width Keys:** It performs best when all keys have the same number of digits or can be padded to a uniform length. Handling variable-length keys adds complexity.
*   **Space Complexity:** It requires auxiliary space, typically $O(N + k)$, for the counting array and output array used in each pass of Counting Sort. This can be significant if $k$ (the base) is very large.
*   **Performance Dependency on $k$ and $d$:** If the number of digits ($d$) is very large or the base ($k$) is very large, the $O(d \cdot (N + k))$ complexity can make it slower than $O(N \log N)$ comparison sorts.
*   **Implementation Complexity:** Implementing Radix Sort correctly, especially with a stable auxiliary sort, can be more complex than implementing simpler comparison sorts.

## Real World Applications
1.  **Sorting IP Addresses:** IP addresses (IPv4 or IPv6) can be treated as fixed-length integers or sequences of bytes, making Radix Sort an efficient choice for sorting large lists of network addresses in routers or network management systems.
2.  **Data Processing in Databases:** Databases often use Radix Sort for internal sorting operations, especially when dealing with integer primary keys or fixed-length string fields, due to its potential for linear time performance.
3.  **Graphics and Image Processing:** In computer graphics, Radix Sort can be used for tasks like sorting objects by their Z-depth (distance from the viewer) for rendering, or for sorting pixels based on color components.

## Python Example

```python
def counting_sort(arr, exp):
    """
    A stable counting sort for a specific digit position (exp).
    arr: The list of numbers to be sorted.
    exp: The exponent (1, 10, 100, ...) to determine the current digit.
    """
    n = len(arr)
    output = [0] * n  # Output array
    count = [0] * 10  # Count array for digits 0-9

    # Store count of occurrences in count[]
    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1

    # Change count[i] so that count[i] now contains actual
    # position of this digit in output[]
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Build the output array
    # Iterate from the end to ensure stability
    i = n - 1
    while i >= 0:
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
        i -= 1

    # Copy the output array to arr[], so that arr[] now
    # contains sorted numbers according to current digit
    for i in range(n):
        arr[i] = output[i]

def radix_sort(arr):
    """
    Performs Radix Sort on a list of non-negative integers.
    """
    # Find the maximum number to know number of digits
    max_val = max(arr)

    # Do counting sort for every digit. Note that instead
    # of passing digit number, exp is passed. exp is 10^i
    # where i is current digit number
    exp = 1
    while max_val // exp > 0:
        counting_sort(arr, exp)
        exp *= 10

# Example Usage:
my_list = [170, 45, 75, 90, 802, 24, 2, 66]
print("Original list:", my_list)
radix_sort(my_list)
print("Sorted list:", my_list)

my_list_2 = [329, 457, 657, 839, 436, 720, 355]
print("Original list 2:", my_list_2)
radix_sort(my_list_2)
print("Sorted list 2:", my_list_2)
```

## Interview Questions
1.  **How does Radix Sort differ fundamentally from comparison-based sorts like Merge Sort or Quick Sort?**
    *   **Answer:** Radix Sort is a non-comparative sorting algorithm. It sorts elements by processing individual digits or characters without directly comparing two elements against each other. Comparison-based sorts, on the other hand, determine the sorted order by comparing pairs of elements.
2.  **What is the time complexity of Radix Sort, and under what conditions is it most efficient?**
    *   **Answer:** The time complexity of Radix Sort is $O(d \cdot (N + k))$, where $N$ is the number of elements, $d$ is the maximum number of digits (or key length), and $k$ is the base (radix) of the numbers. It is most efficient when $d$ and $k$ are relatively small and constant, making its complexity approach $O(N)$, which is linear. This is particularly true for fixed-width integers or strings.
3.  **Why is it crucial for the auxiliary sorting algorithm (like Counting Sort) used in each pass of Radix Sort to be stable?**
    *   **Answer:** A stable sorting algorithm preserves the relative order of elements that have equal values. In Radix Sort, when sorting by a less significant digit, elements with the same digit value must maintain their original relative order from the previous pass (based on even less significant digits). If the auxiliary sort were unstable, it could scramble this order, leading to an incorrect final sorted output after subsequent passes.

## Quiz
1.  Which of the following is a key characteristic of Radix Sort?
    a) It is a comparison-based sorting algorithm.
    b) It sorts elements by comparing them pairwise.
    c) It sorts elements by processing individual digits or characters.
    d) Its worst-case time complexity is always $O(N \log N)$.
    **Answer:** c) It sorts elements by processing individual digits or characters.

2.  For Radix Sort to work correctly, the auxiliary sorting algorithm used for each digit pass must be:
    a) Unstable
    b) In-place
    c) Comparison-based
    d) Stable
    **Answer:** d) Stable

## Further Reading
1.  **Wikipedia - Radix Sort:** [https://en.wikipedia.org/wiki/Radix_sort](https://en.wikipedia.org/wiki/Radix_sort)
2.  **GeeksforGeeks - Radix Sort:** [https://www.geeksforgeeks.org/radix-sort/](https://www.geeksforgeeks.org/radix-sort/)
3.  **Khan Academy - Radix Sort (Video/Article):** Search for "Radix Sort Khan Academy" for visual explanations and conceptual understanding.