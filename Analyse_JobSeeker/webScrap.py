from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import time
import pandas as pd
# Initialize webDriver
driver_path = r'C:\Users\amado\Downloads\geckodriver-v0.33.0-win64\geckodriver.exe'
# Set your Firefox Options
options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'  # Adjust this if your path is different
driver = webdriver.Firefox(executable_path=driver_path, firefox_options=options)
#driver = webdriver.Chrome(executable_path=driver_path)

# Navigate to provided URL
url = 'https://www.apec.fr/candidat/recherche-emploi.html/emploi?lieux=711&typesConvention=143684&typesConvention=143685&typesConvention=143686&typesConvention=143687&page=0&motsCles=programmeur'
driver.get(url)
 
#wait= WebDriverWait(driver,10)
job_posts=[]
page=1
job_count=0
nbre_de_post=0
while job_count < 1000:
    try:
        btn = WebDriverWait(driver , 20  ).until(
            EC.element_to_be_clickable((By.XPATH,'//a[contains(text(),"Suiv.")]'))
        )
        btn.click()
        time.sleep(10)
        print(f'on est à la page {page}')
        page+=1
    except:
        pass
    soup = BeautifulSoup(driver.page_source,'html.parser')
    for card in soup.find_all('div', class_='card-offer__text'):
        if job_count >= 1000:
            break
        parent_element = card.find_parent('a')
        href = parent_element['href']
        print(f"URL de l'élément parent : {href}")
       
           
        company= card.find('p', class_='card-offer__company').text.strip()
        titre=card.find('h2', class_='card-title').text.strip()
        desc=card.find('p', class_='card-offer__description').text.strip()
        arrayUL=card.find_all('ul', class_='details-offer')
        salaire= arrayUL[0].find('img', alt='Salaire texte').parent.text.strip() if len(arrayUL[0])>=1 else 'N/A'
        typeC=arrayUL[1].find('img', alt='type de contrat').parent.text.strip() if len(arrayUL[1])>=1 else 'N/A'
        location=arrayUL[1].find('img', alt='localisation').parent.text.strip() if len(arrayUL[1])>=1 else 'N/A'
        dataP=arrayUL[1].find('img', alt='date de publication').parent.text.strip() if len(arrayUL[1])>=1 else 'N/A'
        print(f' La Compagnie : {company}')
        job_count+=1
        job_posts.append({
            'Company': company,
            'Title':titre,
            'Description':desc,
            'Salaire':salaire,
            'Type de Contrat':typeC,
            'Localisation':location,
            'Date de Publication':dataP
        })
    if(len(job_posts)==nbre_de_post):
        print('aucun changement')
        break
    nbre_de_post=len(job_posts)
   
    print(f'on a trouvé {job_count} emplois...')
df = pd.DataFrame(job_posts)
print('Saving data....')
df.to_csv('joBSave.csv', index=False)
driver.quit()