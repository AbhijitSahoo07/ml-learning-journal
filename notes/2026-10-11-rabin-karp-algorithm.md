# Rabin-Karp Algorithm

## Overview
The Rabin-Karp algorithm is a string-searching algorithm that uses hashing to find any one of a set of pattern strings in a text. Unlike naive string matching algorithms that compare characters one by one, Rabin-Karp leverages the power of hashing to speed up the search process significantly, especially in its average-case performance. It's particularly efficient when searching for multiple patterns simultaneously. The core idea is to compute a hash value for the pattern and then compare this hash value with the hash values of all possible substrings of the text that have the same length as the pattern. If the hash values match, a character-by-character comparison is performed to confirm an actual match (as hash collisions can occur). The clever part is using a "rolling hash" function, which allows the hash of the next substring to be computed very quickly from the hash of the previous substring, avoiding recomputing the hash from scratch each time.

## What Problem It Solves
The Rabin-Karp algorithm primarily solves the **string matching problem**, also known as **pattern searching**. This problem involves finding all occurrences of a shorter string (the "pattern") within a longer string (the "text").

Consider these challenges:
*   **Inefficiency of Naive Approaches**: A brute-force or naive approach would involve comparing the pattern with every possible substring of the text. If the text has length $N$ and the pattern has length $M$, this would take $O((N-M+1)M)$ time in the worst case, which can be very slow for large texts or patterns.
*   **Large Datasets**: In scenarios involving vast amounts of text data (e.g., genomic sequences, large documents, network traffic logs), efficient pattern searching is crucial.
*   **Multiple Patterns**: Sometimes, you need to find not just one pattern, but a whole set of patterns within a text. Rabin-Karp can be extended to handle this efficiently.

**Why is it needed in machine learning?**
While Rabin-Karp is fundamentally a computer science algorithm, its principles and applications are highly relevant in various machine learning contexts, especially those dealing with text and sequence data:
*   **Text Preprocessing and Feature Engineering**: In Natural Language Processing (NLP), identifying specific keywords, phrases (n-grams), or regular expressions within text documents is a common task. Rabin-Karp can efficiently find these patterns, which can then be used as features for classification, sentiment analysis, or topic modeling.
*   **Plagiarism Detection**: Detecting copied content involves finding identical or highly similar sequences of words or sentences. Rabin-Karp can be used to quickly identify matching blocks of text between documents.
*   **Bioinformatics**: In genomics and proteomics, searching for specific DNA or protein sequences (patterns) within larger biological sequences (text) is a fundamental operation. This is crucial for gene discovery, mutation detection, and understanding protein functions.
*   **Data Deduplication**: Identifying and removing duplicate records or blocks of data in large datasets often relies on finding identical patterns or substrings.
*   **Network Intrusion Detection**: Systems might use Rabin-Karp to quickly scan network packets for known malicious signatures or patterns.

In essence, whenever an ML pipeline involves processing large sequences or text data and requires efficient identification of specific sub-sequences or patterns, algorithms like Rabin-Karp provide a powerful tool for preprocessing, feature extraction, or direct analysis.

## How It Works
The Rabin-Karp algorithm works by using a hash function to efficiently compare substrings of the text with the pattern. Here's a step-by-step breakdown:

1.  **Choose a Hash Function**: The algorithm relies on a polynomial rolling hash function. This function converts a string into an integer hash value. The key property of a rolling hash is that it can be updated very quickly when a character is removed from one end and a new character is added to the other end of a substring.
    *   A common choice is to treat the string as a number in a base-$p$ numeral system, where $p$ is a prime number (e.g., 31 or 53, larger than the number of possible characters).
    *   To keep hash values from becoming too large, calculations are performed modulo a large prime number $m$.

2.  **Compute Pattern Hash**: Calculate the hash value for the given `pattern` string. Let's call this `pattern_hash`.

3.  **Compute Initial Text Substring Hash**: Calculate the hash value for the first substring of the `text` that has the same length as the `pattern`. Let's call this `text_hash`. This substring starts at index 0 and ends at `len(pattern) - 1`.

4.  **Compare Hashes and Verify**:
    *   Compare `pattern_hash` with `text_hash`.
    *   **If they match**: There's a *potential* match. Because hash collisions can occur (different strings can have the same hash value), a character-by-character comparison is necessary to confirm if the actual strings are identical. This is called a "spurious hit" if the hashes match but the strings don't. If the characters match, we've found an occurrence of the pattern.
    *   **If they don't match**: Move to the next step.

5.  **Slide the Window (Rolling Hash)**:
    *   If the current `text_hash` doesn't match `pattern_hash` (or after verifying a match), we need to consider the next substring in the text. This means "sliding" our window one character to the right.
    *   Instead of recomputing the hash for the new substring from scratch (which would be slow), we use the rolling hash property. The hash of the new substring can be efficiently calculated from the hash of the previous substring by:
        *   Subtracting the contribution of the character leaving the window.
        *   Multiplying by the base $p$ to shift the remaining characters.
        *   Adding the contribution of the new character entering the window.
    *   All these operations are performed modulo $m$.

6.  **Repeat**: Continue steps 4 and 5 until the sliding window reaches the end of the `text`.

**Example Walkthrough:**

Text: `ABCCDDAABBC`
Pattern: `AABB`
Pattern Length (M): 4

Let's assume character values: A=1, B=2, C=3, D=4
Prime base $p=5$, Modulus $m=101$ (a large prime)

1.  **Pattern Hash**: `AABB`
    $h(\text{AABB}) = (1 \cdot 5^3 + 1 \cdot 5^2 + 2 \cdot 5^1 + 2 \cdot 5^0) \pmod{101}$
    $h(\text{AABB}) = (1 \cdot 125 + 1 \cdot 25 + 2 \cdot 5 + 2 \cdot 1) \pmod{101}$
    $h(\text{AABB}) = (125 + 25 + 10 + 2) \pmod{101}$
    $h(\text{AABB}) = 162 \pmod{101} = 61$
    So, `pattern_hash = 61`.

2.  **First Window (index 0-3): `ABCC`**
    $h(\text{ABCC}) = (1 \cdot 5^3 + 2 \cdot 5^2 + 3 \cdot 5^1 + 3 \cdot 5^0) \pmod{101}$
    $h(\text{ABCC}) = (125 + 50 + 15 + 3) \pmod{101}$
    $h(\text{ABCC}) = 193 \pmod{101} = 92$
    `text_hash = 92`.
    `pattern_hash (61)` != `text_hash (92)`. No match.

3.  **Slide Window to index 1-4: `BCCD`**
    Previous window: `ABCC` (hash 92)
    Character leaving: `A` (value 1)
    Character entering: `D` (value 4)
    The formula for rolling hash is:
    $h_{new} = ((h_{old} - \text{val}(\text{char_leaving}) \cdot p^{M-1}) \cdot p + \text{val}(\text{char_entering})) \pmod m$
    First, calculate $p^{M-1} = 5^{4-1} = 5^3 = 125$.
    $h_{new} = ((92 - 1 \cdot 125) \cdot 5 + 4) \pmod{101}$
    $h_{new} = ((92 - 125) \cdot 5 + 4) \pmod{101}$
    $h_{new} = (-33 \cdot 5 + 4) \pmod{101}$
    $h_{new} = (-165 + 4) \pmod{101}$
    $h_{new} = -161 \pmod{101}$
    To get a positive result for modulo of negative numbers: $-161 + 2 \cdot 101 = -161 + 202 = 41$.
    So, `text_hash = 41`.
    `pattern_hash (61)` != `text_hash (41)`. No match.

4.  **Slide Window to index 2-5: `CCDD`**
    Previous window: `BCCD` (hash 41)
    Character leaving: `B` (value 2)
    Character entering: `D` (value 4)
    $h_{new} = ((41 - 2 \cdot 125) \cdot 5 + 4) \pmod{101}$
    $h_{new} = ((41 - 250) \cdot 5 + 4) \pmod{101}$
    $h_{new} = (-209 \cdot 5 + 4) \pmod{101}$
    $h_{new} = (-1045 + 4) \pmod{101}$
    $h_{new} = -1041 \pmod{101}$
    $-1041 + 11 \cdot 101 = -1041 + 1111 = 70$.
    So, `text_hash = 70`.
    `pattern_hash (61)` != `text_hash (70)`. No match.

... and so on. This process continues until a hash match is found, followed by character-by-character verification.

Eventually, when the window is `AABB` (at index 6-9):
$h(\text{AABB}) = 61$.
`pattern_hash (61)` == `text_hash (61)`. Potential match!
Verify character by character: `text[6:10]` is `AABB`, which matches `pattern`. Found at index 6.

## Mathematical Intuition
The core of the Rabin-Karp algorithm lies in its clever use of a **polynomial rolling hash function** and **modular arithmetic**.

Let's represent a string $S$ of length $k$ as a sequence of characters $s_0, s_1, \dots, s_{k-1}$. We assign a numerical value to each character (e.g., its ASCII value, or 1 for 'a', 2 for 'b', etc.).

The hash function $h(S)$ for a string $S = s_0s_1\dots s_{k-1}$ is defined as:
$$h(S) = (s_0 p^{k-1} + s_1 p^{k-2} + \dots + s_{k-1} p^0) \pmod m$$
Here:
*   $s_i$ is the numerical value of the $i$-th character of the string.
*   $p$ is a prime number, chosen as the base for the polynomial. It should be larger than the number of possible distinct characters (e.g., 256 for ASCII, or 31/53 for lowercase English letters). A larger prime helps distribute hash values more evenly.
*   $m$ is a large prime number, chosen as the modulus. This keeps the hash values within a manageable range and helps reduce the chance of collisions. A common choice is a large prime like $10^9 + 7$ or $2^{61}-1$.

**Breaking down the equation:**
This formula treats the string as a number in base $p$. For example, if $p=10$ and characters are digits, "123" would be $1 \cdot 10^2 + 2 \cdot 10^1 + 3 \cdot 10^0$. The modulo $m$ is applied to prevent the hash values from growing too large, which would lead to overflow and make comparisons impractical.

**Rolling Hash Intuition:**
The power of Rabin-Karp comes from its ability to compute the hash of the next substring in $O(1)$ time, given the hash of the current substring.

Let's say we have a substring $S_{current} = s_i s_{i+1} \dots s_{i+k-1}$ and its hash $h(S_{current})$.
We want to compute the hash of the next substring $S_{next} = s_{i+1} s_{i+2} \dots s_{i+k}$.

The hash of $S_{current}$ is:
$$h(S_{current}) = (s_i p^{k-1} + s_{i+1} p^{k-2} + \dots + s_{i+k-1} p^0) \pmod m$$

To get $h(S_{next})$, we need to:
1.  **Remove the contribution of the leading character $s_i$**:
    Subtract $s_i p^{k-1}$ from $h(S_{current})$.
    $h_{temp1} = (h(S_{current}) - s_i p^{k-1}) \pmod m$
    *Note: If the result is negative, add $m$ to make it positive: $(h_{temp1} + m) \pmod m$.*

2.  **Shift the remaining characters**:
    Multiply the result by $p$. This effectively shifts $s_{i+1}$ from $p^{k-2}$ to $p^{k-1}$, $s_{i+2}$ from $p^{k-3}$ to $p^{k-2}$, and so on.
    $h_{temp2} = (h_{temp1} \cdot p) \pmod m$

3.  **Add the contribution of the new trailing character $s_{i+k}$**:
    Add $s_{i+k} p^0$ (which is just $s_{i+k}$) to the result.
    $h(S_{next}) = (h_{temp2} + s_{i+k}) \pmod m$

Combining these steps, the rolling hash update formula is:
$$h(S_{next}) = ((h(S_{current}) - s_i p^{k-1}) \cdot p + s_{i+k}) \pmod m$$

**Pre-calculating $p^{k-1}$**:
The term $p^{k-1} \pmod m$ (let's call it `power_p_k_minus_1`) needs to be calculated only once at the beginning. This is because $k$ (pattern length) is constant.
So, the formula becomes:
$$h(S_{next}) = ((h(S_{current}) - s_i \cdot \text{power\_p\_k\_minus\_1}) \cdot p + s_{i+k}) \pmod m$$

**Why modular arithmetic?**
Without modulo $m$, the hash values would quickly become astronomically large, exceeding standard integer data types and making calculations slow or impossible. Modulo arithmetic keeps the hash values within a fixed range $[0, m-1]$.

**Collision Handling:**
It's possible for two different strings to have the same hash value (a hash collision). This is why, when `pattern_hash` matches `text_hash`, a character-by-character comparison (a "verification step") is crucial to confirm a true match and avoid "spurious hits". The choice of large prime $p$ and $m$ helps minimize the probability of collisions.

## Advantages
*   **Average-Case Efficiency**: On average, Rabin-Karp performs very well, with a time complexity of $O(N+M)$, where $N$ is the length of the text and $M$ is the length of the pattern. This is because hash comparisons are $O(1)$, and character-by-character verification is rarely needed if collisions are infrequent.
*   **Simplicity**: The core idea of hashing and rolling hash is relatively straightforward to understand and implement compared to more complex algorithms like KMP.
*   **Multiple Pattern Search**: It can be easily extended to find multiple patterns simultaneously. You can compute hashes for all patterns and store them in a hash table. Then, for each text substring hash, you check if it exists in the set of pattern hashes. This makes it very efficient for finding any of a large number of patterns.
*   **Flexibility in Hash Function**: While polynomial hashing is common, other rolling hash functions can be used depending on the specific application and character set.
*   **Suitable for Large Alphabets**: It works well with large alphabets (e.g., Unicode characters, DNA sequences) as the character values are simply numbers in the hash function.

## Disadvantages
*   **Worst-Case Performance**: In the worst case, if there are many hash collisions (e.g., due to a poorly chosen hash function, or specially crafted input text), the algorithm might degenerate to $O(NM)$ time complexity. This happens if almost every hash match leads to a full character-by-character comparison.
*   **Spurious Hits**: Hash collisions lead to "spurious hits" where hash values match, but the actual strings do not. This necessitates the character-by-character verification step, which adds overhead.
*   **Choice of Hash Parameters**: The performance heavily depends on the choice of the prime base $p$ and the modulus $m$. Poor choices can lead to a high number of collisions and degrade performance.
*   **Not Optimal for Single Pattern**: For searching a single pattern, algorithms like Knuth-Morris-Pratt (KMP) or Boyer-Moore have a guaranteed worst-case time complexity of $O(N+M)$, which is better than Rabin-Karp's potential $O(NM)$ worst case.
*   **Implementation Complexity for Modulo Arithmetic**: Handling negative results from modulo operations (e.g., `(a - b) % m` in some languages can yield negative results if `a < b`) requires careful implementation to ensure correctness.

## Real World Applications
1.  **Plagiarism Detection**: Educational institutions and content platforms use Rabin-Karp to detect plagiarism. By breaking down documents into fixed-size chunks (e.g., sentences or paragraphs) and computing their hashes, it can quickly identify matching or highly similar blocks of text between a submitted document and a vast database of existing works.
2.  **Bioinformatics (DNA/Protein Sequence Matching)**: In computational biology, scientists frequently need to search for specific genetic sequences (patterns) within long DNA or RNA strands (text) or protein sequences. Rabin-Karp can efficiently locate these motifs, which is crucial for identifying genes, regulatory elements, or disease markers.
3.  **Network Intrusion Detection Systems (NIDS)**: NIDS often scan incoming network traffic for known malicious patterns or "signatures" (e.g., specific byte sequences indicating malware, attack commands, or forbidden content). Rabin-Karp can be employed to quickly match these signatures against the stream of network packets, enabling real-time threat detection.
4.  **Data Deduplication and File Synchronization**: Cloud storage services and backup solutions use techniques similar to Rabin-Karp for data deduplication. By hashing blocks of data, they can identify identical blocks and store only one copy, saving storage space. Similarly, for file synchronization, it can quickly determine which parts of a file have changed.
5.  **Text Editors and IDEs (Find/Replace Functionality)**: While often optimized with more advanced algorithms, the core idea of efficiently finding occurrences of a search string within a larger document is a direct application. For simple find operations, especially when searching for multiple terms, Rabin-Karp's principles can be applied.

## Python Example

```python
import random

def rabin_karp_search(text, pattern, prime_base=257, modulus=10**9 + 7):
    """
    Implements the Rabin-Karp algorithm for string matching.

    Args:
        text (str): The main text to search within.
        pattern (str): The pattern string to search for.
        prime_base (int): A prime number used as the base for the hash function.
                          Should be larger than the number of possible characters.
        modulus (int): A large prime number used as the modulus for hash calculations.
                       Helps keep hash values manageable and reduces collisions.

    Returns:
        list: A list of starting indices where the pattern is found in the text.
    """
    n = len(text)
    m = len(pattern)
    
    if m == 0:
        return []
    if n < m:
        return []

    # List to store the starting indices of found patterns
    found_indices = []

    # Calculate (prime_base^(m-1)) % modulus once
    # This is used to remove the leading character's contribution efficiently
    h_power = pow(prime_base, m - 1, modulus)

    # Calculate hash for the pattern
    pattern_hash = 0
    for i in range(m):
        pattern_hash = (pattern_hash * prime_base + ord(pattern[i])) % modulus

    # Calculate hash for the first window of text
    text_hash = 0
    for i in range(m):
        text_hash = (text_hash * prime_base + ord(text[i])) % modulus

    # Slide the window across the text
    for i in range(n - m + 1):
        # If hashes match, perform character-by-character verification
        if pattern_hash == text_hash:
            # Potential match, verify character by character to handle spurious hits
            match = True
            for j in range(m):
                if text[i + j] != pattern[j]:
                    match = False
                    break
            if match:
                found_indices.append(i)

        # Calculate hash for the next window (if not the last window)
        if i < n - m:
            # Remove leading character's contribution
            # Ensure result is positive after subtraction
            text_hash = (text_hash - ord(text[i]) * h_power) % modulus
            if text_hash < 0:
                text_hash += modulus # Ensure positive result

            # Add new trailing character's contribution
            text_hash = (text_hash * prime_base + ord(text[i + m])) % modulus

    return found_indices

# --- Example Usage ---
if __name__ == "__main__":
    # Dummy dataset (text and patterns)
    long_text = (
        "The quick brown fox jumps over the lazy dog. "
        "The dog barks loudly. The fox is quick."
        "This is a test text for the Rabin-Karp algorithm. "
        "We are looking for specific patterns in this text."
        "The quick brown fox is a common phrase."
    )
    
    patterns_to_find = ["fox", "dog", "quick brown", "algorithm", "not_found", "quick brown fox"]

    print(f"Searching in text:\n'{long_text}'\n")

    for pattern in patterns_to_find:
        print(f"Searching for pattern: '{pattern}'")
        
        # Using default prime_base and modulus
        indices = rabin_karp_search(long_text, pattern)
        
        if indices:
            print(f"  Pattern found at indices: {indices}")
            for idx in indices:
                print(f"    Match: '{long_text[idx : idx + len(pattern)]}'")
        else:
            print("  Pattern not found.")
        print("-" * 30)

    # Example with a custom prime_base and modulus
    print("\n--- Custom Hash Parameters Example ---")
    custom_text = "banana"
    custom_pattern = "ana"
    # Using smaller primes for demonstration, but larger primes are better in practice
    custom_prime_base = 11
    custom_modulus = 101 
    
    print(f"Searching in text: '{custom_text}' for pattern: '{custom_pattern}'")
    indices_custom = rabin_karp_search(custom_text, custom_pattern, custom_prime_base, custom_modulus)
    if indices_custom:
        print(f"  Pattern found at indices: {indices_custom}")
        for idx in indices_custom:
            print(f"    Match: '{custom_text[idx : idx + len(custom_pattern)]}'")
    else:
        print("  Pattern not found.")
    print("-" * 30)
```

**Explanation of the Python Code:**

1.  **`rabin_karp_search(text, pattern, prime_base, modulus)` function**:
    *   Takes the `text`, `pattern`, and optional `prime_base` and `modulus` as input.
    *   `n` and `m` store the lengths of the text and pattern, respectively.
    *   Handles edge cases where the pattern is empty or longer than the text.
    *   `found_indices`: A list to store all starting indices where the pattern is found.

2.  **`h_power = pow(prime_base, m - 1, modulus)`**:
    *   This pre-calculates $p^{M-1} \pmod m$. This value is crucial for efficiently removing the contribution of the leading character in the rolling hash. `pow(base, exp, mod)` is a highly efficient built-in Python function for modular exponentiation.

3.  **Initial Hash Calculation (Pattern and First Text Window)**:
    *   `pattern_hash` and `text_hash` are computed for the `pattern` and the first `m` characters of the `text`, respectively.
    *   The loop `for i in range(m)` implements the polynomial hash function: `hash = (hash * prime_base + ord(character)) % modulus`. `ord(character)` converts a character to its ASCII integer value.

4.  **Sliding Window Loop (`for i in range(n - m + 1)`)**:
    *   This loop iterates through all possible starting positions `i` for the pattern in the text.
    *   **Hash Comparison**: `if pattern_hash == text_hash:`
        *   If the hashes match, it's a *potential* match.
        *   **Verification**: A nested loop `for j in range(m)` performs a character-by-character comparison (`text[i + j] != pattern[j]`). This is essential to rule out "spurious hits" (hash collisions).
        *   If the verification confirms a true match, the index `i` is added to `found_indices`.

    *   **Rolling Hash Update (`if i < n - m`)**:
        *   This block executes for all windows except the very last one.
        *   `text_hash = (text_hash - ord(text[i]) * h_power) % modulus`: Subtracts the contribution of the character leaving the window (`text[i]`).
        *   `if text_hash < 0: text_hash += modulus`: Ensures the hash remains positive, as Python's `%` operator can return negative results for negative numbers.
        *   `text_hash = (text_hash * prime_base + ord(text[i + m])) % modulus`: Multiplies by `prime_base` to shift existing characters and adds the contribution of the new character entering the window (`text[i + m]`).

5.  **Return `found_indices`**: The function returns the list of all starting positions where the pattern was found.

The example usage demonstrates how to call the function with various patterns, including one that isn't found, and also shows how to customize the hash parameters.

## Interview Questions

1.  **What is the Rabin-Karp algorithm, and what problem does it solve?**
    *   **Answer:** Rabin-Karp is a string-searching algorithm that finds occurrences of a pattern string within a larger text string. It solves the string matching problem by using hashing to efficiently compare substrings of the text with the pattern.

2.  **How does Rabin-Karp use hashing to improve efficiency over a naive string search?**
    *   **Answer:** Instead of comparing characters one by one for every possible substring, Rabin-Karp computes a hash value for the pattern and for each substring of the text. Hash comparisons are much faster ($O(1)$) than character-by-character comparisons ($O(M)$). Only when hash values match does it perform a full character-by-character verification, significantly reducing the number of expensive comparisons.

3.  **Explain the concept of a "rolling hash" in Rabin-Karp.**
    *   **Answer:** A rolling hash is a hash function that allows you to compute the hash of the next substring in $O(1)$ time, given the hash of the current substring. Instead of recomputing the hash from scratch for each new window, it efficiently updates the hash by subtracting the contribution of the character leaving the window, shifting the remaining characters (by multiplying by the base), and adding the contribution of the new character entering the window.

4.  **What is a "spurious hit" in Rabin-Karp, and how is it handled?**
    *   **Answer:** A spurious hit (or hash collision) occurs when the hash value of a text substring matches the hash value of the pattern, but the actual strings are different. This happens because different strings can sometimes produce the same hash value. Rabin-Karp handles spurious hits by performing a character-by-character comparison (verification step) whenever a hash match occurs. If the strings don't match after verification, it's a spurious hit, and the algorithm continues searching.

5.  **What is the time complexity of Rabin-Karp in the average and worst cases?**
    *   **Answer:**
        *   **Average Case:** $O(N+M)$, where $N$ is the length of the text and $M$ is the length of the pattern. This is because hash computations and updates are $O(1)$, and character-by-character verification is rarely needed due to infrequent collisions.
        *   **Worst Case:** $O(NM)$. This occurs when there are many hash collisions, forcing the algorithm to perform character-by-character verification for almost every possible substring. This can happen with poorly chosen hash parameters or specially crafted inputs.

6.  **What factors influence the choice of the prime base ($p$) and modulus ($m$) in the hash function?**
    *   **Answer:**
        *   **Prime Base ($p$):** Should be a prime number larger than the size of the alphabet (e.g., >256 for ASCII). A larger prime helps distribute hash values more evenly, reducing collisions.
        *   **Modulus ($m$):** Should be a large prime number. A large modulus reduces the probability of hash collisions and helps keep hash values within a manageable range, preventing integer overflow. Common choices are $10^9 + 7$ or $2^{61}-1$.

7.  **Compare Rabin-Karp with the Knuth-Morris-Pratt (KMP) algorithm.**
    *   **Answer:**
        *   **Rabin-Karp:** Uses hashing and rolling hash. Average case $O(N+M)$, worst case $O(NM)$. Simpler to implement for multiple patterns.
        *   **KMP:** Uses a precomputed "LPS array" (Longest Prefix Suffix) to avoid re-scanning characters. Guaranteed worst-case $O(N+M)$. More complex to implement, typically for single pattern search.
        *   **Preference:** Rabin-Karp is often preferred for multiple pattern searches or when average-case performance is acceptable. KMP is preferred when a guaranteed optimal worst-case performance for a single pattern is critical.

8.  **Can Rabin-Karp be used to find multiple patterns simultaneously? If so, how?**
    *   **Answer:** Yes, Rabin-Karp is very efficient for finding multiple patterns simultaneously. You would compute the hash for each pattern and store these pattern hashes in a hash set (or hash table). Then, as you slide the window through the text and compute the hash of each text substring, you simply check if this `text_hash` exists in your set of `pattern_hashes`. If it does, you perform the character-by-character verification against all patterns that share that hash.

9.  **What are the space complexity requirements of Rabin-Karp?**
    *   **Answer:** The space complexity is $O(M)$ for storing the pattern and its hash, and $O(1)$ for storing the current text substring's hash. If searching for multiple patterns, it would be $O(\sum M_i)$ to store all pattern hashes, where $M_i$ is the length of each pattern.

10. **In what real-world scenarios would you choose Rabin-Karp over other string matching algorithms?**
    *   **Answer:** Rabin-Karp is a good choice for:
        *   **Plagiarism detection:** Comparing large documents for matching blocks of text.
        *   **Bioinformatics:** Searching for specific DNA/protein sequences in large genomic data.
        *   **Network intrusion detection:** Scanning network traffic for known malicious signatures.
        *   **Data deduplication:** Identifying duplicate data blocks in storage systems.
        *   Any scenario where finding *any* of a large set of patterns is required, or where average-case $O(N+M)$ performance is sufficient and worst-case $O(NM)$ is unlikely due to good hash parameter choices.

## Quiz

1.  **What is the primary technique used by the Rabin-Karp algorithm to speed up string matching?**
    A) Suffix trees
    B) Finite automata
    C) Hashing and rolling hash
    D) Dynamic programming

2.  **Which of the following best describes a "spurious hit" in Rabin-Karp?**
    A) When the pattern is found in the text.
    B) When the hash of a text substring matches the pattern's hash, but the actual strings are different.
    C) When the algorithm fails to find a pattern that exists.
    D) When the hash function produces a negative value.

3.  **What is the average-case time complexity of the Rabin-Karp algorithm for searching a pattern of length $M$ in a text of length $N$?**
    A) $O(NM)$
    B) $O(N+M)$
    C) $O(N \log M)$
    D) $O(M \log N)$

4.  **How does the rolling hash function update the hash for the next window in Rabin-Karp?**
    A) It recomputes the hash for the entire new window from scratch.
    B) It only adds the hash of the new character entering the window.
    C) It subtracts the contribution of the leaving character, shifts the remaining hash, and adds the contribution of the entering character.
    D) It uses a lookup table to find the next hash value.

5.  **Which of these is a significant advantage of Rabin-Karp, especially compared to KMP?**
    A) Guaranteed $O(N+M)$ worst-case time complexity.
    B) Simpler implementation for single pattern search.
    C) Efficiently finds multiple patterns simultaneously.
    D) Does not require character-by-character verification.

---

### Answer Key

1.  **C) Hashing and rolling hash**
    *   **Explanation:** Rabin-Karp's efficiency comes from converting strings to hash values and using a rolling hash to update these values quickly, avoiding repeated full string comparisons.

2.  **B) When the hash of a text substring matches the pattern's hash, but the actual strings are different.**
    *   **Explanation:** This is the definition of a hash collision in the context of string matching, which Rabin-Karp handles by performing a character-by-character verification.

3.  **B) $O(N+M)$**
    *   **Explanation:** In the average case, with a good hash function and few collisions, hash comparisons are $O(1)$, leading to an overall $O(N+M)$ complexity.

4.  **C) It subtracts the contribution of the leaving character, shifts the remaining hash, and adds the contribution of the entering character.**
    *   **Explanation:** This is the core mechanism of a polynomial rolling hash, allowing $O(1)$ updates for the next window's hash.

5.  **C) Efficiently finds multiple patterns simultaneously.**
    *   **Explanation:** Rabin-Karp can easily be extended to search for a set of patterns by storing all pattern hashes in a hash set and checking each text substring's hash against this set. KMP is typically optimized for single pattern search.

## Further Reading

1.  **Introduction to Algorithms (CLRS)**: Chapter 32, "String Matching," specifically the section on the Rabin-Karp algorithm. This is a classic textbook and provides a rigorous mathematical treatment.
    *   *Resource:* Often available in university libraries or for purchase.
2.  **GeeksforGeeks - Rabin-Karp Algorithm**: A highly detailed and beginner-friendly explanation with code examples in various languages.
    *   *Link:* [https://www.geeksforgeeks.org/rabin-karp-algorithm-for-pattern-searching/](https://www.geeksforgeeks.org/rabin-karp-algorithm-for-pattern-searching/)
3.  **Wikipedia - Rabin-Karp Algorithm**: Provides a good overview, historical context, and links to related concepts.
    *   *Link:* [https://en.wikipedia.org/wiki/Rabin%E2%80%93Karp_algorithm](https://en.wikipedia.org/wiki/Rabin%E2%80%93Karp_algorithm)