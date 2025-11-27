import pandas as pd
import mysql.connector as sql
from datetime import datetime

# -------------------------------
# 1. CONNECT TO MYSQL DATABASE
# -------------------------------
conn = sql.connect(
    host="localhost",
    user="root",
    password="",
    database="e_commerce"
)

# -------------------------------
# 2. LOAD ORDERS DATA
# -------------------------------
query = """
SELECT 
    customer_id,
    order_id,
    order_date,
    total_amount
FROM orders;
"""

df = pd.read_sql(query, conn)
df['order_date'] = pd.to_datetime(df['order_date'])
print("df['order_date']:",df['order_date'])
print("\n")

# -------------------------------
# 3. CALCULATE RFM METRICS
# -------------------------------

# Latest date in dataset
max_date = df['order_date'].max()

rfm = df.groupby('customer_id').agg({
    'order_date': lambda x: (max_date - x.max()).days,  # Recency
    'order_id': 'nunique',                              # Frequency
    'total_amount': 'sum'                               # Monetary
}).reset_index()

rfm.columns = ['customer_id', 'Recency', 'Frequency', 'Monetary']
print("rfm:",rfm)
print("\n")
print("rfm.columns:",rfm.columns)
print("\n")

# -------------------------------
# 4. RFM SCORING (1–5 scale)
# -------------------------------
rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5,4,3,2,1]).astype(int)
rfm['F_Score'] = pd.qcut(rfm['Frequency'], 5, labels=[1,2,3,4,5]).astype(int)
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1,2,3,4,5]).astype(int)

# Final RFM Score
rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)
print("rfm['R_Score']:",rfm['R_Score'])
print("\n")
print("rfm['F_Score']:",rfm['F_Score'])
print("\n")
print("rfm['M_Score']:",rfm['M_Score'])
print("\n")

print("rfm['RFM_Score']:",rfm['RFM_Score'])
print("\n")

# -------------------------------
# 5. SAVE OUTPUT TO EXCEL
# -------------------------------
rfm.to_excel("rfm_output.xlsx", index=False)

print("RFM scoring completed. Excel file saved as rfm_output.xlsx")
