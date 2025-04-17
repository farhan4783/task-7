import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Create and connect to the SQLite database
conn = sqlite3.connect("sales_data.db")
cursor = conn.cursor()

# Step 2: Create a simple 'sales' table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT,
    quantity INTEGER,
    price REAL
)
""")

# Step 3: Insert sample sales data
sample_data = [
    ("Apples", 10, 0.5),
    ("Bananas", 15, 0.3),
    ("Oranges", 8, 0.6),
    ("Apples", 5, 0.5),
    ("Bananas", 12, 0.3),
    ("Oranges", 10, 0.6),
]
cursor.executemany("INSERT INTO sales (product, quantity, price) VALUES (?, ?, ?)", sample_data)
conn.commit()

# Step 4: Run SQL query to get summary
query = """
SELECT product,
       SUM(quantity) AS total_qty,
       SUM(quantity * price) AS revenue
FROM sales
GROUP BY product
"""

df = pd.read_sql_query(query, conn)

# Step 5: Print the results
print("Sales Summary:\n")
print(df)

# Step 6: Plot a bar chart for revenue by product
df.plot(kind='bar', x='product', y='revenue', legend=False, color='skyblue')
plt.title("Revenue by Product")
plt.ylabel("Revenue ($)")
plt.tight_layout()
plt.savefig("sales_chart.png")
plt.show()

# Step 7: Close the connection
conn.close()
