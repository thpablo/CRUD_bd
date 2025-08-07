from app import db, app
from sqlalchemy import text

def execute_sql_from_file(connection, filepath):
    print(f"Reading and executing {filepath}...")
    with open(filepath, 'r') as f:
        sql_script = f.read()

    # Split script into individual statements and execute them
    # This is important for compatibility across different SQL databases.
    for statement in sql_script.split(';'):
        if statement.strip():
            connection.execute(text(statement))
    print(f"Successfully executed {filepath}")

print("Connecting to the database...")
with app.app_context():
    try:
        with db.engine.connect() as connection:
            print("Starting database creation process...")

            # Begin a transaction
            trans = connection.begin()

            # Execute init.sql to create schema
            execute_sql_from_file(connection, 'init.sql')

            # Execute populate.sql to insert data
            execute_sql_from_file(connection, 'populate.sql')

            # Commit the transaction to make the changes permanent
            trans.commit()

            print("\nDatabase created and populated successfully from init.sql and populate.sql!")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        # If an error occurs, the transaction should be rolled back automatically
        # by the 'with' statement context exit.
        print("Transaction rolled back due to an error.")
