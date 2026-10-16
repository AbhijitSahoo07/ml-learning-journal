# SQL Window Functions

## Overview
SQL Window Functions are a powerful feature in SQL that allow you to perform calculations across a set of table rows that are related to the current row. Unlike aggregate functions (like `SUM()`, `AVG()`, `COUNT()`) which collapse rows into a single summary row, window functions return a value for *each* row, similar to how a regular query returns a row for each record. The "window" refers to the set of rows on which the function operates, defined by the `OVER()` clause. This clause specifies how to partition the data (divide it into groups) and how to order the rows within each partition, allowing for sophisticated analytical calculations without reducing the number of rows returned by the query.

## What Problem It Solves
SQL Window Functions address several core problems and challenges in data analysis and preparation, especially relevant for machine learning:

1.  **Complex Analytical Calculations:** Before window functions, performing calculations like moving averages, cumulative sums, ranking within groups, or comparing a row's value to an average of its peers often required self-joins, subqueries, or complex procedural logic. These methods were often inefficient, difficult to read, and prone to errors.
2.  **Maintaining Row Granularity:** Standard aggregate functions (`GROUP BY`) summarize data, meaning you lose the individual row details. For example, if you want to calculate the average sales for each product category *and* still see each individual sale transaction, a `GROUP BY` query wouldn't work directly. Window functions allow you to perform aggregations while preserving the original row count and detail.
3.  **Feature Engineering for Machine Learning:** In machine learning, creating relevant features from raw data is crucial. Window functions are invaluable for generating time-series features (e.g., "sales over the last 7 days," "average customer spend in the last 3 transactions"), ranking features (e.g., "product's rank by sales within its category"), or comparative features (e.g., "deviation from category average"). These features can significantly improve model performance.
4.  **Performance and Readability:** By performing calculations in a single pass over the data, window functions are often more performant than equivalent solutions involving multiple self-joins or subqueries. They also make complex analytical queries much more readable and maintainable.
5.  **Handling Gaps and Trends:** They are excellent for identifying trends, calculating differences between consecutive rows (e.g., daily sales growth), or filling gaps in time-series data by looking at preceding or succeeding values.

In essence, window functions bridge the gap between row-level operations and aggregate operations, providing a flexible and efficient way to enrich datasets with contextual information, which is a common requirement in data science and machine learning workflows.

## How It Works
The core mechanism of SQL Window Functions revolves around the `OVER()` clause, which defines the "window" or set of rows on which the function operates. Let's break down its components:

1.  **Window Function Type:** This is the actual function you want to apply. There are three main categories:
    *   **Aggregate Window Functions:** These are standard aggregate functions (`SUM()`, `AVG()`, `COUNT()`, `MIN()`, `MAX()`) used as window functions. They calculate an aggregate value over the defined window for each row.
    *   **Ranking Window Functions:** These assign a rank to each row within its partition based on a specified order (`ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `NTILE()`).
    *   **Analytic Window Functions:** These perform calculations like fetching values from preceding or succeeding rows (`LAG()`, `LEAD()`), calculating first/last values (`FIRST_VALUE()`, `LAST_VALUE()`), or calculating cumulative distributions (`CUME_DIST()`, `PERCENT_RANK()`).

2.  **`OVER()` Clause:** This is where the magic happens. It defines the window for the function.
    *   **`PARTITION BY`:** This optional clause divides the result set into partitions (groups) based on one or more columns. The window function is applied independently to each partition. If `PARTITION BY` is omitted, the entire result set is treated as a single partition.
        *   *Analogy:* Imagine you have a list of students from different classes. `PARTITION BY class_id` would group students by their class. Any calculation would then be performed *within* each class, independently of other classes.
    *   **`ORDER BY`:** This optional clause specifies the logical order of rows within each partition (or the entire result set if no `PARTITION BY` is used). This is crucial for ranking functions and for functions that depend on the order of rows (like `LAG()`, `LEAD()`, `SUM()` for cumulative sums).
        *   *Analogy:* Within each class, `ORDER BY score DESC` would sort students by their score in descending order.
    *   **Window Frame Clause (Optional):** This further refines the set of rows within the current partition that the window function operates on. It defines a "sliding window" or "frame" relative to the current row.
        *   `ROWS` or `RANGE`: Specifies the frame based on a physical number of rows or a logical range of values.
        *   `BETWEEN <start_bound> AND <end_bound>`: Defines the start and end of the frame.
            *   `UNBOUNDED PRECEDING`: From the first row of the partition.
            *   `N PRECEDING`: N rows before the current row.
            *   `CURRENT ROW`: The current row.
            *   `N FOLLOWING`: N rows after the current row.
            *   `UNBOUNDED FOLLOWING`: To the last row of the partition.
        *   *Default Frame:* If no window frame is specified:
            *   For `ORDER BY` clauses: `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` (cumulative behavior).
            *   Without `ORDER BY` clauses: `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` (entire partition).

**Example Flow:**

Let's say you want to calculate the cumulative sales for each product category, ordered by date.

1.  **Data Input:** Your table has `product_category`, `sale_date`, `sale_amount`.
2.  **`PARTITION BY product_category`:** The database first divides all sales records into separate groups, one for each unique product category (e.g., 'Electronics', 'Clothing', 'Books').
3.  **`ORDER BY sale_date`:** Within each of these partitions, the rows are then sorted by `sale_date` in ascending order.
4.  **`SUM(sale_amount) OVER (PARTITION BY product_category ORDER BY sale_date)`:** For each row, the `SUM()` function is applied. The "window" for this `SUM()` operation includes all rows *within the current product category partition* that have a `sale_date` less than or equal to the current row's `sale_date` (due to the default cumulative frame when `ORDER BY` is present).
5.  **Output:** The query returns all original rows, but now each row has an additional column showing the cumulative sales up to that point for its respective product category.

This step-by-step process allows for highly flexible and powerful data transformations.

## Mathematical Intuition
While SQL Window Functions don't involve complex mathematical models like those in machine learning algorithms, their "mathematical intuition" lies in the precise definition and application of operations over dynamically defined subsets of data. The core idea is to apply a function (often an aggregate or ranking function) to a specific "window" of rows, rather than the entire dataset or a static `GROUP BY` group.

Let's break down the logic using common window function types:

1.  **Partitioning ($P$):**
    The `PARTITION BY` clause divides the dataset into disjoint subsets, $P_1, P_2, \dots, P_k$. Each partition is treated independently.
    If we have a table $T$ with rows $r_1, r_2, \dots, r_N$, and we partition by a column $C$, then $T = P_1 \cup P_2 \cup \dots \cup P_k$, where $P_i \cap P_j = \emptyset$ for $i \neq j$.
    All calculations for a row $r \in P_i$ will only consider other rows within $P_i$.

2.  **Ordering ($O$):**
    Within each partition $P_i$, the `ORDER BY` clause establishes a specific sequence for the rows. Let's say for a partition $P_i$, the rows are ordered as $r_{i,1}, r_{i,2}, \dots, r_{i,m_i}$. This ordering is crucial for functions that depend on sequence (like cumulative sums, ranks, or fetching previous/next values).

3.  **Window Frame ($W$):**
    For each row $r_{i,j}$ (the $j$-th row in partition $P_i$), a specific window frame $W_{i,j}$ is defined. This frame is a subset of rows within $P_i$ that are "visible" to the window function for the current row $r_{i,j}$. The frame is typically defined relative to $r_{i,j}$ using `ROWS` or `RANGE` and `PRECEDING`/`FOLLOWING`/`CURRENT ROW`.

    *   **Default Frame (with `ORDER BY`):** If `ORDER BY` is present but no explicit frame is given, the default frame is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`. This means for row $r_{i,j}$, the window $W_{i,j}$ includes all rows $r_{i,k}$ in $P_i$ such that $r_{i,k}$ comes before or is the same as $r_{i,j}$ according to the `ORDER BY` criteria.
        *   Mathematically, if $O$ defines a non-decreasing order for values $v_k$ in the ordering column, then for row $r_{i,j}$ with value $v_j$, the window $W_{i,j} = \{r_{i,k} \in P_i \mid v_k \le v_j\}$.

    *   **Default Frame (without `ORDER BY`):** If neither `PARTITION BY` nor `ORDER BY` is present, the entire dataset is one partition, and the window is `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`. If `PARTITION BY` is present but `ORDER BY` is not, the window is `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` for each partition. This means for any row $r_{i,j}$, the window $W_{i,j}$ is the entire partition $P_i$.

4.  **Function Application ($F$):**
    Once the window $W_{i,j}$ is defined for each row $r_{i,j}$, the chosen window function $F$ is applied to the values within $W_{i,j}$.

    *   **Aggregate Functions (e.g., `SUM`, `AVG`):**
        For a column $X$, the sum for row $r_{i,j}$ is:
        $$ \text{SUM}(X)_{i,j} = \sum_{r_{i,k} \in W_{i,j}} X(r_{i,k}) $$
        The average for row $r_{i,j}$ is:
        $$ \text{AVG}(X)_{i,j} = \frac{1}{|W_{i,j}|} \sum_{r_{i,k} \in W_{i,j}} X(r_{i,k}) $$
        Where $|W_{i,j}|$ is the number of rows in the window $W_{i,j}$.

        *Example: Cumulative Sum*
        If we have sales data $(s_1, s_2, \dots, s_m)$ for a partition, ordered by date.
        For the $j$-th sale $s_j$, the cumulative sum $C_j$ is:
        $$ C_j = \sum_{k=1}^{j} s_k $$
        This is achieved with `SUM(sale_amount) OVER (PARTITION BY category ORDER BY sale_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`.

        *Example: Moving Average (3-day window)*
        For a time series of values $(v_1, v_2, \dots, v_m)$, the 3-day moving average for $v_j$ would be:
        $$ MA_j = \frac{v_{j-2} + v_{j-1} + v_j}{3} $$
        This corresponds to `AVG(value) OVER (ORDER BY date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)`.

    *   **Ranking Functions (e.g., `RANK`, `ROW_NUMBER`):**
        These functions assign an integer rank based on the `ORDER BY` clause within the partition.
        *   `ROW_NUMBER()`: Assigns a unique, sequential integer to each row within its partition, starting from 1. If rows are ordered $r_1, r_2, \dots, r_m$, then $ROW\_NUMBER(r_j) = j$.
        *   `RANK()`: Assigns the same rank to rows with identical values in the `ORDER BY` columns. The next rank is skipped. If $k$ rows have the same rank, the next rank will be $k + (\text{number of tied rows})$.
        *   `DENSE_RANK()`: Similar to `RANK()`, but no ranks are skipped. If $k$ rows have the same rank, the next rank will be $k+1$.

    *   **Analytic Functions (e.g., `LAG`, `LEAD`):**
        These functions retrieve values from a row at a specified offset from the current row within the partition.
        *   `LAG(X, n, default_value)`: Retrieves the value of column $X$ from the row $n$ positions *before* the current row in the partition, according to the `ORDER BY` clause. If no such row exists, `default_value` is returned.
        *   `LEAD(X, n, default_value)`: Retrieves the value of column $X$ from the row $n$ positions *after* the current row.

The mathematical intuition is about precisely defining the scope (the window $W_{i,j}$) for each calculation, allowing for context-aware computations that are impossible with simple `GROUP BY` aggregates.

## Advantages
*   **Preserves Row Detail:** Unlike `GROUP BY` which collapses rows, window functions return a result for *each* row, allowing you to enrich your dataset with aggregated or ranked information without losing individual record granularity.
*   **Powerful Analytical Capabilities:** Enables complex calculations like moving averages, cumulative sums, running totals, rankings, percentiles, and comparisons to previous/next rows, all within a single query.
*   **Simplified Complex Queries:** Replaces the need for cumbersome self-joins, subqueries, or temporary tables for many analytical tasks, leading to cleaner, more readable, and often more maintainable SQL code.
*   **Improved Performance:** Often more efficient than alternative methods (like correlated subqueries or multiple joins) because the database can perform the calculations in a single pass over the partitioned and ordered data.
*   **Feature Engineering:** Extremely valuable for machine learning data preparation, allowing the creation of rich, context-dependent features (e.g., "average sales last 7 days," "customer's rank by spend in their region") directly within SQL.
*   **Flexibility with Window Frames:** The ability to define precise window frames (`ROWS BETWEEN ... AND ...`) offers fine-grained control over which rows are included in the calculation for each specific row.

## Disadvantages
*   **Steep Learning Curve for Beginners:** The `OVER()` clause, `PARTITION BY`, `ORDER BY`, and especially the window frame syntax can be intimidating and confusing for those new to SQL or advanced analytics.
*   **Potential for Performance Issues (Large Datasets):** While generally efficient, poorly designed window functions on very large datasets (especially without proper indexing on `PARTITION BY` and `ORDER BY` columns) can still be resource-intensive, requiring significant memory and CPU for sorting and partitioning.
*   **Debugging Complexity:** When queries become very complex with multiple nested window functions or intricate window frames, debugging can be challenging.
*   **Limited Functionality in Some Databases:** While widely supported in modern relational databases (PostgreSQL, SQL Server, Oracle, MySQL 8+, BigQuery, Snowflake), older versions or less common databases might have limited or no support for certain window functions or frame clauses.
*   **No Direct Filtering of Window Results:** You cannot directly filter the results of a window function in the `WHERE` clause. You must use a subquery or a Common Table Expression (CTE) to apply filters based on the window function's output.

## Real World Applications
1.  **E-commerce and Retail Analytics:**
    *   **Calculating Moving Averages of Sales:** Determine the 7-day or 30-day moving average of product sales to identify trends, smooth out daily fluctuations, and forecast demand.
    *   **Ranking Products/Customers:** Rank products by sales within their category or customers by their total spend within a specific region to identify top performers or VIPs.
    *   **Customer Lifetime Value (CLTV) Features:** Calculate cumulative spend for each customer over time, or the average order value for their last N purchases, as features for CLTV prediction models.

2.  **Financial Services and Fraud Detection:**
    *   **Transaction Pattern Analysis:** Identify unusual spending patterns by comparing a customer's current transaction amount to their average transaction amount over the last 10 transactions using `AVG()` with a `ROWS` frame.
    *   **Cumulative Sum of Transactions:** Calculate the running total of transaction amounts within a short period (e.g., 1 hour) for a specific account to flag potential fraudulent activity if the sum exceeds a threshold.
    *   **Lag/Lead for Account Activity:** Compare the current transaction's location or merchant to the previous transaction's using `LAG()` to detect suspicious changes.

3.  **Healthcare and Patient Monitoring:**
    *   **Patient Vitals Trend Analysis:** Calculate the moving average of a patient's heart rate or blood pressure readings over a specific time window to detect deteriorating conditions.
    *   **Cumulative Medication Dosage:** Track the cumulative dosage of a medication administered to a patient over a treatment period to ensure it stays within safe limits.
    *   **Ranking Hospital Performance:** Rank hospitals or departments based on patient outcomes or readmission rates within specific regions or specialties.

4.  **Sports Analytics:**
    *   **Player Performance Metrics:** Calculate a player's average points per game over their last 5 games, or their rank among teammates for a specific statistic within a season.
    *   **Team Standings and Streaks:** Determine a team's current winning/losing streak or their position in the league standings based on cumulative points.
    *   **Game-by-Game Comparisons:** Compare a player's current game statistics to their previous game's statistics using `LAG()` to analyze performance changes.

5.  **Logistics and Supply Chain:**
    *   **Inventory Movement Tracking:** Calculate the cumulative quantity of an item shipped or received over a period to monitor inventory levels.
    *   **Delivery Performance:** Determine the average delivery time for a specific route or driver over the last month, or rank drivers by their on-time delivery rate.
    *   **Route Optimization:** Analyze historical data to find the average travel time between two points, considering different times of day, using window functions to aggregate data over specific time windows.

## Python Example

While SQL Window Functions are inherently a database feature, we can simulate their core concepts using the Pandas library in Python, which is often used for data manipulation and feature engineering in machine learning workflows. This example will demonstrate how to calculate a cumulative sum and a moving average, analogous to what SQL window functions achieve.

```python
import pandas as pd
import numpy as np

# 1. Generate a dummy dataset
# Let's create sales data for different products over several dates.
data = {
    'product_id': [101, 101, 101, 101, 102, 102, 102, 103, 103, 103, 103, 103],
    'sale_date': pd.to_datetime([
        '2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04',
        '2023-01-01', '2023-01-02', '2023-01-03',
        '2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05'
    ]),
    'sale_amount': [100, 150, 120, 200, 50, 75, 60, 200, 220, 180, 250, 300]
}
df = pd.DataFrame(data)

# Sort the DataFrame by product_id and sale_date, which is crucial for window operations
df = df.sort_values(by=['product_id', 'sale_date']).reset_index(drop=True)

print("Original DataFrame:")
print(df)
print("\n" + "="*50 + "\n")

# 2. Simulate SQL Window Functions using Pandas

# --- Example 1: Cumulative Sum of Sales per Product (SUM() OVER (PARTITION BY product_id ORDER BY sale_date)) ---
# This calculates the running total of sales for each product, ordered by date.
# In Pandas, this is achieved using groupby() for partitioning and cumsum() for cumulative sum.
df['cumulative_sales'] = df.groupby('product_id')['sale_amount'].cumsum()

print("DataFrame with Cumulative Sales:")
print(df)
print("\n" + "="*50 + "\n")

# --- Example 2: 2-Day Moving Average of Sales per Product (AVG() OVER (PARTITION BY product_id ORDER BY sale_date ROWS BETWEEN 1 PRECEDING AND CURRENT ROW)) ---
# This calculates the average sales for the current day and the previous day for each product.
# In Pandas, this involves groupby() for partitioning and rolling() for the window frame.
# The 'window=2' means current row + 1 preceding row.
df['2_day_moving_avg_sales'] = df.groupby('product_id')['sale_amount'].rolling(window=2, min_periods=1).mean().reset_index(level=0, drop=True)

print("DataFrame with 2-Day Moving Average Sales:")
print(df)
print("\n" + "="*50 + "\n")

# --- Example 3: Rank of Sales per Product (RANK() OVER (PARTITION BY product_id ORDER BY sale_amount DESC)) ---
# This ranks sales within each product group based on sale_amount in descending order.
# In Pandas, this uses groupby() and rank().
# method='dense' is similar to DENSE_RANK(), 'average' is default, 'min' is like RANK().
df['sales_rank_per_product'] = df.groupby('product_id')['sale_amount'].rank(method='dense', ascending=False)

print("DataFrame with Sales Rank per Product:")
print(df)
print("\n" + "="*50 + "\n")

# --- Example 4: Lagged Sales (LAG(sale_amount, 1) OVER (PARTITION BY product_id ORDER BY sale_date)) ---
# This gets the sale amount from the previous day for each product.
# In Pandas, this uses groupby() and shift().
df['previous_day_sales'] = df.groupby('product_id')['sale_amount'].shift(1)

print("DataFrame with Previous Day Sales (Lag):")
print(df)
print("\n" + "="*50 + "\n")

# --- Example 5: Percentage of Total Sales per Product (sale_amount / SUM(sale_amount) OVER (PARTITION BY product_id)) ---
# This calculates each sale's contribution to the total sales of its product.
# In Pandas, transform() is useful here as it returns a Series with the same index as the original.
df['product_total_sales'] = df.groupby('product_id')['sale_amount'].transform('sum')
df['percentage_of_product_total'] = df['sale_amount'] / df['product_total_sales']

print("DataFrame with Percentage of Product Total Sales:")
print(df)
print("\n" + "="*50 + "\n")

# Clean up temporary column if needed
df = df.drop(columns=['product_total_sales'])

print("Final DataFrame with various window-like calculations:")
print(df)
```

**Explanation of the Python Code:**

1.  **Dummy Dataset Generation:** We create a Pandas DataFrame with `product_id`, `sale_date`, and `sale_amount`. It's crucial to sort the data by `product_id` (for partitioning) and `sale_date` (for ordering within partitions) before applying window-like operations.
2.  **Cumulative Sum (`cumsum()`):**
    *   `df.groupby('product_id')`: This is analogous to `PARTITION BY product_id`. It creates groups for each unique product.
    *   `['sale_amount'].cumsum()`: For each group, `cumsum()` calculates the running total of `sale_amount`, effectively mimicking `SUM(sale_amount) OVER (PARTITION BY product_id ORDER BY sale_date)`.
3.  **Moving Average (`rolling().mean()`):**
    *   `df.groupby('product_id')`: Partitions the data by product.
    *   `['sale_amount'].rolling(window=2, min_periods=1).mean()`: For each group, `rolling(window=2)` defines a sliding window of 2 rows (current + 1 preceding). `min_periods=1` ensures that if there's only one row in the window (e.g., the very first row of a partition), it still calculates the mean (which would just be the value itself). `.mean()` then calculates the average over this window. This is equivalent to `AVG(sale_amount) OVER (PARTITION BY product_id ORDER BY sale_date ROWS BETWEEN 1 PRECEDING AND CURRENT ROW)`.
4.  **Ranking (`rank()`):**
    *   `df.groupby('product_id')`: Partitions by product.
    *   `['sale_amount'].rank(method='dense', ascending=False)`: Ranks the `sale_amount` within each product group. `method='dense'` is like SQL's `DENSE_RANK()`, assigning consecutive ranks without gaps. `ascending=False` means higher sales get a lower rank (e.g., 1st, 2nd).
5.  **Lagged Value (`shift()`):**
    *   `df.groupby('product_id')`: Partitions by product.
    *   `['sale_amount'].shift(1)`: For each group, `shift(1)` moves the `sale_amount` values down by 1 row, effectively fetching the value from the previous row. This is equivalent to `LAG(sale_amount, 1) OVER (PARTITION BY product_id ORDER BY sale_date)`.
6.  **Percentage of Total (`transform('sum')`):**
    *   `df.groupby('product_id')['sale_amount'].transform('sum')`: `transform('sum')` is a powerful Pandas function. It performs the sum for each group but then broadcasts the result back to *each original row* of that group. This is like `SUM(sale_amount) OVER (PARTITION BY product_id)` (without an `ORDER BY` in the window, meaning the sum over the entire partition).
    *   We then divide the individual `sale_amount` by this product's total sales to get the percentage.

This Python example demonstrates how the concepts of partitioning, ordering, and applying functions over defined windows, central to SQL Window Functions, can be implemented using Pandas for data manipulation in a machine learning context.

## Interview Questions

1.  **What are SQL Window Functions, and how do they differ from standard aggregate functions (like `GROUP BY`)?**
    *   **Answer:** SQL Window Functions perform calculations across a set of table rows that are related to the current row. They differ from standard aggregate functions in that they do *not* collapse rows into a single summary row. Instead, they return a value for *each* row in the original result set, enriching the data with contextual information while preserving row granularity. Standard aggregate functions with `GROUP BY` reduce the number of rows, providing one summary row per group.

2.  **Explain the purpose of the `OVER()` clause in a window function.**
    *   **Answer:** The `OVER()` clause is fundamental to window functions. It defines the "window" or set of rows on which the window function operates. It can contain `PARTITION BY` (to divide the data into groups), `ORDER BY` (to sort rows within each partition), and an optional window frame clause (to specify a subset of rows within the partition relative to the current row).

3.  **What is `PARTITION BY` used for in a window function?**
    *   **Answer:** `PARTITION BY` divides the result set into logical groups or "partitions." The window function is then applied independently to each partition. It's similar to the `GROUP BY` clause but without collapsing the rows. For example, `PARTITION BY customer_id` would perform the window calculation separately for each customer.

4.  **When would you use `ORDER BY` within the `OVER()` clause?**
    *   **Answer:** `ORDER BY` within the `OVER()` clause specifies the logical order of rows *within each partition* (or the entire result set if no `PARTITION BY` is used). It's crucial for:
        *   **Ranking functions:** (`ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`) which depend on a defined order.
        *   **Cumulative calculations:** (`SUM()`, `AVG()`) where the result depends on the sequence of rows (e.g., running totals, moving averages).
        *   **Analytic functions:** (`LAG()`, `LEAD()`, `FIRST_VALUE()`, `LAST_VALUE()`) which retrieve values based on their position relative to the current row.

5.  **Name and describe three types of window functions.**
    *   **Answer:**
        1.  **Aggregate Window Functions:** Standard aggregate functions (`SUM()`, `AVG()`, `COUNT()`, `MIN()`, `MAX()`) used with an `OVER()` clause. They calculate an aggregate over the defined window for each row.
        2.  **Ranking Window Functions:** Assign a rank to each row within its partition based on a specified order. Examples include `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `NTILE()`.
        3.  **Analytic Window Functions:** Perform calculations that retrieve values from other rows in the window or calculate distributions. Examples include `LAG()`, `LEAD()`, `FIRST_VALUE()`, `LAST_VALUE()`, `CUME_DIST()`, `PERCENT_RANK()`.

6.  **Explain the difference between `ROW_NUMBER()`, `RANK()`, and `DENSE_RANK()`?**
    *   **Answer:** All three assign ranks within a partition based on an `ORDER BY` clause:
        *   `ROW_NUMBER()`: Assigns a unique, sequential integer to each row, starting from 1. If there are ties in the ordering column, the assignment is arbitrary but unique.
        *   `RANK()`: Assigns the same rank to rows with identical values in the `ORDER BY` columns. It then skips the next rank(s). For example, if two rows are ranked 1, the next rank will be 3.
        *   `DENSE_RANK()`: Assigns the same rank to rows with identical values, but it does *not* skip ranks. If two rows are ranked 1, the next rank will be 2.

7.  **What is a window frame, and how do `ROWS` and `RANGE` differ?**
    *   **Answer:** A window frame is an optional clause within `OVER()` that further refines the set of rows *within the current partition* that the window function operates on. It defines a "sliding window" relative to the current row.
        *   `ROWS`: Defines the frame based on a physical number of rows relative to the current row (e.g., `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` means the current row and the 2 rows immediately before it).
        *   `RANGE`: Defines the frame based on a logical range of values in the `ORDER BY` column relative to the current row's value. For example, `RANGE BETWEEN 10 PRECEDING AND CURRENT ROW` would include all rows whose `ORDER BY` value is within 10 units of the current row's `ORDER BY` value. `RANGE` is more complex and less commonly used than `ROWS` for simple moving averages.

8.  **How would you calculate a 3-day moving average of sales for each product using a window function?**
    *   **Answer:**
        ```sql
        SELECT
            product_id,
            sale_date,
            sale_amount,
            AVG(sale_amount) OVER (
                PARTITION BY product_id
                ORDER BY sale_date
                ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
            ) AS three_day_moving_avg_sales
        FROM
            sales_data;
        ```
        This query partitions the data by `product_id`, orders it by `sale_date`, and for each row, calculates the average `sale_amount` over the current row and the two preceding rows within that product's partition.

9.  **Can you filter the results of a window function directly in the `WHERE` clause? If not, how would you achieve this?**
    *   **Answer:** No, you cannot directly filter the results of a window function in the `WHERE` clause because window functions are evaluated *after* the `WHERE` clause. To filter based on a window function's output, you must use a subquery or a Common Table Expression (CTE).
    *   **Example using CTE:**
        ```sql
        WITH RankedSales AS (
            SELECT
                product_id,
                sale_date,
                sale_amount,
                RANK() OVER (PARTITION BY product_id ORDER BY sale_amount DESC) AS sales_rank
            FROM
                sales_data
        )
        SELECT
            product_id,
            sale_date,
            sale_amount
        FROM
            RankedSales
        WHERE
            sales_rank <= 3; -- Filter for top 3 sales per product
        ```

10. **Describe a scenario where `LAG()` or `LEAD()` would be useful.**
    *   **Answer:** `LAG()` and `LEAD()` are useful for comparing values between consecutive rows within a partition.
        *   **`LAG()`:** Useful for calculating the difference from the previous period, such as daily sales growth (`sale_amount - LAG(sale_amount, 1) OVER (ORDER BY sale_date)`), or comparing a stock price to its previous day's closing price.
        *   **`LEAD()`:** Useful for looking ahead, such as calculating the difference to the next period, or determining the time until the next event in a sequence. For example, calculating the duration of a customer's session by subtracting the current login time from the `LEAD()` of their next login time.

## Quiz

1.  Which of the following is a key characteristic of SQL Window Functions?
    A) They always reduce the number of rows in the output.
    B) They perform calculations across a set of related rows while preserving row granularity.
    C) They can only be used with aggregate functions like `SUM()` and `AVG()`.
    D) They are evaluated before the `WHERE` clause.

2.  What is the primary purpose of the `PARTITION BY` clause in a window function?
    A) To sort the entire result set before applying the function.
    B) To filter rows based on a condition.
    C) To divide the result set into independent groups for the window function.
    D) To define the number of rows included in the window frame.

3.  You want to assign a unique, sequential number to each transaction within a customer's history, ordered by transaction date. Which window function would you use?
    A) `RANK()`
    B) `DENSE_RANK()`
    C) `ROW_NUMBER()`
    D) `NTILE()`

4.  Consider the following SQL snippet: `AVG(value) OVER (ORDER BY date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)`. What does `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` define?
    A) The average of the current row and the two rows immediately following it.
    B) The average of the current row and the two rows immediately preceding it.
    C) The average of all rows from the beginning of the partition up to the current row.
    D) The average of all rows in the entire partition.

5.  Which of the following statements about filtering window function results is true?
    A) You can use the `WHERE` clause directly on the output of a window function.
    B) You must use a `HAVING` clause to filter window function results.
    C) You need to wrap the query with the window function in a subquery or CTE to filter its results.
    D) Window functions cannot be filtered; they always return all rows.

---

### Answer Key

1.  **B) They perform calculations across a set of related rows while preserving row granularity.**
    *   **Explanation:** This is the defining characteristic of window functions. Unlike `GROUP BY`, they don't collapse rows, allowing you to add contextual information to each individual record.

2.  **C) To divide the result set into independent groups for the window function.**
    *   **Explanation:** `PARTITION BY` creates logical groups, and the window function operates separately within each of these groups.

3.  **C) `ROW_NUMBER()`**
    *   **Explanation:** `ROW_NUMBER()` assigns a unique, sequential integer to each row within its partition, which is exactly what's needed for a unique numbering of transactions. `RANK()` and `DENSE_RANK()` handle ties differently, and `NTILE()` divides into N groups.

4.  **B) The average of the current row and the two rows immediately preceding it.**
    *   **Explanation:** `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` explicitly defines a window frame that includes the current row and the two rows that come before it in the specified order.

5.  **C) You need to wrap the query with the window function in a subquery or CTE to filter its results.**
    *   **Explanation:** Window functions are evaluated after the `WHERE` clause. Therefore, to filter based on their output, you must first compute the window function in a subquery or CTE, and then apply the `WHERE` clause to the results of that inner query.

## Further Reading

1.  **PostgreSQL Documentation on Window Functions:** A comprehensive and well-explained official documentation that covers all aspects of window functions with clear examples.
    *   [https://www.postgresql.org/docs/current/tutorial-window.html](https://www.postgresql.org/docs/current/tutorial-window.html)

2.  **SQL Server Documentation on Window Functions:** Microsoft's official documentation provides detailed explanations and syntax for SQL Server, which is largely applicable to other SQL dialects.
    *   [https://learn.microsoft.com/en-us/sql/t-sql/queries/select-over-clause-transact-sql?view=sql-server-ver16](https://learn.microsoft.com/en-us/sql/t-sql/queries/select-over-clause-transact-sql?view=sql-server-ver16)

3.  **Mode Analytics SQL Window Functions Tutorial:** A highly practical and beginner-friendly tutorial with interactive examples and common use cases.
    *   [https://mode.com/sql-tutorial/sql-window-functions/](https://mode.com/sql-tutorial/sql-window-functions/)