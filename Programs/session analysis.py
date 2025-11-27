import mysql.connector
import pandas as pd

# -----------------------------
# 1. CONNECT TO MYSQL
# -----------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",                  # <-- your MySQL password
    database="e_commerce" # <-- replace with your DB name
)

# Load data from browsing behavior table
query = "SELECT * FROM browsing_behavior;"
df = pd.read_sql(query, conn)

conn.close()
print("Data Loaded Succesfully")
print("\n")

# -----------------------------
# 2. SESSION ANALYSIS
# -----------------------------

# A. Basic metrics
total_sessions = df['session_id'].nunique()
avg_duration = df['session_duration_sec'].mean()
avg_pages = df['pages_visited'].mean()

basic_metrics = pd.DataFrame({
    "Metric": ["Total Sessions", "Average Duration (sec)", "Average Pages per Session"],
    "Value": [total_sessions, avg_duration, avg_pages]
})

print("total_sessions:",total_sessions)
print("\n")
print("avg_duration:",avg_duration)
print("\n")
print("avg_pages:",avg_pages)
print("\n")
print("basic_metrics:",basic_metrics)
print("\n")

# B. Sessions per customer
sessions_per_customer = (
    df.groupby("customer_id")["session_id"]
    .nunique()
    .reset_index()
    .rename(columns={"session_id":"sessions_count"})
)
print("sessions_per_customer:",sessions_per_customer)
print("\n")

# C. Device-wise behavior
device_analysis = df.groupby('device_type').agg({
    'session_id': 'nunique',
    'session_duration_sec': 'mean',
    'pages_visited': 'mean'
}).reset_index()
print("device_analysis:",device_analysis)
print("\n")

# D. Top viewed categories
top_categories = (
    df['viewed_category']
    .value_counts()
    .reset_index()
)
top_categories.columns = ["Category", "Count"]

print("top_categories:",top_categories)
print("\n")
print("top_categories.columns:",top_categories.columns)
print("\n")

# E. Longest sessions
longest_sessions = df.sort_values("session_duration_sec", ascending=False).head(50)
print("longest_session:",longest_sessions)
print("\n")

# F. Heavy users
threshold = df['pages_visited'].mean()
heavy_users = df[df['pages_visited'] > threshold][['customer_id', 'pages_visited']]

print("threshold:",threshold)
print("\n")
print("heavy_users:",heavy_users)
print("\n")

# -----------------------------
# 3. SAVE ALL OUTPUTS TO EXCEL
# -----------------------------
output_path = "session_analysis_output.xlsx"

with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name="Raw Data", index=False)
    basic_metrics.to_excel(writer, sheet_name="Basic Metrics", index=False)
    sessions_per_customer.to_excel(writer, sheet_name="Sessions per Customer", index=False)
    device_analysis.to_excel(writer, sheet_name="Device Analysis", index=False)
    top_categories.to_excel(writer, sheet_name="Top Categories", index=False)
    longest_sessions.to_excel(writer, sheet_name="Longest Sessions", index=False)
    heavy_users.to_excel(writer, sheet_name="Heavy Users", index=False)

print("Excel file created:", output_path)
