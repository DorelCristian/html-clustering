# src/loader.py

import os

def list_html_files(root_dir="data"):

    #parcurg directorul si returnez toate fisierele .html
    html_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for fname in filenames:
            if fname.lower().endswith(".html"):
                full_path = os.path.join(dirpath, fname)
                html_files.append(full_path)
    return html_files

