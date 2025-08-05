from app import db, app
from sqlalchemy import text

print("Connecting to the database...")
with app.app_context():
    # Open and read the SQL file
    print("Reading schema.sql...")
    with open('schema.sql', 'r') as f:
        sql_script = f.read()

    # Execute the SQL script
    # We use a try-except block to catch any potential errors during execution
    try:
        print("Executing SQL script...")
        with db.engine.connect() as connection:
            # Split script into individual statements and execute them
            for statement in sql_script.split(';'):
                if statement.strip():
                    connection.execute(text(statement))
            # Commit the transaction to make the changes permanent
            connection.commit()
        print("Database schema created successfully from schema.sql!")
    except Exception as e:
        print(f"An error occurred: {e}")
