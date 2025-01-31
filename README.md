# Paris Olympics 2024 Data

This project uses the https://www.kaggle.com/datasets/piterfm/paris-2024-olympic-summer-games?resource=download dataset to build a database
that is then used to create a website displaying the data within.

Many thanks to Petro for this phenomenal dataset.

## Features

- Converts csvs into a PostgreSQL database.
- Utilises the React framework to build an informative dashboard. (in progress)

## Getting Started

### Prerequisites

- Python 3.x installed on your system.
- PostgreSQL installed on your system.
- Pandas, sqlachemy and psycopg2 installed on your system or within your environment. They can be installed using this command:
    ```bash
    pip install pandas sqlachemy psycopg2
    ```

### Creating the database.

- To create the database, create a file called "create_db.py" within the po24 directory and run it.
- The file contents are as follows:

    ```bash
    import psycopg2
    from psycopg2 import sql

    # Database connection parameters
    db_user = 'db_user'        # Replace with your PostgreSQL user
    db_password = 'db_password'   # Replace with your PostgreSQL password
    db_host = 'db_host'     # localhost for example
    db_port = 'db_port'     # 5432 or 8000 for example

    # Connect to the default PostgreSQL database
    conn = psycopg2.connect(
        dbname='postgres',  # Connect to the default 'postgres' database
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    conn.autocommit = True  # Enable autocommit mode to allow database creation

    # Create a cursor object
    cur = conn.cursor()

    # Define the database name and schemas
    db_name = 'Paris_Olympics_2024'
    schemas = ['General', 'Results']

    # Create the new database
    cur.execute(sql.SQL("CREATE DATABASE {}").format(
        sql.Identifier(db_name))
    )

    # Close the connection to the default database
    cur.close()
    conn.close()

    # Reconnect to the newly created database
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    conn.autocommit = True  # Enable autocommit mode for schema creation

    # Create a new cursor object
    cur = conn.cursor()

    # Create schemas
    for schema in schemas:
        cur.execute(sql.SQL("CREATE SCHEMA {}").format(
            sql.Identifier(schema))
        )
        print(f"Schema '{schema}' created.")

    # Close the cursor and connection
    cur.close()
    conn.close()

    print(f"Database '{db_name}' and schemas created successfully.")

    ```

### Creating the API endpoints.

- To create the API endpoints, create a .py file and use 
- The file contents are as follows:

    ```bash
    from flask import Flask, jsonify
    from flask_cors import CORS
    import psycopg2

    app = Flask(__name__)
    CORS(app, origins=['http://localhost:3000']) # Restricting to React's origins
    

    def get_db_connection():
        conn = psycopg2.connect(
            dbname='dbname',  # Replace placeholder values with your required values
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        return conn

    @app.route('/api/medals')   # Name the API something relevant 
    def get_medals_data():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM "General"."Medals"') # Use the SQL query neccessary
        medals = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(medals)

    if __name__ == '__main__':
        app.run(debug=True)

    ```