from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def preprocess(text):
    return text.replace(" ", "")

def cosine_similarity_tfidf(sent1, sent2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([sent1, sent2])
    similarity_score =  cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()[0]
    print(f"유사도 점수: {similarity_score:.4f}")
    return similarity_score

def jaccard_similarity(sent1, sent2):
    set1 = set(sent1)
    set2 = set(sent2)
    return len(set1 & set2) / len(set1 | set2)

from Levenshtein import distance as levenshtein_distance

def levenshtein_similarity(sent1, sent2):
    return 1 - levenshtein_distance(sent1, sent2) / max(len(sent1), len(sent2))


def ngram_similarity(sent1, sent2, n=2):
    def ngrams(text, n):
        return [text[i:i + n] for i in range(len(text) - n + 1)]

    ngrams1 = set(ngrams(sent1, n))
    ngrams2 = set(ngrams(sent2, n))
    return len(ngrams1 & ngrams2) / len(ngrams1 | ngrams2)


def calculate_similarity(query1, query2):
    # Preprocess texts
    query1 = preprocess(query1)
    query2 = preprocess(query2)

    # Tokenize using a morphological analyzer (optional for Korean)
    # query1_tokens = tokenize_korean(query1)
    # query2_tokens = tokenize_korean(query2)

    # Calculate similarities
    cos_sim = cosine_similarity_tfidf(query1, query2)
    jac_sim = jaccard_similarity(query1, query2)
    lev_sim = levenshtein_similarity(query1, query2)
    ngram_sim = ngram_similarity(query1, query2)

    return {
        "cosine_similarity": f"{cos_sim:.4f}",
        "jaccard_similarity": jac_sim,
        "levenshtein_similarity": lev_sim,
        "ngram_similarity": ngram_sim,
    }


# Example usage
result = calculate_similarity("전세 자금 대풀트에 대해 알려줘", "전세자금대출")
print(result)

result = calculate_similarity("보금 자리 론에 대해 알려줘", "보금자리론")
print(result)

result = calculate_similarity("론 자리 보금에 대해 알려줘", "보금자리론")
print(result)