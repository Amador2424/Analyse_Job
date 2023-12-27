from flask import Flask, request, jsonify
import snowflake.connector as sf
from dotenv import load_dotenv
import os
from pydantic import BaseModel
# Load environment variables from .env file
load_dotenv()
class JobSeeker(BaseModel):
    user_id: str
    cv: str
    skills: list
app = Flask(__name__)

def get_snowflake_connection():
    try:
        conn = sf.connect(
            user=os.getenv('USER'),
            password=os.getenv('PASSWORD'),
            account=os.getenv('ACCOUNT'),
            database=os.getenv('DATABASE')
        )
        return conn
    except Exception as e:
        print(f"Error connecting to Snowflake: {e}")
        raise

@app.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']  # Assurez-vous de hasher ce mot de passe en production
        email = data['email']

        conn = get_snowflake_connection()
        cs = conn.cursor()

        # Insérer l'utilisateur dans la base de données
        cs.execute("INSERT INTO Users (Username, Password, Email) VALUES (%s, %s, %s)", (username, password, email))
        conn.commit()

        # Récupérer l'ID de l'utilisateur
        cs.execute("SELECT UserID FROM Users WHERE Email = %s", (email,))
        user_id = cs.fetchone()[0]

        return jsonify({"status": "success", "message": "User registered successfully", "user_id": user_id}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cs.close()
        conn.close()
@app.route('/login', methods=['POST'])
def login_user():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']

        conn = get_snowflake_connection()
        cs = conn.cursor()
        cs.execute("SELECT Password FROM Users WHERE Username = %s", (username,))
        user_data = cs.fetchone()
        if user_data and user_data[0] == password:
            return jsonify({"status": "success", "message": "Login successful"}), 200
        else:
            return jsonify({"status": "error", "message": "Invalid username or password"}), 401
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cs.close()
        conn.close()

@app.route('/add_job_seeker', methods=['POST'])
def add_job_seeker():
    try:
        job_seeker_data = request.get_json()
        job_seeker = JobSeeker(**job_seeker_data)

        conn = get_snowflake_connection()
        cs = conn.cursor()

        cs.execute("INSERT INTO jobseekers (UserID, CV, Skills) VALUES (%s, %s, %s)",
                   (job_seeker.user_id, job_seeker.cv, ', '.join(job_seeker.skills)))
        conn.commit()

        return {"status": "success", "message": "Job seeker ajouté avec succès"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        if cs:
            cs.close()
        if conn:
            conn.close()
            
if __name__ == '__main__':
    app.run(debug=True)
