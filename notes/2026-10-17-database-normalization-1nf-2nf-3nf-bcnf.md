# Database Normalization (1NF, 2NF, 3NF, BCNF)

## Overview
Database Normalization is a systematic approach to organizing data in a database to reduce data redundancy and improve data integrity. It's like tidying up a messy room: you put things where they belong, so it's easier to find them, less likely to lose them, and you don't have multiple copies of the same item lying around.

The core idea is to decompose large, "unnormalized" tables into smaller, more manageable tables, and then link these tables using relationships (typically through primary and foreign keys). This process follows a set of rules, or "normal forms," which are progressive levels of normalization. The most commonly discussed normal forms are:

*   **1NF (First Normal Form)**: The basic level, ensuring data is atomic and structured.
*   **2NF (Second Normal Form)**: Builds on 1NF, addressing partial dependencies.
*   **3NF (Third Normal Form)**: Builds on 2NF, addressing transitive dependencies.
*   **BCNF (Boyce-Codd Normal Form)**: A stricter version of 3NF, handling specific types of anomalies not covered by 3NF.

While primarily a database design concept, understanding normalization is crucial in machine learning because the quality and structure of your data directly impact model performance. Well-normalized data is typically cleaner, more consistent, and easier to work with, leading to more robust and reliable ML models.

## What Problem It Solves
Database Normalization primarily addresses several critical problems that arise in poorly designed databases, which can severely impact data quality and, consequently, machine learning model performance:

1.  **Data Redundancy**: Storing the same piece of information multiple times.
    *   **Problem**: Wastes storage space, makes the database larger and slower, and increases the risk of inconsistencies. For ML, redundant features can sometimes lead to multicollinearity issues or simply make data processing less efficient.
2.  **Data Anomalies**: These are inconsistencies that occur when data is not properly normalized.
    *   **Insertion Anomaly**: Cannot insert a new record without having complete information for all attributes, even if some are not yet known. For example, you can't add a new product without an associated supplier if supplier details are part of the product table.
    *   **Update Anomaly**: Changing a piece of data requires updating multiple records, and if one update is missed, data becomes inconsistent. For example, if a customer's address is stored in multiple order records, changing it requires updating every single order they've ever placed.
    *   **Deletion Anomaly**: Deleting a record might unintentionally delete other valuable information. For example, deleting the last order for a specific product might also delete all information about that product if product details are only stored within order records.
    *   **Impact on ML**: Data anomalies lead to dirty, inconsistent, and unreliable data. ML models trained on such data will learn incorrect patterns, leading to poor predictions, biased results, and a lack of generalization. Inconsistent data can also make feature engineering much harder and error-prone.

3.  **Data Inconsistency**: Different versions of the same data exist in the database.
    *   **Problem**: Leads to unreliable information, making it difficult to trust the data for reporting, analysis, or training ML models. If a customer's address is different in two places, which one is correct?
    *   **Impact on ML**: ML models thrive on consistent patterns. Inconsistent data introduces noise and ambiguity, making it harder for the model to identify true relationships and generalize effectively. It can also lead to incorrect feature values, directly impacting model accuracy.

4.  **Difficulty in Data Maintenance**: Managing and updating a denormalized database is complex and error-prone due to the issues above.
    *   **Impact on ML**: Data scientists spend a significant amount of time cleaning and preparing data. A denormalized database drastically increases this effort, diverting time from model development and experimentation.

By solving these problems, normalization ensures that data is stored logically, efficiently, and consistently, providing a solid foundation for accurate data analysis and robust machine learning model development.

## How It Works
Database normalization works by systematically decomposing a large table into smaller, related tables based on a set of rules called normal forms. The process typically involves identifying functional dependencies and then restructuring the tables to eliminate redundancy and anomalies.

Let's break down the normal forms:

### Functional Dependency
The cornerstone of normalization is the concept of **functional dependency**.
A functional dependency $X \rightarrow Y$ means that the value of attribute set $X$ uniquely determines the value of attribute set $Y$. In simpler terms, if you know $X$, you can always find $Y$.
*   Example: `StudentID` $\rightarrow$ `StudentName` (Knowing the StudentID tells you the StudentName).
*   Example: `OrderID` $\rightarrow$ `OrderDate`, `CustomerID` (Knowing the OrderID tells you the OrderDate and CustomerID).

### Normal Forms

#### 1. First Normal Form (1NF)
A table is in 1NF if and only if:
*   **Atomic Values**: Each column contains atomic (indivisible) values. This means no multi-valued attributes (e.g., a single cell containing "red, blue, green" for colors) and no composite attributes (e.g., a single cell containing "John Doe" for a name that should be "FirstName" and "LastName").
*   **No Repeating Groups**: There are no repeating groups of columns. Each row must be unique, and each column should have a unique name.

**Example (Before 1NF):**
| OrderID | CustomerName | Product | Quantity | Price |
| :------ | :----------- | :------ | :------- | :---- |
| 101     | Alice        | A, B    | 2, 1     | 10, 20 |
| 102     | Bob          | C       | 3        | 15    |

Here, `Product`, `Quantity`, and `Price` are repeating groups.

**Example (After 1NF):**
To achieve 1NF, we break down the repeating groups into separate rows.
| OrderID | CustomerName | Product | Quantity | Price |
| :------ | :----------- | :------ | :------- | :---- |
| 101     | Alice        | A       | 2        | 10    |
| 101     | Alice        | B       | 1        | 20    |
| 102     | Bob          | C       | 3        | 15    |

Now, each cell contains a single, atomic value. The primary key would likely be a composite key of `(OrderID, Product)`.

#### 2. Second Normal Form (2NF)
A table is in 2NF if and only if:
*   It is in **1NF**.
*   **No Partial Dependencies**: All non-key attributes are fully functionally dependent on the *entire* primary key. This means if the primary key is composite (made of multiple columns), no non-key attribute should depend on only *part* of the primary key.

**Example (Before 2NF - using 1NF table above):**
Primary Key: `(OrderID, Product)`
Functional Dependencies:
*   `(OrderID, Product)` $\rightarrow$ `Quantity`, `Price` (Full dependency)
*   `OrderID` $\rightarrow$ `CustomerName` (Partial dependency - `CustomerName` depends only on `OrderID`, not `Product`)

**Example (After 2NF):**
We split the table into two: one for orders and customers, and another for order items.
**`Orders` Table:**
| OrderID | CustomerName |
| :------ | :----------- |
| 101     | Alice        |
| 102     | Bob          |
Primary Key: `OrderID`

**`Order_Items` Table:**
| OrderID | Product | Quantity | Price |
| :------ | :------ | :------- | :---- |
| 101     | A       | 2        | 10    |
| 101     | B       | 1        | 20    |
| 102     | C       | 3        | 15    |
Primary Key: `(OrderID, Product)`
Foreign Key: `OrderID` references `Orders.OrderID`

Now, `CustomerName` is fully dependent on `OrderID` in the `Orders` table, and `Quantity`, `Price` are fully dependent on `(OrderID, Product)` in the `Order_Items` table.

#### 3. Third Normal Form (3NF)
A table is in 3NF if and only if:
*   It is in **2NF**.
*   **No Transitive Dependencies**: No non-key attribute is functionally dependent on another non-key attribute. In other words, non-key attributes should only depend on the primary key, not on other non-key attributes.

**Example (Before 3NF - using `Orders` table from 2NF):**
**`Orders` Table:**
| OrderID | CustomerName | CustomerCity |
| :------ | :----------- | :----------- |
| 101     | Alice        | New York     |
| 102     | Bob          | London       |
Primary Key: `OrderID`
Functional Dependencies:
*   `OrderID` $\rightarrow$ `CustomerName`, `CustomerCity`
*   `CustomerName` $\rightarrow$ `CustomerCity` (Transitive dependency - `CustomerCity` depends on `CustomerName`, which is a non-key attribute, not directly on `OrderID`)

**Example (After 3NF):**
We split the `Orders` table into `Orders` and `Customers`.
**`Orders` Table:**
| OrderID | CustomerID |
| :------ | :--------- |
| 101     | C1         |
| 102     | C2         |
Primary Key: `OrderID`
Foreign Key: `CustomerID` references `Customers.CustomerID`

**`Customers` Table:**
| CustomerID | CustomerName | CustomerCity |
| :--------- | :----------- | :----------- |
| C1         | Alice        | New York     |
| C2         | Bob          | London       |
Primary Key: `CustomerID`

Now, `CustomerName` and `CustomerCity` are directly dependent on `CustomerID` in the `Customers` table, and `CustomerID` is directly dependent on `OrderID` in the `Orders` table. No non-key attribute depends on another non-key attribute.

#### 4. Boyce-Codd Normal Form (BCNF)
BCNF is a stricter version of 3NF. A table is in BCNF if and only if:
*   It is in **3NF**.
*   **Every determinant is a candidate key**. A determinant is any attribute or set of attributes that functionally determines another attribute. A candidate key is any attribute or set of attributes that can uniquely identify a row in a table (it could be chosen as the primary key).

The difference between 3NF and BCNF arises in tables with:
*   Multiple overlapping candidate keys.
*   A table has a non-key attribute that is a determinant of part of a candidate key.

**Example (Before BCNF - a simplified `Student_Course_Professor` table):**
Assume:
*   A student can take multiple courses.
*   A course can be taught by multiple professors.
*   A professor teaches only one course.
*   A student taking a specific course is taught by a specific professor for that course.

| StudentID | Course | Professor |
| :-------- | :----- | :-------- |
| S1        | C1     | P1        |
| S1        | C2     | P2        |
| S2        | C1     | P1        |
| S3        | C3     | P3        |

Functional Dependencies:
1.  `(StudentID, Course)` $\rightarrow$ `Professor` (Primary Key determines Professor)
2.  `Professor` $\rightarrow$ `Course` (A professor teaches only one course)

Candidate Keys: `(StudentID, Course)` and `(StudentID, Professor)`

This table is in 3NF because:
*   It's in 2NF (no partial dependencies).
*   No non-key attribute (`Professor`) is transitively dependent on the primary key `(StudentID, Course)` via another non-key attribute.

However, it's **not in BCNF** because `Professor` is a determinant (`Professor` $\rightarrow$ `Course`), but `Professor` is *not* a candidate key. `(StudentID, Professor)` is a candidate key, but `Professor` alone is not.

**Example (After BCNF):**
We decompose the table into two:
**`Student_Enrollment` Table:**
| StudentID | Course |
| :-------- | :----- |
| S1        | C1     |
| S1        | C2     |
| S2        | C1     |
| S3        | C3     |
Primary Key: `(StudentID, Course)`

**`Course_Professor` Table:**
| Professor | Course |
| :-------- | :----- |
| P1        | C1     |
| P2        | C2     |
| P3        | C3     |
Primary Key: `Professor`
Foreign Key: `Course` references `Student_Enrollment.Course` (or a separate `Courses` table if it existed).

Now, in `Course_Professor`, `Professor` is a determinant and also a candidate key. In `Student_Enrollment`, `(StudentID, Course)` is the determinant and a candidate key. Both tables are in BCNF.

The process of normalization involves moving from 1NF to 2NF, then to 3NF, and sometimes to BCNF, by identifying and removing dependencies that violate the rules of each normal form.

## Mathematical Intuition
While database normalization isn't about continuous functions or calculus, its "mathematical intuition" lies in **set theory** and **relational algebra**, specifically the formal definition and inference rules of **functional dependencies**. These rules provide the logical framework for identifying and resolving data redundancies and anomalies.

The core concept is the **functional dependency (FD)**.
Let $R$ be a relation (table) and $A, B$ be sets of attributes of $R$.
A functional dependency $A \rightarrow B$ exists if, for any two tuples (rows) $t_1$ and $t_2$ in $R$, if $t_1[A] = t_2[A]$ (the values of attributes in $A$ are the same for both tuples), then $t_1[B] = t_2[B]$ (the values of attributes in $B$ must also be the same).
In simpler terms, the values of attributes in $A$ uniquely determine the values of attributes in $B$.

For example, in a table with `(StudentID, StudentName, Major)`, if `StudentID` is unique, then `StudentID` functionally determines `StudentName` and `Major`. We write this as `StudentID` $\rightarrow$ `StudentName` and `StudentID` $\rightarrow$ `Major`.

The "mathematics" of how we reason about and derive new functional dependencies from existing ones is governed by **Armstrong's Axioms**. These are a set of sound and complete inference rules for functional dependencies. "Sound" means any FD derived using these rules is valid, and "complete" means all valid FDs can be derived.

Let $A, B, C$ be sets of attributes in a relation $R$.

1.  **Axiom of Reflexivity**: If $B \subseteq A$, then $A \rightarrow B$.
    *   **Intuition**: If a set of attributes $A$ contains another set of attributes $B$, then $A$ trivially determines $B$. For example, if you know `(StudentID, CourseID)`, you certainly know `StudentID`. So, `(StudentID, CourseID)` $\rightarrow$ `StudentID`. This is a self-evident truth.

2.  **Axiom of Augmentation**: If $A \rightarrow B$, then $AC \rightarrow BC$.
    *   **Intuition**: If $A$ determines $B$, then adding a set of attributes $C$ to both sides of the dependency doesn't break the determination. If `StudentID` $\rightarrow$ `StudentName`, then `(StudentID, CourseID)` $\rightarrow$ `(StudentName, CourseID)`. Knowing more information (CourseID) doesn't make you "unknow" the student's name.

3.  **Axiom of Transitivity**: If $A \rightarrow B$ and $B \rightarrow C$, then $A \rightarrow C$.
    *   **Intuition**: This is like the transitive property in mathematics. If $A$ determines $B$, and $B$ in turn determines $C$, then $A$ must also determine $C$. For example, if `StudentID` $\rightarrow$ `Major` and `Major` $\rightarrow$ `DepartmentHead`, then `StudentID` $\rightarrow$ `DepartmentHead`. This axiom is directly targeted by 3NF, which aims to eliminate transitive dependencies.

These axioms, along with derived rules (like decomposition, union, pseudotransitivity), form the logical basis for:
*   **Finding Candidate Keys**: Identifying minimal sets of attributes that can uniquely identify a tuple.
*   **Identifying Dependencies**: Discovering partial and transitive dependencies that violate normal forms.
*   **Decomposition**: Breaking down relations into smaller ones to satisfy normal form rules while preserving dependencies and data.

The process of normalization essentially involves applying these logical rules to restructure the database schema, ensuring that the functional dependencies are aligned with the chosen primary keys in each table, thereby minimizing redundancy and anomalies.

## Advantages
*   **Reduced Data Redundancy**: Eliminates duplicate data, saving storage space and making the database more efficient.
*   **Improved Data Integrity**: Ensures data consistency by storing each piece of information in a single, authoritative location. This prevents update, insertion, and deletion anomalies.
*   **Better Data Consistency**: Reduces the chances of conflicting data entries, leading to more reliable information for reporting and analysis.
*   **Easier Data Maintenance**: Updates and modifications are simpler and less error-prone as changes only need to be made in one place.
*   **Enhanced Query Performance (often)**: Smaller, more focused tables can sometimes lead to faster query execution, especially for queries that don't require joining many tables.
*   **Simplified Database Design**: Breaking down complex tables into smaller, logical units makes the database schema easier to understand and manage.
*   **Better Foundation for Machine Learning**: Provides clean, consistent, and well-structured data, which is crucial for training accurate and robust ML models. It simplifies feature engineering and reduces the need for extensive data cleaning.
*   **Flexibility and Scalability**: A well-normalized database is easier to extend and adapt to new requirements without major restructuring.

## Disadvantages
*   **Increased Query Complexity**: Retrieving data that spans multiple normalized tables often requires joining several tables. This can make queries more complex to write and understand.
*   **Potential Performance Overhead (for reads)**: While normalization can improve performance for some operations, complex queries involving many joins can sometimes be slower than querying a single, denormalized table, especially for analytical workloads.
*   **More Tables to Manage**: A normalized database consists of many smaller tables, which can increase the overall complexity of the database schema and management overhead.
*   **Over-Normalization**: Normalizing beyond 3NF or BCNF (e.g., to 4NF or 5NF) can sometimes lead to an excessive number of tables, making the database overly complex and potentially degrading performance without significant benefits.
*   **Not Always Ideal for Analytical Workloads (OLAP)**: Data warehouses and analytical systems (OLAP) often prefer denormalized or partially denormalized schemas (like star or snowflake schemas) to optimize for read performance and simplify complex analytical queries, even at the cost of some redundancy.
*   **Can Be Difficult to Implement for Existing Systems**: Normalizing a large, existing denormalized database can be a complex and time-consuming task.

## Real World Applications
Database normalization is a fundamental principle in relational database design and is applied across virtually all industries that rely on structured data.

1.  **E-commerce Platforms (e.g., Amazon, Shopify)**:
    *   **Use Case**: Managing customer information, product catalogs, orders, payments, and shipping details.
    *   **Normalization in Action**: Customer details (name, address, contact) are stored in a `Customers` table. Product details (name, description, price) are in a `Products` table. Order information (order ID, date, total) is in an `Orders` table, which links to `Customers` and an `Order_Items` table (linking to `Products`) to detail what was purchased. This prevents redundant customer addresses in every order and ensures product details are consistent across all orders.

2.  **Banking and Financial Systems**:
    *   **Use Case**: Managing customer accounts, transactions, loans, and financial products.
    *   **Normalization in Action**: `Customers` table holds personal details. `Accounts` table holds account numbers, types, and balances, linked to `Customers`. `Transactions` table records every debit/credit, linked to `Accounts`. This ensures that customer details are stored once, and account information is consistent, preventing critical financial data anomalies.

3.  **Healthcare Management Systems (e.g., Electronic Health Records - EHR)**:
    *   **Use Case**: Storing patient demographics, medical history, diagnoses, treatments, prescriptions, and appointments.
    *   **Normalization in Action**: `Patients` table for personal info. `Doctors` table for physician details. `Appointments` table linking patients and doctors with dates/times. `Medical_Records` table storing diagnoses and treatments, linked to patients. This prevents redundant patient information across multiple visits or treatments and ensures that medical data is consistent and accurate, which is critical for patient care.

4.  **Inventory and Supply Chain Management**:
    *   **Use Case**: Tracking products, suppliers, warehouses, and stock levels.
    *   **Normalization in Action**: `Products` table for item details. `Suppliers` table for vendor information. `Warehouses` table for location details. `Inventory` table linking products to warehouses with stock quantities. `Purchase_Orders` table linking suppliers to products. This ensures that product details are consistent, supplier information is stored once, and inventory levels are accurately managed without conflicting entries.

5.  **Social Media Platforms (e.g., Facebook, LinkedIn)**:
    *   **Use Case**: Managing user profiles, posts, friendships/connections, messages, and media.
    *   **Normalization in Action**: `Users` table for profile information. `Posts` table for content, linked to `Users`. `Friendships` table (a many-to-many relationship table) linking two user IDs. `Messages` table linking sender and receiver user IDs. This structure efficiently manages vast amounts of interconnected data, preventing redundancy in user profiles and ensuring consistent relationships.

## Python Example
Database normalization is primarily a schema design process, not a data transformation operation typically performed directly with Python libraries like `scikit-learn` or `numpy` in the same way you'd normalize features (e.g., min-max scaling). However, we can *simulate* the process of taking a denormalized dataset (represented as a Pandas DataFrame) and decomposing it into multiple normalized DataFrames to illustrate 1NF, 2NF, and 3NF.

This example will:
1.  Create a denormalized DataFrame.
2.  Demonstrate how to achieve 1NF by ensuring atomic values.
3.  Demonstrate how to achieve 2NF by splitting tables to remove partial dependencies.
4.  Demonstrate how to achieve 3NF by splitting tables to remove transitive dependencies.

```python
import pandas as pd

# 1. Create a Denormalized DataFrame (violates 1NF, 2NF, 3NF)
# This table combines customer, order, and product information,
# and also has non-atomic values and transitive dependencies.
data = {
    'OrderID': [101, 101, 102, 103, 103],
    'OrderDate': ['2023-01-15', '2023-01-15', '2023-01-16', '2023-01-17', '2023-01-17'],
    'CustomerID': ['C001', 'C001', 'C002', 'C001', 'C001'],
    'CustomerName': ['Alice Smith', 'Alice Smith', 'Bob Johnson', 'Alice Smith', 'Alice Smith'],
    'CustomerCity': ['New York', 'New York', 'London', 'New York', 'New York'],
    'ProductDetails': ['Laptop (SKU001), Mouse (SKU002)', 'Laptop (SKU001), Mouse (SKU002)', 'Keyboard (SKU003)', 'Monitor (SKU004)', 'Monitor (SKU004)'], # Non-atomic
    'ProductSKU': ['SKU001,SKU002', 'SKU001,SKU002', 'SKU003', 'SKU004', 'SKU004'], # Non-atomic
    'ProductName': ['Laptop,Mouse', 'Laptop,Mouse', 'Keyboard', 'Monitor', 'Monitor'], # Non-atomic
    'Quantity': ['1,1', '1,1', '2', '1', '1'], # Non-atomic
    'Price': ['1200,25', '1200,25', '75', '300', '300'], # Non-atomic
    'ShippingZone': ['East', 'East', 'West', 'East', 'East'],
    'ZoneCost': [10, 10, 15, 10, 10] # Transitive dependency: ShippingZone -> ZoneCost
}
denormalized_df = pd.DataFrame(data)
print("--- Original Denormalized DataFrame ---")
print(denormalized_df)
print("\nProblems:")
print("1. Non-atomic values in ProductDetails, ProductSKU, ProductName, Quantity, Price.")
print("2. Redundancy: CustomerName, CustomerCity, ShippingZone, ZoneCost repeated for each order item.")
print("3. Partial Dependency: CustomerName, CustomerCity depend only on OrderID (part of a potential composite key).")
print("4. Transitive Dependency: ZoneCost depends on ShippingZone (non-key attribute).")

# --- Step 1: Achieve 1NF (First Normal Form) ---
# 1NF requires atomic values and no repeating groups.
# We'll explode the multi-valued columns into separate rows.

# First, let's clean up the ProductDetails column to just get the product name for splitting
# For simplicity, we'll assume ProductSKU, ProductName, Quantity, Price are comma-separated lists
# and correspond to each other.
denormalized_df['ProductSKU_list'] = denormalized_df['ProductSKU'].apply(lambda x: x.split(','))
denormalized_df['ProductName_list'] = denormalized_df['ProductName'].apply(lambda x: x.split(','))
denormalized_df['Quantity_list'] = denormalized_df['Quantity'].apply(lambda x: [int(q) for q in x.split(',')])
denormalized_df['Price_list'] = denormalized_df['Price'].apply(lambda x: [float(p) for p in x.split(',')])

# Create a list of dictionaries for the new rows
rows = []
for index, row in denormalized_df.iterrows():
    for i in range(len(row['ProductSKU_list'])):
        new_row = {
            'OrderID': row['OrderID'],
            'OrderDate': row['OrderDate'],
            'CustomerID': row['CustomerID'],
            'CustomerName': row['CustomerName'],
            'CustomerCity': row['CustomerCity'],
            'ProductSKU': row['ProductSKU_list'][i],
            'ProductName': row['ProductName_list'][i],
            'Quantity': row['Quantity_list'][i],
            'Price': row['Price_list'][i],
            'ShippingZone': row['ShippingZone'],
            'ZoneCost': row['ZoneCost']
        }
        rows.append(new_row)

df_1nf = pd.DataFrame(rows)
print("\n--- DataFrame in 1NF ---")
print(df_1nf)
print("\nAchieved 1NF by: Each cell now contains a single, atomic value. No repeating groups.")
print("Primary Key for this table would be (OrderID, ProductSKU).")

# --- Step 2: Achieve 2NF (Second Normal Form) ---
# 2NF requires 1NF + no partial dependencies.
# Here, CustomerName, CustomerCity, ShippingZone, ZoneCost depend only on OrderID (part of PK).
# We'll split the table into:
# 1. Orders (OrderID, OrderDate, CustomerID, CustomerName, CustomerCity, ShippingZone, ZoneCost)
# 2. Order_Items (OrderID, ProductSKU, ProductName, Quantity, Price)

# Create Orders table (contains OrderID, Customer, Shipping info)
# We need to drop duplicates based on OrderID to ensure each order appears once.
orders_df = df_1nf[['OrderID', 'OrderDate', 'CustomerID', 'CustomerName', 'CustomerCity', 'ShippingZone', 'ZoneCost']].drop_duplicates(subset=['OrderID']).reset_index(drop=True)

# Create Order_Items table (contains details for each item in an order)
order_items_df = df_1nf[['OrderID', 'ProductSKU', 'ProductName', 'Quantity', 'Price']].reset_index(drop=True)

print("\n--- Tables in 2NF ---")
print("\nOrders Table (Primary Key: OrderID)")
print(orders_df)
print("\nOrder_Items Table (Primary Key: (OrderID, ProductSKU))")
print(order_items_df)
print("\nAchieved 2NF by: Separating attributes that were partially dependent on the composite primary key (OrderID, ProductSKU).")
print("CustomerName, CustomerCity, ShippingZone, ZoneCost now depend fully on OrderID in the Orders table.")

# --- Step 3: Achieve 3NF (Third Normal Form) ---
# 3NF requires 2NF + no transitive dependencies.
# In the Orders table, we have: CustomerID -> CustomerName, CustomerCity (assuming CustomerID is unique)
# And ShippingZone -> ZoneCost (transitive dependency: ZoneCost depends on ShippingZone, which is a non-key attribute)
# We'll split the Orders table further into:
# 1. Orders (OrderID, OrderDate, CustomerID, ShippingZone)
# 2. Customers (CustomerID, CustomerName, CustomerCity)
# 3. Shipping_Zones (ShippingZone, ZoneCost)

# Create Customers table
customers_df = orders_df[['CustomerID', 'CustomerName', 'CustomerCity']].drop_duplicates(subset=['CustomerID']).reset_index(drop=True)

# Create Shipping_Zones table
shipping_zones_df = orders_df[['ShippingZone', 'ZoneCost']].drop_duplicates(subset=['ShippingZone']).reset_index(drop=True)

# Update Orders table to only contain foreign keys and its own attributes
orders_3nf_df = orders_df[['OrderID', 'OrderDate', 'CustomerID', 'ShippingZone']].reset_index(drop=True)

print("\n--- Tables in 3NF ---")
print("\nOrders Table (Primary Key: OrderID, Foreign Keys: CustomerID, ShippingZone)")
print(orders_3nf_df)
print("\nCustomers Table (Primary Key: CustomerID)")
print(customers_df)
print("\nShipping_Zones Table (Primary Key: ShippingZone)")
print(shipping_zones_df)
print("\nOrder_Items Table (from 2NF, already in 3NF - Primary Key: (OrderID, ProductSKU), Foreign Key: OrderID)")
print(order_items_df)
print("\nAchieved 3NF by: Removing transitive dependencies.")
print("CustomerName, CustomerCity now depend directly on CustomerID in the Customers table.")
print("ZoneCost now depends directly on ShippingZone in the Shipping_Zones table.")

# --- BCNF Consideration ---
# For this specific example, the tables are likely already in BCNF.
# BCNF addresses cases where a non-key attribute is a determinant of a candidate key.
# In our `Shipping_Zones` table, `ShippingZone` is the primary key and also the determinant for `ZoneCost`.
# In `Customers`, `CustomerID` is the primary key and determinant for `CustomerName`, `CustomerCity`.
# In `Orders`, `OrderID` is the primary key and determinant for `OrderDate`, `CustomerID`, `ShippingZone`.
# In `Order_Items`, `(OrderID, ProductSKU)` is the primary key and determinant for `ProductName`, `Quantity`, `Price`.
# All determinants are candidate keys, so these tables are in BCNF.

print("\n--- BCNF Status ---")
print("The resulting tables (Orders, Customers, Shipping_Zones, Order_Items) are also in BCNF because all determinants are candidate keys.")

# Example of how to join them back for a full view (if needed for analysis)
print("\n--- Example: Joining tables to reconstruct a view ---")
full_order_details = orders_3nf_df.merge(customers_df, on='CustomerID', how='left') \
                                  .merge(shipping_zones_df, on='ShippingZone', how='left') \
                                  .merge(order_items_df, on='OrderID', how='left')
print(full_order_details)
print("\nNotice how joining allows us to get the full picture, but the data is stored efficiently and without redundancy.")
```

**Explanation of the Python Example:**

1.  **Denormalized DataFrame**: We start with a single `denormalized_df` that intentionally violates all normal forms. It has:
    *   Multi-valued cells (`ProductSKU`, `ProductName`, `Quantity`, `Price`).
    *   Redundant customer and shipping information.
    *   `CustomerName` and `CustomerCity` depend on `CustomerID`, which is part of the `OrderID`'s context, but if `(OrderID, ProductSKU)` were the primary key, they'd be partially dependent.
    *   `ZoneCost` depends on `ShippingZone`, which is a non-key attribute (transitive dependency).

2.  **1NF (First Normal Form)**:
    *   We identify the columns with comma-separated values (`ProductSKU`, `ProductName`, `Quantity`, `Price`).
    *   We "explode" these lists into separate rows. For each original row, if it had multiple products, it now becomes multiple rows, one for each product.
    *   The `df_1nf` now has atomic values in each cell. The primary key would be a composite of `(OrderID, ProductSKU)`.

3.  **2NF (Second Normal Form)**:
    *   In `df_1nf`, `CustomerName`, `CustomerCity`, `ShippingZone`, `ZoneCost` depend only on `OrderID`, not on the full composite primary key `(OrderID, ProductSKU)`. This is a partial dependency.
    *   To resolve this, we create two new tables:
        *   `orders_df`: Contains `OrderID` and all attributes that depend *only* on `OrderID` (customer details, shipping details). We use `drop_duplicates(subset=['OrderID'])` to ensure each order appears only once.
        *   `order_items_df`: Contains `OrderID`, `ProductSKU`, and attributes that depend on the *full* composite key `(OrderID, ProductSKU)` (product name, quantity, price).
    *   Now, in `orders_df`, `OrderID` is the primary key, and all its attributes are fully dependent on it. In `order_items_df`, `(OrderID, ProductSKU)` is the primary key, and all its attributes are fully dependent on it.

4.  **3NF (Third Normal Form)**:
    *   In `orders_df` (from 2NF), we still have transitive dependencies:
        *   `CustomerID` $\rightarrow$ `CustomerName`, `CustomerCity` (assuming `CustomerID` is unique). `CustomerName` and `CustomerCity` are non-key attributes that depend on another non-key attribute (`CustomerID`).
        *   `ShippingZone` $\rightarrow$ `ZoneCost`. `ZoneCost` is a non-key attribute that depends on another non-key attribute (`ShippingZone`).
    *   To resolve this, we further decompose `orders_df` into:
        *   `customers_df`: Contains `CustomerID`, `CustomerName`, `CustomerCity`. `CustomerID` is the primary key.
        *   `shipping_zones_df`: Contains `ShippingZone`, `ZoneCost`. `ShippingZone` is the primary key.
        *   `orders_3nf_df`: The original `orders_df` but now only containing `OrderID`, `OrderDate`, and foreign keys (`CustomerID`, `ShippingZone`) to link to the new tables.
    *   All tables are now in 3NF, as there are no transitive dependencies.

5.  **BCNF (Boyce-Codd Normal Form)**:
    *   For the tables derived, they also satisfy BCNF because in each table, every determinant (an attribute or set of attributes that determines another attribute) is also a candidate key. For instance, in `shipping_zones_df`, `ShippingZone` determines `ZoneCost`, and `ShippingZone` is also the primary (and only candidate) key.

This Python example demonstrates the *structural transformation* of data to adhere to normalization principles, which is crucial for database design and ultimately for data quality in ML pipelines.

## Interview Questions

1.  **What is Database Normalization, and why is it important?**
    *   **Answer**: Database Normalization is a systematic process of organizing data in a relational database to reduce data redundancy and improve data integrity. It's important because it minimizes storage space, prevents data anomalies (insertion, update, deletion), ensures data consistency, and makes the database easier to maintain and query. For ML, it provides cleaner, more reliable data for training.

2.  **Explain the concept of Functional Dependency with an example.**
    *   **Answer**: A functional dependency $X \rightarrow Y$ means that the value of attribute set $X$ uniquely determines the value of attribute set $Y$. If you know $X$, you can always find $Y$. For example, in a `Students` table, `StudentID` $\rightarrow$ `StudentName` means that each `StudentID` corresponds to exactly one `StudentName`.

3.  **What are the main types of data anomalies that normalization helps to prevent?**
    *   **Answer**:
        *   **Insertion Anomaly**: Inability to add new data without also adding data for unrelated attributes.
        *   **Update Anomaly**: Needing to update the same information in multiple places, leading to inconsistencies if one update is missed.
        *   **Deletion Anomaly**: Losing valuable data unintentionally when deleting a record that contains other, unrelated information.

4.  **Describe First Normal Form (1NF). Provide an example of a table that violates 1NF and how to fix it.**
    *   **Answer**: A table is in 1NF if all its attributes contain atomic (indivisible) values, and there are no repeating groups of columns.
    *   **Violation Example**: A `Customers` table with a `PhoneNumbers` column containing "123-456-7890, 987-654-3210".
    *   **Fix**: Split `PhoneNumbers` into separate rows or create a separate `Customer_Phones` table, ensuring each phone number is in its own row.

5.  **What is Second Normal Form (2NF)? How does it differ from 1NF?**
    *   **Answer**: A table is in 2NF if it is in 1NF and all non-key attributes are fully functionally dependent on the *entire* primary key. It differs from 1NF by addressing partial dependencies, which occur when a non-key attribute depends on only a part of a composite primary key.

6.  **Explain Third Normal Form (3NF). What is a transitive dependency?**
    *   **Answer**: A table is in 3NF if it is in 2NF and there are no transitive dependencies. A transitive dependency occurs when a non-key attribute is functionally dependent on another non-key attribute. In other words, a non-key attribute should only depend on the primary key, not on other non-key attributes.
    *   **Example**: If `StudentID` $\rightarrow$ `Major` and `Major` $\rightarrow$ `DepartmentHead`, then `StudentID` $\rightarrow$ `DepartmentHead` is a transitive dependency.

7.  **What is Boyce-Codd Normal Form (BCNF), and how does it relate to 3NF?**
    *   **Answer**: BCNF is a stricter version of 3NF. A table is in BCNF if it is in 3NF and every determinant is a candidate key. It addresses specific anomalies that 3NF might miss, particularly in tables with multiple overlapping candidate keys where a non-key attribute determines part of a candidate key. All BCNF tables are 3NF, but not all 3NF tables are BCNF.

8.  **When might you choose to denormalize a database, and what are the potential trade-offs?**
    *   **Answer**: Denormalization is often chosen for performance optimization, especially in data warehousing or OLAP (Online Analytical Processing) systems where read performance for complex analytical queries is prioritized over write performance and strict data integrity.
    *   **Trade-offs**:
        *   **Pros**: Faster query execution for specific analytical queries, simpler queries (fewer joins), easier reporting.
        *   **Cons**: Increased data redundancy, higher risk of data anomalies and inconsistencies, larger storage requirements, more complex data maintenance.

9.  **How does database normalization benefit machine learning projects?**
    *   **Answer**: Normalized data is typically cleaner, more consistent, and less redundant. This directly benefits ML by:
        *   **Improving Data Quality**: Reduces noise and inconsistencies, leading to more accurate models.
        *   **Simplifying Feature Engineering**: Easier to extract and combine features from well-structured tables.
        *   **Reducing Data Preprocessing**: Less time spent on cleaning and handling anomalies.
        *   **Ensuring Data Integrity**: Models learn from reliable data, leading to more robust and generalizable predictions.

10. **Can a table be in 3NF but not in BCNF? If so, provide an example.**
    *   **Answer**: Yes, a table can be in 3NF but not in BCNF. This occurs when a table has multiple overlapping candidate keys, and a non-key attribute determines part of a candidate key.
    *   **Example**: Consider a `Student_Course_Professor` table with attributes `(StudentID, Course, Professor)`.
        *   Assume: `(StudentID, Course)` is a candidate key.
        *   Assume: `(StudentID, Professor)` is also a candidate key.
        *   Assume: `Professor` $\rightarrow$ `Course` (each professor teaches only one course).
        *   This table is in 3NF because there are no transitive dependencies. However, it's not in BCNF because `Professor` is a determinant (`Professor` $\rightarrow$ `Course`), but `Professor` alone is not a candidate key. To be in BCNF, `Professor` would need to be a candidate key.

## Quiz

1.  Which of the following is the primary goal of database normalization?
    A) To increase data redundancy for faster backups.
    B) To reduce data redundancy and improve data integrity.
    C) To make database queries more complex.
    D) To store all data in a single, large table.

2.  A table is in First Normal Form (1NF) if:
    A) All non-key attributes are fully functionally dependent on the primary key.
    B) It contains no transitive dependencies.
    C) All attributes contain atomic values and there are no repeating groups.
    D) Every determinant is a candidate key.

3.  What type of dependency does Second Normal Form (2NF) primarily address?
    A) Transitive dependency
    B) Multi-valued dependency
    C) Partial dependency
    D) Join dependency

4.  If a non-key attribute is functionally dependent on another non-key attribute, this violates which normal form?
    A) 1NF
    B) 2NF
    C) 3NF
    D) BCNF

5.  Which normal form is considered a stricter version of 3NF, requiring that every determinant be a candidate key?
    A) 1NF
    B) 2NF
    C) 3NF
    D) BCNF

### Answer Key

1.  **B) To reduce data redundancy and improve data integrity.**
    *   **Explanation**: This is the core purpose of normalization. Reducing redundancy saves space and prevents inconsistencies, while improving integrity ensures data accuracy and reliability.

2.  **C) All attributes contain atomic values and there are no repeating groups.**
    *   **Explanation**: 1NF is the most basic form, focusing on the structure of the data within cells and rows. Options A, B, and D relate to higher normal forms.

3.  **C) Partial dependency.**
    *   **Explanation**: 2NF specifically addresses partial dependencies, where a non-key attribute depends on only a part of a composite primary key.

4.  **C) 3NF.**
    *   **Explanation**: This describes a transitive dependency, which is the primary concern of Third Normal Form.

5.  **D) BCNF.**
    *   **Explanation**: Boyce-Codd Normal Form is a stricter version of 3NF that resolves anomalies that might still exist in 3NF tables where determinants are not candidate keys.

## Further Reading

1.  **Database System Concepts by Silberschatz, Korth, and Sudarshan**: A classic textbook for database systems, with detailed chapters on relational database design and normalization.
    *   [Amazon Link (for reference, search for latest edition)](https://www.amazon.com/Database-System-Concepts-Abraham-Silberschatz/dp/0078022150) (Note: This is a generic link, search for the specific edition you need)

2.  **Fundamentals of Database Systems by Elmasri and Navathe**: Another highly regarded textbook covering database theory, including comprehensive sections on functional dependencies and normal forms.
    *   [Amazon Link (for reference, search for latest edition)](https://www.amazon.com/Fundamentals-Database-Systems-Ramez-Elmasri/dp/0133970779) (Note: This is a generic link, search for the specific edition you need)

3.  **Wikipedia - Database Normalization**: A good starting point for a quick overview and links to more detailed explanations of each normal form.
    *   [https://en.wikipedia.org/wiki/Database_normalization](https://en.wikipedia.org/wiki/Database_normalization)

4.  **GeeksforGeeks - Normalization in DBMS**: Provides clear explanations and examples for each normal form.
    *   [https://www.geeksforgeeks.org/normalization-in-dbms/](https://www.geeksforgeeks.org/normalization-in-dbms/)