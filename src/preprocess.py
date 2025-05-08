from bs4 import BeautifulSoup
import re

def extract_visible_text(html_content: str) -> str:

    #Primește conținutul HTML ca string și returnează textul vizibil,
    #fără tag-uri <script>, <style> sau spații inutile.

    soup = BeautifulSoup(html_content, "lxml")
    # Dezarhivează și elimină script/style/noscript
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ")
    # Înlocuiește multiple spații/taburi/linii noi cu un singur spațiu
    text = re.sub(r"\s+", " ", text).strip()
    return text

def load_and_extract(filepath: str) -> str:
    #Încarcă HTML-ul de pe disc și întoarce textul preprocesat.
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()
    return extract_visible_text(html)
