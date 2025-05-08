# src/main.py

import argparse
import os
import json
import numpy as np
from sklearn.metrics import silhouette_score

from loader import list_html_files
from preprocess import load_and_extract
from features import build_tfidf_matrix
from similarity import compute_cosine_sim
from cluster import cluster_documents, cluster_dbscan

# Range‐uri hard‐codate pentru tuning
AGGLO_MIN, AGGLO_MAX, AGGLO_STEPS = 0.5, 1.0, 6
DB_EPS_MIN, DB_EPS_MAX, DB_EPS_STEPS = 0.3, 0.9, 7
DB_MIN_SAMPLES, DB_MAX_SAMPLES     = 2,   5

def labels_from_clusters(clusters_idx, n_docs):
    labels = np.full(n_docs, -1, dtype=int)
    for i, grp in enumerate(clusters_idx):
        for idx in grp:
            labels[idx] = i
    return labels

def parse_args():
    p = argparse.ArgumentParser(
        description="Tuning automat Agglomerative vs DBSCAN pentru un folder cu HTML."
    )
    p.add_argument(
        "--input",
        required=True,
        help="Folder cu HTML-uri (ex: data/tier1)"
    )
    p.add_argument(
        "--output",
        default="clusters_tuned.json",
        help="Fișier JSON de output (default: clusters_tuned.json)"
    )
    return p.parse_args()

def main():
    args = parse_args()
    files      = list_html_files(args.input)
    texts      = [load_and_extract(fp) for fp in files]
    tfidf, vec = build_tfidf_matrix(texts)
    sim_matrix = compute_cosine_sim(tfidf)
    n_docs     = len(files)

    best = {
        'agglo': {'score': -1, 'threshold': None, 'clusters': None},
        'dbscan': {'score': -1, 'eps': None, 'min_samples': None, 'clusters': None}
    }

    # 1) Grid‐search Agglomerative
    for thr in np.linspace(AGGLO_MIN, AGGLO_MAX, AGGLO_STEPS):
        clusters = cluster_documents(sim_matrix, threshold=thr)
        labels   = labels_from_clusters(clusters, n_docs)
        k = len(set(labels))
        if 2 <= k < n_docs:
            score = silhouette_score(tfidf, labels, metric='cosine')
            if score > best['agglo']['score']:
                best['agglo'].update({'score': score, 'threshold': thr, 'clusters': clusters})

    # 2) Grid‐search DBSCAN
    for eps in np.linspace(DB_EPS_MIN, DB_EPS_MAX, DB_EPS_STEPS):
        for ms in range(DB_MIN_SAMPLES, DB_MAX_SAMPLES + 1):
            clusters = cluster_dbscan(sim_matrix, eps=eps, min_samples=ms)
            labels   = labels_from_clusters(clusters, n_docs)
            k = len(set(labels))
            if 2 <= k < n_docs:
                score = silhouette_score(tfidf, labels, metric='cosine')
                if score > best['dbscan']['score']:
                    best['dbscan'].update({
                        'score': score,
                        'eps': eps,
                        'min_samples': ms,
                        'clusters': clusters
                    })

    # 3) Afișăm rezultatele tuning‐ului
    print(f"-- Tuning pentru: {args.input}")
    if best['agglo']['threshold'] is not None:
        print(f"Agglomerative → threshold={best['agglo']['threshold']:.3f}, silhouette={best['agglo']['score']:.4f}")
    else:
        print("Agglomerative → nici un clustering valid găsit.")
    if best['dbscan']['eps'] is not None:
        print(f"DBSCAN        → eps={best['dbscan']['eps']:.3f}, min_samples={best['dbscan']['min_samples']}, silhouette={best['dbscan']['score']:.4f}")
    else:
        print("DBSCAN        → nici un clustering valid găsit.")
    print()

    # 4) Alegem cel mai bun
    if best['agglo']['score'] >= best['dbscan']['score']:
        chosen, clusters_best = 'Agglomerative', best['agglo']['clusters']
    else:
        chosen, clusters_best = 'DBSCAN', best['dbscan']['clusters']
    print(f"Algoritm ales: {chosen}")

    # 5) Salvăm grupările
    output_clusters = [
        [os.path.basename(files[i]) for i in grp]
        for grp in clusters_best
    ]
    with open(args.output, 'w', encoding='utf-8') as fo:
        json.dump(output_clusters, fo, ensure_ascii=False, indent=2)
    print(f"Grupe salvate în {args.output}")

if __name__ == "__main__":
    main()
