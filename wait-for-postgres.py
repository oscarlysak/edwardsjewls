import sys
import psycopg2
from time import sleep
import subprocess  # Needed to call Django manage.py commands

def wait_for_postgres(dbname, user, password, host):
    while True:
        try:
            conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
            conn.close()
            print("PostgreSQL is ready!")
            break
        except psycopg2.OperationalError:
            print("PostgreSQL is not ready. Waiting...")
            sleep(1)

    # Once DB is ready, execute further commands
    print("Running Django migrations...")
    subprocess.call(['python', 'manage.py', 'migrate'])

    print("Populating the database with initial data...")
    subprocess.call(['python', 'manage.py', 'populate_users'])

    print("Starting Django development server...")
    subprocess.call(['python', 'manage.py', 'runserver', '0.0.0.0:8000'])

if __name__ == "__main__":
    wait_for_postgres(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
