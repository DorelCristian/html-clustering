import numpy as np

from sklearn.cluster import AgglomerativeClustering, DBSCAN

def cluster_documents(sim_matrix: np.ndarray, threshold: float = 0.5):
    # transform similaritatea în distanță
    dist_matrix = 1.0 - sim_matrix

    clustering = AgglomerativeClustering(
        n_clusters=None,
        metric="precomputed",
        linkage="complete",
        distance_threshold=1.0 - threshold
    )
    labels = clustering.fit_predict(dist_matrix)

    clusters: dict[int, list[int]] = {}
    for idx, lab in enumerate(labels):
        clusters.setdefault(lab, []).append(idx)

    return list(clusters.values())

def cluster_dbscan(sim_matrix: np.ndarray,
                   eps: float = 0.5,
                   min_samples: int = 2) -> list[list[int]]:
    """
    Clustering DBSCAN pe matricea de similaritate.
    Fiecare doc apare exact o dată; outlierii devin clustere singleton.
    """
    # Transform similaritatea în distanță și orice negativ devine 0
    dist = 1.0 - sim_matrix
    dist = np.clip(dist, 0.0, None)

    db = DBSCAN(
        eps=eps,
        min_samples=min_samples,
        metric="precomputed"
    )
    labels = db.fit_predict(dist)

    # Grupez indexii
    clusters: dict[int, list[int]] = {}
    noise = []
    for idx, lab in enumerate(labels):
        if lab == -1:
            noise.append(idx)
        else:
            clusters.setdefault(lab, []).append(idx)

    #  Transform fiecare outlier într-un cluster singleton
    for idx in noise:
        clusters.setdefault(f"noise_{idx}", []).append(idx)

    return list(clusters.values())
