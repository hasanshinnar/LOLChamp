import pyodbc

try:
    conn = pyodbc.connect(
        r"Driver={ODBC Driver 17 for SQL Server};"
        r"Server=DESKTOP-JAB9N5J\SQLEXPRESS;"
        "Database=LOLChamps;"
        "Trusted_Connection=yes;"
    )
    print("Connection Successful!")
except Exception as e:
    print("Connection failed:", e)
