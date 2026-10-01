# Linear Probing

## Overview
Linear Probing is a fundamental technique used in hash tables to resolve "collisions." Imagine you have a set of items, and you want to store them in a way that allows for very fast retrieval. A hash table does this by using a "hash function" to convert each item's key into an index in an array. Ideally, each key maps to a unique index. However, sometimes two different keys might produce the same index – this is called a **collision**. When a collision occurs, we can't just overwrite the existing item. Linear Probing is one of the simplest strategies to find the *next available slot* in the hash table by sequentially checking subsequent positions until an empty one is found. It's like looking for an empty parking spot: if your assigned spot is taken, you just drive to the next one, then the next, and so on, until you find an open space.

## What Problem It Solves
Linear Probing primarily solves the problem of **hash collisions** in hash tables.

Here's a breakdown of why this problem exists and why Linear Probing is needed:

1.  **Hash Functions and Indices:** A hash function takes an input (a key, like a word or an ID) and converts it into a fixed-size numerical value, typically an integer index within an array. The goal is to distribute keys evenly across the array, allowing for $O(1)$ (constant time) average-case lookup, insertion, and deletion.

2.  **The Pigeonhole Principle:** A hash table has a finite size (e.g., an array of 100 slots). The number of possible keys, however, can be much larger (e.g., all possible strings). According to the Pigeonhole Principle, if you have more pigeons than pigeonholes, at least one pigeonhole must contain more than one pigeon. Similarly, if you have more possible keys than hash table slots, it's inevitable that different keys will sometimes map to the same index. This is a **hash collision**.

3.  **Consequences of Collisions:** If not handled, a collision means that a new item would overwrite an existing item, leading to data loss, or that you wouldn't be able to find the correct item later. This defeats the purpose of a hash table, which is fast and reliable data storage and retrieval.

4.  **Why Linear Probing is Needed:** When a hash function generates an index that is already occupied, Linear Probing provides a deterministic and straightforward way to find an alternative, empty slot. Instead of giving up or using complex data structures, it simply "probes" (checks) the next slot, then the next, and so on, until an empty one is found. This ensures that every item can be stored and later retrieved, even in the presence of collisions.

In machine learning, while Linear Probing itself isn't an ML algorithm, the underlying concept of efficient data storage and collision resolution is crucial for various tasks:
*   **Feature Hashing (Hashing Trick):** This technique maps high-dimensional categorical features to a fixed-size vector using hash functions. While feature hashing typically handles collisions by summing values at the same index rather than probing for an empty slot, it relies on the efficiency of hashing. Understanding collision resolution methods like linear probing provides a foundational understanding of how such systems manage potential conflicts.
*   **Large-scale Data Processing:** When dealing with massive datasets, efficient in-memory key-value stores (which often use hash tables) are essential for caching, aggregations, and intermediate computations.
*   **Approximate Nearest Neighbors (ANN):** Some ANN algorithms use hashing techniques (like Locality Sensitive Hashing) to group similar items. Efficient storage and retrieval of these hashed items might involve hash table implementations that use probing.

## How It Works
Linear Probing is a simple, step-by-step process for handling collisions in a hash table. Let's break down how it works for insertion, searching, and deletion.

Assume we have a hash table (an array) of a fixed size, say $M$. Our hash function $h(k)$ takes a key $k$ and returns an initial index $0 \le \text{index} < M$.

### 1. Insertion
When you want to insert a key-value pair $(k, v)$:

1.  **Calculate Initial Index:** Apply the hash function to the key: `index = h(k)`.
2.  **Check Slot:** Look at the slot `table[index]`.
    *   **If Empty:** If `table[index]` is empty, place the key-value pair there: `table[index] = (k, v)`. You're done.
    *   **If Occupied (Collision):** If `table[index]` is already occupied by a *different* key, a collision has occurred.
3.  **Probe Linearly:** Increment the index and check the next slot: `index = (index + 1) % M`. (The modulo operator `% M` ensures that we wrap around to the beginning of the table if we reach the end).
4.  **Repeat:** Continue checking `table[index]`, `table[(index + 1) % M]`, `table[(index + 2) % M]`, and so on, until an empty slot is found.
5.  **Insert:** Once an empty slot is found, insert the key-value pair there.

**Example:**
Let's say our hash table has size $M=7$. Our hash function is $h(k) = k \pmod 7$.
We want to insert keys: 10, 20, 30.

*   **Insert 10:**
    *   $h(10) = 10 \pmod 7 = 3$.
    *   `table[3]` is empty. Insert (10, value) at `table[3]`.
    *   Table: `[_, _, _, (10,v), _, _, _]`

*   **Insert 20:**
    *   $h(20) = 20 \pmod 7 = 6$.
    *   `table[6]` is empty. Insert (20, value) at `table[6]`.
    *   Table: `[_, _, _, (10,v), _, _, (20,v)]`

*   **Insert 30:**
    *   $h(30) = 30 \pmod 7 = 2$.
    *   `table[2]` is empty. Insert (30, value) at `table[2]`.
    *   Table: `[_, _, (30,v), (10,v), _, _, (20,v)]`

Now, let's insert **17**:
*   $h(17) = 17 \pmod 7 = 3$.
*   `table[3]` is occupied by (10,v). **Collision!**
*   Probe 1: `index = (3 + 1) % 7 = 4`. `table[4]` is empty. Insert (17, value) at `table[4]`.
*   Table: `[_, _, (30,v), (10,v), (17,v), _, (20,v)]`

### 2. Searching
When you want to search for a key $k$:

1.  **Calculate Initial Index:** `index = h(k)`.
2.  **Check Slot:** Look at `table[index]`.
    *   **If Empty:** If `table[index]` is empty, the key is definitely not in the table (because if it were, it would have been placed here or further down the probe sequence). Key not found.
    *   **If Key Matches:** If `table[index]` contains the key $k$, you've found it. Return its value.
    *   **If Key Mismatches (Collision):** If `table[index]` contains a *different* key, it means the key you're looking for might be further down its probe sequence.
3.  **Probe Linearly:** Increment the index: `index = (index + 1) % M`.
4.  **Repeat:** Continue checking slots linearly until either:
    *   The key is found.
    *   An empty slot is encountered (key not in table).
    *   You've traversed the entire table (key not in table, and table is full or has a cycle).

**Example (using the table from above):**
Table: `[_, _, (30,v), (10,v), (17,v), _, (20,v)]`

*   **Search for 10:**
    *   $h(10) = 3$.
    *   `table[3]` contains (10,v). Key found!

*   **Search for 17:**
    *   $h(17) = 3$.
    *   `table[3]` contains (10,v) (mismatch).
    *   Probe 1: `index = (3 + 1) % 7 = 4`. `table[4]` contains (17,v). Key found!

*   **Search for 50:**
    *   $h(50) = 50 \pmod 7 = 1$.
    *   `table[1]` is empty. Key not found.

### 3. Deletion
Deletion in Linear Probing is tricky because simply removing an item can break the search path for other items that were placed further down due to a collision with the deleted item.

To handle this, two common approaches are:

1.  **Lazy Deletion (Tombstones):** Instead of truly removing the item, replace it with a special "tombstone" marker (e.g., `DELETED`).
    *   **Insertion:** Treat tombstones as occupied slots (continue probing past them) but can be overwritten if an item with the *same key* is re-inserted. Or, if an empty slot is found, the tombstone can be replaced.
    *   **Search:** Treat tombstones as occupied slots (continue probing past them) until the key is found or an actual empty slot is encountered.
    *   **Disadvantage:** Tombstones can fill up the table, increasing search times and making the table appear full even when it has "logically" empty slots.

2.  **Re-hashing:** When an item is deleted, all items in the same cluster (the sequence of occupied slots starting from the deleted item's original hash index) are re-hashed and re-inserted into the table. This is more complex but maintains optimal search paths.

Due to the complexity of deletion, Linear Probing is often preferred in scenarios where deletions are rare or where a simple "clear all" operation is sufficient.

## Mathematical Intuition
The mathematical intuition behind Linear Probing revolves around the hash function, the probing sequence, and the concept of the load factor.

### 1. Hash Function
The core of any hash table is the hash function, $h(k)$. This function maps a key $k$ to an initial index in the hash table array. A common simple hash function for integer keys is the modulo operator:
$$h(k) = k \pmod M$$
where:
*   $k$ is the key.
*   $M$ is the size of the hash table (the number of available slots).

The result $h(k)$ is an integer between $0$ and $M-1$, representing the initial slot where the key *should* be placed.

### 2. Probing Sequence
When a collision occurs at $h(k)$, Linear Probing generates a sequence of alternative indices by simply incrementing the index by 1 (and wrapping around the table using the modulo operator). The probing sequence for a key $k$ is given by:
$$h(k, i) = (h(k) + i) \pmod M$$
where:
*   $h(k)$ is the initial hash value of the key $k$.
*   $i$ is the probe number, starting from $0, 1, 2, \dots, M-1$.

So, for a key $k$:
*   The first slot to check is $h(k, 0) = (h(k) + 0) \pmod M = h(k) \pmod M$.
*   If that's occupied, the next slot is $h(k, 1) = (h(k) + 1) \pmod M$.
*   Then $h(k, 2) = (h(k) + 2) \pmod M$.
*   And so on, until an empty slot is found for insertion, or the key is found for searching, or an empty slot is encountered (key not found).

This linear progression is what gives Linear Probing its name.

### 3. Load Factor ($\alpha$)
The performance of a hash table, especially one using open addressing like Linear Probing, is heavily dependent on its **load factor**, denoted by $\alpha$.
$$\alpha = \frac{N}{M}$$
where:
*   $N$ is the number of items currently stored in the hash table.
*   $M$ is the total size (number of slots) of the hash table.

The load factor represents how "full" the hash table is.
*   For open addressing schemes like Linear Probing, $\alpha$ must always be less than or equal to 1 ($\alpha \le 1$), because you cannot store more items than there are slots. In practice, it's usually kept well below 1 (e.g., $\alpha < 0.7$) to maintain good performance.

**Impact of Load Factor:**
The expected number of probes for an **unsuccessful search** (or insertion into an empty slot) using Linear Probing is approximately:
$$E[\text{probes}_{\text{unsuccessful}}] \approx \frac{1}{2} \left(1 + \frac{1}{(1-\alpha)^2}\right)$$
And for a **successful search**:
$$E[\text{probes}_{\text{successful}}] \approx \frac{1}{2} \left(1 + \frac{1}{1-\alpha}\right)$$

These formulas highlight a critical aspect: as $\alpha$ approaches 1 (the table gets fuller), the denominator $(1-\alpha)$ approaches 0, causing the number of probes to increase dramatically. For example:
*   If $\alpha = 0.5$, $E[\text{probes}_{\text{unsuccessful}}] \approx \frac{1}{2}(1 + \frac{1}{(0.5)^2}) = \frac{1}{2}(1 + 4) = 2.5$ probes.
*   If $\alpha = 0.9$, $E[\text{probes}_{\text{unsuccessful}}] \approx \frac{1}{2}(1 + \frac{1}{(0.1)^2}) = \frac{1}{2}(1 + 100) = 50.5$ probes!

This exponential increase in probes is due to a phenomenon called **primary clustering**.

### 4. Primary Clustering
Primary clustering is the main mathematical drawback of Linear Probing. It occurs because if a collision happens at index $i$, the next available slot will be $i+1$, then $i+2$, and so on. This means that keys that hash to $i$, $i-1$, $i-2$, etc., will all tend to "cluster" together into a contiguous block of occupied slots.

Imagine a block of $k$ occupied slots. Any new key that hashes into this block (or immediately before it) will have to probe through all $k$ slots to find an empty one, and then it will extend the block by one more slot. This makes the block even longer, increasing the probability that future keys will also hash into or near it, thus making the block grow even faster. This self-reinforcing process leads to very long probe sequences and significantly degrades performance as the load factor increases.

In essence, the mathematical intuition shows that while simple, Linear Probing's performance is highly sensitive to the load factor, and its linear probing sequence inherently leads to performance degradation due to primary clustering.

## Advantages
Linear Probing offers several benefits, especially due to its simplicity and memory characteristics:

*   **Simplicity of Implementation:** It is one of the easiest collision resolution techniques to understand and implement. The logic for finding the next slot (just `index = (index + 1) % M`) is straightforward.
*   **Excellent Cache Performance (Cache Locality):** When probing linearly, successive memory accesses are to adjacent memory locations. Modern computer architectures are optimized for this kind of sequential access (spatial locality), as data is often fetched in blocks (cache lines). This means that once the initial slot is accessed, subsequent probes are likely to hit data already in the CPU cache, leading to faster access times compared to methods that jump around memory (like separate chaining with linked lists or quadratic probing).
*   **No Overhead for Pointers:** Unlike separate chaining, which uses linked lists (requiring extra memory for pointers/references), Linear Probing stores all items directly within the main hash table array. This saves memory and can be more efficient for small key-value pairs.
*   **Memory Efficiency:** Because it doesn't use extra data structures like linked lists, the memory footprint is generally smaller for the same number of stored items, especially if the keys and values are small.
*   **Guaranteed to Find a Slot (if table not full):** As long as the hash table is not completely full ($\alpha < 1$), Linear Probing is guaranteed to find an empty slot for insertion or to find the key during a search (assuming no infinite loops due to bugs or full table).

## Disadvantages
Despite its simplicity, Linear Probing has significant drawbacks, primarily related to its performance characteristics under higher load factors:

*   **Primary Clustering:** This is the most severe disadvantage. When collisions occur, keys tend to group together into contiguous blocks of occupied slots. Any new key that hashes into or near one of these blocks will have to probe through the entire block, extending it further. This self-reinforcing process leads to very long probe sequences, significantly degrading performance for insertions, searches, and deletions as the table fills up.
*   **Performance Degradation with High Load Factors:** As the load factor ($\alpha$) increases (i.e., the table gets fuller), the probability of collisions and the length of probe sequences increase exponentially due to primary clustering. This means that the average-case $O(1)$ performance can quickly degrade towards $O(N)$ in the worst case, where $N$ is the number of items. It's generally recommended to keep the load factor below 0.5 to 0.7 for Linear Probing.
*   **Complex Deletion:** Deleting an item is problematic. Simply removing an item and marking its slot as empty can "break" the search path for other items that were placed further down the probe sequence because they collided with the now-deleted item. To fix this, either "tombstones" (special markers for deleted slots) must be used, or a complex re-hashing process for the entire cluster must be performed. Both solutions have their own overheads and complexities.
    *   **Tombstones:** Increase search times (as they must be skipped) and can make the table appear full, even if many items have been logically deleted.
    *   **Re-hashing:** Can be computationally expensive, especially for large clusters.
*   **Sensitivity to Hash Function Quality:** While true for all hash tables, Linear Probing's performance is particularly sensitive to a poor hash function that doesn't distribute keys evenly. If keys tend to cluster in the initial hash values, Linear Probing will exacerbate this clustering.
*   **Table Resizing Overhead:** To maintain good performance, hash tables using Linear Probing often need to be resized (re-hashed into a larger table) when the load factor exceeds a certain threshold. This resizing operation can be very expensive, as all existing items must be re-inserted into the new, larger table.

## Real World Applications
While Linear Probing is a fundamental data structure concept rather than an ML algorithm itself, its principles of efficient key-value storage and collision resolution are critical in various software systems, including those that support machine learning infrastructure. Here are 3-5 concrete real-world use cases:

1.  **In-memory Caches and Dictionaries:** Many applications, including those serving ML models, rely on fast in-memory caches (e.g., Redis, Memcached, or custom application-level caches) to store frequently accessed data, configuration settings, or intermediate computation results. Hash tables using open addressing (like Linear Probing) are often employed here due to their speed and memory efficiency, especially when cache locality is important. For instance, a system might cache the output of an expensive feature engineering step for specific user IDs.
2.  **Compiler Symbol Tables:** Compilers and interpreters use symbol tables to store information about identifiers (variables, functions, classes) during the parsing and compilation phases. These tables need extremely fast lookups to resolve names and check scope. Hash tables, often implemented with open addressing schemes like Linear Probing, are a common choice for their speed and relatively low memory overhead compared to tree-based structures.
3.  **Implementing Sets and Maps in Standard Libraries:** The underlying implementation of `HashSet` or `HashMap` (or `dict` in Python, though Python's `dict` uses a more sophisticated variant of open addressing) in many programming languages might use Linear Probing or a similar open addressing scheme. These data structures are ubiquitous in any software development, including building ML pipelines, data preprocessing scripts, or custom data structures for specific ML tasks.
4.  **Database Indexing (Specific Scenarios):** While B-trees are more common for disk-based database indexing, in-memory hash indexes for specific tables or temporary data structures within a database system might utilize open addressing. For example, a database might use a hash index for a temporary table created during a complex query, where fast lookups are paramount and the data is transient.
5.  **Network Routers and Firewalls:** High-performance network devices need to quickly look up IP addresses, port numbers, or packet headers to make routing decisions or apply firewall rules. Hash tables are often used for these lookups, and the choice of collision resolution can impact throughput. Linear Probing might be considered for its cache efficiency in hardware-accelerated lookups.

## Python Example
Here's a complete, standalone Python code snippet demonstrating a simple hash table implementation using Linear Probing. This example will show how to insert key-value pairs and search for keys, handling collisions by probing linearly.

```python
import numpy as np

class LinearProbingHashTable:
    """
    A simple hash table implementation using Linear Probing for collision resolution.
    """
    def __init__(self, capacity=10):
        """
        Initializes the hash table with a given capacity.
        Each slot can store a (key, value) tuple.
        None indicates an empty slot.
        'DELETED' is a special marker for lazy deletion.
        """
        self.capacity = capacity
        self.table = [None] * self.capacity
        self.size = 0 # Number of actual items stored

        # Define special markers
        self.EMPTY = None
        self.DELETED = "DELETED" # Using a string for simplicity, could be a unique object

    def _hash(self, key):
        """
        Simple hash function: uses Python's built-in hash() and modulo capacity.
        """
        return hash(key) % self.capacity

    def _get_next_index(self, index):
        """
        Calculates the next index for linear probing.
        """
        return (index + 1) % self.capacity

    def insert(self, key, value):
        """
        Inserts a key-value pair into the hash table.
        Handles collisions using linear probing.
        Resizes if load factor exceeds 0.7 (a common heuristic).
        """
        if self.size / self.capacity >= 0.7:
            print(f"Load factor {self.size / self.capacity:.2f} too high. Resizing table...")
            self._resize()

        initial_index = self._hash(key)
        index = initial_index
        
        # Probe linearly until an empty or DELETED slot is found, or the key is found
        while self.table[index] is not self.EMPTY:
            if self.table[index] is not self.DELETED and self.table[index][0] == key:
                # Key already exists, update its value
                self.table[index] = (key, value)
                print(f"Updated key '{key}' at index {index}.")
                return
            
            index = self._get_next_index(index)
            if index == initial_index: # Full table or cycle detected
                raise Exception("Hash table is full or cannot find a slot for insertion.")

        # Found an empty or DELETED slot, insert the new key-value pair
        self.table[index] = (key, value)
        self.size += 1
        print(f"Inserted ('{key}', '{value}') at index {index}.")

    def search(self, key):
        """
        Searches for a key in the hash table.
        Returns the value if found, otherwise None.
        """
        initial_index = self._hash(key)
        index = initial_index
        
        # Probe linearly until the key is found or an empty slot is encountered
        while self.table[index] is not self.EMPTY:
            if self.table[index] is not self.DELETED and self.table[index][0] == key:
                print(f"Found key '{key}' with value '{self.table[index][1]}' at index {index}.")
                return self.table[index][1]
            
            index = self._get_next_index(index)
            if index == initial_index: # Full table or cycle detected without finding key
                break # Key not found

        print(f"Key '{key}' not found.")
        return None

    def delete(self, key):
        """
        Deletes a key from the hash table using lazy deletion (tombstones).
        """
        initial_index = self._hash(key)
        index = initial_index

        while self.table[index] is not self.EMPTY:
            if self.table[index] is not self.DELETED and self.table[index][0] == key:
                self.table[index] = self.DELETED # Mark as deleted (tombstone)
                self.size -= 1
                print(f"Deleted key '{key}' at index {index} (marked as DELETED).")
                return True
            
            index = self._get_next_index(index)
            if index == initial_index:
                break # Key not found

        print(f"Key '{key}' not found for deletion.")
        return False

    def _resize(self):
        """
        Resizes the hash table to approximately double its current capacity.
        All existing items are re-hashed into the new table.
        """
        old_table = self.table
        old_capacity = self.capacity
        
        self.capacity = self._get_next_prime(old_capacity * 2) # Use a prime number for better distribution
        self.table = [None] * self.capacity
        self.size = 0 # Reset size, will be re-counted during re-insertion

        print(f"Resizing from {old_capacity} to {self.capacity}...")

        for item in old_table:
            if item is not self.EMPTY and item is not self.DELETED:
                key, value = item
                # Re-insert into the new table
                # Note: We call the internal insert method to avoid recursive resize checks
                # and to ensure proper handling of the new table's state.
                # For simplicity, we'll just call the public insert, but in a real impl,
                # you might have an internal _insert_without_resize method.
                # For this example, we'll just re-insert.
                self.insert(key, value)
        print("Resizing complete.")

    def _is_prime(self, num):
        """Helper to check if a number is prime."""
        if num < 2: return False
        for i in range(2, int(np.sqrt(num)) + 1):
            if num % i == 0: return False
        return True

    def _get_next_prime(self, num):
        """Helper to find the next prime number greater than or equal to num."""
        while not self._is_prime(num):
            num += 1
        return num

    def display(self):
        """Prints the current state of the hash table."""
        print("\n--- Hash Table State ---")
        for i, item in enumerate(self.table):
            if item is self.EMPTY:
                print(f"Index {i}: EMPTY")
            elif item is self.DELETED:
                print(f"Index {i}: DELETED")
            else:
                print(f"Index {i}: {item[0]} -> {item[1]}")
        print(f"Current size: {self.size}, Capacity: {self.capacity}, Load Factor: {self.size / self.capacity:.2f}")
        print("------------------------\n")

# --- Demonstration ---
if __name__ == "__main__":
    # Initialize hash table with a small capacity to easily observe collisions and resizing
    ht = LinearProbingHashTable(capacity=5) 
    ht.display()

    # Insert some key-value pairs
    print("--- Inserting items ---")
    ht.insert("apple", 10) # hash("apple") % 5
    ht.insert("banana", 20) # hash("banana") % 5
    ht.insert("cherry", 30) # hash("cherry") % 5
    ht.insert("date", 40) # hash("date") % 5
    ht.insert("elderberry", 50) # hash("elderberry") % 5 - This might cause a collision and probe
    ht.display()

    # Let's force some collisions with specific keys
    # We need to find keys that hash to the same initial index
    # Example: if capacity is 5, keys with hash % 5 = 0, 1, 2, 3, 4
    # Let's assume 'apple' hashes to 0, 'banana' to 1, 'cherry' to 2, 'date' to 3, 'elderberry' to 4
    # Let's try to insert 'grape' which might hash to 0 (collision with 'apple')
    # For demonstration, let's use simple integer keys for predictable hashing
    print("\n--- Resetting and demonstrating with integer keys for predictable collisions ---")
    ht_int = LinearProbingHashTable(capacity=7) # Using a prime capacity
    ht_int.display()

    ht_int.insert(10, "Value for 10") # 10 % 7 = 3
    ht_int.insert(20, "Value for 20") # 20 % 7 = 6
    ht_int.insert(30, "Value for 30") # 30 % 7 = 2
    ht_int.insert(17, "Value for 17") # 17 % 7 = 3 (Collision with 10 at index 3, probes to 4)
    ht_int.insert(24, "Value for 24") # 24 % 7 = 3 (Collision with 10, then 17, probes to 5)
    ht_int.display()

    # Search for items
    print("--- Searching for items ---")
    ht_int.search(10) # Should find at index 3
    ht_int.search(17) # Should find at index 4 (after probing)
    ht_int.search(24) # Should find at index 5 (after probing)
    ht_int.search(50) # 50 % 7 = 1. Should be not found.
    ht_int.search(30) # Should find at index 2
    ht_int.display()

    # Delete an item
    print("--- Deleting an item ---")
    ht_int.delete(17) # Deletes the item that caused a probe
    ht_int.display()

    # Search for the deleted item (should not be found)
    print("--- Searching for deleted item ---")
    ht_int.search(17) # Should be not found, but probe past DELETED marker
    ht_int.search(24) # Should still be found, probing past DELETED marker
    ht_int.display()

    # Insert a new item that might fill a DELETED slot or cause further probing
    print("--- Inserting after deletion ---")
    ht_int.insert(31, "Value for 31") # 31 % 7 = 3. Collides with 10, then DELETED at 4, inserts at 4.
    ht_int.display()

    # Demonstrate resizing
    print("--- Demonstrating Resizing ---")
    ht_resize = LinearProbingHashTable(capacity=3)
    ht_resize.insert("A", 1)
    ht_resize.insert("B", 2)
    ht_resize.insert("C", 3) # This will trigger resize as load factor becomes 1.0
    ht_resize.display()
    ht_resize.insert("D", 4) # Insert into the new, larger table
    ht_resize.display()
```

**Explanation of the Python Code:**

1.  **`LinearProbingHashTable` Class:**
    *   `__init__(self, capacity=10)`: Initializes the hash table as a Python list (`self.table`) filled with `None` (representing empty slots). `self.size` tracks the number of actual elements. `self.DELETED` is a special marker for lazy deletion.
    *   `_hash(self, key)`: A simple hash function using Python's built-in `hash()` and the modulo operator to get an index within the table's `capacity`.
    *   `_get_next_index(self, index)`: Implements the linear probing step: `(index + 1) % self.capacity`.
    *   `insert(self, key, value)`:
        *   Checks the load factor and triggers `_resize()` if it's too high (e.g., >= 0.7).
        *   Calculates the `initial_index`.
        *   Enters a `while` loop to probe linearly:
            *   If the current slot is `None` (empty) or `DELETED`, it inserts the item there.
            *   If the key already exists in the current slot, it updates the value.
            *   If the slot is occupied by a *different* key, it moves to the `_get_next_index`.
            *   Includes a check `if index == initial_index` to detect if the table is full or if it has cycled without finding a spot.
    *   `search(self, key)`:
        *   Similar probing logic to `insert`.
        *   Continues probing until the key is found, or an `EMPTY` slot is encountered (meaning the key is not in the table), or it cycles back to the `initial_index`.
        *   Crucially, it *continues probing past `DELETED` slots* because the actual key might have been placed after a deleted item.
    *   `delete(self, key)`:
        *   Implements **lazy deletion** using the `DELETED` marker (tombstone).
        *   When a key is found, its slot is marked `DELETED`, and `self.size` is decremented. The actual `(key, value)` tuple remains in memory until overwritten or resized, but it's logically removed.
    *   `_resize(self)`:
        *   Creates a new, larger table (typically double the size, often to a prime number for better distribution).
        *   Iterates through all non-empty, non-deleted items in the `old_table` and re-inserts them into the `new_table`. This is an expensive operation but necessary to maintain performance.
    *   `_is_prime` and `_get_next_prime`: Helper functions to ensure the table capacity is a prime number, which often helps in better distribution of keys and reduces clustering.
    *   `display(self)`: Prints the current state of the hash table for easy visualization.

The `if __name__ == "__main__":` block demonstrates the usage with both string and integer keys, showing insertions, collisions, searches, deletions, and resizing.

## Interview Questions

Here are at least 10 relevant technical interview questions about Linear Probing, complete with comprehensive, detailed answers.

1.  **What is Linear Probing, and what problem does it solve?**
    *   **Answer:** Linear Probing is a collision resolution strategy used in hash tables. When a hash function maps two or more different keys to the same index (a collision), Linear Probing resolves this by sequentially checking the next available slots in the hash table array (i.e., `index + 1`, `index + 2`, etc., wrapping around if necessary) until an empty slot is found for insertion, or the target key is found during a search. It solves the problem of ensuring that all items can be stored and retrieved efficiently even when hash collisions occur.

2.  **How does Linear Probing work for insertion and search operations?**
    *   **Answer (Insertion):** To insert a key-value pair, first compute its initial hash index `h(key)`. Check `table[h(key)]`. If it's empty, insert the item. If it's occupied by a different key (collision), check `table[(h(key) + 1) % M]`, then `table[(h(key) + 2) % M]`, and so on, until an empty slot is found.
    *   **Answer (Search):** To search for a key, compute its initial hash index `h(key)`. Check `table[h(key)]`. If the key is found, return its value. If the slot is empty, the key is not in the table. If the slot is occupied by a different key, continue checking `table[(h(key) + 1) % M]`, `table[(h(key) + 2) % M]`, etc., until the key is found or an empty slot is encountered (indicating the key is not present).

3.  **What is "primary clustering" in the context of Linear Probing, and why is it a problem?**
    *   **Answer:** Primary clustering is a phenomenon where occupied slots in a hash table using Linear Probing tend to form contiguous blocks. If a collision occurs, Linear Probing places the item in the next available slot, which extends any existing cluster. This makes the cluster longer, increasing the probability that future keys will also hash into or near this growing block, thus further extending it. This is a problem because it leads to very long probe sequences for insertions, searches, and deletions, significantly degrading the hash table's performance from $O(1)$ average-case to potentially $O(N)$ in the worst case as the load factor increases.

4.  **What is the load factor, and how does it affect Linear Probing's performance?**
    *   **Answer:** The load factor ($\alpha$) is the ratio of the number of items stored ($N$) to the total capacity of the hash table ($M$), i.e., $\alpha = N/M$. For Linear Probing, the load factor must be $\le 1$. As the load factor increases, the performance of Linear Probing degrades significantly due to primary clustering. The average number of probes for an unsuccessful search (or insertion) increases exponentially as $\alpha$ approaches 1. It's generally recommended to keep $\alpha$ below 0.5 to 0.7 to maintain good performance.

5.  **How do you handle deletion in a Linear Probing hash table? What are the challenges?**
    *   **Answer:** Deletion is tricky in Linear Probing. Simply marking a slot as empty can "break" the search path for other items that were placed further down the probe sequence because they initially collided with the deleted item.
        *   **Lazy Deletion (Tombstones):** The most common approach is to use a special "tombstone" marker (e.g., `DELETED`) instead of truly emptying the slot. During insertion, tombstones are treated as occupied (you probe past them to find an empty slot, but they can be overwritten). During search, tombstones are also treated as occupied (you probe past them) until the key is found or an actual empty slot is encountered.
        *   **Challenges:** Tombstones increase search times because they must be skipped. They also make the table appear logically fuller than it is, contributing to performance degradation and potentially triggering premature resizing.
        *   **Re-hashing:** Another, more complex approach is to re-hash all items in the cluster following the deleted item. This is computationally expensive.

6.  **Compare Linear Probing with Separate Chaining. When would you choose one over the other?**
    *   **Answer:**
        *   **Separate Chaining:** Each slot in the hash table array points to a linked list (or other data structure) containing all keys that hash to that index.
        *   **Linear Probing (Open Addressing):** All items are stored directly in the hash table array; collisions are resolved by finding the next empty slot.
        *   **Comparison:**
            *   **Memory:** Linear Probing is generally more memory-efficient as it doesn't require extra pointers for linked lists. Separate Chaining has pointer overhead.
            *   **Cache Performance:** Linear Probing has better cache locality due to sequential memory access. Separate Chaining jumps around memory, leading to poorer cache performance.
            *   **Clustering:** Linear Probing suffers from primary clustering. Separate Chaining can suffer from secondary clustering (if the hash function is poor), but not primary.
            *   **Load Factor:** Separate Chaining can handle load factors greater than 1 (more items than slots) gracefully. Linear Probing's performance degrades rapidly as $\alpha$ approaches 1.
            *   **Deletion:** Deletion is simpler in Separate Chaining (just remove from the linked list). It's complex in Linear Probing.
        *   **Choice:**
            *   Choose **Linear Probing** when memory is a critical concern, cache performance is highly valued, and deletions are rare or handled by full table re-hashing. It's good for relatively low load factors.
            *   Choose **Separate Chaining** when load factors might be high, deletions are frequent, or when the performance degradation due to clustering is unacceptable. It's generally more robust.

7.  **What are the advantages of using Linear Probing?**
    *   **Answer:**
        *   **Simplicity:** Easy to implement.
        *   **Cache Performance:** Excellent cache locality due to sequential memory access.
        *   **Memory Efficiency:** No overhead for pointers or extra data structures like linked lists.
        *   **Guaranteed Slot:** Will always find a slot if the table is not full.

8.  **What are the disadvantages of using Linear Probing?**
    *   **Answer:**
        *   **Primary Clustering:** Leads to long probe sequences and degraded performance.
        *   **Performance Degradation:** Performance drops sharply as the load factor increases.
        *   **Complex Deletion:** Requires tombstones or re-hashing, adding complexity and potential performance issues.
        *   **Table Resizing:** Requires expensive re-hashing of all elements when the load factor threshold is reached.

9.  **Can Linear Probing be used if the hash table is full?**
    *   **Answer:** No. If the hash table is completely full ($\alpha = 1$), Linear Probing cannot find an empty slot for insertion, nor can it distinguish between a key not being present and the table being full during a search if the key is not found. It would enter an infinite loop trying to find an empty slot. This is why hash tables using Linear Probing must be resized (expanded) before they become completely full.

10. **How can you mitigate the effects of primary clustering in open addressing schemes?**
    *   **Answer:** While Linear Probing inherently suffers from primary clustering, other open addressing schemes aim to mitigate it:
        *   **Quadratic Probing:** Uses a quadratic sequence for probing: $h(k, i) = (h(k) + c_1 i + c_2 i^2) \pmod M$. This helps spread out collisions more effectively, reducing primary clustering but introducing "secondary clustering" (keys hashing to the same initial index follow the same probe sequence).
        *   **Double Hashing:** Uses a second hash function $h_2(k)$ to determine the step size for probing: $h(k, i) = (h_1(k) + i \cdot h_2(k)) \pmod M$. This generates a unique probe sequence for each key, virtually eliminating both primary and secondary clustering, offering the best performance among open addressing methods.
        *   **Resizing:** Keeping the load factor low by resizing the table when it gets too full is crucial for all open addressing schemes, including Linear Probing, to prevent severe performance degradation.

## Quiz

1.  What is the primary purpose of Linear Probing in a hash table?
    A) To calculate the initial hash index for a key.
    B) To sort the elements within the hash table.
    C) To resolve collisions when multiple keys map to the same index.
    D) To encrypt data stored in the hash table.

2.  Which of the following is a major disadvantage of Linear Probing?
    A) High memory consumption due to linked lists.
    B) Poor cache performance.
    C) Primary clustering.
    D) Difficulty in calculating the initial hash index.

3.  If a hash table has a capacity of $M=10$ and currently stores $N=7$ items, what is its load factor?
    A) 0.7
    B) 1.0
    C) 0.3
    D) 7.0

4.  When searching for a key in a Linear Probing hash table, if you encounter a "DELETED" marker (tombstone) at the current probe index, what should you do?
    A) Conclude that the key is not in the table.
    B) Stop searching and return `None`.
    C) Continue probing to the next slot.
    D) Re-insert the key at that "DELETED" slot.

5.  Which of the following statements about Linear Probing is true?
    A) It requires external data structures like linked lists for collision resolution.
    B) Its performance improves as the load factor approaches 1.
    C) It offers good cache locality due to sequential memory access.
    D) Deletion is straightforward and does not require special handling.

### Answer Key

1.  **C) To resolve collisions when multiple keys map to the same index.**
    *   **Explanation:** Linear Probing is a specific technique for handling the situation where a hash function produces the same index for different keys, ensuring all items can be stored and retrieved.

2.  **C) Primary clustering.**
    *   **Explanation:** Primary clustering is the most significant drawback of Linear Probing, where occupied slots form contiguous blocks, leading to longer probe sequences and degraded performance. Options A and B are disadvantages of separate chaining, not linear probing.

3.  **A) 0.7**
    *   **Explanation:** The load factor ($\alpha$) is calculated as $N/M$. In this case, $7/10 = 0.7$.

4.  **C) Continue probing to the next slot.**
    *   **Explanation:** Tombstones (`DELETED` markers) indicate that an item *was* there but is now logically removed. Other items might have been placed after this deleted item due to collisions, so you must continue probing to find the target key or an actual empty slot.

5.  **C) It offers good cache locality due to sequential memory access.**
    *   **Explanation:** Because Linear Probing checks adjacent memory locations, it benefits from CPU cache mechanisms, leading to faster access times. Option A describes separate chaining. Option B is false; performance degrades as the load factor approaches 1. Option D is false; deletion is complex and requires tombstones or re-hashing.

## Further Reading

1.  **"Introduction to Algorithms" by Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein (CLRS):** Chapter 11, "Hash Tables," provides a rigorous and detailed explanation of hash tables, including open addressing techniques like Linear Probing, Quadratic Probing, and Double Hashing. This is a classic textbook for algorithms and data structures.
    *   *Search for: "CLRS Hash Tables Open Addressing"*

2.  **Wikipedia - Linear Probing:** A good starting point for a concise overview, definitions, and links to related concepts. It often includes pseudocode and mathematical formulas.
    *   *Link: [https://en.wikipedia.org/wiki/Linear_probing](https://en.wikipedia.org/wiki/Linear_probing)*

3.  **GeeksforGeeks - Hashing | Set 3 (Open Addressing and Linear Probing):** This resource provides a beginner-friendly explanation with examples and often includes C++ or Java code implementations. It's great for understanding the concepts with practical illustrations.
    *   *Link: [https://www.geeksforgeeks.org/hashing-set-3-open-addressing-linear-probing/](https://www.geeksforgeeks.org/hashing-set-3-open-addressing-linear-probing/)*