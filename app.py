import psycopg2
from psycopg2 import pool
import datetime
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    #return "Hello, Test web App!"
    # Build a connection string from the variables
    host = "c.akamaipoc-postgres-db.postgres.database.azure.com"
    dbname = "citus"
    user = "citus"
    password = "Akamai123"
    sslmode = "require"
    try:
        conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
        postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(1, 20,conn_string)
        if (postgreSQL_pool):
            print("Connection pool created successfully")

        # Use getconn() to get a connection from the connection pool
        conn = postgreSQL_pool.getconn()
        cursor = conn.cursor()
    except Exception as err:
        return "error :" + str(serr)

    '''
    cursor.execute("SELECT * FROM Events;")
    rows = cursor.fetchall()

    # Print all rows
    for row in rows:
        print("Data row = (%s, %s, %s)" %(str(row[0]), str(row[1]), str(row[2])))

    '''
    now = datetime.datetime.now()
    current_time = now.strftime("%Y:%m:%d:%H:%M:%S")


    # Drop previous table of same name if one exists
    cursor.execute("DROP TABLE IF EXISTS Events;")
    print("Finished dropping table (if existed)")

    # Create a table
    cursor.execute("CREATE TABLE Events (event_id SERIAL, timestamp text, event text);")
    print("Finished creating table")

    # Create a index
    cursor.execute("CREATE INDEX idx_event_id ON Events(event_id);")
    print("Finished creating index")

    # Insert some data into the table
    cursor.execute("INSERT INTO Events  (timestamp, event) VALUES (%s, %s);", (current_time,"Test Event"))
    print("Inserted 2 rows of data")

    # Clean up
    conn.commit()
    cursor.close()
    conn.close()
    return "done"
