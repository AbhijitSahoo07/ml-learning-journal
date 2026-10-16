# Query Optimization

## Overview
Query Optimization is a fundamental process in database management systems (DBMS) and data processing frameworks that aims to find the most efficient way to execute a given query. When you write a query (e.g., in SQL) to retrieve data, there are often many different sequences of operations (called execution plans) that can produce the same result. Some plans might be incredibly fast, while others could take hours or even days, consuming vast amounts of computational resources.

The primary goal of query optimization is to analyze a query and determine the optimal execution plan – the one that minimizes resource consumption (like CPU, memory, and disk I/O) and execution time. This process is crucial for the performance and scalability of any data-intensive application, including those that power machine learning pipelines.

## What Problem It Solves
Query Optimization addresses several critical problems:

1.  **Slow Query Execution:** Without optimization, queries might be executed in a naive or inefficient manner, leading to unacceptably long response times, especially with large datasets.
2.  **High Resource Consumption:** Inefficient queries can hog CPU, memory, and disk I/O, impacting the performance of other operations on the database server and increasing operational costs.
3.  **Complexity of Data Access:** Users don't need to know the intricate details of how data is stored (e.g., which index to use, how to join tables efficiently). The optimizer abstracts this complexity, allowing users to focus on *what* data they want, not *how* to get it.
4.  **Scalability Challenges:** As datasets grow, the difference between an optimized and unoptimized query plan becomes exponentially larger. Optimization ensures that systems can handle increasing data volumes without a proportional increase in query time.

**Why is it needed in machine learning?**
Machine learning models are data-hungry. Training complex models often requires processing massive datasets, performing extensive feature engineering, and retrieving specific subsets of data for inference. If the underlying data access mechanisms (databases, data lakes, feature stores) are slow due to unoptimized queries:
*   **Data Loading becomes a bottleneck:** Retrieving data for training or evaluation can take hours, delaying the entire ML lifecycle.
*   **Feature Engineering is inefficient:** Complex transformations and aggregations on raw data, often expressed as queries, will run slowly.
*   **Model Training is stalled:** If data cannot be fed to the model efficiently, GPU/CPU resources might sit idle, wasting computational power.
*   **Real-time Inference suffers:** For online ML systems, slow data retrieval for feature lookups can lead to high latency, making real-time predictions impractical.

In essence, query optimization ensures that the data foundation for ML is robust, fast, and scalable, allowing ML engineers and data scientists to focus on model development rather than waiting for data.

## How It Works
Query optimization typically involves several phases, often orchestrated by a component called the "query optimizer" within a DBMS:

1.  **Parsing and Translation:**
    *   The user's SQL query is first parsed to check for syntax errors and translated into an internal, logical representation, often a relational algebra tree or a query graph. This representation describes *what* the query needs to do, without specifying *how*.

2.  **Algebraic Optimization (Logical Optimization):**
    *   In this phase, the optimizer applies a set of heuristic rules and equivalences from relational algebra to transform the logical query plan into an equivalent, but potentially more efficient, logical plan. These transformations don't consider the physical storage details (like indexes) but aim to reduce the amount of data processed or the number of operations.
    *   **Examples of rules:**
        *   **Predicate Pushdown:** Moving selection (WHERE clause) operations down the query tree so they are applied as early as possible, reducing the number of rows processed by subsequent operations (like joins).
        *   **Projection Pushdown:** Moving projection (SELECT clause) operations down, reducing the number of columns processed.
        *   **Join Reordering:** Changing the order of joins, as some join orders can be significantly more efficient than others, especially with multi-table joins.

3.  **Cost-Based Optimization (Physical Optimization):**
    *   This is the most complex and critical phase. The optimizer explores various physical execution strategies for the logically optimized plan. For each strategy, it estimates the "cost" (e.g., I/O operations, CPU cycles, network traffic) and chooses the one with the lowest estimated cost.
    *   **Key components:**
        *   **Access Path Selection:** Deciding how to retrieve data from tables (e.g., full table scan, using an index, which index to use).
        *   **Join Strategy Selection:** Choosing the algorithm for joining tables (e.g., nested loop join, hash join, sort-merge join).
        *   **Operator Ordering:** Deciding the order of operations like filtering, sorting, and aggregation.
    *   **To estimate costs, the optimizer relies heavily on:**
        *   **Database Statistics:** Information about the data itself, such as the number of rows in a table (cardinality), the distribution of values in columns (histograms), the number of distinct values, and index properties. These statistics are periodically collected and updated by the DBMS.
        *   **Cost Model:** A mathematical model that quantifies the cost of different physical operations (e.g., reading a page from disk, comparing two values, performing a hash).

4.  **Execution Plan Generation:**
    *   Once the optimal physical plan is chosen, the optimizer generates an executable plan, which is a detailed step-by-step instruction set for the database engine to follow. This plan specifies exactly which indexes to use, which join algorithms to apply, and in what order.

## Mathematical Intuition
The core of cost-based query optimization lies in estimating the cost of different execution plans. This involves two main mathematical concepts: **cardinality estimation** and **cost modeling**.

1.  **Cardinality Estimation:**
    *   This is the process of estimating the number of rows that will result from an operation (e.g., after a filter, after a join). Accurate cardinality estimates are crucial because they directly impact the estimated cost of subsequent operations.
    *   **Selectivity:** For a predicate (e.g., `WHERE age > 30`), selectivity is the fraction of rows that satisfy the predicate.
        *   For a simple equality predicate $P(A = v)$:
            $$ \text{Selectivity}(A=v) = \frac{\text{Number of rows where } A=v}{\text{Total number of rows}} $$
            This can be estimated using histograms or frequency counts stored in statistics.
        *   For a range predicate $P(A > v)$ or $P(A < v)$:
            $$ \text{Selectivity}(A > v) \approx \frac{\text{Max_value}(A) - v}{\text{Max_value}(A) - \text{Min_value}(A)} $$
            This assumes a uniform distribution, but histograms provide more accurate estimates.
        *   For conjunctions (AND) of independent predicates $P_1 \land P_2$:
            $$ \text{Selectivity}(P_1 \land P_2) = \text{Selectivity}(P_1) \times \text{Selectivity}(P_2) $$
        *   For disjunctions (OR) of independent predicates $P_1 \lor P_2$:
            $$ \text{Selectivity}(P_1 \lor P_2) = \text{Selectivity}(P_1) + \text{Selectivity}(P_2) - (\text{Selectivity}(P_1) \times \text{Selectivity}(P_2)) $$
    *   The estimated output cardinality for an operation is then:
        $$ \text{Estimated Output Cardinality} = \text{Input Cardinality} \times \text{Selectivity} $$

2.  **Cost Model:**
    *   The optimizer uses a cost function to assign a numerical cost to each operation in an execution plan. This cost is typically a weighted sum of various resource consumptions.
    *   A simplified cost function for an entire plan $P$ might look like:
        $$ C(P) = w_{IO} \cdot \text{IO_cost}(P) + w_{CPU} \cdot \text{CPU_cost}(P) + w_{NET} \cdot \text{Network_cost}(P) $$
        Where $w_{IO}$, $w_{CPU}$, $w_{NET}$ are weights reflecting the relative cost of each resource.
    *   **Examples of operation costs:**
        *   **Table Scan:** Cost is proportional to the number of data pages in the table.
            $$ C_{\text{TableScan}}(R) = \text{Number of pages in } R \times \text{Cost per page read} $$
        *   **Index Scan:** Cost depends on the depth of the index tree and the number of data pages pointed to by the index entries.
            $$ C_{\text{IndexScan}}(R, \text{Index}) = \text{Index traversal cost} + \text{Number of data pages accessed} \times \text{Cost per page read} $$
        *   **Join Operations:**
            *   **Nested Loop Join (NLJ):** For joining tables $R_1$ (outer) and $R_2$ (inner), the cost is roughly:
                $$ C_{\text{NLJ}}(R_1, R_2) \approx \text{Pages}(R_1) + (\text{Cardinality}(R_1) \times \text{Pages}(R_2)) $$
                This is very expensive if $R_1$ is large.
            *   **Hash Join:** Involves building a hash table on the smaller relation and probing it with the larger relation. Cost is roughly proportional to the sum of pages of both relations, plus hashing overhead.
            *   **Sort-Merge Join:** Involves sorting both relations on the join key, then merging them. Cost is dominated by sorting.

The optimizer explores a search space of possible execution plans, calculates the estimated cost for each, and selects the plan with the minimum cost. This search can be complex, often using dynamic programming or greedy algorithms to avoid exploring an astronomically large number of plans.

## Advantages
*   **Improved Performance:** Significantly reduces query execution time, leading to faster application responses and better user experience.
*   **Resource Efficiency:** Minimizes CPU, memory, and I/O usage, allowing the database to handle more concurrent queries and reducing hardware costs.
*   **Abstraction for Users:** Users can write declarative queries (what they want) without needing to know the physical storage details or optimal execution strategies (how to get it).
*   **Adaptability:** Optimizers can adapt to changes in data distribution, table sizes, and available indexes by re-evaluating query plans.
*   **Scalability:** Enables databases to handle ever-growing datasets and increasing query loads efficiently.
*   **Crucial for ML Pipelines:** Provides fast and efficient access to data, which is vital for timely feature engineering, model training, and inference in machine learning workflows.

## Disadvantages
*   **Optimizer Overhead:** For very simple queries, the time spent by the optimizer to find the "best" plan might sometimes exceed the time saved by executing that plan, adding a slight overhead.
*   **Reliance on Accurate Statistics:** The optimizer's effectiveness heavily depends on up-to-date and accurate database statistics. Stale or incorrect statistics can lead to suboptimal plan choices.
*   **Complexity:** Query optimizers are incredibly complex pieces of software, making them difficult to design, implement, and debug.
*   **Suboptimal Plans:** In certain complex scenarios (e.g., highly correlated data, complex subqueries, very large multi-table joins, or data skew not captured by statistics), the optimizer might still choose a suboptimal plan.
*   **Parameter Sensitivity:** Some optimizers can be sensitive to configuration parameters, requiring expert tuning.
*   **Limited Search Space:** Due to the combinatorial explosion of possible plans, optimizers often use heuristics or prune the search space, meaning they might not always find the *absolute* best plan, but a "good enough" one.

## Real World Applications
1.  **Relational Database Management Systems (RDBMS):** Every major RDBMS like **PostgreSQL, MySQL, Oracle, SQL Server, and DB2** has a sophisticated query optimizer at its core. When you execute a `SELECT`, `INSERT`, `UPDATE`, or `DELETE` statement, the optimizer kicks in to determine the most efficient way to perform the operation.
2.  **Big Data Processing Frameworks:** Tools designed for large-scale data processing, such as **Apache Spark SQL, Apache Hive, and Presto/Trino**, incorporate advanced query optimizers. These optimizers are crucial for efficiently processing petabytes of data across distributed clusters, translating high-level SQL or DataFrame operations into optimized physical execution plans (e.g., using techniques like predicate pushdown, join reordering, and intelligent shuffling).
3.  **Data Warehousing and Business Intelligence (BI) Tools:** In data warehouses, users run complex analytical queries (OLAP queries) that often involve aggregations over massive historical datasets. Query optimizers in these systems (e.g., Snowflake, Google BigQuery, Amazon Redshift) are specialized to handle such workloads, ensuring that BI dashboards and reports load quickly.
4.  **Feature Stores for Machine Learning:** Feature stores (like Feast, Hopsworks) are specialized data systems designed to serve features for ML models consistently and efficiently. Their underlying data retrieval mechanisms heavily rely on query optimization to quickly fetch the right features for training or real-time inference, often involving complex joins and filters across various data sources.
5.  **Search Engines and Information Retrieval Systems:** While not always SQL-based, the principles of query optimization are applied in search engines (e.g., Elasticsearch, Solr) to efficiently retrieve relevant documents. This involves optimizing the execution of search queries, ranking algorithms, and filtering operations to provide fast and accurate results.

## Python Example
As query optimization is typically an internal mechanism of a database or data processing engine, directly implementing a full-fledged optimizer in Python with standard ML libraries is beyond the scope of a beginner-friendly example. Instead, we'll demonstrate the *concept* of optimization by showing how different ways of expressing a data retrieval "query" in Pandas can lead to vastly different performance, mimicking how an optimizer chooses the most efficient execution path.

This example will compare two ways to filter a large Pandas DataFrame and measure their performance.

```python
import pandas as pd
import numpy as np
import time

# 1. Generate a dummy dataset
# We'll create a large DataFrame to make performance differences noticeable.
np.random.seed(42) # for reproducibility
data_size = 1_000_000 # 1 million rows

df = pd.DataFrame({
    'feature_A': np.random.rand(data_size) * 100, # Continuous feature
    'feature_B': np.random.randint(0, 10, data_size), # Categorical-like integer feature
    'feature_C': np.random.choice(['cat', 'dog', 'bird', 'fish', 'snake'], data_size), # String categorical feature
    'target': np.random.randint(0, 2, data_size) # Binary target variable
})

print("Original DataFrame head:")
print(df.head())
print(f"\nDataFrame size: {len(df)} rows\n")

# Define a "query": Filter rows where feature_A > 50, feature_B is even, and feature_C is 'cat'

# --- Approach 1: Chained Filtering (less optimized in some contexts) ---
# This approach applies filters sequentially. Pandas might create intermediate DataFrames,
# which can be less efficient for large datasets due to memory allocation and copying.
print("--- Approach 1: Chained Filtering ---")
start_time = time.time()

# First filter
filtered_df_1 = df[df['feature_A'] > 50]
# Second filter on the result of the first
filtered_df_1 = filtered_df_1[filtered_df_1['feature_B'] % 2 == 0]
# Third filter on the result of the second
filtered_df_1 = filtered_df_1[filtered_df_1['feature_C'] == 'cat']

end_time = time.time()
time_1 = end_time - start_time
print(f"Time taken: {time_1:.4f} seconds")
print(f"Resulting DataFrame size: {len(filtered_df_1)} rows\n")

# --- Approach 2: Combined Boolean Indexing (often more optimized) ---
# This approach creates a single boolean mask by combining all conditions
# using logical operators (& for AND, | for OR). Pandas can then apply this
# mask in a single pass, which is generally more efficient as it avoids
# intermediate DataFrame creation.
print("--- Approach 2: Combined Boolean Indexing ---")
start_time = time.time()

filtered_df_2 = df[
    (df['feature_A'] > 50) & # Condition 1
    (df['feature_B'] % 2 == 0) & # Condition 2
    (df['feature_C'] == 'cat') # Condition 3
]

end_time = time.time()
time_2 = end_time - start_time
print(f"Time taken: {time_2:.4f} seconds")
print(f"Resulting DataFrame size: {len(filtered_df_2)} rows\n")

# Verify that both approaches yield the same result
assert filtered_df_1.equals(filtered_df_2), "The results from both approaches are not identical!"
print("\nBoth approaches yield the same result (verified).")

# Compare performance
print("\n--- Performance Comparison ---")
if time_1 > time_2:
    print(f"Approach 2 (Combined Boolean Indexing) was {time_1 / time_2:.2f} times faster than Approach 1 (Chained Filtering).")
elif time_2 > time_1:
    print(f"Approach 1 (Chained Filtering) was {time_2 / time_1:.2f} times faster than Approach 2 (unlikely for this specific case).")
else:
    print("Both approaches took approximately the same amount of time.")

print("\nThis simple example illustrates how different ways of expressing a data retrieval 'query' can lead to different performance characteristics. A database query optimizer performs a much more sophisticated version of this, analyzing various execution plans (like using indexes, different join algorithms, etc.) and selecting the most efficient one based on cost models and statistics.")

```

**Explanation of the Python Example:**
The example simulates a "query" to filter a large Pandas DataFrame.
*   **Approach 1 (Chained Filtering):** Applies each filter condition sequentially. While seemingly intuitive, Pandas might create temporary copies of the DataFrame after each filter, which can be memory-intensive and slower for large datasets.
*   **Approach 2 (Combined Boolean Indexing):** Combines all filter conditions into a single boolean mask using the `&` (AND) operator. This mask is then applied to the DataFrame in one go. Pandas can often optimize this by processing all conditions in a single pass, leading to better performance.

By measuring the execution time for both, we observe that the combined boolean indexing approach is typically faster. This mirrors the core idea of query optimization: finding a more efficient *plan* (in this case, a more efficient way to express the filtering logic) to achieve the same result. A real database optimizer would consider many more factors, including indexes, join algorithms, and data distribution, to pick the truly optimal plan.

## Interview Questions

1.  **What is Query Optimization?**
    *   **Answer:** Query Optimization is the process of identifying the most efficient execution plan for a given database query. Its goal is to minimize resource consumption (CPU, I/O, memory) and execution time, ensuring that data is retrieved or manipulated as quickly as possible.

2.  **Why is Query Optimization important in database systems?**
    *   **Answer:** It's crucial for several reasons: it ensures fast query response times, reduces server load, improves system scalability, and allows users to write declarative queries without needing to understand the underlying physical storage details. Without it, even simple queries on large datasets could become prohibitively slow.

3.  **Briefly describe the main phases of query optimization.**
    *   **Answer:** The main phases are:
        1.  **Parsing and Translation:** The query is parsed for syntax and translated into an internal, logical representation (e.g., relational algebra tree).
        2.  **Algebraic Optimization (Logical Optimization):** The logical plan is transformed using relational algebra rules (e.g., predicate pushdown, join reordering) to an equivalent but more efficient logical plan.
        3.  **Cost-Based Optimization (Physical Optimization):** The optimizer explores various physical execution strategies for the logical plan, estimates their cost using statistics and a cost model, and selects the plan with the lowest estimated cost.
        4.  **Execution Plan Generation:** The chosen optimal physical plan is translated into an executable set of instructions for the database engine.

4.  **What is the role of statistics in query optimization?**
    *   **Answer:** Database statistics (e.g., number of rows, value distribution in columns via histograms, index information) are vital for cost-based optimization. They allow the optimizer to accurately estimate the cardinality (number of rows) resulting from operations and the selectivity of predicates. These estimates are then used in the cost model to predict the resource consumption of different execution plans.

5.  **Explain the difference between rule-based and cost-based optimization.**
    *   **Answer:**
        *   **Rule-based optimization (RBO):** Applies a fixed set of predefined heuristic rules to transform a query plan. These rules are general guidelines (e.g., "always push selections down"). It doesn't consider the actual data characteristics or resource costs. It's simpler but can be suboptimal.
        *   **Cost-based optimization (CBO):** Explores multiple execution plans, estimates the resource cost (I/O, CPU) for each plan based on database statistics and a cost model, and chooses the plan with the lowest estimated cost. It's more complex but generally produces much better plans. Modern DBMS primarily use CBO.

6.  **What is a query execution plan?**
    *   **Answer:** A query execution plan (or query plan) is a detailed, step-by-step sequence of operations that the database system will perform to execute a given query. It specifies how data will be accessed (e.g., full table scan, index scan), how tables will be joined (e.g., nested loop, hash join), the order of operations, and any sorting or aggregation steps. It's the output of the query optimizer.

7.  **How does an optimizer estimate the cost of an execution plan?**
    *   **Answer:** An optimizer estimates cost by:
        1.  **Cardinality Estimation:** Using database statistics (histograms, distinct value counts) to predict the number of rows that will result from each operation (e.g., after filtering or joining).
        2.  **Cost Model Application:** Applying a mathematical cost model that assigns a numerical cost (often in terms of I/O operations, CPU cycles, or a weighted combination) to each physical operation (e.g., reading a page, comparing values, hashing). The total cost of a plan is the sum of the costs of its individual operations, considering the estimated cardinalities.

8.  **What are some common strategies an optimizer uses to improve query performance?**
    *   **Answer:**
        *   **Predicate Pushdown:** Applying filters as early as possible to reduce the amount of data processed by subsequent operations.
        *   **Projection Pushdown:** Selecting only necessary columns early to reduce data transfer and memory usage.
        *   **Join Reordering:** Changing the order of joins to minimize intermediate result sizes.
        *   **Access Path Selection:** Choosing between a full table scan or using an index (and which index) to retrieve data.
        *   **Join Algorithm Selection:** Deciding which join algorithm (e.g., nested loop, hash join, sort-merge join) is most efficient for the given tables and join conditions.
        *   **Materialization/Caching:** Deciding whether to store intermediate results in memory or on disk.

9.  **When might a query optimizer choose a suboptimal plan?**
    *   **Answer:** A query optimizer might choose a suboptimal plan if:
        *   **Stale/Inaccurate Statistics:** The database statistics are outdated or don't accurately reflect the current data distribution.
        *   **Data Skew:** The data distribution is highly skewed, and the statistics don't capture this effectively.
        *   **Complex Queries:** The query is too complex, involving many joins, subqueries, or user-defined functions, making it difficult for the optimizer to explore all optimal paths.
        *   **Missing Indexes:** Necessary indexes are not present, forcing the optimizer to choose less efficient full table scans.
        *   **Optimizer Limitations:** The optimizer's cost model might not perfectly reflect real-world hardware performance, or its search algorithm might prune the optimal path too early.

10. **How does query optimization relate to machine learning workflows?**
    *   **Answer:** Query optimization is indirectly but critically important for ML workflows. ML models are data-intensive, requiring efficient access to large datasets for:
        *   **Feature Engineering:** Complex transformations and aggregations on raw data, often expressed as queries, need to run fast.
        *   **Model Training:** Efficient data loading ensures that training pipelines are not bottlenecked by data retrieval, allowing GPUs/CPUs to be fully utilized.
        *   **Inference:** For real-time ML, fast feature lookups via optimized queries are essential for low-latency predictions.
    *   By ensuring fast and efficient data access, query optimization forms the bedrock for scalable and performant ML pipelines.

## Quiz

1.  What is the primary goal of Query Optimization?
    A) To simplify SQL syntax for users.
    B) To ensure data integrity and consistency.
    C) To find the most efficient way to execute a query.
    D) To automatically generate new queries.

2.  Which of the following is NOT a typical phase in query optimization?
    A) Parsing and Translation.
    B) Algebraic Optimization.
    C) Model Training and Prediction.
    D) Cost-Based Optimization.

3.  What role do database statistics play in cost-based query optimization?
    A) They define the database schema.
    B) They help estimate the cost and selectivity of operations.
    C) They encrypt sensitive data.
    D) They are used to back up the database.

4.  If a query optimizer consistently chooses a suboptimal plan, what is a common reason?
    A) The query is too simple.
    B) The database statistics are outdated or inaccurate.
    C) The database has too few indexes.
    D) The user has insufficient permissions.

5.  How does Query Optimization indirectly benefit Machine Learning?
    A) It directly trains ML models faster.
    B) It optimizes the internal algorithms of ML models.
    C) It ensures efficient and fast access to data for ML feature engineering and training.
    D) It automatically selects the best ML model for a given task.

---

### Answer Key

1.  **C) To find the most efficient way to execute a query.**
    *   **Explanation:** The core purpose of query optimization is to determine the execution plan that minimizes resource usage and execution time, not to simplify syntax, ensure integrity, or generate new queries.

2.  **C) Model Training and Prediction.**
    *   **Explanation:** Model Training and Prediction are phases in a machine learning workflow, not directly part of the database query optimization process. The other options are standard phases.

3.  **B) They help estimate the cost and selectivity of operations.**
    *   **Explanation:** Statistics provide crucial information about data distribution and cardinality, which the optimizer uses to estimate how many rows an operation will produce and how much resource it will consume.

4.  **B) The database statistics are outdated or inaccurate.**
    *   **Explanation:** The optimizer relies heavily on accurate statistics to make informed decisions. If statistics are stale, its cost estimates will be wrong, leading to suboptimal plan choices. While missing indexes (C) can lead to suboptimal plans, outdated statistics are a more direct cause of the *optimizer choosing* a bad plan among available options.

5.  **C) It ensures efficient and fast access to data for ML feature engineering and training.**
    *   **Explanation:** Query optimization doesn't directly interact with ML model training or algorithms. Instead, it provides the critical foundation of fast and efficient data retrieval, which is essential for preparing data (feature engineering) and feeding it to ML models for training and inference.

## Further Reading

1.  **PostgreSQL Documentation - The Query Planner:** A detailed explanation of how a real-world query optimizer works in one of the most popular open-source databases.
    *   [https://www.postgresql.org/docs/current/sql-explain.html](https://www.postgresql.org/docs/current/sql-explain.html) (Start with `EXPLAIN` and then explore related sections on query planning.)

2.  **"Database System Concepts" by Silberschatz, Korth, Sudarshan:** A classic textbook for database systems. Chapter 13 (or similar, depending on edition) typically covers Query Processing and Optimization in depth.
    *   (Search for the latest edition online or in libraries. A good starting point for understanding the theoretical underpinnings.)

3.  **Apache Spark SQL Optimization:** For those interested in big data and ML, understanding how query optimization works in distributed systems like Spark is crucial.
    *   [https://spark.apache.org/docs/latest/sql-performance-tuning.html](https://spark.apache.org/docs/latest/sql-performance-tuning.html) (Focus on the "Optimization" sections.)