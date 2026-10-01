# Quadratic Probing

## Overview
Quadratic Probing is a technique used in hash tables to resolve collisions. When two different keys hash to the same index (a "collision"), we need a strategy to find an alternative, empty slot for the new key. Quadratic probing is one such strategy, belonging to a family of techniques called "open addressing." Unlike "separate chaining" which uses linked lists at each index, open addressing methods search for another slot directly within the hash table itself. Quadratic probing attempts to alleviate some of the issues faced by simpler open addressing methods like linear probing, particularly the problem of "primary clustering." It does this by using a quadratic function to determine the next probe location, making the jumps larger and more spread out.

## What Problem It Solves
Quadratic probing primarily addresses the problem of **hash collisions** and, more specifically, **primary clustering** in hash tables that use open addressing.

1.  **Hash Collisions**: A hash function maps keys to indices in an array. Since the number of possible keys is often much larger than the size of the hash table, it's inevitable that different keys will sometimes map to the same index. This is a collision. When a collision occurs, we cannot simply overwrite the existing data; we need a way to find another available slot.

2.  **Primary Clustering (Problem with Linear Probing)**: Linear probing is a simple collision resolution technique where, upon a collision at index $h(key)$, it tries $(h(key) + 1) \pmod{table\_size}$, then $(h(key) + 2) \pmod{table\_size}$, and so on. The problem with linear probing is that it tends to create long "runs" or "clusters" of occupied slots. If a collision occurs within such a cluster, the new key will be placed at the end of it, extending the cluster. This means that any subsequent key that hashes into or near this cluster will have to traverse the entire cluster, leading to slower insertion and retrieval times. These growing clusters are known as **primary clustering**.

Quadratic probing aims to solve primary clustering by making the probe sequence "jump" further away from the initial collision point. Instead of checking adjacent slots, it checks slots at quadratically increasing offsets, which helps to distribute keys more evenly and reduce the formation of large, contiguous clusters.

In machine learning, efficient data structures are crucial. For instance, hash tables are used in:
*   **Feature Hashing**: Mapping high-dimensional categorical features to a fixed-size vector space. Collisions here mean different features map to the same vector index, and efficient resolution is key.
*   **Caching**: Storing frequently accessed data (e.g., model parameters, intermediate computation results) for quick retrieval.
*   **Symbol Tables**: In compilers or interpreters for ML frameworks, symbol tables store variable names and their properties, requiring fast lookups.
*   **Data Preprocessing**: For tasks like counting word frequencies or building dictionaries for one-hot encoding, hash tables provide efficient storage and retrieval.

Inefficient collision resolution can significantly slow down these operations, impacting the overall performance of ML algorithms and systems.

## How It Works
Quadratic probing works by calculating a sequence of probe locations using a quadratic function when a collision occurs. Here's a step-by-step breakdown:

1.  **Initial Hash Calculation**:
    *   When you want to insert a `key` (or search for one), you first compute its initial hash value using a primary hash function: $h(key)$.
    *   This gives you an initial index, say `idx_0 = h(key) % table_size`.

2.  **Checking the Initial Slot**:
    *   Check if the slot at `idx_0` is empty.
    *   If it's empty, the `key` (and its associated `value`) can be placed there.
    *   If it's occupied, a collision has occurred.

3.  **Probing for an Alternative Slot (Quadratic Sequence)**:
    *   If `idx_0` is occupied, quadratic probing starts a sequence of probes. The $i$-th probe (starting with $i=1$) is calculated using the formula:
        $probe\_index = (h(key) + i^2) \pmod{table\_size}$
        (A more general form is $(h(key) + c_1 \cdot i + c_2 \cdot i^2) \pmod{table\_size}$, but $c_1=0$ and $c_2=1$ is common for simplicity and effectiveness).

    *   **First Probe ($i=1$)**: Calculate $idx_1 = (h(key) + 1^2) \pmod{table\_size}$. Check if `idx_1` is empty.
    *   **Second Probe ($i=2$)**: If `idx_1` is occupied, calculate $idx_2 = (h(key) + 2^2) \pmod{table\_size}$. Check if `idx_2` is empty.
    *   **Third Probe ($i=3$)**: If `idx_2` is occupied, calculate $idx_3 = (h(key) + 3^2) \pmod{table\_size}$. Check if `idx_3` is empty.
    *   This process continues, incrementing $i$ and calculating $i^2$, until an empty slot is found or a predefined maximum number of probes is reached (indicating the table is full or an infinite loop is detected).

4.  **Insertion/Retrieval**:
    *   **Insertion**: Once an empty slot is found at `probe_index`, the `key` and `value` are stored there.
    *   **Retrieval**: When searching for a `key`, the same probing sequence is followed. If the `key` is found at any `probe_index`, its associated `value` is returned. If an empty slot is encountered during probing, it means the `key` is not in the table (because if it were, it would have been placed there or earlier in the sequence). If the maximum probes are reached without finding the key or an empty slot, the key is not in the table.

**Example Walkthrough:**
Let's say we have a hash table of size 10, and our hash function is $h(key) = key \pmod{10}$.
We want to insert keys: 12, 22, 32.

*   **Insert 12**:
    *   $h(12) = 12 \pmod{10} = 2$.
    *   Slot 2 is empty. Insert 12 at index 2.
    *   Table: `[_, _, 12, _, _, _, _, _, _, _]`

*   **Insert 22**:
    *   $h(22) = 22 \pmod{10} = 2$.
    *   Slot 2 is occupied by 12 (collision!).
    *   Start quadratic probing ($i=1$):
        *   $probe\_index = (h(22) + 1^2) \pmod{10} = (2 + 1) \pmod{10} = 3$.
    *   Slot 3 is empty. Insert 22 at index 3.
    *   Table: `[_, _, 12, 22, _, _, _, _, _, _]`

*   **Insert 32**:
    *   $h(32) = 32 \pmod{10} = 2$.
    *   Slot 2 is occupied by 12 (collision!).
    *   Start quadratic probing ($i=1$):
        *   $probe\_index = (h(32) + 1^2) \pmod{10} = (2 + 1) \pmod{10} = 3$.
    *   Slot 3 is occupied by 22 (collision!).
    *   Continue probing ($i=2$):
        *   $probe\_index = (h(32) + 2^2) \pmod{10} = (2 + 4) \pmod{10} = 6$.
    *   Slot 6 is empty. Insert 32 at index 6.
    *   Table: `[_, _, 12, 22, _, _, 32, _, _, _]`

Notice how 32, despite initially hashing to 2, ended up at index 6, skipping 3, 4, and 5. This helps prevent the long contiguous blocks seen in linear probing.

## Mathematical Intuition
The core idea behind quadratic probing is to use a non-linear increment to find the next available slot in the hash table. Instead of adding a constant value (like 1 in linear probing), we add a value that increases quadratically with each probe attempt.

Let's define the components:
*   $h(key)$: This is our primary hash function, which maps a `key` to an initial index in the hash table. This index is typically in the range $[0, table\_size - 1]$.
*   $table\_size$: The total number of slots in our hash table.
*   $i$: This is the probe number, starting from $i=0$ for the initial hash, and then $i=1, 2, 3, \dots$ for subsequent probes.

The general formula for the $i$-th probe location (where $i=0$ is the initial hash, and $i=1, 2, \dots$ are for subsequent probes) is:

$$h(key, i) = (h(key) + c_1 \cdot i + c_2 \cdot i^2) \pmod{table\_size}$$

Let's break down this formula:

*   **$h(key)$**: This is the initial hash value. It's the starting point for our search.
*   **$c_1 \cdot i + c_2 \cdot i^2$**: This is the "offset" or "step" that is added to the initial hash value.
    *   $c_1$ and $c_2$ are constants. For simplicity and common implementations, $c_1$ is often set to $0$ and $c_2$ to $1$.
    *   If $c_1 = 0$ and $c_2 = 1$, the formula simplifies to:
        $$h(key, i) = (h(key) + i^2) \pmod{table\_size}$$
    *   Let's analyze the sequence of offsets generated by $i^2$:
        *   For $i=0$: Offset is $0^2 = 0$. This gives the initial hash index: $h(key, 0) = (h(key) + 0) \pmod{table\_size}$.
        *   For $i=1$: Offset is $1^2 = 1$. The first probe is at $(h(key) + 1) \pmod{table\_size}$.
        *   For $i=2$: Offset is $2^2 = 4$. The second probe is at $(h(key) + 4) \pmod{table\_size}$.
        *   For $i=3$: Offset is $3^2 = 9$. The third probe is at $(h(key) + 9) \pmod{table\_size}$.
        *   For $i=4$: Offset is $4^2 = 16$. The fourth probe is at $(h(key) + 16) \pmod{table\_size}$.
        And so on.

*   **$\pmod{table\_size}$**: The modulo operator ensures that the calculated index always wraps around to stay within the bounds of the hash table array (i.e., between $0$ and $table\_size - 1$).

**Why $i^2$?**
The quadratic term $i^2$ ensures that the step size increases with each probe. This means that successive probes jump further and further away from the initial collision point.
*   Linear probing uses steps of $1, 2, 3, \dots$.
*   Quadratic probing uses steps of $0, 1, 4, 9, 16, \dots$.

This increasing step size helps to:
1.  **Avoid Primary Clustering**: By not always checking adjacent slots, it breaks up the long contiguous blocks of occupied cells that linear probing creates.
2.  **Explore More of the Table**: The jumps allow the algorithm to quickly explore different parts of the table, increasing the chances of finding an empty slot sooner, especially in a sparsely populated table.

**Important Consideration for $table\_size$**:
For quadratic probing to guarantee finding an empty slot (if one exists) and to visit all possible slots in the table (or at least half of them before repeating a sequence), the `table_size` should ideally be a prime number. If the table size is a power of 2, it can also work, but specific choices of $c_1$ and $c_2$ might be needed, and it might only visit a limited number of slots. A common recommendation is to use a prime number for `table_size` and ensure the load factor (number of items / table size) is less than 0.5. This guarantees that an empty slot will always be found if the table is not full.

## Advantages
*   **Reduces Primary Clustering**: This is the main advantage. By taking larger, non-linear steps, quadratic probing prevents the formation of long contiguous blocks of occupied cells that plague linear probing. This leads to faster average-case performance for insertions and searches compared to linear probing when collisions are frequent.
*   **Better Distribution of Keys**: The quadratic step helps to spread out keys more evenly across the hash table, reducing the likelihood of subsequent collisions at adjacent slots.
*   **Simpler to Implement than Double Hashing**: While double hashing often provides even better performance, quadratic probing is conceptually simpler to implement as it only requires one hash function and a simple quadratic increment.
*   **Good Performance for Moderate Load Factors**: When the hash table is not too full (e.g., load factor < 0.5), quadratic probing generally performs well, finding empty slots quickly.

## Disadvantages
*   **Secondary Clustering**: While it solves primary clustering, quadratic probing introduces a new problem called **secondary clustering**. This occurs when multiple keys hash to the *same initial index* and thus follow the *exact same probe sequence*. Even though they don't form contiguous blocks, they still collide repeatedly along the same path, leading to performance degradation.
*   **Guaranteed Slot Finding (Load Factor Constraint)**: Quadratic probing does not guarantee finding an empty slot if the table is more than half full (load factor > 0.5), even if empty slots exist. To guarantee finding a slot, the table size must be a prime number, and the load factor must be less than or equal to 0.5. If these conditions are not met, it's possible to enter an infinite loop or fail to find an empty slot even when the table is not full.
*   **Requires Table Resizing**: Due to the load factor constraint, hash tables using quadratic probing often need to be resized (rehashed into a larger table) more frequently than those using separate chaining or even linear probing (which can theoretically fill up to 100% load, though performance degrades severely).
*   **Deletion is Complex**: Deleting items from an open-addressed hash table is generally tricky. Simply marking a slot as empty can break the search chain for other items that might have probed past that slot. Special "tombstone" markers are often used, which complicates insertion and search logic and can degrade performance over time if not handled carefully (e.g., by periodic re-hashing).
*   **Less Cache-Friendly than Linear Probing**: Linear probing accesses memory locations that are physically close to each other, which can benefit from CPU cache locality. Quadratic probing's jumps mean it accesses more dispersed memory locations, potentially leading to more cache misses.

## Real World Applications
While quadratic probing is a fundamental data structure concept rather than a machine learning algorithm itself, its efficiency directly impacts the performance of many systems and algorithms, including those used in machine learning. Here are 3-5 concrete real-world use cases:

1.  **Database Indexing and Caching**:
    *   **Use Case**: Databases frequently use hash tables for indexing specific columns or for caching query results. When a database needs to quickly look up a record based on a key (e.g., a user ID, product SKU), a hash index can provide O(1) average-case lookup time. Caches also rely on fast key-value lookups.
    *   **Application of Quadratic Probing**: Efficient collision resolution like quadratic probing ensures that these lookups remain fast even under high load or with many collisions, preventing performance bottlenecks in database operations crucial for data-intensive ML applications.

2.  **Symbol Tables in Compilers and Interpreters (e.g., for ML Frameworks)**:
    *   **Use Case**: Compilers and interpreters (like those for Python, which is heavily used in ML) use symbol tables to store information about variables, functions, and classes (their names, types, scope, memory addresses). When a program accesses a variable, the symbol table is queried.
    *   **Application of Quadratic Probing**: Fast symbol table lookups are critical for the performance of any programming language runtime. If an ML framework like TensorFlow or PyTorch uses a hash table internally for managing computational graph nodes or variable names, quadratic probing can contribute to the overall speed of model compilation and execution by ensuring efficient access to these symbols.

3.  **Network Routers and Firewalls**:
    *   **Use Case**: Network devices like routers and firewalls need to quickly look up routing tables, access control lists (ACLs), or connection states based on IP addresses, port numbers, or other packet headers. These lookups must be extremely fast to handle high network traffic.
    *   **Application of Quadratic Probing**: Hash tables are often employed for these lookups. Quadratic probing helps maintain high throughput by efficiently resolving collisions in these critical, high-speed data structures, ensuring packets are forwarded or filtered with minimal latency.

4.  **Data Deduplication and Caching in Storage Systems**:
    *   **Use Case**: Storage systems (e.g., file systems, object storage, content delivery networks) often use hash tables to detect duplicate data blocks for storage optimization (deduplication) or to cache frequently accessed data.
    *   **Application of Quadratic Probing**: When a new data block arrives, its hash is computed, and the hash table is checked to see if an identical block already exists. Efficient collision resolution with quadratic probing ensures that these checks are fast, reducing storage requirements and improving read performance, which is vital for large datasets often used in machine learning.

5.  **Implementing Hash Sets and Hash Maps in Standard Libraries**:
    *   **Use Case**: Many programming languages' standard libraries provide `HashSet` and `HashMap` (or `Dictionary`) data structures. These are fundamental building blocks for countless applications, including those in machine learning for tasks like counting unique items, grouping data, or creating lookup tables for feature engineering.
    *   **Application of Quadratic Probing**: While specific implementations vary (some use separate chaining, others use open addressing), quadratic probing is a viable and sometimes chosen strategy for open addressing. Its presence in the underlying implementation contributes to the overall efficiency and reliability of these widely used data structures, indirectly supporting ML development.

## Python Example
Since Quadratic Probing is a data structure concept, not a machine learning model, the Python example will demonstrate a custom `HashTable` implementation using quadratic probing for collision resolution. We'll show how to insert and retrieve key-value pairs.

```python
import math

class QuadraticProbingHashTable:
    """
    A simple hash table implementation using quadratic probing for collision resolution.
    """
    def __init__(self, capacity=11): # Start with a prime capacity
        self.capacity = self._get_next_prime(capacity) # Ensure capacity is prime
        self.table = [None] * self.capacity
        self.size = 0 # Number of actual items stored
        self.DELETED = object() # Sentinel for deleted items

    def _get_next_prime(self, n):
        """Helper to find the next prime number greater than or equal to n."""
        while True:
            if self._is_prime(n):
                return n
            n += 1

    def _is_prime(self, num):
        """Helper to check if a number is prime."""
        if num < 2:
            return False
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                return False
        return True

    def _hash(self, key):
        """
        Simple hash function: sum of ASCII values modulo capacity.
        For non-string keys, we use hash() built-in.
        """
        if isinstance(key, str):
            return sum(ord(char) for char in key) % self.capacity
        else:
            return hash(key) % self.capacity

    def _probe(self, initial_index, i):
        """
        Calculates the next probe index using quadratic probing formula:
        (initial_index + i^2) % capacity
        """
        return (initial_index + i*i) % self.capacity

    def insert(self, key, value):
        """
        Inserts a key-value pair into the hash table.
        Handles collisions using quadratic probing.
        """
        if self.size >= self.capacity / 2: # Resize if load factor > 0.5
            print(f"Load factor high ({self.size}/{self.capacity}). Resizing table...")
            self._resize()

        initial_index = self._hash(key)
        
        for i in range(self.capacity): # Iterate up to capacity to find a slot
            probe_index = self._probe(initial_index, i)
            
            # If slot is empty or marked as DELETED, insert here
            if self.table[probe_index] is None or self.table[probe_index] is self.DELETED:
                self.table[probe_index] = (key, value)
                self.size += 1
                print(f"Inserted '{key}':'{value}' at index {probe_index} after {i} probes.")
                return
            
            # If key already exists, update its value
            if self.table[probe_index][0] == key:
                old_value = self.table[probe_index][1]
                self.table[probe_index] = (key, value)
                print(f"Updated '{key}' from '{old_value}' to '{value}' at index {probe_index} after {i} probes.")
                return
        
        # If loop finishes, table is full or cannot find a slot (should not happen with proper resizing)
        print(f"Error: Could not insert '{key}'. Table might be full or probe sequence exhausted.")

    def search(self, key):
        """
        Searches for a key in the hash table.
        Follows the same quadratic probing sequence.
        """
        initial_index = self._hash(key)
        
        for i in range(self.capacity):
            probe_index = self._probe(initial_index, i)
            
            # If slot is None, key is not in table (it would have been inserted here or earlier)
            if self.table[probe_index] is None:
                print(f"Search for '{key}': Not found after {i} probes (encountered empty slot).")
                return None
            
            # If key found, return its value
            if self.table[probe_index] is not self.DELETED and self.table[probe_index][0] == key:
                print(f"Search for '{key}': Found '{self.table[probe_index][1]}' at index {probe_index} after {i} probes.")
                return self.table[probe_index][1]
        
        # If loop finishes, key not found
        print(f"Search for '{key}': Not found after {self.capacity} probes (table exhausted).")
        return None

    def delete(self, key):
        """
        Deletes a key-value pair from the hash table.
        Uses a sentinel (DELETED) to mark deleted slots.
        """
        initial_index = self._hash(key)
        
        for i in range(self.capacity):
            probe_index = self._probe(initial_index, i)
            
            if self.table[probe_index] is None:
                print(f"Delete '{key}': Not found.")
                return False # Key not found
            
            if self.table[probe_index] is not self.DELETED and self.table[probe_index][0] == key:
                self.table[probe_index] = self.DELETED # Mark as deleted
                self.size -= 1
                print(f"Deleted '{key}' at index {probe_index} after {i} probes.")
                return True
        
        print(f"Delete '{key}': Not found after {self.capacity} probes.")
        return False

    def _resize(self):
        """
        Resizes the hash table to a new, larger prime capacity.
        Rehashes all existing items.
        """
        old_table = self.table
        old_capacity = self.capacity
        
        self.capacity = self._get_next_prime(old_capacity * 2) # Double capacity and find next prime
        self.table = [None] * self.capacity
        self.size = 0 # Reset size, will be re-calculated during re-insertion

        print(f"Resizing from {old_capacity} to {self.capacity}...")
        for item in old_table:
            if item is not None and item is not self.DELETED:
                key, value = item
                self.insert(key, value) # Re-insert into new table

    def display(self):
        """Prints the current state of the hash table."""
        print("\n--- Hash Table State ---")
        for i, item in enumerate(self.table):
            if item is None:
                print(f"[{i}]: None")
            elif item is self.DELETED:
                print(f"[{i}]: DELETED")
            else:
                print(f"[{i}]: {item[0]} -> {item[1]}")
        print(f"Current size: {self.size}, Capacity: {self.capacity}\n")

# --- Demonstration ---
if __name__ == "__main__":
    print("Initializing Quadratic Probing Hash Table...")
    ht = QuadraticProbingHashTable(capacity=7) # Start with a small prime capacity for demonstration
    ht.display()

    print("--- Inserting elements ---")
    ht.insert("apple", 10)
    ht.insert("banana", 20)
    ht.insert("cherry", 30)
    ht.insert("date", 40) # This might cause a collision
    ht.insert("elderberry", 50) # More collisions
    ht.insert("fig", 60)
    ht.display()

    print("--- Inserting a key that causes a collision and probes ---")
    # Let's assume 'grape' hashes to an occupied slot
    # Example: if hash('apple') % 7 = 1, hash('grape') % 7 = 1
    # For demonstration, let's pick keys that are likely to collide with our simple hash
    # ord('a')=97, ord('g')=103
    # sum(ord(c) for c in 'apple') = 97+112+112+108+101 = 530. 530 % 7 = 5
    # sum(ord(c) for c in 'grape') = 103+114+97+112+101 = 527. 527 % 7 = 2
    # sum(ord(c) for c in 'hello') = 104+101+108+108+111 = 532. 532 % 7 = 6
    # sum(ord(c) for c in 'world') = 119+111+114+108+100 = 552. 552 % 7 = 1
    # Let's try to force a collision with 'apple' (initial hash 5)
    # We need a key that hashes to 5.
    # 'zebra' = 122+101+98+114+97 = 532. 532 % 7 = 6
    # 'mango' = 109+97+110+103+111 = 530. 530 % 7 = 5. Perfect!
    ht.insert("mango", 70) # Should collide with 'apple' (initial hash 5)
    ht.display()

    print("--- Searching for elements ---")
    ht.search("banana")
    ht.search("mango")
    ht.search("nonexistent")
    ht.search("apple")

    print("--- Updating an existing element ---")
    ht.insert("apple", 100) # Update 'apple'
    ht.display()
    ht.search("apple")

    print("--- Deleting an element ---")
    ht.delete("cherry")
    ht.display()
    ht.search("cherry") # Should not be found

    print("--- Inserting more elements to trigger resize ---")
    ht.insert("kiwi", 80)
    ht.insert("lemon", 90)
    ht.insert("orange", 110) # This should trigger a resize as load factor will exceed 0.5
    ht.display()

    ht.insert("pear", 120)
    ht.display()
```

**Explanation of the Code:**

1.  **`QuadraticProbingHashTable` Class**:
    *   `__init__(self, capacity=11)`: Initializes the hash table. It ensures the `capacity` is a prime number using `_get_next_prime` because prime capacities are crucial for quadratic probing to work effectively and guarantee finding an empty slot (if load factor < 0.5). `self.table` is a list initialized with `None`. `self.size` tracks the number of actual items. `self.DELETED` is a sentinel object used for deletion.
    *   `_get_next_prime(self, n)` and `_is_prime(self, num)`: Helper methods to find the next prime number.
    *   `_hash(self, key)`: A simple hash function. For strings, it sums ASCII values; for other types, it uses Python's built-in `hash()`. The result is then modulo `self.capacity` to get an index within the table bounds.
    *   `_probe(self, initial_index, i)`: This is the heart of quadratic probing. It calculates the $i$-th probe index using the formula `(initial_index + i*i) % self.capacity`.
    *   `insert(self, key, value)`:
        *   Checks if the load factor (`self.size / self.capacity`) is too high (e.g., >= 0.5). If so, it calls `_resize()`.
        *   Calculates the `initial_index`.
        *   It then iterates using `i` from 0 up to `self.capacity - 1` to generate probe indices.
        *   If an empty slot (`None`) or a `DELETED` slot is found, the `(key, value)` pair is inserted.
        *   If the `key` is already found, its `value` is updated.
        *   Includes print statements to show the probing process.
    *   `search(self, key)`:
        *   Similar to `insert`, it calculates the `initial_index` and then follows the same quadratic probing sequence.
        *   If it finds the `key`, it returns the `value`.
        *   If it encounters a `None` slot, it means the key is definitely not in the table (because if it were, it would have been placed at this slot or an earlier one in its probe sequence).
        *   It ignores `DELETED` slots and continues probing.
    *   `delete(self, key)`:
        *   Finds the `key` using quadratic probing.
        *   Instead of setting the slot to `None`, it sets it to `self.DELETED`. This is crucial for open addressing, as setting it to `None` would break the search path for other keys that might have probed past this slot.
    *   `_resize(self)`:
        *   Creates a new table with a larger prime capacity (typically double the old capacity, then find the next prime).
        *   Iterates through all non-`None` and non-`DELETED` items in the `old_table` and re-inserts them into the `new_table`. This is necessary because the hash indices change with a new `capacity`.
    *   `display(self)`: A utility method to print the current state of the hash table.

This example clearly demonstrates the mechanics of quadratic probing, including collision resolution, updates, deletions, and the important aspect of resizing to maintain performance.

## Interview Questions

1.  **What is Quadratic Probing and what problem does it solve?**
    *   **Answer**: Quadratic Probing is a collision resolution technique used in hash tables that employ open addressing. When a hash function maps two different keys to the same index (a collision), quadratic probing finds the next available slot by adding a quadratic increment to the initial hash index. It primarily solves the problem of **primary clustering** that occurs in linear probing, where keys tend to form long contiguous blocks, slowing down operations.

2.  **How does Quadratic Probing differ from Linear Probing?**
    *   **Answer**: Both are open addressing techniques. Linear probing checks slots at $(h(key) + i) \pmod{table\_size}$, meaning it checks adjacent slots (steps of 1, 2, 3...). Quadratic probing checks slots at $(h(key) + i^2) \pmod{table\_size}$ (steps of 1, 4, 9...). The key difference is the step size: linear probing uses a constant step, while quadratic probing uses an increasing, non-linear step, which helps to spread out keys more effectively and reduce primary clustering.

3.  **Explain the formula for Quadratic Probing.**
    *   **Answer**: The formula for the $i$-th probe location is $h(key, i) = (h(key) + c_1 \cdot i + c_2 \cdot i^2) \pmod{table\_size}$.
        *   $h(key)$ is the initial hash value.
        *   $i$ is the probe number (starting from 0 for the initial hash, then 1, 2, 3...).
        *   $c_1$ and $c_2$ are constants, often simplified to $c_1=0$ and $c_2=1$, resulting in $h(key, i) = (h(key) + i^2) \pmod{table\_size}$.
        *   $\pmod{table\_size}$ ensures the index wraps around within the table bounds.

4.  **What is primary clustering, and how does Quadratic Probing mitigate it?**
    *   **Answer**: Primary clustering is a phenomenon in linear probing where collisions lead to the formation of large, contiguous blocks of occupied slots. New insertions or searches that hash into or near these blocks have to traverse the entire cluster, degrading performance. Quadratic probing mitigates this by using a quadratic step size ($i^2$), which causes probes to jump further away from the initial collision point. This prevents keys from always filling adjacent slots, thus breaking up the long contiguous clusters.

5.  **What is secondary clustering, and is Quadratic Probing susceptible to it?**
    *   **Answer**: Yes, quadratic probing is susceptible to secondary clustering. Secondary clustering occurs when multiple keys that hash to the *same initial index* ($h(key)$) will follow the *exact same probe sequence*. Even though these sequences don't form contiguous blocks like primary clustering, they still repeatedly collide with each other along their shared probe path, leading to performance degradation.

6.  **What are the advantages of Quadratic Probing?**
    *   **Answer**:
        *   Effectively reduces primary clustering compared to linear probing.
        *   Distributes keys more evenly across the table.
        *   Generally offers better average-case performance than linear probing, especially at moderate load factors.
        *   Simpler to implement than double hashing.

7.  **What are the disadvantages or limitations of Quadratic Probing?**
    *   **Answer**:
        *   Suffers from secondary clustering.
        *   Does not guarantee finding an empty slot if the table's load factor exceeds 0.5 (even if empty slots exist), unless the table size is a prime number.
        *   Requires careful selection of table size (ideally a prime number) and load factor management (keep below 0.5) to ensure efficiency and correctness.
        *   Deletion is complex, requiring "tombstone" markers, which can degrade performance over time.
        *   Less cache-friendly than linear probing due to non-contiguous memory access.

8.  **What is the recommended load factor for a hash table using Quadratic Probing, and why?**
    *   **Answer**: The recommended load factor for quadratic probing is typically less than or equal to 0.5. This is because, if the table size is a prime number and the load factor is $\le 0.5$, quadratic probing is guaranteed to find an empty slot if one exists. Exceeding this load factor, especially with a non-prime table size, can lead to infinite loops or failure to find an empty slot even when the table is not full.

9.  **How does deletion work in a Quadratic Probing hash table?**
    *   **Answer**: Deletion in open addressing schemes like quadratic probing is tricky. Simply setting a deleted slot to `None` can break the search path for other keys that might have probed past that slot to reach their final destination. To solve this, a special "tombstone" marker (e.g., a `DELETED` sentinel object) is used. When an item is deleted, its slot is marked with this tombstone. During search, the algorithm treats tombstone slots as occupied (continues probing) but during insertion, it treats them as empty (can overwrite them). This adds complexity and can degrade performance over time if many tombstones accumulate, necessitating periodic re-hashing.

10. **When would you choose Quadratic Probing over Linear Probing or Separate Chaining?**
    *   **Answer**:
        *   **Over Linear Probing**: Choose quadratic probing when primary clustering is a significant concern, and you need better average-case performance for insertions and searches, especially with moderate load factors.
        *   **Over Separate Chaining**: Choose quadratic probing (or any open addressing) when memory locality is a concern (though linear probing is better for this), or when you want to avoid the overhead of pointers and dynamic memory allocation associated with linked lists in separate chaining. However, separate chaining generally handles higher load factors better and simplifies deletion. Quadratic probing is a good middle-ground when you want to avoid primary clustering but find double hashing too complex or separate chaining's memory overhead undesirable.

## Quiz

1.  Which problem does Quadratic Probing primarily aim to solve that is prevalent in Linear Probing?
    A) Memory fragmentation
    B) Primary clustering
    C) Secondary clustering
    D) Hash function inefficiency

2.  What is the general formula for the $i$-th probe in Quadratic Probing (assuming $c_1=0, c_2=1$)?
    A) $(h(key) + i) \pmod{table\_size}$
    B) $(h(key) + i^2) \pmod{table\_size}$
    C) $(h(key) \cdot i) \pmod{table\_size}$
    D) $(h(key) - i^2) \pmod{table\_size}$

3.  If a hash table uses Quadratic Probing and has a load factor greater than 0.5, what is a potential issue?
    A) It will always lead to an infinite loop.
    B) It guarantees finding an empty slot faster.
    C) It might fail to find an empty slot even if one exists.
    D) It automatically switches to separate chaining.

4.  What is "secondary clustering" in the context of Quadratic Probing?
    A) The formation of long contiguous blocks of occupied cells.
    B) When multiple keys hash to different initial indices but follow the same probe sequence.
    C) When multiple keys hash to the same initial index and thus follow the exact same probe sequence.
    D) A problem that only occurs in separate chaining.

5.  When deleting an item from a hash table using Quadratic Probing, why is it generally not advisable to simply set the slot to `None`?
    A) It makes the table less cache-friendly.
    B) It can lead to primary clustering.
    C) It might break the search path for other items that probed past the deleted slot.
    D) It increases the table's load factor.

---

### Answer Key

1.  **B) Primary clustering**
    *   **Explanation**: Quadratic probing was specifically designed to mitigate primary clustering, which is the tendency for linear probing to form long runs of occupied slots.

2.  **B) $(h(key) + i^2) \pmod{table\_size}$**
    *   **Explanation**: This is the standard simplified formula for quadratic probing, where $i^2$ represents the quadratic offset from the initial hash.

3.  **C) It might fail to find an empty slot even if one exists.**
    *   **Explanation**: For quadratic probing to guarantee finding an empty slot (if one exists), the table size should be prime, and the load factor should be $\le 0.5$. Exceeding this can lead to situations where an empty slot is never reached by the probe sequence.

4.  **C) When multiple keys hash to the same initial index and thus follow the exact same probe sequence.**
    *   **Explanation**: Secondary clustering is a limitation of quadratic probing where keys with the same initial hash value will always follow the same sequence of probes, leading to repeated collisions among them.

5.  **C) It might break the search path for other items that probed past the deleted slot.**
    *   **Explanation**: In open addressing, if a slot is simply set to `None` after deletion, a subsequent search for a key that was placed further down the probe sequence (because it collided with the now-deleted item) would stop prematurely at the `None` slot, incorrectly concluding the key is not present. Tombstone markers are used to avoid this.

## Further Reading

1.  **"Introduction to Algorithms" by Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein (CLRS)**: Chapter on Hash Tables. This is a classic textbook for algorithms and data structures, providing a rigorous and detailed explanation of hashing, collision resolution techniques (including quadratic probing), and their mathematical analysis.
    *   *Note*: Look for the section on "Open Addressing" within the "Hash Tables" chapter.

2.  **GeeksforGeeks - Quadratic Probing**: A popular online resource for computer science topics. Their article on Quadratic Probing provides a clear explanation, examples, and often includes code snippets in various languages.
    *   [https://www.geeksforgeeks.org/quadratic-probing-in-hashing/](https://wwweksforgeeks.org/quadratic-probing-in-hashing/)

3.  **Wikipedia - Quadratic Probing**: Provides a good overview, mathematical details, and references to other related concepts in hashing.
    *   [https://en.wikipedia.org/wiki/Quadratic_probing](https://en.wikipedia.org/wiki/Quadratic_probing)