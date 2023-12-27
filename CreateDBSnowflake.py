from flask import Flask
import snowflake.connector as sf
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

def get_snowflake_connection():
    try:
        conn = sf.connect(
            user=os.getenv('USER'),
            password=os.getenv('PASSWORD'),
            account=os.getenv('ACCOUNT'),
            database=os.getenv('DATABASE')
        )
        print("Successfully connected to Snowflake.")
        return conn
    except Exception as e:
        print(f"Error connecting to Snowflake: {e}")
        raise

@app.route('/setup_db')
def setup_database():
    try:
        conn = get_snowflake_connection()
        cs = conn.cursor()

        # Fetch the database name from environment variables or define it
        database = os.getenv('DATABASE')

    #     # Create Database
    #     print('Creating Database...')
        #     # Create Tables 
    #     print('Creating Tables...')
    #     cs.execute("""
    #     CREATE OR REPLACE TABLE Users (
    #     UserID INT AUTOINCREMENT PRIMARY KEY,
    #     Username VARCHAR(255) NOT NULL,
    #     Password VARCHAR(255) NOT NULL,
    #     Email VARCHAR(255) NOT NULL
    #     );
    #     """)
    #     cs.execute("""
    #     CREATE OR REPLACE TABLE JobSeekers (
    #     JobSeekerID INT AUTOINCREMENT PRIMARY KEY,
    #     UserID INT,
    #     CV TEXT,
    #     Skills TEXT,
    #     FOREIGN KEY (UserID) REFERENCES Users(UserID)
    #     );
    #  """)
    #     cs.execute("""
    #     CREATE OR REPLACE TABLE Employers (
    #     EmployerID INT AUTOINCREMENT PRIMARY KEY,
    #     UserID INT,
    #     InfoProfile TEXT,
    #     Job_Posted INT,
    #     FOREIGN KEY (UserID) REFERENCES Users(UserID)
    #     );
    #     """)
    #     cs.execute("""
    #     CREATE OR REPLACE TABLE JobDetails (
    #     JobID INT AUTOINCREMENT PRIMARY KEY,
    #     Title VARCHAR(255),
    #     Descriptions TEXT,
    #     Skills TEXT,
    #     Salary DECIMAL(10,2),
    #     TypeJob VARCHAR(255),
    #     Enterprise VARCHAR(255),
    #     Localisation VARCHAR(255)
    #     );
    #     """)
    #     cs.execute("""
    #     CREATE OR REPLACE TABLE JobPostingManager (
    #     PostingManagerID INT AUTOINCREMENT PRIMARY KEY,
    #     JobID INT,
    #     EmployerID INT,
    #     FOREIGN KEY (JobID) REFERENCES JobDetails(JobID),
    #     FOREIGN KEY (EmployerID) REFERENCES Employers(EmployerID)
    #     );
    #     """)

    # # Example INSERT operation
    #     cs.execute("INSERT INTO Users (Username, Password, Email) VALUES ('testUser', 'testPass', 'test@example.com')")

    # # Example READ operation
    #     cs.execute("SELECT * FROM Users")
    #     print("Display data:")
    #     data = cs.fetchall()
    #     print(data)
    #     return "Database setup completed successfully."
    except Exception as e:
         return f"Error setting up database: {e}"

if __name__ == '__main__':
    setup_database()
    app.run(debug=True)
