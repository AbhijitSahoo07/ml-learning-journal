# Extendible Hashing

## Overview
Extendible Hashing is a dynamic hashing technique used primarily in database management systems and file systems to efficiently store and retrieve data on disk. Unlike static hashing methods, which have a fixed number of buckets, Extendible Hashing can grow or shrink dynamically as data is added or removed, preventing performance degradation due to excessive collisions and long overflow chains.

At its core, Extendible Hashing uses a two-level structure:
1.  **A Directory**: This is an array of pointers (or references) to data buckets. The size of the directory can double when needed.
2.  **Data Buckets**: These are fixed-size storage units that hold the actual data records. Each bucket has a "local depth" associated with it, indicating how many bits of the hash value are used to determine which records belong to that specific bucket.

The key idea is to use a portion of the hash value (determined by a "global depth") to index into the directory, which then points to the correct data bucket. When a bucket overflows, it splits, and the directory might also expand if the split requires more addressable space than currently available. This dynamic nature ensures that the average number of disk accesses for a search operation remains low, typically one or two, even with a growing dataset.

## What Problem It Solves
Extendible Hashing addresses several critical problems inherent in traditional static hashing and even some dynamic hashing schemes:

1.  **Fixed Size Limitations of Static Hashing**:
    *   **Problem**: Static hashing schemes (like simple modulo hashing) allocate a fixed number of buckets at the beginning. If the dataset grows significantly beyond the initial capacity, buckets become overfilled, leading to many collisions.
    *   **Consequence**: This results in long overflow chains (e.g., using linked lists for overflow), drastically increasing the number of disk I/O operations required to find a record, thus degrading performance. Rebuilding the entire hash table with a larger size is an expensive operation.
    *   **Extendible Hashing Solution**: It dynamically adjusts its structure (directory and buckets) to accommodate growth without needing a full rebuild, maintaining efficient access times.

2.  **Inefficient Space Utilization**:
    *   **Problem**: If a static hash table is sized for peak load, it might be sparsely populated for much of its lifetime, wasting disk space. If it's sized for average load, it will suffer performance issues during peak loads.
    *   **Extendible Hashing Solution**: It only allocates buckets as needed, and the directory expands incrementally, leading to better average space utilization over time.

3.  **Performance Degradation with Growth**:
    *   **Problem**: As data is inserted into a static hash table, the average number of probes (or disk accesses) to find a record increases.
    *   **Extendible Hashing Solution**: By allowing the directory and buckets to split and grow, Extendible Hashing aims to keep the average number of disk accesses (typically 1-2) constant, regardless of the dataset size, ensuring consistent performance.

4.  **Complexity of Linear Hashing's Overflow Handling**:
    *   **Problem**: Linear Hashing, another dynamic scheme, handles overflow by splitting buckets sequentially, which might not be the bucket that actually overflowed. This can lead to temporary performance dips and requires more complex overflow chains.
    *   **Extendible Hashing Solution**: When a bucket overflows, *that specific bucket* is split, directly addressing the collision issue where it occurs. This often leads to more localized and efficient resolution of overflows.

In machine learning contexts, while Extendible Hashing isn't an ML algorithm itself, it's a crucial data structure for managing large datasets that ML models operate on. For instance:
*   **Feature Stores**: Efficiently retrieving specific features for model training or inference from a large feature store.
*   **Database Indexing**: Underlying indexing mechanisms in databases that store training data or model outputs.
*   **Caching Systems**: Implementing high-performance caches for frequently accessed data or model predictions.
*   **Distributed Systems**: Concepts of dynamic partitioning and addressing can be seen in distributed hash tables (DHTs) which are fundamental in large-scale ML infrastructure.

## How It Works

Extendible Hashing operates using a directory and a set of data buckets. Let's break down its mechanism step-by-step:

**Core Components:**

1.  **Hash Function**: A function $h(key)$ that maps a key to a fixed-size integer (e.g., 32-bit or 64-bit).
2.  **Global Depth (GD)**: An integer representing the number of bits from the hash value used to index into the directory. The directory size is $2^{GD}$.
3.  **Directory**: An array of pointers, where each entry points to a data bucket.
4.  **Data Bucket**: A fixed-size storage unit that holds key-value pairs. Each bucket has:
    *   **Local Depth (LD)**: An integer representing the number of bits from the hash value that *this specific bucket* uses to distinguish its contents. $LD \le GD$.
    *   **Capacity**: The maximum number of records a bucket can hold.

**Operations:**

### 1. Initialization

*   Start with a global depth $GD = 0$ or $GD = 1$.
*   Create a directory of size $2^{GD}$ (e.g., 1 or 2 entries).
*   Create one or two initial empty buckets. All directory entries point to these initial buckets.
*   Each initial bucket has a local depth $LD = GD$.

### 2. Insertion of a Key-Value Pair $(K, V)$

1.  **Hash the Key**: Compute the hash value $H = h(K)$.
2.  **Determine Directory Index**: Take the last $GD$ bits of $H$ to get the directory index $I$.
    *   For example, if $GD=2$, and $H = \dots 10110_2$, the index would be $10_2 = 2$.
3.  **Access Directory**: Go to `Directory[I]` to find the pointer to the target bucket $B$.
4.  **Check Bucket Capacity**:
    *   **If $B$ has space**: Insert $(K, V)$ into $B$. Done.
    *   **If $B$ is full (overflow)**: A split operation is required.
        *   **Increment Local Depth**: Increment $B$'s local depth: $B.LD \leftarrow B.LD + 1$.
        *   **Check Global Depth vs. Local Depth**:
            *   **Case 1: $B.LD \le GD$ (Local depth is less than or equal to global depth)**
                *   This means there's enough addressable space in the current directory to distinguish between the old bucket and the new one.
                *   Create a `NewBucket` with $NewBucket.LD = B.LD$.
                *   **Redistribute Records**: Rehash all records (including the new one) from $B$ into $B$ and `NewBucket` using the *new* $B.LD$ bits. Records whose hash values end with the original $B.LD-1$ bits followed by a `0` go to $B$, and those ending with `1` go to `NewBucket`.
                *   **Update Directory Pointers**: Identify all directory entries that previously pointed to $B$. Some of these will now point to $B$, and others will point to `NewBucket`, based on their $B.LD$-bit suffix.
                    *   Specifically, if $B.LD$ is the new local depth, then all directory entries $I'$ such that the last $B.LD$ bits of $I'$ match the suffix of $B$'s original records will be split. Those ending with `0` (at the $B.LD$-th bit) will point to $B$, and those ending with `1` will point to `NewBucket`.
            *   **Case 2: $B.LD > GD$ (Local depth is greater than global depth)**
                *   This means the current directory is not large enough to distinguish the new bucket. The directory itself must expand.
                *   **Double Directory Size**: Increment $GD \leftarrow GD + 1$. Create a new directory twice the size of the old one. Copy all pointers from the old directory to the new one, effectively duplicating each pointer.
                    *   For example, if `Directory[I]` pointed to `Bucket X`, then in the new directory, `Directory[I]` and `Directory[I + 2^(GD-1)]` will both point to `Bucket X`.
                *   Now, the condition $B.LD \le GD$ holds (since $B.LD$ was just incremented to $GD+1$, and $GD$ was incremented to $GD+1$, so $B.LD = GD$). Proceed with the bucket splitting and redistribution as in Case 1.

### 3. Search for a Key $K$

1.  **Hash the Key**: Compute $H = h(K)$.
2.  **Determine Directory Index**: Take the last $GD$ bits of $H$ to get the directory index $I$.
3.  **Access Directory**: Go to `Directory[I]` to find the pointer to the target bucket $B$.
4.  **Search Bucket**: Search for $K$ within $B$. If found, return its value; otherwise, $K$ is not present.

### 4. Deletion of a Key $K$

Deletion is possible but more complex, especially regarding bucket merging and directory shrinking.
1.  **Search for $K$**: Locate the bucket $B$ containing $K$.
2.  **Remove $K$**: Delete $K$ from $B$.
3.  **Optional Merging**: If $B$ becomes underfull or empty, it might be merged with a "buddy" bucket (a bucket that split from $B$ previously and shares the same $LD-1$ prefix). If all buckets can be merged such that their $LD$ is less than $GD$, the directory can potentially shrink. This merging logic is often omitted in basic implementations due to its complexity.

## Mathematical Intuition

The mathematical intuition behind Extendible Hashing revolves around bit manipulation of hash values and the relationship between global depth ($GD$) and local depth ($LD$).

Let $h(key)$ be a hash function that produces a sufficiently long sequence of bits. For simplicity, let's assume it produces a 32-bit integer.

1.  **Directory Size and Global Depth**:
    The global depth, $GD$, determines the number of bits from the hash value used to index the directory.
    The size of the directory is $2^{GD}$.
    If $GD=1$, the directory has $2^1=2$ entries.
    If $GD=2$, the directory has $2^2=4$ entries.
    And so on.
    The index $I$ into the directory is derived from the last $GD$ bits of the hash value $H$:
    $$I = H \pmod{2^{GD}}$$
    or, more precisely, by masking the last $GD$ bits:
    $$I = H \ \& \ (2^{GD} - 1)$$
    This means that all keys whose hash values end with the same $GD$ bits will initially map to the same directory entry.

2.  **Bucket Identification and Local Depth**:
    Each bucket $B$ has a local depth, $LD_B$. This $LD_B$ indicates how many bits of the hash value are *actually used* to determine which records belong to *this specific bucket*.
    All records within a bucket $B$ must share the same suffix of $LD_B$ bits in their hash values.
    For example, if $LD_B=2$, all records in $B$ might have hash values ending in `01`.
    Crucially, $LD_B \le GD$. This means a bucket might be pointed to by multiple directory entries if $LD_B < GD$.
    If $LD_B < GD$, then $2^{GD - LD_B}$ directory entries will point to the same bucket $B$. These entries will have hash suffixes that match the $LD_B$ bits of $B$, but differ in the higher $GD - LD_B$ bits.
    For example, if $GD=3$ and $LD_B=2$, and $B$ stores records ending in `01`, then directory entries corresponding to hash suffixes `001` and `101` (i.e., $1$ and $5$) would both point to $B$.

3.  **Bucket Splitting**:
    When a bucket $B$ overflows, its local depth $LD_B$ is incremented to $LD_B'$.
    The records in $B$ are then redistributed based on the new $LD_B'$ bits.
    If the original $LD_B$ was $k$, and all records in $B$ ended with $b_{k-1} \dots b_0$, then after incrementing to $LD_B' = k+1$:
    *   Records whose hash values end with $0 b_{k-1} \dots b_0$ go to the original bucket $B$.
    *   Records whose hash values end with $1 b_{k-1} \dots b_0$ go to a new bucket, $B'$.
    This effectively splits the set of hash values that previously mapped to $B$ into two distinct sets.

4.  **Directory Doubling**:
    Directory doubling occurs when a bucket $B$ overflows, and its local depth $LD_B$ is already equal to the global depth $GD$.
    This means that $B$ is currently pointed to by only one directory entry (or a set of entries that all share the same $GD$-bit suffix). To split $B$ further, we need to use an additional bit, which means we need to increase the global depth.
    When $GD$ is incremented to $GD+1$, the directory size doubles from $2^{GD}$ to $2^{GD+1}$.
    Each old directory entry `Directory[I]` is effectively duplicated:
    *   `NewDirectory[I]` points to what `OldDirectory[I]` pointed to.
    *   `NewDirectory[I + 2^GD]` also points to what `OldDirectory[I]` pointed to.
    This ensures that all existing pointers are preserved, and new "slots" are created in the directory to accommodate future splits that require the additional bit. After doubling, the $GD$ is now equal to the new $LD_B$ (which was $GD+1$), allowing the bucket split to proceed as described in point 3.

The mathematical elegance lies in how the bitwise operations ensure that:
*   Keys are always directed to the correct bucket based on their hash suffix.
*   Splits are localized and efficient, only affecting the necessary buckets and directory pointers.
*   The directory only grows when absolutely necessary, minimizing wasted space while maintaining performance.

## Advantages

*   **Dynamic Resizing**: The hash table can grow and shrink dynamically, adapting to the number of records without requiring a complete rebuild.
*   **Consistent Performance**: On average, only one or two disk accesses are needed to retrieve a record, regardless of the database size. This is a significant improvement over static hashing with overflow chains.
*   **No Long Overflow Chains**: Unlike static hashing, Extendible Hashing avoids long chains of overflow buckets, which can severely degrade performance. When a bucket overflows, it splits, distributing its contents.
*   **Efficient Space Utilization**: Buckets are only created when needed, and the directory only doubles when a split requires more addressable space, leading to better average space utilization compared to pre-allocating a very large static hash table.
*   **Simple Search Operation**: The search operation is straightforward: hash, index directory, access bucket.

## Disadvantages

*   **Directory Can Grow Large**: In cases where data is highly skewed (many keys hash to similar prefixes), the directory can grow very large, potentially consuming significant memory, even if many buckets are empty or underutilized.
*   **Directory Doubling Cost**: Doubling the directory can be an expensive operation, as it involves allocating new memory and copying all existing pointers. While infrequent, it can cause temporary performance spikes.
*   **Potential for Empty/Underutilized Buckets**: After a split, one of the new buckets might remain empty or sparsely populated, leading to some wasted space.
*   **Complexity of Implementation**: Implementing Extendible Hashing, especially with deletion and potential directory shrinking/bucket merging, is more complex than static hashing.
*   **Not Ideal for Range Queries**: Like most hash-based structures, Extendible Hashing is optimized for exact-match lookups. It performs poorly for range queries (e.g., "find all keys between X and Y") because logically contiguous keys might be stored in physically distant buckets.

## Real World Applications

1.  **Database Indexing**: Extendible Hashing is a viable option for implementing hash indexes in database management systems (DBMS). While B-trees are more common for general-purpose indexing due to their efficiency with range queries, hash indexes (including those based on Extendible Hashing) are excellent for exact-match lookups, especially in scenarios where data is frequently accessed by a primary key. Some NoSQL databases or specialized key-value stores might leverage such dynamic hashing schemes.

2.  **File Systems**: Modern file systems often use various indexing and allocation strategies to manage files and directories efficiently. Extendible Hashing can be adapted to manage blocks on disk, mapping file names or block IDs to their physical locations, ensuring quick access to file data even as the file system grows.

3.  **Caching Systems**: High-performance caching systems (e.g., in-memory caches, distributed caches) require extremely fast lookups for cached objects. Extendible Hashing can be used to map cache keys to their corresponding data blocks or memory locations, providing near-constant time access for cache hits and efficient handling of cache growth.

4.  **Distributed Hash Tables (DHTs)**: While not a direct implementation, the core principles of dynamic resizing and distributed addressing in Extendible Hashing share conceptual similarities with Distributed Hash Tables (DHTs) used in peer-to-peer networks (like BitTorrent's DHT or Apache Cassandra's consistent hashing). DHTs need to dynamically add or remove nodes (analogous to buckets) and redistribute data while maintaining efficient lookup performance across a large, distributed system.

## Python Example

Implementing a full, robust Extendible Hashing system from scratch can be quite involved. For a beginner-friendly example, we'll create a simplified version focusing on the core logic of insertion, bucket splitting, and directory doubling. We'll use a simple hash function and `numpy` for potential bitwise operations (though standard Python integers handle this well).

```python
import numpy as np
import random

class Bucket:
    """Represents a data bucket in Extendible Hashing."""
    def __init__(self, capacity, local_depth):
        self.capacity = capacity
        self.records = [] # Stores (key, value) tuples
        self.local_depth = local_depth

    def is_full(self):
        return len(self.records) >= self.capacity

    def add_record(self, key, value):
        if not self.is_full():
            self.records.append((key, value))
            return True
        return False

    def find_record(self, key):
        for k, v in self.records:
            if k == key:
                return v
        return None

    def __str__(self):
        return f"Bucket(LD={self.local_depth}, Records={self.records})"

class ExtendibleHashing:
    """
    A simplified implementation of Extendible Hashing.
    Uses a simple hash function for demonstration.
    """
    def __init__(self, bucket_capacity=2, initial_global_depth=1):
        self.bucket_capacity = bucket_capacity
        self.global_depth = initial_global_depth
        
        # Initialize directory with 2^global_depth pointers
        # All pointers initially point to the same single bucket
        initial_bucket = Bucket(self.bucket_capacity, self.global_depth)
        self.directory = [initial_bucket] * (2 ** self.global_depth)
        
        # Keep track of unique buckets to avoid creating duplicates
        self.unique_buckets = {id(initial_bucket): initial_bucket}

    def _hash(self, key):
        """
        A simple hash function. For real-world, use a cryptographically
        stronger hash or a hash designed for distribution.
        We'll use Python's built-in hash and ensure it's positive.
        """
        return hash(key) & 0xFFFFFFFF # Ensure positive 32-bit hash

    def _get_directory_index(self, hashed_key):
        """
        Calculates the directory index using the last 'global_depth' bits.
        """
        return hashed_key & ((1 << self.global_depth) - 1)

    def _get_bucket_suffix(self, hashed_key, depth):
        """
        Calculates the suffix for a bucket using 'depth' bits.
        """
        return hashed_key & ((1 << depth) - 1)

    def insert(self, key, value):
        hashed_key = self._hash(key)
        
        while True: # Loop to handle potential directory doubling and re-insertion
            dir_index = self._get_directory_index(hashed_key)
            bucket = self.directory[dir_index]

            if not bucket.is_full():
                bucket.add_record(key, value)
                print(f"Inserted ({key}, {value}) into bucket at index {dir_index} (LD={bucket.local_depth})")
                return
            else:
                # Bucket is full, need to split
                print(f"Bucket at index {dir_index} (LD={bucket.local_depth}) is full. Splitting...")

                if bucket.local_depth == self.global_depth:
                    # Case 1: Local depth equals global depth, need to double directory
                    print(f"Global depth ({self.global_depth}) == Local depth ({bucket.local_depth}). Doubling directory.")
                    self._double_directory()
                    # After doubling, the global_depth has increased, so re-calculate dir_index
                    dir_index = self._get_directory_index(hashed_key)
                    # The loop will continue, and now the condition bucket.local_depth < self.global_depth will be true
                    # for the *original* bucket, allowing it to split without further directory doubling.
                    # We don't break here, we let the loop re-evaluate with the new global_depth.
                
                # Case 2: Local depth is less than global depth, or directory just doubled
                # Split the bucket
                bucket.local_depth += 1
                new_bucket = Bucket(self.bucket_capacity, bucket.local_depth)
                self.unique_buckets[id(new_bucket)] = new_bucket
                print(f"New bucket created with LD={new_bucket.local_depth}")

                # Redistribute records from the old bucket to the old and new buckets
                old_records = list(bucket.records) # Make a copy
                bucket.records = [] # Clear old bucket
                
                print(f"Redistributing records from old bucket (LD={bucket.local_depth-1} -> {bucket.local_depth}): {old_records}")
                for r_key, r_value in old_records:
                    r_hashed_key = self._hash(r_key)
                    if self._get_bucket_suffix(r_hashed_key, bucket.local_depth) == self._get_bucket_suffix(hashed_key, bucket.local_depth):
                        # This condition is a bit tricky. The new bucket suffix is determined by the new local_depth.
                        # We need to check the (local_depth-1)-th bit (the new distinguishing bit).
                        # If the (local_depth-1)-th bit is 0, it goes to the original bucket.
                        # If the (local_depth-1)-th bit is 1, it goes to the new bucket.
                        
                        # The suffix for the original bucket (after split) will have the (LD-1)-th bit as 0
                        # The suffix for the new bucket will have the (LD-1)-th bit as 1
                        
                        # Let's use the full suffix for clarity
                        if (r_hashed_key >> (bucket.local_depth - 1)) & 1 == 0: # Check the new distinguishing bit
                            bucket.add_record(r_key, r_value)
                        else:
                            new_bucket.add_record(r_key, r_value)
                    else:
                        # This record doesn't belong to the current split path.
                        # This scenario shouldn't happen if the directory pointers are correct.
                        # For simplicity, we'll re-add based on the new local_depth.
                        if (r_hashed_key >> (bucket.local_depth - 1)) & 1 == 0:
                            bucket.add_record(r_key, r_value)
                        else:
                            new_bucket.add_record(r_key, r_value)

                # Update directory pointers
                # All directory entries that previously pointed to the old bucket
                # and now match the new local_depth suffix for the new bucket,
                # should point to the new bucket.
                
                # The original bucket's suffix (up to LD-1 bits) is shared.
                # The new distinguishing bit (LD-1) determines which bucket.
                
                # Find the common prefix for the buckets
                common_prefix_mask = (1 << (bucket.local_depth - 1)) - 1
                common_prefix = self._get_bucket_suffix(hashed_key, bucket.local_depth - 1)

                # Iterate through directory entries and update pointers
                for i in range(len(self.directory)):
                    if self.directory[i] is bucket: # Only update if it points to the old bucket
                        # Check the (local_depth-1)-th bit of the directory index 'i'
                        if (i >> (bucket.local_depth - 1)) & 1 == 0:
                            # This index should point to the original bucket (ending with 0 at new bit)
                            self.directory[i] = bucket
                        else:
                            # This index should point to the new bucket (ending with 1 at new bit)
                            self.directory[i] = new_bucket
                
                # Now, re-attempt to insert the original key-value pair
                # The loop will continue, and the key will be inserted into the correct (newly split) bucket.

    def _double_directory(self):
        """Doubles the directory size and updates global depth."""
        old_directory = self.directory
        self.global_depth += 1
        new_directory_size = 2 ** self.global_depth
        self.directory = [None] * new_directory_size

        for i in range(len(old_directory)):
            # Each old entry now maps to two new entries
            self.directory[i] = old_directory[i]
            self.directory[i + (1 << (self.global_depth - 1))] = old_directory[i]
        print(f"Directory doubled. New global depth: {self.global_depth}")

    def search(self, key):
        hashed_key = self._hash(key)
        dir_index = self._get_directory_index(hashed_key)
        bucket = self.directory[dir_index]
        
        print(f"Searching for key '{key}' (hashed: {hashed_key}) in bucket at index {dir_index} (LD={bucket.local_depth})...")
        value = bucket.find_record(key)
        if value is not None:
            print(f"Found: ({key}, {value})")
        else:
            print(f"Key '{key}' not found.")
        return value

    def print_state(self):
        print("\n--- Extendible Hashing State ---")
        print(f"Global Depth: {self.global_depth}")
        print(f"Directory Size: {len(self.directory)}")
        
        # Use a set to print each unique bucket only once
        printed_buckets = set()
        for i, bucket in enumerate(self.directory):
            if id(bucket) not in printed_buckets:
                print(f"  Bucket (ID: {id(bucket)}) - LD: {bucket.local_depth}, Records: {bucket.records}")
                printed_buckets.add(id(bucket))
        
        print("\nDirectory Mapping:")
        for i, bucket in enumerate(self.directory):
            # Show the binary representation of the index for clarity
            binary_index = bin(i)[2:].zfill(self.global_depth)
            print(f"  Index {i} (binary: {binary_index}) -> Bucket (ID: {id(bucket)})")
        print("------------------------------\n")

# --- Demonstration ---
if __name__ == "__main__":
    print("Initializing Extendible Hashing with bucket capacity 2 and initial global depth 1.")
    eh = ExtendibleHashing(bucket_capacity=2, initial_global_depth=1)
    eh.print_state()

    # Insert some data
    data_to_insert = [
        ("apple", 10), ("banana", 20), ("cherry", 30), ("date", 40),
        ("elderberry", 50), ("fig", 60), ("grape", 70), ("honeydew", 80)
    ]

    for key, value in data_to_insert:
        print(f"\n--- Inserting ({key}, {value}) ---")
        eh.insert(key, value)
        eh.print_state()

    # Search for existing and non-existing keys
    print("\n--- Searching for keys ---")
    eh.search("banana")
    eh.search("grape")
    eh.search("kiwi") # Non-existent

    # Demonstrate more insertions to force more splits and directory doubling
    print("\n--- Inserting more data to force further splits ---")
    eh.insert("lemon", 90)
    eh.print_state()
    eh.insert("mango", 100)
    eh.print_state()
    eh.insert("nectarine", 110)
    eh.print_state()
    eh.insert("orange", 120)
    eh.print_state()
    eh.insert("pear", 130)
    eh.print_state()
```

**Explanation of the Python Example:**

1.  **`Bucket` Class**: A simple class to represent a data bucket. It holds `records` (list of key-value tuples), `capacity`, and `local_depth`. It has methods to check if it's full, add a record, and find a record.
2.  **`ExtendibleHashing` Class**:
    *   **`__init__`**: Initializes the system with a `bucket_capacity` and `initial_global_depth`. It creates the initial directory and a single bucket that all directory entries point to. `unique_buckets` dictionary helps in tracking distinct bucket objects.
    *   **`_hash(self, key)`**: A basic hash function using Python's built-in `hash()`. In a real system, a more robust and distribution-friendly hash function would be used. We mask it to 32 bits and ensure it's positive.
    *   **`_get_directory_index(self, hashed_key)`**: Computes the directory index by taking the last `global_depth` bits of the hashed key.
    *   **`_get_bucket_suffix(self, hashed_key, depth)`**: Helper to get the suffix of a hash value up to a given `depth`.
    *   **`insert(self, key, value)`**: This is the core logic.
        *   It uses a `while True` loop to handle cases where a directory doubling occurs, requiring a re-evaluation of the directory index and re-attempting the insertion.
        *   If the target bucket is not full, the record is added.
        *   If the bucket is full:
            *   It checks if `bucket.local_depth == self.global_depth`. If true, the directory must double first (`_double_directory()`).
            *   Then, the bucket's `local_depth` is incremented.
            *   A `new_bucket` is created.
            *   All records from the *old* bucket are re-hashed and redistributed between the `old_bucket` and `new_bucket` based on the *new* `local_depth`'s distinguishing bit.
            *   Finally, the `directory` pointers are updated to point to the correct `old_bucket` or `new_bucket` based on their index's suffix.
    *   **`_double_directory(self)`**: Creates a new directory twice the size, copies pointers, and increments `global_depth`.
    *   **`search(self, key)`**: Hashes the key, finds the directory index, and searches within the pointed-to bucket.
    *   **`print_state(self)`**: A utility function to visualize the current state of the directory and buckets, showing global depth, local depths, and record contents.

This example provides a clear, step-by-step simulation of how Extendible Hashing dynamically manages data storage and retrieval, demonstrating its key features like bucket splitting and directory doubling.

## Interview Questions

Here are 10 relevant technical interview questions about Extendible Hashing, complete with comprehensive answers:

1.  **Q: What is Extendible Hashing, and what problem does it primarily solve?**
    *   **A:** Extendible Hashing is a dynamic hashing technique that allows a hash table to grow or shrink gracefully as data is inserted or deleted, without requiring a complete rehashing of all records. It primarily solves the problem of performance degradation in static hashing schemes due to bucket overflows and long overflow chains when the dataset size changes significantly. It maintains efficient (typically 1-2 disk accesses) retrieval performance regardless of data volume.

2.  **Q: Explain the two main components of an Extendible Hashing structure.**
    *   **A:** The two main components are:
        1.  **Directory**: An array of pointers (or references) to data buckets. Its size is $2^{GD}$, where $GD$ is the global depth. The directory can double in size when needed.
        2.  **Data Buckets**: Fixed-size storage units that hold the actual key-value pairs. Each bucket has a `local depth (LD)` associated with it, indicating how many bits of the hash value are used to determine which records belong to that specific bucket.

3.  **Q: Differentiate between Global Depth (GD) and Local Depth (LD) in Extendible Hashing.**
    *   **A:**
        *   **Global Depth (GD)**: This is a property of the *entire hash structure*. It represents the number of bits from the hash value that are used to index into the directory. The directory size is $2^{GD}$. All directory entries use the global depth to determine their position.
        *   **Local Depth (LD)**: This is a property of an *individual data bucket*. It represents the number of bits from the hash value that are *actually used* to distinguish the records stored within that specific bucket. All records in a bucket must share the same suffix of $LD$ bits.
        *   **Relationship**: $LD \le GD$. If $LD < GD$, it means multiple directory entries (which differ in their higher bits beyond $LD$) point to the same bucket. If $LD = GD$, then only one directory entry points to that specific bucket.

4.  **Q: Describe the process of inserting a new record into an Extendible Hashing structure, specifically focusing on bucket overflow.**
    *   **A:**
        1.  **Hash**: Compute the hash value $H$ of the new key.
        2.  **Find Bucket**: Use the last $GD$ bits of $H$ to find the directory index $I$, and follow the pointer to the target bucket $B$.
        3.  **Check Capacity**: If $B$ has space, insert the record.
        4.  **Handle Overflow**: If $B$ is full:
            *   Increment $B$'s local depth: $B.LD \leftarrow B.LD + 1$.
            *   **If $B.LD > GD$**: This means the directory is not large enough to distinguish the new bucket. The directory must double. Increment $GD \leftarrow GD + 1$. Create a new directory twice the size, copying old pointers (each old entry maps to two new entries).
            *   **Split Bucket**: Create a `NewBucket` with $NewBucket.LD = B.LD$. Redistribute all records (including the new one) from $B$ into $B$ and `NewBucket` based on the new $B.LD$ bits (specifically, the new distinguishing bit).
            *   **Update Directory**: Update the directory pointers. All directory entries that previously pointed to $B$ and now match the suffix for `NewBucket` (based on $B.LD$) are updated to point to `NewBucket`. Other relevant entries continue to point to $B$.
            *   The insertion then effectively retries with the new structure.

5.  **Q: When does the directory in Extendible Hashing double, and what is the cost associated with this operation?**
    *   **A:** The directory doubles when a bucket overflows, and its local depth ($LD$) is already equal to the global depth ($GD$). This signifies that the current directory size ($2^{GD}$) is insufficient to create a new, distinct pointer for the split bucket, as all $GD$ bits are already being used to address the current bucket.
    *   **Cost**: Directory doubling involves:
        *   Allocating a new directory array twice the size of the old one.
        *   Copying all pointers from the old directory to the new one (each old pointer is duplicated).
        *   Updating the global depth.
        While this operation is $O(2^{GD})$ or $O(N_{directory})$, it's relatively infrequent compared to bucket splits and amortized over many insertions. It can cause a temporary performance spike but ensures continued efficient access.

6.  **Q: What are the main advantages of Extendible Hashing over static hashing?**
    *   **A:**
        *   **Dynamic Sizing**: Adapts to data growth/shrinkage without full rehashing.
        *   **Consistent Performance**: Maintains low average disk accesses (1-2) regardless of dataset size.
        *   **No Long Overflow Chains**: Splits buckets to resolve collisions, avoiding performance degradation.
        *   **Better Space Utilization**: Only allocates buckets and expands the directory as needed.

7.  **Q: What are some disadvantages or limitations of Extendible Hashing?**
    *   **A:**
        *   **Large Directory**: The directory can become very large if data is skewed, potentially consuming significant memory.
        *   **Directory Doubling Cost**: While infrequent, doubling the directory is an $O(2^{GD})$ operation that can be costly.
        *   **Potential for Empty Buckets**: After a split, one of the new buckets might remain empty or sparsely populated, leading to some wasted space.
        *   **Complexity**: Implementation is more complex than static hashing, especially for deletion and merging.
        *   **Poor for Range Queries**: Like other hash-based structures, it's not efficient for range-based searches.

8.  **Q: How does Extendible Hashing ensure that the average number of disk accesses remains low?**
    *   **A:** Extendible Hashing ensures low disk accesses by dynamically adjusting its structure. When a bucket overflows, it splits, distributing its contents and preventing the formation of long overflow chains. The directory also expands when necessary to provide distinct pointers to these new buckets. This means that, ideally, a search operation involves one disk access to read the directory entry and a second disk access to read the target data bucket, keeping the average at 1-2 accesses.

9.  **Q: Can Extendible Hashing be used for deletion? If so, what are the complexities?**
    *   **A:** Yes, deletion is possible. The process involves:
        1.  Locating and removing the record from its bucket.
        2.  **Complexity**: The main complexity lies in potentially merging buckets and shrinking the directory. If a bucket becomes empty or underfull, it might be merged with its "buddy" bucket (the bucket it split from). If all buckets can be merged such that their local depths become less than the global depth, the directory *could* potentially shrink. However, implementing this merging and directory shrinking logic is significantly more complex than insertion, often involving tracking buddy buckets and checking conditions for merging and directory halving. Many practical implementations might omit directory shrinking for simplicity or rely on periodic garbage collection.

10. **Q: In what real-world scenarios or applications would Extendible Hashing be a suitable choice?**
    *   **A:** Extendible Hashing is suitable for applications requiring:
        *   **High-performance exact-match lookups**: Such as primary key indexing in databases or key-value stores.
        *   **Dynamic data growth**: Where the dataset size is unpredictable and can change significantly over time.
        *   **Minimizing disk I/O**: Critical for systems where data resides on disk and disk access is a bottleneck (e.g., file systems, large databases).
        *   **Caching systems**: For fast retrieval of cached objects based on their keys.
        It's particularly useful when range queries are not a primary concern.

## Quiz

1.  What is the primary advantage of Extendible Hashing over static hashing?
    A) It uses less memory overall.
    B) It provides efficient range queries.
    C) It dynamically adjusts its size to maintain consistent performance.
    D) It guarantees zero collisions.

2.  If the Global Depth (GD) is 3, what is the maximum number of entries in the directory?
    A) 3
    B) 6
    C) 8
    D) 16

3.  A bucket overflows, and its Local Depth (LD) is equal to the Global Depth (GD). What is the immediate next step in Extendible Hashing?
    A) The bucket is simply cleared.
    B) The directory size is doubled.
    C) The bucket is merged with another bucket.
    D) The global depth is decremented.

4.  Which of the following is a disadvantage of Extendible Hashing?
    A) Inability to handle deletions.
    B) Poor performance for exact-match lookups.
    C) The directory can grow very large, potentially wasting memory.
    D) It requires a full rehashing of all data on every insertion.

5.  If a bucket has a Local Depth (LD) of 2 and the Global Depth (GD) is 4, how many directory entries point to this single bucket?
    A) 1
    B) 2
    C) 4
    D) 8

---

### Answer Key

1.  **C) It dynamically adjusts its size to maintain consistent performance.**
    *   **Explanation**: The core strength of Extendible Hashing is its ability to grow or shrink, preventing performance degradation due to overflows, which is a major issue in static hashing.

2.  **C) 8**
    *   **Explanation**: The directory size is $2^{GD}$. If $GD=3$, then $2^3 = 8$.

3.  **B) The directory size is doubled.**
    *   **Explanation**: When $LD = GD$ and a bucket overflows, it means the current directory doesn't have enough distinct pointers to accommodate the split. Therefore, the directory must double to increase the global depth and provide more addressable space.

4.  **C) The directory can grow very large, potentially wasting memory.**
    *   **Explanation**: While efficient in many ways, a significant drawback is that the directory can become very large, especially with skewed data, leading to increased memory consumption.

5.  **C) 4**
    *   **Explanation**: If $LD < GD$, then $2^{GD - LD}$ directory entries point to the same bucket. In this case, $2^{4 - 2} = 2^2 = 4$. These 4 entries would share the same last 2 bits of their index but differ in the higher 2 bits.

## Further Reading

1.  **"Database System Concepts" by Silberschatz, Korth, and Sudarshan**: This classic textbook on database systems provides a detailed and accessible explanation of Extendible Hashing, often including diagrams and examples. Look for chapters on "Indexing and Hashing" or "File Structures."
2.  **"Introduction to Algorithms" by Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein (CLRS)**: While not solely focused on databases, CLRS covers hashing techniques in depth. You might find discussions on dynamic hashing that touch upon the principles behind Extendible Hashing, offering a more theoretical computer science perspective.
3.  **Online Course Materials / University Lectures**: Many universities offer free online course materials or lecture notes on data structures and database systems. Searching for "Extendible Hashing lecture notes" from reputable institutions (e.g., MIT, Stanford, UC Berkeley) can provide excellent supplementary explanations and visual aids. For example, a search for "Extendible Hashing Stanford" might lead to relevant course content.