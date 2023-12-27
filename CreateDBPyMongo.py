from flask import Flask, request, jsonify
from pymongo import MongoClient, errors
import bcrypt

app = Flask(__name__)
client = MongoClient('mongodb://127.0.0.1:27017/', serverSelectionTimeoutMS=5000)
db = client['Job']

class UserModel:
    def __init__(self, username, password, email):
        self.username = username
        self.password = self.hash_password(password)
        self.email = email

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

class JobSeekerModel:
    def __init__(self, user_id, cv, skills):
        self.user_id = user_id
        self.cv = cv
        self.skills = skills

class EmployerModel:
    def __init__(self, user_id, info_profile, job_posted):
        self.user_id = user_id
        self.info_profile = info_profile
        self.job_posted = job_posted

class JobDetailsModel:
    def __init__(self, title, descriptions, skills, salary, type_job, enterprise, location):
        self.title = title
        self.descriptions = descriptions
        self.skills = skills
        self.salary = salary
        self.type_job = type_job
        self.enterprise = enterprise
        self.location = location

class JobPostingManagerModel:
    def __init__(self, job_id, employer_id):
        self.job_id = job_id
        self.employer_id = employer_id


if __name__ == '__main__':
    try:
        client.server_info()
        print("MongoDB server is connected.")
    except errors.ServerSelectionTimeoutError:
        print("Failed to connect to MongoDB server. Please check if MongoDB is running on the specified port.")

    app.run(debug=True)
