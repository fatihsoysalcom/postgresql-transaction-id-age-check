import os
import psycopg2
from psycopg2 import Error

# --- PostgreSQL Connection Configuration ---
# Set these environment variables before running the script.
# Example: export PG_HOST='localhost' PG_DBNAME='your_db' PG_USER='your_user' PG_PASSWORD='your_password'
DB_HOST = os.getenv('PG_HOST', 'localhost')
DB_NAME = os.getenv('PG_DBNAME', 'postgres') # Default to 'postgres' database
DB_USER = os.getenv('PG_USER', 'postgres')
DB_PASSWORD = os.getenv('PG_PASSWORD', '')

def check_xid_age():
    conn = None
    cursor = None
    try:
        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        print("--- PostgreSQL Transaction ID (XID) Age Check ---")
        print(f"Connected to: {DB_USER}@{DB_HOST}/{DB_NAME}")
        print("\nThis script demonstrates how to monitor Transaction ID (XID) age in PostgreSQL.")
        print("High XID age indicates proximity to a wraparound event, which can halt your database.")

        # 1. Get the current transaction ID
        cursor.execute("SELECT txid_current();")
        current_xid = cursor.fetchone()[0]
        print(f"\n1. Current Transaction ID (XID): {current_xid}")
        print("   (This shows the latest assigned XID. The wraparound risk is about the *age* of old XIDs.)")

        # 2. Check database-level XID age (datfrozenxid)
        # datfrozenxid is the transaction ID below which all transactions have been 'frozen' (marked as visible to all).
        # age(datfrozenxid) shows how many XIDs have been assigned since the oldest unfrozen XID in the database.
        # A high value (e.g., approaching 2 billion) indicates a potential wraparound issue.
        print("\n2. Database-level XID Age (age(datfrozenxid)):")
        cursor.execute("SELECT datname, age(datfrozenxid) FROM pg_database ORDER BY age(datfrozenxid) DESC;")
        db_xid_ages = cursor.fetchall()
        for db_name, xid_age in db_xid_ages:
            print(f"   Database '{db_name}': {xid_age} transactions old")
        print("   (Monitor these values. If any approach 2 billion, VACUUM FREEZE or autovacuum tuning is critical.)")

        # 3. Check table-level XID age (relfrozenxid)
        # Similar to datfrozenxid, but for individual tables. This helps identify specific tables
        # that might be preventing autovacuum from freezing old transactions.
        print("\n3. Top 10 Table-level XID Age (age(relfrozenxid)):")
        cursor.execute("SELECT relname, age(relfrozenxid) FROM pg_class WHERE relkind IN ('r', 'm') AND relfrozenxid IS NOT NULL ORDER BY age(relfrozenxid) DESC LIMIT 10;")
        table_xid_ages = cursor.fetchall()
        if table_xid_ages:
            for table_name, xid_age in table_xid_ages:
                print(f"   Table '{table_name}': {xid_age} transactions old")
        else:
            print("   No tables found with relfrozenxid (or not enough data).")
        print("   (High values here point to specific tables needing attention, e.g., manual VACUUM.)")

    except Error as e:
        print(f"Error connecting to PostgreSQL or executing query: {e}")
        print("Please ensure PostgreSQL is running and connection details (PG_HOST, PG_DBNAME, PG_USER, PG_PASSWORD) are correct.")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            print("\nConnection closed.")

if __name__ == "__main__":
    check_xid_age()
