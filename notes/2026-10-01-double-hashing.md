# Double Hashing

## Overview
Hashing is a fundamental technique in computer science used to map data of arbitrary size to fixed-size values, typically integers, which serve as indices in an array (a hash table). This allows for very fast data retrieval, insertion, and deletion, ideally in $O(1)$ average time complexity. However, a perfect hash function that maps every unique key to a unique index is rare, especially with a finite-sized hash table. When two different keys map to the same index, it's called a **collision**.

**Double Hashing** is an advanced and highly effective collision resolution technique used in hash tables. When a collision occurs, instead of simply looking at the next available slot (like linear probing) or using a quadratic step (like quadratic probing), Double Hashing uses a *second independent hash function* to determine the step size for probing. This approach aims to generate a more uniform and diverse sequence of probe locations, significantly reducing the problem of "clustering" that plagues simpler collision resolution methods. It's a powerful method for maintaining the efficiency of hash tables even under high load factors.

## What Problem It Solves
Double Hashing primarily addresses the inefficiencies and performance degradation caused by **collisions** in hash tables, specifically targeting two types of clustering:

1.  **Primary Clustering**: This problem is most evident in **linear probing**. When a collision occurs with linear probing, the algorithm simply searches for the next empty slot sequentially (e.g., index $i+1, i+2, i+3, \dots$). If many keys hash to the same general area, or if a few collisions occur close to each other, they form long "runs" or clusters of occupied slots. Subsequent insertions or searches in this area become very slow, as they have to traverse these long clusters. Double Hashing avoids this by not using a fixed step size.

2.  **Secondary Clustering**: This issue arises in techniques like **quadratic probing**. While quadratic probing (probing at $i+1^2, i+2^2, i+3^2, \dots$) helps mitigate primary clustering by spreading out probes, it introduces a new problem: secondary clustering. If two *different* keys initially hash to the *same* index $h_1(key_1) = h_1(key_2)$, they will follow the *exact same sequence* of probe locations. This means they effectively "collide" repeatedly, leading to similar performance issues as primary clustering, just with a different pattern. Double Hashing solves this by using a *second hash function* that depends on the *key itself*, not just the initial hash index. This ensures that even if two keys hash to the same initial index, their *second hash values* (and thus their probe sequences) will likely be different.

In essence, Double Hashing is needed to maintain the near $O(1)$ average-case performance of hash tables by ensuring that probe sequences are as independent and uniformly distributed as possible, even when collisions are frequent.

## How It Works
Double Hashing works by employing two distinct hash functions, $h_1(key)$ and $h_2(key)$, to determine the probe sequence when a collision occurs. Here's a step-by-step breakdown:

1.  **Initial Hash Calculation**:
    *   When you want to insert a `key` (or search for it), the first step is to calculate its initial hash index using the primary hash function, $h_1(key)$.
    *   Let's say the hash table has `M` slots. A common choice for $h_1(key)$ is $key \pmod M$.
    *   The calculated index is $idx = h_1(key)$.

2.  **Check for Collision**:
    *   Check if the slot at $idx$ in the hash table is empty.
    *   If it's empty, the `key` can be inserted (or found) there. The process stops.

3.  **Calculate Step Size (Second Hash Function)**:
    *   If the slot at $idx$ is *occupied* (a collision), we need to find an alternative slot. Instead of a fixed step (linear probing) or a quadratically increasing step (quadratic probing), we calculate a *dynamic step size* using a second hash function, $h_2(key)$.
    *   The value returned by $h_2(key)$ determines how many steps we take from the current position to find the next potential slot.
    *   Crucially, $h_2(key)$ must *never* return zero, as a zero step size would mean we repeatedly check the same occupied slot forever. Also, $h_2(key)$ should ideally be relatively prime to the table size `M` to ensure that all slots in the table can eventually be visited if needed. A common choice for $h_2(key)$ is $R - (key \pmod R)$, where $R$ is a prime number smaller than `M`.

4.  **Probe Sequence Generation**:
    *   The sequence of probe locations is generated using the formula:
        $$(h_1(key) + i \cdot h_2(key)) \pmod M$$
        where:
        *   $h_1(key)$ is the initial hash index.
        *   $h_2(key)$ is the step size calculated by the second hash function.
        *   $i$ is the probe attempt number, starting from $0$ for the initial hash, then $1, 2, 3, \dots$ for subsequent probes.
        *   $M$ is the size of the hash table.

5.  **Iterative Probing**:
    *   For $i=0$, we check $(h_1(key) + 0 \cdot h_2(key)) \pmod M = h_1(key) \pmod M$. This is the initial slot.
    *   If occupied, for $i=1$, we check $(h_1(key) + 1 \cdot h_2(key)) \pmod M$.
    *   If occupied, for $i=2$, we check $(h_1(key) + 2 \cdot h_2(key)) \pmod M$.
    *   This process continues, incrementing $i$, until an empty slot is found for insertion, or the key is found during a search, or all possible slots have been checked (indicating the table is full or the key is not present).

**Example**:
Let's say we have a hash table of size $M=10$.
Our hash functions are:
$h_1(key) = key \pmod{10}$
$h_2(key) = 7 - (key \pmod 7)$ (where 7 is a prime smaller than 10)

Suppose we want to insert `key = 12`.
1.  $h_1(12) = 12 \pmod{10} = 2$.
2.  Let's say slot `2` is *occupied*.
3.  Calculate $h_2(12) = 7 - (12 \pmod 7) = 7 - 5 = 2$. So, our step size is 2.
4.  Probe sequence:
    *   $i=0$: $(2 + 0 \cdot 2) \pmod{10} = 2$. (Occupied)
    *   $i=1$: $(2 + 1 \cdot 2) \pmod{10} = 4$. (Let's say slot `4` is *occupied*)
    *   $i=2$: $(2 + 2 \cdot 2) \pmod{10} = 6$. (Let's say slot `6` is *occupied*)
    *   $i=3$: $(2 + 3 \cdot 2) \pmod{10} = 8$. (Let's say slot `8` is *empty`). Insert `12` at index `8`.

Now, suppose we want to insert `key = 22`.
1.  $h_1(22) = 22 \pmod{10} = 2$. (Initial collision with `12`'s original spot)
2.  Slot `2` is occupied.
3.  Calculate $h_2(22) = 7 - (22 \pmod 7) = 7 - 1 = 6$. So, our step size is 6.
4.  Probe sequence:
    *   $i=0$: $(2 + 0 \cdot 6) \pmod{10} = 2$. (Occupied)
    *   $i=1$: $(2 + 1 \cdot 6) \pmod{10} = 8$. (Occupied by `12`)
    *   $i=2$: $(2 + 2 \cdot 6) \pmod{10} = (2 + 12) \pmod{10} = 14 \pmod{10} = 4$. (Occupied)
    *   $i=3$: $(2 + 3 \cdot 6) \pmod{10} = (2 + 18) \pmod{10} = 20 \pmod{10} = 0$. (Let's say slot `0` is *empty`). Insert `22` at index `0`.

Notice how `12` and `22` both initially hash to index `2`, but they follow completely different probe sequences (`2, 4, 6, 8, ...` for `12` and `2, 8, 4, 0, ...` for `22`) because their $h_2$ values are different. This is the power of Double Hashing in preventing secondary clustering.

## Mathematical Intuition
The core mathematical idea behind Double Hashing lies in generating a unique and comprehensive probe sequence for each key, independent of other keys' initial hash values.

Let $M$ be the size of the hash table.
The general formula for the $i$-th probe location for a given $key$ is:
$$h(key, i) = (h_1(key) + i \cdot h_2(key)) \pmod M$$
where:
*   $h_1(key)$ is the primary hash function, which maps the key to an initial index in the range $[0, M-1]$. A common choice is $h_1(key) = key \pmod M$.
*   $h_2(key)$ is the secondary hash function, which determines the step size for probing. This function must satisfy two critical properties:
    1.  **$h_2(key) \neq 0$**: The step size must never be zero. If $h_2(key)$ were zero, then for any $i > 0$, the probe location would always be $h_1(key)$, leading to an infinite loop if $h_1(key)$ is occupied.
    2.  **$h_2(key)$ must be relatively prime to $M$**: This means that the greatest common divisor (GCD) of $h_2(key)$ and $M$ must be 1, i.e., $\text{gcd}(h_2(key), M) = 1$. This property is crucial because it guarantees that the probe sequence will eventually visit *every single slot* in the hash table before repeating. If $\text{gcd}(h_2(key), M) > 1$, the probe sequence would only visit $M / \text{gcd}(h_2(key), M)$ slots, potentially failing to find an empty slot even if the table is not full.

**Common choices for $h_2(key)$ to satisfy these properties:**

*   **If $M$ is a prime number**:
    A simple and effective choice for $h_2(key)$ is $h_2(key) = 1 + (key \pmod{M-1})$.
    *   This ensures $h_2(key)$ is always between $1$ and $M-1$.
    *   Since $M$ is prime, any number between $1$ and $M-1$ will be relatively prime to $M$.
    *   Thus, both conditions are met.

*   **If $M$ is a power of 2 (e.g., $M = 2^k$)**:
    This is generally not recommended for double hashing because it's hard to guarantee $\text{gcd}(h_2(key), M) = 1$ unless $h_2(key)$ is always odd.
    However, if $M$ is a power of 2, one could choose $h_2(key)$ to always produce an odd number. For example, $h_2(key) = (\text{some\_other\_hash}(key) \pmod{M/2}) \cdot 2 + 1$.

*   **General case (most common and robust)**:
    Choose $M$ to be a prime number. Then, choose a prime number $R$ that is smaller than $M$ (e.g., $R = M-2$ if $M-2$ is prime, or the largest prime less than $M$).
    Then, $h_2(key) = R - (key \pmod R)$.
    *   This ensures $h_2(key)$ is in the range $[1, R]$.
    *   Since $R < M$ and $M$ is prime, $h_2(key)$ will be relatively prime to $M$ (unless $h_2(key)$ happens to be $M$ itself, which is impossible here).
    *   This method is widely used because it's simple and effective.

The mathematical beauty of double hashing lies in its ability to generate a pseudo-random sequence of probes for each key. By combining two hash functions, it creates a unique "stride" for each key, making the probe sequence dependent on the key's value in two different ways. This significantly reduces the chances of different keys following the same probe path, thereby minimizing clustering and maintaining the efficiency of the hash table.

## Advantages
*   **Reduces Primary Clustering**: Unlike linear probing, the step size is not fixed at 1. Each key gets a unique step size, preventing the formation of long contiguous blocks of occupied slots.
*   **Reduces Secondary Clustering**: Unlike quadratic probing, keys that initially hash to the same index ($h_1(key_1) = h_1(key_2)$) will likely have different second hash values ($h_2(key_1) \neq h_2(key_2)$). This means they will follow completely different probe sequences, avoiding the problem where identical initial hashes lead to identical probe paths.
*   **Better Performance**: On average, double hashing requires fewer probes to find an empty slot or a target key compared to linear or quadratic probing, especially as the hash table approaches its capacity (higher load factors). This leads to faster insertion, search, and deletion operations.
*   **More Uniform Probe Sequences**: The combination of two hash functions creates a more diverse and uniformly distributed set of probe sequences across the hash table, making better use of the available space.
*   **Good for High Load Factors**: It performs relatively well even when the hash table is quite full, where linear and quadratic probing would degrade significantly.

## Disadvantages
*   **Requires Two Hash Functions**: Implementing double hashing is more complex as it necessitates the design and implementation of two distinct hash functions, $h_1$ and $h_2$.
*   **Careful Selection of $h_2(key)$**: The second hash function $h_2(key)$ must be chosen carefully to ensure it never returns zero and is relatively prime to the hash table size $M$. A poor choice can lead to infinite loops or failure to find an empty slot even when one exists.
*   **Increased Computation**: Calculating two hash functions for every probe attempt (in the worst case) can be slightly more computationally intensive than calculating a single hash function and then simple arithmetic for linear or quadratic probing. However, this overhead is usually negligible compared to the benefits of reduced probes.
*   **Potential for Poor Performance with Bad Hash Functions**: If the two hash functions are not well-designed (e.g., they are correlated or produce many collisions themselves), the benefits of double hashing can be diminished.
*   **Deletion Complexity**: Deleting items from an open-addressed hash table (including double hashing) can be tricky. Simply removing an item can break the probe sequence for other items that might have passed through that slot. This often requires marking slots as "deleted" rather than truly emptying them, which adds complexity and can degrade search performance over time if not handled with periodic re-hashing.

## Real World Applications
Double Hashing, as a robust collision resolution strategy, is primarily used in the implementation of hash tables, which are fundamental data structures across various domains.

1.  **In-Memory Data Structures (Dictionaries/Maps)**:
    Many programming languages' built-in dictionary or map types (like Python's `dict`, Java's `HashMap`, C++'s `std::unordered_map`) use hash tables internally. While the exact collision resolution strategy can vary (some use separate chaining, others open addressing), double hashing is a strong candidate for open addressing implementations due to its efficiency in preventing clustering. These data structures are ubiquitous for fast key-value lookups.

2.  **Compiler Symbol Tables**:
    Compilers use symbol tables to store information about identifiers (variables, functions, classes) defined in a program. Hash tables are an excellent choice for symbol tables because they allow for very fast insertion and lookup of symbols, which are critical operations during compilation. Double hashing helps ensure that symbol lookup remains efficient even with a large number of symbols.

3.  **Caching Systems**:
    Caches (e.g., CPU caches, web caches, database caches) store frequently accessed data to speed up retrieval. Hash tables are often used to map keys (like memory addresses, URLs, or query IDs) to their cached values. Efficient collision resolution like double hashing is vital to ensure quick access to cached items and minimize cache misses, which can significantly impact performance.

4.  **Database Indexing**:
    While B-trees are more common for disk-based database indexing due to their disk-friendly structure, hash indexes are used in specific scenarios, especially for in-memory databases or for exact-match lookups where data distribution is uniform. Hash tables with double hashing can provide extremely fast access to records given a key, making them suitable for certain types of database queries.

5.  **Network Routers and Firewalls**:
    Network devices like routers and firewalls often use hash tables to store routing tables, access control lists (ACLs), or connection tracking information. Fast lookups are essential for processing network packets at high speeds. Double hashing can contribute to the efficiency of these lookups, ensuring that network traffic is handled without significant delays.

## Python Example
Here's a Python example demonstrating a simple hash table implementation using Double Hashing for collision resolution. We'll use a prime number for the table size to simplify the $h_2(key)$ function.

```python
import numpy as np

class DoubleHashingHashTable:
    def __init__(self, size):
        """
        Initializes a hash table with a given size using double hashing.
        The size should ideally be a prime number for better performance.
        """
        self.size = size
        self.table = [None] * size
        self.num_elements = 0
        # A prime number smaller than self.size for the second hash function
        # For simplicity, we'll pick a fixed prime. In a real scenario,
        # you might find the largest prime less than self.size.
        self.R = self._get_largest_prime_less_than(size)
        if self.R is None:
            raise ValueError("Could not find a suitable prime R for the given size.")

    def _is_prime(self, n):
        """Helper to check if a number is prime."""
        if n < 2:
            return False
        for i in range(2, int(np.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    def _get_largest_prime_less_than(self, n):
        """Finds the largest prime number less than n."""
        for i in range(n - 1, 1, -1):
            if self._is_prime(i):
                return i
        return None # Should not happen for reasonable n

    def _hash1(self, key):
        """Primary hash function: key % table_size"""
        return key % self.size

    def _hash2(self, key):
        """
        Secondary hash function: R - (key % R)
        Ensures step size is non-zero and relatively prime to self.size
        (assuming self.size is prime and R < self.size).
        """
        # Ensure h2(key) is never 0. If key % R == 0, then R - 0 = R.
        # If R is prime and self.size is prime, and R < self.size,
        # then R is relatively prime to self.size.
        return self.R - (key % self.R)

    def insert(self, key, value):
        """Inserts a key-value pair into the hash table."""
        if self.num_elements == self.size:
            print(f"Hash table is full. Cannot insert {key}.")
            return

        initial_index = self._hash1(key)
        step_size = self._hash2(key)

        for i in range(self.size): # Iterate up to self.size probes
            current_index = (initial_index + i * step_size) % self.size

            if self.table[current_index] is None: # Found an empty slot
                self.table[current_index] = (key, value)
                self.num_elements += 1
                print(f"Inserted ({key}, {value}) at index {current_index} after {i+1} probes.")
                return
            elif self.table[current_index][0] == key: # Key already exists, update value
                self.table[current_index] = (key, value)
                print(f"Updated key {key} at index {current_index} after {i+1} probes.")
                return
        
        # This part should ideally not be reached if the table is not full
        # and h2 is chosen correctly to visit all slots.
        print(f"Failed to insert {key}. Table might be full or probe sequence exhausted.")


    def search(self, key):
        """Searches for a key in the hash table and returns its value."""
        initial_index = self._hash1(key)
        step_size = self._hash2(key)

        for i in range(self.size):
            current_index = (initial_index + i * step_size) % self.size

            if self.table[current_index] is None: # Empty slot, key not found
                print(f"Key {key} not found after {i+1} probes (encountered empty slot).")
                return None
            elif self.table[current_index][0] == key: # Key found
                print(f"Key {key} found at index {current_index} after {i+1} probes. Value: {self.table[current_index][1]}")
                return self.table[current_index][1]
        
        print(f"Key {key} not found after exhausting all probes.")
        return None

    def delete(self, key):
        """
        Deletes a key from the hash table.
        In open addressing, deletion is tricky. We mark the slot as 'deleted'
        instead of None, to not break probe sequences for other elements.
        A special 'DELETED' marker is used.
        """
        DELETED = "DELETED_MARKER" # A unique object to mark deleted slots

        initial_index = self._hash1(key)
        step_size = self._hash2(key)

        for i in range(self.size):
            current_index = (initial_index + i * step_size) % self.size

            if self.table[current_index] is None: # Empty slot, key not found
                print(f"Cannot delete {key}: not found after {i+1} probes.")
                return False
            elif self.table[current_index] == DELETED: # Skip deleted slots
                continue
            elif self.table[current_index][0] == key: # Key found, mark as deleted
                self.table[current_index] = DELETED
                self.num_elements -= 1
                print(f"Deleted key {key} from index {current_index} after {i+1} probes.")
                return True
        
        print(f"Cannot delete {key}: not found after exhausting all probes.")
        return False

    def display(self):
        """Prints the current state of the hash table."""
        print("\n--- Hash Table State ---")
        for i, item in enumerate(self.table):
            if item == "DELETED_MARKER":
                print(f"Index {i}: DELETED")
            else:
                print(f"Index {i}: {item}")
        print(f"Number of elements: {self.num_elements}/{self.size}")
        print("------------------------")

# --- Demonstration ---
if __name__ == "__main__":
    # Choose a prime size for the hash table
    table_size = 11 # A prime number

    print(f"Initializing Double Hashing Hash Table with size {table_size}")
    ht = DoubleHashingHashTable(table_size)
    print(f"Second hash function prime R: {ht.R}")

    # Insert some key-value pairs
    print("\n--- Inserting elements ---")
    ht.insert(10, "Apple") # h1(10)=10, h2(10)=7-(10%7)=7-3=4
    ht.insert(21, "Banana") # h1(21)=10, h2(21)=7-(21%7)=7-0=7
    ht.insert(32, "Cherry") # h1(32)=10, h2(32)=7-(32%7)=7-4=3
    ht.insert(1, "Date")   # h1(1)=1, h2(1)=7-(1%7)=7-1=6
    ht.insert(12, "Elderberry") # h1(12)=1, h2(12)=7-(12%7)=7-5=2
    ht.insert(23, "Fig")    # h1(23)=1, h2(23)=7-(23%7)=7-2=5
    ht.insert(44, "Grape")  # h1(44)=0, h2(44)=7-(44%7)=7-2=5

    ht.display()

    # Search for elements
    print("\n--- Searching elements ---")
    ht.search(10)
    ht.search(21)
    ht.search(32)
    ht.search(1)
    ht.search(12)
    ht.search(23)
    ht.search(44)
    ht.search(99) # Not present

    # Demonstrate updating a key
    print("\n--- Updating an element ---")
    ht.insert(10, "Apricot") # Update Apple to Apricot
    ht.display()
    ht.search(10)

    # Demonstrate deletion
    print("\n--- Deleting elements ---")
    ht.delete(21) # Delete Banana
    ht.delete(1)  # Delete Date
    ht.delete(99) # Try to delete non-existent key
    ht.display()

    # Search for a deleted key and an existing key that might have passed through a deleted slot
    print("\n--- Searching after deletion ---")
    ht.search(21) # Should not be found
    ht.search(32) # Should still be found, even if it passed through 21's original spot
    ht.search(12) # Should still be found

    # Insert more elements to fill up and test collision with DELETED marker
    print("\n--- Inserting more elements ---")
    ht.insert(55, "Honeydew") # h1(55)=0, h2(55)=7-(55%7)=7-6=1
    ht.insert(66, "Iceberg")  # h1(66)=0, h2(66)=7-(66%7)=7-3=4
    ht.insert(77, "Jalapeno") # h1(77)=0, h2(77)=7-(77%7)=7-0=7
    ht.insert(88, "Kiwi")     # h1(88)=0, h2(88)=7-(88%7)=7-4=3

    ht.display()

    # Try to insert into a full table
    print("\n--- Attempting to insert into a full table ---")
    ht.insert(99, "Lemon") # Table should be full now
    ht.display()
```

**Explanation of the Python Code:**

1.  **`DoubleHashingHashTable` Class**:
    *   `__init__(self, size)`: Initializes the hash table with a list of `None`s. `size` should ideally be a prime number. It also calculates `R`, a prime number smaller than `size`, which is crucial for the `_hash2` function.
    *   `_is_prime(self, n)` and `_get_largest_prime_less_than(self, n)`: Helper methods to find a suitable prime `R`.
    *   `_hash1(self, key)`: The primary hash function, simply `key % self.size`.
    *   `_hash2(self, key)`: The secondary hash function, `self.R - (key % self.R)`. This ensures the step size is never zero and is relatively prime to `self.size` (given `self.size` is prime and `self.R < self.size`).
    *   `insert(self, key, value)`:
        *   Calculates `initial_index` using `_hash1` and `step_size` using `_hash2`.
        *   It then enters a loop, probing `self.size` times (maximum possible probes).
        *   `current_index = (initial_index + i * step_size) % self.size` calculates the next probe location.
        *   If the slot is `None` or contains a `DELETED_MARKER`, the key-value pair is inserted.
        *   If the key already exists, its value is updated.
    *   `search(self, key)`:
        *   Similar to `insert`, it calculates `initial_index` and `step_size`.
        *   It probes through the sequence. If it finds `None`, the key is not in the table. If it finds the `DELETED_MARKER`, it continues probing. If it finds the key, it returns the value.
    *   `delete(self, key)`:
        *   Deletion in open addressing is complex. Instead of setting a slot to `None`, which could break the search path for other elements that collided and probed past this slot, we mark it with a special `DELETED_MARKER`. This allows searches to continue past deleted slots.
    *   `display(self)`: A utility function to print the current state of the hash table.

2.  **Demonstration (`if __name__ == "__main__":`)**:
    *   Creates a hash table of size 11 (a prime number).
    *   Inserts several key-value pairs, demonstrating how collisions are resolved using different step sizes. Notice how keys 10, 21, 32 all initially hash to index 10, but get placed at different locations due to their unique `h2` values. Similarly for 1, 12, 23.
    *   Demonstrates searching for existing and non-existent keys.
    *   Shows how updating a key works.
    *   Illustrates the deletion process using the `DELETED_MARKER` and how subsequent searches still work correctly.
    *   Finally, attempts to insert into a full table.

This example provides a practical understanding of how Double Hashing functions in a real (albeit simplified) hash table implementation.

## Interview Questions

1.  **What is Double Hashing and how does it differ from other open addressing collision resolution techniques?**
    *   **Answer**: Double Hashing is an open addressing collision resolution technique that uses two independent hash functions, $h_1(key)$ and $h_2(key)$. When a collision occurs at $h_1(key)$, subsequent probe locations are determined by adding multiples of $h_2(key)$ to the initial hash: $(h_1(key) + i \cdot h_2(key)) \pmod M$.
    *   It differs from:
        *   **Linear Probing**: Which uses a fixed step size of 1 (i.e., $(h_1(key) + i) \pmod M$). This leads to primary clustering.
        *   **Quadratic Probing**: Which uses a quadratically increasing step size (i.e., $(h_1(key) + i^2) \pmod M$). This avoids primary clustering but suffers from secondary clustering, where keys with the same initial hash follow the exact same probe sequence.
    *   Double Hashing avoids both primary and secondary clustering by generating a unique probe sequence for each key, even if they initially hash to the same location, because $h_2(key)$ depends on the key itself.

2.  **What are the two critical requirements for the second hash function, $h_2(key)$, in Double Hashing?**
    *   **Answer**:
        1.  **$h_2(key)$ must never return zero**: If $h_2(key)$ were zero, the probe sequence would always return to the initial $h_1(key)$ index, leading to an infinite loop if that slot is occupied.
        2.  **$h_2(key)$ must be relatively prime to the hash table size $M$**: This means $\text{gcd}(h_2(key), M) = 1$. This property guarantees that the probe sequence will eventually visit every slot in the hash table before repeating, ensuring that an empty slot can always be found if the table is not full.

3.  **Explain primary and secondary clustering. How does Double Hashing address these issues?**
    *   **Answer**:
        *   **Primary Clustering**: Occurs in linear probing when collisions cause long "runs" of occupied slots. New insertions or searches in these areas become slow as they have to traverse these clusters. Double Hashing avoids this because the step size ($h_2(key)$) is not fixed at 1; it varies for each key, breaking up these runs.
        *   **Secondary Clustering**: Occurs in quadratic probing when keys that hash to the same initial index ($h_1(key)$) follow the exact same probe sequence. Double Hashing addresses this by using $h_2(key)$, which depends on the key itself. Even if $h_1(key_1) = h_1(key_2)$, it's highly probable that $h_2(key_1) \neq h_2(key_2)$, leading to different probe sequences for $key_1$ and $key_2$.

4.  **Provide an example of suitable hash functions $h_1(key)$ and $h_2(key)$ for a hash table of size $M$.**
    *   **Answer**:
        *   Let $M$ be a prime number (e.g., $M=11$).
        *   **$h_1(key) = key \pmod M$** (e.g., $h_1(key) = key \pmod{11}$).
        *   **$h_2(key) = R - (key \pmod R)$**, where $R$ is a prime number smaller than $M$ (e.g., $R=7$). So, $h_2(key) = 7 - (key \pmod 7)$.
        *   This choice for $h_2(key)$ ensures it's always between 1 and $R$, and since $R < M$ and $M$ is prime, $h_2(key)$ will be relatively prime to $M$.

5.  **What are the time complexities for insertion, search, and deletion in a well-designed Double Hashing hash table?**
    *   **Answer**:
        *   **Average Case**: $O(1)$. With good hash functions and a reasonable load factor, operations typically require a constant number of probes.
        *   **Worst Case**: $O(M)$, where $M$ is the table size. In the worst-case scenario (e.g., all keys hash to the same initial index and $h_2$ values, or the table is nearly full and many collisions occur), an operation might have to probe almost all slots in the table.

6.  **When would you choose Double Hashing over separate chaining for collision resolution?**
    *   **Answer**:
        *   **Memory Locality**: Open addressing techniques like Double Hashing can offer better cache performance because all elements are stored directly in the array, leading to better memory locality compared to separate chaining which involves pointers and linked lists (or other data structures) scattered in memory.
        *   **No Pointers Overhead**: Open addressing avoids the overhead of storing pointers for linked lists, potentially saving memory if keys and values are small.
        *   **Predictable Performance (under high load)**: Double Hashing tends to degrade more gracefully than linear or quadratic probing under high load factors, making its performance more predictable than simpler open addressing schemes.
        *   **When memory is a contiguous block**: If you have a fixed-size array and want to maximize its utilization without external data structures.

7.  **Can Double Hashing completely eliminate collisions? Why or why not?**
    *   **Answer**: No, Double Hashing cannot completely eliminate collisions. Collisions are an inherent property of hashing when the number of possible keys is much larger than the hash table size. Double Hashing is a *collision resolution technique*, meaning it provides a strategy to handle collisions when they occur, rather than preventing them entirely. Its goal is to minimize the *impact* of collisions on performance by finding alternative slots efficiently.

8.  **Discuss the implications of deletion in a Double Hashing hash table.**
    *   **Answer**: Deletion in open-addressed hash tables, including Double Hashing, is complex. Simply setting a deleted slot to `None` can "break" the probe sequence for other keys that might have collided and probed *past* that now-empty slot to find their correct location. If a search encounters a `None` prematurely, it might incorrectly conclude that the key is not present.
    *   The common solution is to use a special **"DELETED" marker** (sometimes called a "tombstone"). When an item is deleted, its slot is marked as `DELETED` instead of `None`. During a search, if a `DELETED` marker is encountered, the search continues probing as if the slot were occupied. During insertion, a `DELETED` slot can be overwritten. This adds complexity and can degrade search performance over time if many slots are marked `DELETED`, necessitating periodic re-hashing.

9.  **What happens if $h_2(key)$ is not relatively prime to $M$?**
    *   **Answer**: If $h_2(key)$ is not relatively prime to $M$ (i.e., $\text{gcd}(h_2(key), M) > 1$), the probe sequence $(h_1(key) + i \cdot h_2(key)) \pmod M$ will not visit all $M$ slots in the hash table. Instead, it will only visit $M / \text{gcd}(h_2(key), M)$ distinct slots. This means that even if the hash table is not full, the algorithm might fail to find an empty slot or the target key, leading to an infinite loop or incorrect "not found" results. This is why careful selection of $h_2(key)$ and often a prime table size $M$ are crucial.

10. **How does Double Hashing compare to separate chaining in terms of memory usage and cache performance?**
    *   **Answer**:
        *   **Memory Usage**:
            *   **Double Hashing (Open Addressing)**: Generally uses less memory overhead per entry because it doesn't store explicit pointers for linked lists. However, it might require a larger table size to maintain a low load factor for good performance, and unused slots still consume memory.
            *   **Separate Chaining**: Requires extra memory for pointers in each linked list node. If keys/values are small, this pointer overhead can be significant.
        *   **Cache Performance**:
            *   **Double Hashing**: Tends to have better cache performance. All elements are stored contiguously in the main array. When probing, subsequent accesses are likely to be in nearby memory locations, benefiting from CPU cache lines.
            *   **Separate Chaining**: Can have poorer cache performance. The linked list nodes for a given bucket might be scattered throughout memory, leading to more cache misses when traversing a chain.

## Quiz

1.  Which problem does Double Hashing primarily aim to solve that linear probing suffers from?
    A) Memory fragmentation
    B) Primary clustering
    C) Secondary clustering
    D) Hash function computation time

2.  What is the main advantage of Double Hashing over quadratic probing?
    A) It uses fewer hash functions.
    B) It completely eliminates collisions.
    C) It prevents secondary clustering.
    D) It has simpler implementation.

3.  If a hash table has size $M=10$ and $h_2(key)$ returns a step size of 5, what is a potential issue?
    A) The hash table will become full too quickly.
    B) The probe sequence might not visit all slots.
    C) The first hash function $h_1(key)$ is likely poorly chosen.
    D) This is an ideal scenario for Double Hashing.

4.  Which of the following is a critical requirement for the second hash function $h_2(key)$ in Double Hashing?
    A) It must always return an even number.
    B) It must be computationally faster than $h_1(key)$.
    C) It must be relatively prime to the hash table size $M$.
    D) It must return 0 for at least one key.

5.  In Double Hashing, if $h_1(key) = 5$, $h_2(key) = 3$, and the table size $M=10$, what would be the first three probe locations (for $i=0, 1, 2$)?
    A) 5, 8, 1
    B) 5, 6, 7
    C) 5, 2, 9
    D) 5, 0, 5

---

### Answer Key

1.  **B) Primary clustering**
    *   **Explanation**: Linear probing suffers from primary clustering, where long runs of occupied slots form. Double Hashing uses a variable step size to break up these clusters.

2.  **C) It prevents secondary clustering.**
    *   **Explanation**: Quadratic probing avoids primary clustering but introduces secondary clustering, where keys with the same initial hash follow the same probe sequence. Double Hashing uses a second hash function dependent on the key, ensuring different probe sequences even for keys with the same initial hash.

3.  **B) The probe sequence might not visit all slots.**
    *   **Explanation**: If $M=10$ and $h_2(key)=5$, then $\text{gcd}(10, 5) = 5 \neq 1$. This means the probe sequence will only visit $10/5 = 2$ distinct slots, potentially failing to find an empty slot even if the table is not full.

4.  **C) It must be relatively prime to the hash table size $M$.**
    *   **Explanation**: This property ensures that the probe sequence generated by Double Hashing will eventually visit every slot in the hash table, guaranteeing that an empty slot can be found if one exists.

5.  **A) 5, 8, 1**
    *   **Explanation**:
        *   For $i=0$: $(5 + 0 \cdot 3) \pmod{10} = 5 \pmod{10} = 5$.
        *   For $i=1$: $(5 + 1 \cdot 3) \pmod{10} = 8 \pmod{10} = 8$.
        *   For $i=2$: $(5 + 2 \cdot 3) \pmod{10} = (5 + 6) \pmod{10} = 11 \pmod{10} = 1$.

## Further Reading

1.  **"Introduction to Algorithms" by Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein (CLRS)**:
    *   Chapter on Hash Tables (typically Chapter 11 or similar). This is a classic textbook that provides a rigorous and detailed explanation of hashing, collision resolution techniques including double hashing, and their mathematical analysis.
    *   [Search for "CLRS Hash Tables" or "CLRS Double Hashing" online for relevant sections or summaries.]

2.  **GeeksforGeeks - Double Hashing**:
    *   A popular online resource for computer science topics. Their article on Double Hashing provides a clear explanation, examples, and often includes code snippets in C++ or Java.
    *   [Link: `https://www.geeksforgeeks.org/double-hashing/`]

3.  **Wikipedia - Double Hashing**:
    *   The Wikipedia page on Double Hashing offers a concise overview, mathematical formulas, and comparisons with other probing methods. It's a good starting point for understanding the core concepts.
    *   [Link: `https://en.wikipedia.org/wiki/Double_hashing`]