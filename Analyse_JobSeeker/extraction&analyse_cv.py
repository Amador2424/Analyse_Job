from fastapi import FastAPI, UploadFile, File, HTTPException
from PyPDF2 import PdfReader
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import openai
from langdetect import detect
import os
from dotenv import load_dotenv
import numpy as np
import joblib
app = FastAPI()
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
data = pd.read_csv('job.csv')
model = joblib.load('job_model.joblib')
vectorizer = joblib.load('job_vectorizer.joblib')
encoder = joblib.load('job_encoder.joblib')

@app.post("/uploadpdf/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        reader = PdfReader(file.file)
        content = ""
        for page in reader.pages:
            text = page.extract_text() or ""
            content += text

        if not content:
            raise ValueError("Aucun texte extrait du PDF.")

        prompt_competences = "Extraire et catégoriser les compétences techniques du CV ci-joint.\n\n" + content
        response_competences = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt_competences,
            max_tokens=150
        )
        competences = response_competences.choices[0].text.strip()

        competences_vect = vectorizer.transform([competences])

        data_vect = vectorizer.transform(data['Description'])

        skills_encoded = model.predict(competences_vect)
        predicted_skills = encoder.inverse_transform(skills_encoded)

        job_matches_info = []
        for skill in predicted_skills:
            skill_vect = vectorizer.transform([skill])
            similarity = cosine_similarity(skill_vect, data_vect).flatten()
            top_match_index = np.argmax(similarity)
            job_match = data.iloc[top_match_index]

            job_matches_info.append({
                "skill": skill,
                "company": job_match['Company'],
                "title": job_match['Title']
            })

        return {"job_matches": job_matches_info}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
