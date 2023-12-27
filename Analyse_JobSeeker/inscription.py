import streamlit as st
import requests

# Initialisation des variables de session
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Configuration de la page
st.set_page_config(page_title="Analyseur de CV", layout="wide")

API_LOGIN_URL = "http://127.0.0.1:5000/login"
API_REGISTER_URL = "http://127.0.0.1:5000/register"

# Fonction pour afficher la page d'inscription
def show_register_page():
    st.title("Inscription")
    new_username = st.text_input("Nom d'utilisateur", key="register_username")
    new_password = st.text_input("Mot de passe", type='password', key="register_password")
    new_email = st.text_input("Email", key="register_email")

    if st.button('S\'inscrire', key='register_button'):
        register_data = {"username": new_username, "password": new_password, "email": new_email}
        response = requests.post(API_REGISTER_URL, json=register_data)
        if response.status_code == 201:
            st.success("Inscription réussie!")
            st.session_state['logged_in'] = False  # L'utilisateur doit se connecter après l'inscription
        else:
            st.error("Échec de l'inscription")

# Fonction pour afficher la page de connexion
def show_login_page():
    st.title("Connexion")
    username = st.text_input("Nom d'utilisateur", key="login_username")
    password = st.text_input("Mot de passe", type='password', key="login_password")

    if st.button('Se connecter', key='login_button'):
        login_data = {"username": username, "password": password}
        response = requests.post(API_LOGIN_URL, json=login_data)
        if response.status_code == 200:
            st.success("Connexion réussie!")
            st.session_state['logged_in'] = True
        else:
            st.error("Échec de la connexion")

# Fonction pour afficher le lien vers l'analyse de CV
def show_cv_analyzer_link():
    st.markdown("Cliquez sur le lien ci-dessous pour analyser votre CV:")
    st.markdown("[Analyser mon CV](http://localhost:8502)")

# Affichage de la page en fonction de l'état de session
if st.session_state['logged_in']:
    show_cv_analyzer_link()
else:
    show_login_page()
    st.button('Inscription', on_click=lambda: show_register_page())
