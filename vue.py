import streamlit as st
import requests
from io import BytesIO

st.set_page_config(page_title="Analyseur de CV", layout="wide")
st.title("Analyseur de CV Professionnel")
st.subheader("Découvrez les compétences et les opportunités d'emploi à partir de votre CV")

st.sidebar.title("Menu")
selected_option = st.sidebar.radio(
    "Choisissez une option",
    ("Ajouter un Nouveau User", "Se Connecter", "Ajouter un JobSeeker")
)

API_BASE_URL = "http://127.0.0.1:5000"
API_LOGIN_URL = API_BASE_URL + "/login"
API_REGISTER_URL = API_BASE_URL + "/register"
API_ADD_JOB_SEEKER_URL = API_BASE_URL + "/add_job_seeker"
API_UPLOAD_URL = "http://127.0.0.1:8000/uploadpdf/"

def display_register_form():
    with st.form(key="register_form"):
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        email = st.text_input("Email")
        submit_button = st.form_submit_button("S'inscrire")

        if submit_button:
            response = requests.post(API_REGISTER_URL, json={
        "username": username,
        "password": password,
        "email": email
    })
            if response.status_code == 201:
                response_data = response.json()
                user_id = response_data.get("user_id")
                st.success(f"Inscription réussie! Votre ID utilisateur est : {user_id}")
            else:
                st.error("Une erreur est survenue.")
def display_login_form():
    with st.form(key="login_form"):
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        submit_button = st.form_submit_button("Se connecter")

        if submit_button:
            response = requests.post(API_LOGIN_URL, json={
                "username": username,
                "password": password
            })
            if response.status_code == 200:
                st.success("Connexion réussie!")
               
            else:
                st.error("Identifiants incorrects.")
if selected_option == "Ajouter un Nouveau User":
    display_register_form()
elif selected_option == "Se Connecter":
    display_login_form()

uploaded_file = st.file_uploader("Choisissez un fichier PDF", type="pdf")
job_seeker_data = None

if uploaded_file is not None and selected_option == "Ajouter un JobSeeker":
    file_buffer = BytesIO(uploaded_file.getvalue())
    files = {"file": (uploaded_file.name, file_buffer, "application/pdf")}
    response = requests.post(API_UPLOAD_URL, files=files)

    if response.status_code == 200:
        st.success("Analyse réussie!")
        data = response.json()
        job_seeker_data = {
        "user_id": st.text_input("Entrez votre ID d'utilisateur pour enregistrer ces informations :"),
        "cv": uploaded_file.name,
        "skills": [match['skill'] for match in data['job_matches']]
        }

    st.subheader("Suite à l'analyse de vos compétences et aux compétences recherchées par les compagnies, voici les meilleurs choix pour vous :")

    for match in data['job_matches']:
        st.markdown(f"""
        - **Compétence que l'entreprise recherche:** {match['skill']}
        - **Nom de l'Entreprise :** {match['company']}
        - **Titre du Poste recherché :** {match['title']}
        ---
        """)
else:
    st.error("Une erreur est survenue lors de l'analyse.")

def display_job_seeker_form(job_seeker_data):
    if job_seeker_data and st.button("Enregistrer en tant que Job Seeker"):
        response = requests.post(API_ADD_JOB_SEEKER_URL, json=job_seeker_data)
        if response.status_code == 200:
            st.success("Job Seeker ajouté avec succès!")
        else:
            st.error("Erreur lors de l'ajout du Job Seeker.")

if uploaded_file is not None and selected_option == "Ajouter un JobSeeker" and job_seeker_data:
    display_job_seeker_form(job_seeker_data)
