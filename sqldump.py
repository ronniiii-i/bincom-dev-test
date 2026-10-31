import sqlite3
import MySQLdb

# Connect to local MySQL
mysql_conn = MySQLdb.connect(
    host="127.0.0.1", user="root", passwd="", db="bincom_test", port=3306
)
mysql_cursor = mysql_conn.cursor()

# Connect to SQLite
sqlite_conn = sqlite3.connect("db.sqlite3")
sqlite_cursor = sqlite_conn.cursor()

# Get all tables
mysql_cursor.execute("SHOW TABLES;")
tables = [t[0] for t in mysql_cursor.fetchall()]

for table in tables:
    # Get column names
    mysql_cursor.execute(f"DESCRIBE `{table}`;")
    columns = [col[0] for col in mysql_cursor.fetchall()]

    # Create table in SQLite
    cols_def = ", ".join([f"`{c}` TEXT" for c in columns])
    sqlite_cursor.execute(f"CREATE TABLE IF NOT EXISTS `{table}` ({cols_def});")

    # Copy rows
    mysql_cursor.execute(f"SELECT * FROM `{table}`;")
    rows = mysql_cursor.fetchall()
    placeholders = ", ".join(["?"] * len(columns))

    sqlite_cursor.executemany(
        f"INSERT INTO `{table}` VALUES ({placeholders});", rows
    )

sqlite_conn.commit()
mysql_conn.close()
sqlite_conn.close()
print("Database copied to db.sqlite3 successfully!")