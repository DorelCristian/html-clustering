
from sklearn.metrics.pairwise import cosine_similarity

def compute_cosine_sim(matrix):

    #Primește tfidf_matrix-ul și returnează matricea de similaritate cosine

    sim_matrix = cosine_similarity(matrix)
    return sim_matrix
