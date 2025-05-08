#Proiect HTML Clustering
Am construit un pipeline modular in python care grupeaza documentele HTML pe baza similaritatii. Solutia compara si alege cel mai bun algoritm ( dintre DBSCAN si AgglomerativeClustering) si parametrii pentru fiecare set de date.

##Prezentarea solutiei:
1. **Incarcarea datelor : loader.py**
      Parcurge folderul de intrare si obtine lista cu fisiere .html
2. **Preprocesarea datelor : preprocess.py**
      Elimina tagurile <script>, <style>, <noscript> si comentariile. Normalizeaza spatiile si extrage textul vizibil
3. **Extractia de caracteristici: features.py**
      Construieste o matrice TF-IDF
4.  **Calculul similaritatii: similarity.py**
      Calculeaza similaritatea cosine intre documente, returneaza o matrice NxN cu valori intre 0 si 1
5.  **Clustering : cluster.py**
      Am ales sa fac 2 algoritmi diferiti si apoi sa ii compar, sa aleg pe cel mai bun.
      Agglomerative: linkage complet, distanta= 1 - cosine_similarity
      DBSCAN: metrica precomputed, distanta este tot 1-cosine_similarity
6.  **Tuning si alegere automata : main.py**
      Ruleaza grid-search peste : threshold pentru Agglomerative si peste eps si min_samples pentru DBSCAN
      Calculeaza silhouette_score , metrica cosine, si alege algoritmul cel mai eficient si parametrii cu cel mai bun scor.

Am folosit: 
      TF-IDF + Cosine, deoarece este rapid si eficient pentru text
      Agglomerative vs DBSCAN ca sa combin un algoritm ierarhic cu unul density-based
      Folosesc Silhouette Score deoarece ofera o masura obiectiva asupra performantei celor 2 algoritmi
      Modularitate
##Structura proiectului

html-clustering/
├── data/               # Subdirectoare tier1–tier4 cu fișiere HTML
├── src/
│   ├── loader.py       # Listare recursivă fișiere .html
│   ├── preprocess.py   # Extracție text vizibil
│   ├── features.py     # TF–IDF vectorization
│   ├── similarity.py   # Cosine similarity matrix
│   ├── cluster.py      # Funcții de clustering Agglomerative & DBSCAN
│   └── main.py         # Entry-point pentru tuning și salvare JSON
├── requirements.txt    # Dependențe Python (BeautifulSoup4, scikit-learn etc.)
├── README.md           # Documentație și instrucțiuni
└── .gitignore          # Ignoră venv, __pycache__, fișiere generate 


##Utilizare proiect

Ruleaza scriptul: python src/main.py --input data/tier1 --output tier1_clusters.json
unde:
      --input este calea catre directorul cu fisiere HTML 
      --output numele fisierului JSON in care sa salvam rezultatul
