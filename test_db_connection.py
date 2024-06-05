import psycopg2
try:
    conn = psycopg2.connect(
        dbname="edwardsjewelersdb",
        user="edwardsjewelersadmin",
        password="edwardsjewelerspassword",
        host="172.22.0.2",  # Directly use the DB container's IP to test
        port="5432"
    )
    print("Connection successful")
except Exception as e:
    print("Unable to connect to the database:", e)
finally:
    if conn:
        conn.close()
