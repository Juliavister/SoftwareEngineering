import pyodbc
from db_conn import connection

cur = connection.cursor()
# Assuming 'cur' is a valid SQLite cursor object
latest = []

# Query each table and retrieve the latest row
for table_name in ['USD', 'PLN', 'NOK', 'TL']:
    cur.execute(f"SELECT TOP 1 * FROM {table_name} ORDER BY theDate DESC")
    result = cur.fetchone()
    latest.append(result)

rates = {"EUR": 1, "USD": latest[0][0], "PLN": latest[1][0], "NOK": latest[2][0], "TRY": latest[3][0]}

cur.close()
connection.close()
