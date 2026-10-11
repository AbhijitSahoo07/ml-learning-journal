# Naive String Matching

## Overview
Naive String Matching is the simplest and most straightforward algorithm for finding occurrences of a "pattern" string within a larger "text" string. Imagine you're using the "Ctrl+F" function in a document editor to find a specific word or phrase. Naive String Matching is the most basic way a computer could approach this task. It works by systematically checking every possible position in the text where the pattern could potentially start, and then comparing the pattern character by character with the corresponding segment of the text. It's called "naive" because it doesn't employ any clever optimizations or pre-processing steps; it simply tries every possibility.

## What Problem It Solves
The core problem that Naive String Matching solves is the **substring search problem** or **pattern matching problem**. Given a main string, often called the `text` ($T$), and a smaller string, called the `pattern` ($P$), the goal is to find all occurrences (or at least the first one) of $P$ as a substring within $T$.

This problem is fundamental in computer science and has wide-ranging applications:
*   **Text Editors and Word Processors**: When you search for a word or phrase in a document.
*   **Search Engines**: While highly optimized algorithms are used, the basic principle of finding keywords within large bodies of text is rooted here.
*   **Bioinformatics**: Searching for specific DNA or RNA sequences (patterns) within a longer genetic sequence (text).
*   **Data Validation**: Checking if a specific format or keyword exists within user input or a data stream.
*   **Network Intrusion Detection**: Identifying malicious patterns in network traffic.
*   **Plagiarism Detection**: Finding identical or highly similar phrases in documents.

In machine learning, while not a "machine learning algorithm" in the typical sense (it doesn't learn from data), string matching is a crucial utility. For instance, in Natural Language Processing (NLP), you might need to:
*   **Tokenization**: Identify specific delimiters or patterns to break text into words or sentences.
*   **Feature Engineering**: Extract specific keywords or phrases as features for a model.
*   **Data Cleaning**: Find and replace unwanted substrings or identify specific data formats.
*   **Information Retrieval**: Locate documents containing specific query terms.

Therefore, understanding string matching algorithms, even the naive one, provides a foundational understanding of how text data is processed and manipulated, which is essential for many ML tasks involving text.

## How It Works
The Naive String Matching algorithm operates on two main inputs:
1.  **Text ($T$)**: The larger string in which we want to find the pattern. Let its length be $n$.
2.  **Pattern ($P$)**: The smaller string we are searching for. Let its length be $m$.

The algorithm works by sliding the pattern across the text, one character at a time, and at each position, it compares the pattern with the corresponding segment of the text.

Here's a step-by-step breakdown:

1.  **Initialization**:
    *   Assume the text $T$ has length $n$ and the pattern $P$ has length $m$.
    *   The algorithm will try to match the pattern starting at various positions (called "shifts") within the text. These shifts will range from $s=0$ to $s=n-m$. If $m > n$, no match is possible.

2.  **Outer Loop (Iterating through possible shifts)**:
    *   The algorithm starts by aligning the beginning of the pattern ($P[0]$) with the beginning of the text ($T[0]$). This is shift $s=0$.
    *   It then incrementally shifts the pattern one position to the right, trying $P[0]$ with $T[1]$, then $P[0]$ with $T[2]$, and so on, up to $P[0]$ with $T[n-m]$.
    *   For each shift $s$, it performs a character-by-character comparison.

3.  **Inner Loop (Character-by-character comparison for a given shift)**:
    *   For a particular shift $s$, the algorithm compares $P[0]$ with $T[s]$, then $P[1]$ with $T[s+1]$, then $P[2]$ with $T[s+2]$, and so on, up to $P[m-1]$ with $T[s+m-1]$.
    *   This comparison continues as long as the characters match.

4.  **Match or Mismatch**:
    *   **If all $m$ characters of the pattern match** the corresponding $m$ characters in the text segment $T[s \dots s+m-1]$, then a match is found at shift $s$. The algorithm can then report this match and either stop (if only the first match is needed) or continue to find other matches.
    *   **If a mismatch occurs** at any point during the inner loop (i.e., $P[j] \neq T[s+j]$ for some $j < m$), then the pattern does not match at the current shift $s$. The inner loop terminates, and the algorithm proceeds to the next possible shift $s+1$.

5.  **Termination**:
    *   The outer loop continues until all possible shifts (from $0$ to $n-m$) have been checked.
    *   Once the outer loop finishes, the algorithm terminates, having found all occurrences (or none) of the pattern in the text.

**Example Walkthrough:**

Text $T = \text{"ABABDABACDABABCABAB"}$ ($n=19$)
Pattern $P = \text{"ABABCABAB"}$ ($m=9$)

*   **Shift $s=0$**:
    $T$: A B A B D A B A C D A B A B C A B A B
    $P$: A B A B C A B A B
    Mismatch at $P[4]$ ('C') vs $T[4]$ ('D'). Move to next shift.

*   **Shift $s=1$**:
    $T$: A B A B D A B A C D A B A B C A B A B
    $P$:   A B A B C A B A B
    Mismatch at $P[0]$ ('A') vs $T[1]$ ('B'). Move to next shift. (Actually, $P[0]$ vs $T[1]$ is the first comparison for this shift, so it's a mismatch immediately).

*   ... (many shifts will have immediate mismatches) ...

*   **Shift $s=10$**:
    $T$: A B A B D A B A C D **A B A B C A B A B**
    $P$:                   **A B A B C A B A B**
    All characters match! A match is found at shift $s=10$.

The algorithm would continue until $s=n-m = 19-9 = 10$. In this specific example, it finds one match at index 10.

## Mathematical Intuition
Let's formalize the process described above.

We have:
*   A text string $T = t_0 t_1 \dots t_{n-1}$ of length $n$.
*   A pattern string $P = p_0 p_1 \dots p_{m-1}$ of length $m$.

The goal is to find all indices $s$ (shifts) such that the substring of $T$ starting at $s$ and having length $m$ is identical to $P$. That is, we are looking for $s$ where $T[s \dots s+m-1] = P[0 \dots m-1]$.

This equality holds if and only if for every character position $j$ from $0$ to $m-1$, the character $t_{s+j}$ in the text matches the character $p_j$ in the pattern.
So, we are searching for shifts $s$ such that:
$$ t_{s+j} = p_j \quad \text{for all } j \in \{0, 1, \dots, m-1\} $$

The Naive String Matching algorithm systematically checks this condition for every possible starting shift $s$. The possible values for $s$ range from $0$ up to $n-m$. If $m > n$, no match is possible, so the range for $s$ is $0 \le s \le n-m$.

The algorithm can be expressed with nested loops:

```
for s from 0 to n-m:  // Outer loop: iterates through all possible shifts
    match = True
    for j from 0 to m-1: // Inner loop: compares characters for current shift s
        if T[s+j] != P[j]:
            match = False
            break // Mismatch found, no need to compare further for this shift
    if match:
        print("Pattern found at shift", s)
```

**Time Complexity Analysis:**

*   **Outer Loop**: The outer loop runs $n-m+1$ times (from $s=0$ to $s=n-m$).
*   **Inner Loop**: In the worst case, for each iteration of the outer loop, the inner loop might run $m$ times (comparing all $m$ characters of the pattern). This happens if the pattern almost matches the text segment, or if the pattern matches entirely.

Consider the worst-case scenario:
*   **Case 1: Text consists of all 'A's, and pattern is 'AAAB'**:
    $T = \text{"AAAAAAAAAA"}$ ($n=10$)
    $P = \text{"AAAB"}$ ($m=4$)
    For each shift, the algorithm will compare 'AAA' before finding a mismatch at the 4th character. This means $m-1$ comparisons for each of the $n-m+1$ shifts.
*   **Case 2: Text is 'ABABABAB' and pattern is 'ABAB'**:
    $T = \text{"ABABABAB"}$ ($n=8$)
    $P = \text{"ABAB"}$ ($m=4$)
    For each shift, the algorithm will compare all $m$ characters.

Therefore, in the worst case, the total number of character comparisons is approximately $(n-m+1) \times m$.
Since $m$ can be up to $n$, this simplifies to $O(n \times m)$.
If $m$ is a small constant, the complexity is $O(n)$.
If $m \approx n/2$, the complexity is $O(n^2)$.

So, the **worst-case time complexity** of Naive String Matching is $O((n-m+1)m)$, which is often simplified to $O(nm)$.

**Space Complexity:**
The algorithm only requires a few variables to store indices and lengths. It does not require additional data structures proportional to the input size. Therefore, its **space complexity** is $O(1)$ (constant space).

## Advantages
*   **Simplicity**: It is very easy to understand, implement, and debug. The logic is straightforward and intuitive.
*   **No Preprocessing**: Unlike more advanced algorithms (e.g., KMP, Rabin-Karp), Naive String Matching does not require any preprocessing of the pattern or text. You can start searching immediately.
*   **Guaranteed to Find All Matches**: If a pattern exists in the text, this algorithm will definitely find all its occurrences.
*   **Low Memory Usage**: It requires only a constant amount of extra space ($O(1)$), making it suitable for environments with limited memory.

## Disadvantages
*   **Inefficiency (Worst-Case)**: Its primary drawback is its poor performance in the worst-case scenario, where its time complexity is $O(nm)$. This can be very slow for large texts and patterns, especially when there are many partial matches.
*   **Redundant Comparisons**: The algorithm often re-examines characters in the text that it has already looked at. For example, if $T = \text{"AAAAAAB"}$ and $P = \text{"AAB"}$, after checking $T[0 \dots 2]$ and finding a mismatch at $T[2]$ vs $P[2]$, it shifts and re-compares $T[1]$ and $T[2]$ with $P[0]$ and $P[1]$. This redundancy is what makes it inefficient.
*   **No "Intelligence"**: It doesn't learn from previous comparisons. A mismatch at one position doesn't help it decide where to shift the pattern more efficiently; it always shifts by just one position.
*   **Not Suitable for Large Datasets**: Due to its quadratic worst-case complexity, it's generally not recommended for applications involving very large texts or frequent searches, where performance is critical.

## Real World Applications
While often outperformed by more advanced algorithms, Naive String Matching still finds use in specific scenarios due to its simplicity and ease of implementation.

1.  **Basic Text Search Utilities**: For small documents or simple "find" operations (like `Ctrl+F` in a basic text editor or a simple `grep` command on a small file), the overhead of more complex algorithms might not be justified. The naive approach is quick to implement and sufficient for these less demanding tasks.
2.  **Educational Purposes**: It's an excellent starting point for teaching string matching algorithms. Its simplicity helps students grasp the fundamental problem and the concept of pattern searching before moving on to more complex and optimized solutions like KMP or Rabin-Karp.
3.  **Proof-of-Concept or Rapid Prototyping**: When quickly testing an idea or building a prototype where performance isn't the absolute top priority, the naive approach can be implemented very quickly.
4.  **Embedded Systems with Limited Resources**: In highly constrained environments where memory and computational power are severely limited, and the strings involved are relatively short, the $O(1)$ space complexity and simple logic of naive matching can be advantageous over algorithms that require more complex data structures or pre-computation.
5.  **As a Component in Hybrid Algorithms**: Sometimes, the naive approach might be used as a fallback or a final verification step within a larger, more complex string matching system, especially for very short patterns or when the search space has been significantly narrowed down by other means.

## Python Example
Here's a complete, standalone Python code snippet demonstrating the Naive String Matching algorithm.

```python
import time

def naive_string_matcher(text, pattern):
    """
    Implements the Naive String Matching algorithm.

    Args:
        text (str): The main string to search within.
        pattern (str): The pattern string to search for.

    Returns:
        list: A list of starting indices in the text where the pattern is found.
              Returns an empty list if no matches are found.
    """
    n = len(text)
    m = len(pattern)
    
    # List to store the starting indices of found matches
    match_indices = []

    # Edge case: if pattern is longer than text, no match is possible
    if m > n:
        print(f"Pattern '{pattern}' (length {m}) is longer than text '{text}' (length {n}). No match possible.")
        return match_indices

    # Outer loop: Iterate through all possible starting positions (shifts) for the pattern
    # The pattern can start from index 0 up to n-m
    for s in range(n - m + 1):
        # Assume a match for the current shift 's'
        current_match = True
        
        # Inner loop: Compare characters of the pattern with the corresponding segment of the text
        for j in range(m):
            # If a character mismatch is found, set current_match to False and break
            if text[s + j] != pattern[j]:
                current_match = False
                break # No need to compare further for this shift
        
        # If current_match is still True after the inner loop, it means all characters matched
        if current_match:
            match_indices.append(s) # Record the starting index of the match

    return match_indices

# --- Demonstration ---

# Dummy Text and Pattern 1
text1 = "ABABDABACDABABCABAB"
pattern1 = "ABABCABAB"
print(f"Text: '{text1}'")
print(f"Pattern: '{pattern1}'")
start_time = time.time()
matches1 = naive_string_matcher(text1, pattern1)
end_time = time.time()
if matches1:
    print(f"Pattern found at indices: {matches1}")
else:
    print("Pattern not found.")
print(f"Time taken: {end_time - start_time:.6f} seconds\n")

# Dummy Text and Pattern 2 (Multiple matches)
text2 = "GEEKSFORGEEKS"
pattern2 = "GEEK"
print(f"Text: '{text2}'")
print(f"Pattern: '{pattern2}'")
start_time = time.time()
matches2 = naive_string_matcher(text2, pattern2)
end_time = time.time()
if matches2:
    print(f"Pattern found at indices: {matches2}")
else:
    print("Pattern not found.")
print(f"Time taken: {end_time - start_time:.6f} seconds\n")

# Dummy Text and Pattern 3 (No match)
text3 = "HELLO WORLD"
pattern3 = "PYTHON"
print(f"Text: '{text3}'")
print(f"Pattern: '{pattern3}'")
start_time = time.time()
matches3 = naive_string_matcher(text3, pattern3)
end_time = time.time()
if matches3:
    print(f"Pattern found at indices: {matches3}")
else:
    print("Pattern not found.")
print(f"Time taken: {end_time - start_time:.6f} seconds\n")

# Dummy Text and Pattern 4 (Worst-case scenario for partial matches)
text4 = "AAAAAAAAB" * 1000 # A very long string of 'A's followed by 'B'
pattern4 = "AAAAAB" # Pattern that almost matches
print(f"Text (partial): '{text4[:50]}...' (length {len(text4)})")
print(f"Pattern: '{pattern4}' (length {len(pattern4)})")
start_time = time.time()
matches4 = naive_string_matcher(text4, pattern4)
end_time = time.time()
if matches4:
    print(f"Pattern found at indices: {matches4[:5]}... (first 5 matches)") # Print only first few if many
else:
    print("Pattern not found.")
print(f"Time taken: {end_time - start_time:.6f} seconds\n")

# Dummy Text and Pattern 5 (Pattern longer than text)
text5 = "short"
pattern5 = "longer_pattern"
print(f"Text: '{text5}'")
print(f"Pattern: '{pattern5}'")
start_time = time.time()
matches5 = naive_string_matcher(text5, pattern5)
end_time = time.time()
if matches5:
    print(f"Pattern found at indices: {matches5}")
else:
    print("Pattern not found.")
print(f"Time taken: {end_time - start_time:.6f} seconds\n")
```

**Explanation of the Code:**

1.  **`naive_string_matcher(text, pattern)` function**:
    *   Takes two string arguments: `text` and `pattern`.
    *   `n = len(text)` and `m = len(pattern)`: Get the lengths of the input strings.
    *   `match_indices = []`: An empty list to store the starting indices where the pattern is found in the text.
    *   **Edge Case `if m > n`**: If the pattern is longer than the text, it's impossible to find a match, so it prints a message and returns an empty list.
    *   **Outer Loop `for s in range(n - m + 1)`**: This loop iterates through all possible starting positions (`s`) for the pattern within the text.
        *   `s` represents the "shift" or the starting index in the `text` where we align the `pattern`.
        *   The loop runs from `s=0` up to `n-m`. For example, if `n=10` and `m=3`, `n-m+1 = 8`, so `s` goes from `0` to `7`. This covers all possible alignments.
    *   **`current_match = True`**: Before starting the inner comparison for each shift `s`, we optimistically assume that a match will be found.
    *   **Inner Loop `for j in range(m)`**: This loop compares characters.
        *   `j` iterates from `0` to `m-1`, representing the index within the `pattern`.
        *   `text[s + j]` is the character in the `text` that corresponds to `pattern[j]` for the current shift `s`.
        *   **`if text[s + j] != pattern[j]`**: If a mismatch is found, it means the pattern does not match at this shift `s`.
            *   `current_match = False`: Set the flag to indicate a mismatch.
            *   `break`: Exit the inner loop immediately because there's no point in comparing further characters for this shift.
    *   **`if current_match:`**: After the inner loop completes (either by `break` or by comparing all `m` characters), if `current_match` is still `True`, it means all characters matched.
        *   `match_indices.append(s)`: The starting index `s` is added to our list of matches.
    *   **`return match_indices`**: Finally, the function returns the list of all found match indices.
2.  **Demonstration Section**:
    *   Several examples are provided with different texts and patterns to show how the function works for single matches, multiple matches, no matches, and a worst-case scenario.
    *   `time.time()` is used to give a very basic idea of execution time, though for such small inputs, the differences will be negligible. For larger inputs, this would highlight the performance issues.

## Interview Questions

1.  **What is Naive String Matching?**
    *   **Answer**: Naive String Matching is the simplest algorithm for finding occurrences of a pattern string within a larger text string. It works by systematically checking every possible alignment of the pattern within the text, comparing characters one by one until a match is found or a mismatch occurs.

2.  **How does the Naive String Matching algorithm work step-by-step?**
    *   **Answer**:
        1.  It takes a `text` string (length $n$) and a `pattern` string (length $m$) as input.
        2.  It iterates through all possible starting positions (shifts $s$) for the pattern in the text, from $s=0$ up to $s=n-m$.
        3.  For each shift $s$, it compares the pattern $P[0 \dots m-1]$ with the corresponding substring of the text $T[s \dots s+m-1]$ character by character.
        4.  If all $m$ characters match, a match is found at shift $s$.
        5.  If a mismatch occurs at any character position $j$ (i.e., $P[j] \neq T[s+j]$), the comparison for the current shift $s$ stops, and the algorithm moves to the next shift $s+1$.

3.  **What is the time complexity of Naive String Matching? Explain why.**
    *   **Answer**: The worst-case time complexity is $O(nm)$.
        *   The outer loop runs $n-m+1$ times (for each possible shift).
        *   In the worst case (e.g., text "AAAAAAB", pattern "AAB"), for each shift, the inner loop might compare almost all $m$ characters before finding a mismatch or a full match.
        *   Thus, the total number of character comparisons can be up to $(n-m+1) \times m$, which simplifies to $O(nm)$.

4.  **What is the space complexity of the Naive String Matching algorithm?**
    *   **Answer**: The space complexity is $O(1)$ (constant space). It only requires a few variables to store lengths, indices, and a flag, regardless of the size of the input strings.

5.  **When is Naive String Matching suitable to use, despite its worst-case inefficiency?**
    *   **Answer**: It's suitable for:
        *   Small text and pattern sizes where performance isn't critical.
        *   Educational purposes, as a simple introduction to string matching.
        *   Rapid prototyping or proof-of-concept implementations due to its ease of coding.
        *   Environments with extremely limited memory where $O(1)$ space is a strong requirement.

6.  **What are the main drawbacks or disadvantages of Naive String Matching?**
    *   **Answer**:
        *   **Inefficiency**: Poor worst-case time complexity ($O(nm)$).
        *   **Redundant Comparisons**: It often re-examines characters in the text that have already been compared, leading to wasted computations.
        *   **No Optimization**: It doesn't use any pre-processing or information from previous mismatches to speed up subsequent comparisons.

7.  **Can Naive String Matching handle overlapping matches? How?**
    *   **Answer**: Yes, it can handle overlapping matches. Since the algorithm systematically checks every possible shift $s$ from $0$ to $n-m$, if a pattern occurs multiple times, even overlapping, each occurrence will be identified when its corresponding shift $s$ is processed. For example, in "AAAA", searching for "AA", it will find matches at $s=0$, $s=1$, and $s=2$.

8.  **How does Naive String Matching compare to more advanced algorithms like Knuth-Morris-Pratt (KMP) or Rabin-Karp?**
    *   **Answer**:
        *   **Complexity**: Naive is $O(nm)$ (worst-case), while KMP is $O(n+m)$ and Rabin-Karp is $O(n+m)$ on average (worst-case $O(nm)$ but rare).
        *   **Preprocessing**: Naive requires no preprocessing. KMP preprocesses the pattern to build a "LPS array" ($O(m)$). Rabin-Karp preprocesses the pattern to compute its hash ($O(m)$).
        *   **Mechanism**: Naive uses brute-force character comparison. KMP uses information from previous mismatches to avoid redundant shifts. Rabin-Karp uses hashing to quickly compare substrings, only performing character-by-character comparison when hashes match (to avoid spurious hits).
        *   **Efficiency**: KMP and Rabin-Karp are significantly more efficient for large texts and patterns, especially in cases where the naive algorithm performs poorly.

9.  **What happens if the pattern string is longer than the text string in Naive String Matching?**
    *   **Answer**: If the pattern string ($m$) is longer than the text string ($n$), no match is possible. The algorithm would typically handle this by either returning an empty list of matches immediately or by having the outer loop `range(n - m + 1)` result in an empty range, thus executing zero iterations and returning an empty list.

10. **Describe a scenario where Naive String Matching might perform reasonably well, even for relatively large inputs.**
    *   **Answer**: Naive String Matching performs reasonably well when the pattern is very short, or when mismatches occur very early in the character comparison for most shifts. For example, if the text is "ABCDEFG..." and the pattern is "XYZ", the first character comparison ($T[s]$ vs $P[0]$) will likely result in a mismatch for most shifts, causing the inner loop to break almost immediately. In such cases, the number of comparisons per shift is close to 1, leading to an overall complexity closer to $O(n)$.

## Quiz

1.  What is the primary goal of Naive String Matching?
    A) To sort a list of strings alphabetically.
    B) To find all occurrences of a pattern string within a text string.
    C) To compress a given text string.
    D) To calculate the similarity between two strings.

2.  What is the worst-case time complexity of the Naive String Matching algorithm, where $n$ is the length of the text and $m$ is the length of the pattern?
    A) $O(n)$
    B) $O(m)$
    C) $O(n+m)$
    D) $O(nm)$

3.  In Naive String Matching, what happens immediately after a character mismatch is found during the comparison of the pattern with a segment of the text?
    A) The algorithm stops and reports no match.
    B) The pattern is shifted one position to the right, and the comparison restarts from the beginning of the pattern.
    C) The pattern is shifted by $m$ positions to the right.
    D) The algorithm attempts to find a partial match.

4.  Which of the following is a key advantage of Naive String Matching?
    A) Its exceptional speed for large datasets.
    B) Its ability to learn from previous mismatches.
    C) Its simplicity and ease of implementation.
    D) Its requirement for extensive preprocessing.

5.  If the pattern string is "AAAA" and the text string is "AAAAAAAA", how many times will the Naive String Matching algorithm report a match?
    A) 1
    B) 2
    C) 3
    D) 5

---

### Answer Key

1.  **B) To find all occurrences of a pattern string within a text string.**
    *   **Explanation**: The fundamental purpose of any string matching algorithm, including the naive one, is to locate where a smaller string (pattern) appears inside a larger string (text).

2.  **D) $O(nm)$**
    *   **Explanation**: In the worst case, the outer loop runs $n-m+1$ times, and for each iteration, the inner loop might perform up to $m$ character comparisons. This leads to a total of approximately $(n-m+1) \times m$ comparisons, which simplifies to $O(nm)$.

3.  **B) The pattern is shifted one position to the right, and the comparison restarts from the beginning of the pattern.**
    *   **Explanation**: Upon a mismatch, the naive algorithm simply moves to the next possible starting position (shift $s+1$) for the pattern in the text and begins comparing from the first character of the pattern again.

4.  **C) Its simplicity and ease of implementation.**
    *   **Explanation**: The Naive String Matching algorithm is known for its straightforward logic, making it easy to understand, implement, and debug, which is its main advantage over more complex algorithms.

5.  **D) 5**
    *   **Explanation**:
        *   Text: "AAAAAAAA" (length 8)
        *   Pattern: "AAAA" (length 4)
        *   Possible shifts ($s$) are from $0$ to $n-m = 8-4 = 4$.
        *   Shift 0: "AAAA" matches "AAAA" at index 0.
        *   Shift 1: "AAAA" matches "AAAA" at index 1.
        *   Shift 2: "AAAA" matches "AAAA" at index 2.
        *   Shift 3: "AAAA" matches "AAAA" at index 3.
        *   Shift 4: "AAAA" matches "AAAA" at index 4.
        *   Total 5 matches.

## Further Reading

1.  **"Introduction to Algorithms" by Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein (CLRS)**: Chapter 32, "String Matching," provides a detailed and rigorous explanation of Naive String Matching, along with other advanced algorithms. This is a classic textbook for algorithms.
    *   *Note: Specific page numbers may vary by edition, but look for the "String Matching" chapter.*

2.  **GeeksforGeeks - Naive Pattern Searching Algorithm**: A well-explained online resource with clear examples and code implementations in various languages. It's excellent for beginners.
    *   [https://www.geeksforgeeks.org/naive-algorithm-for-pattern-searching/](https://www.geeksforgeeks.org/naive-algorithm-for-pattern-searching/)

3.  **Wikipedia - String-searching algorithm**: Provides a good overview of various string-searching algorithms, including Naive String Matching, with links to more detailed explanations.
    *   [https://en.wikipedia.org/wiki/String-searching_algorithm](https://en.wikipedia.org/wiki/String-searching_algorithm)