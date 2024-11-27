import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from Levenshtein import distance as levenshtein_distance
import statistics

def preprocess_text(text):
    """
    한국어 텍스트에서 불필요한 조사 및 어미를 제거하는 함수.
    """
    unnecessary_words = ['에', '는', '이', '가', '을', '를', '의', '와', '과', '로', '으로', '에서', '에게', '께']

    pattern = '|'.join(unnecessary_words)
    processed_text = re.sub(pattern, '', text)
    return processed_text.strip().replace(" ","")  #공백 제거

def jaccard_similarity(sent1, sent2):
    set1 = set(sent1)
    set2 = set(sent2)
    return len(set1 & set2) / len(set1 | set2)

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
    query1 = preprocess_text(query1)
    query2 = preprocess_text(query2)

    jac_sim = jaccard_similarity(query1, query2)
    lev_sim = levenshtein_similarity(query1, query2)
    ngram_sim = ngram_similarity(query1, query2)

    results = [jac_sim, lev_sim, ngram_sim]
    return statistics.mean(results)


def getTopMeta(user_query):
    # JSON 파일들이 저장된 디렉토리 경로
    directory_path = '../doc/metadata'

    # JSON 데이터를 저장할 리스트
    json_data = []

    try:
        # 디렉토리 내 모든 파일 탐색
        for filename in os.listdir(directory_path):
            if filename.endswith('.json'):  # .json 확장자 확인
                file_path = os.path.join(directory_path, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)  # JSON 파일 로드
                    json_data.append(data)  # 로드된 데이터를 리스트에 추가
    except FileNotFoundError as e:
        print(f"Error: {e}")  # 디렉토리가 없을 경우 에러 메시지 출력

    print(user_query)

    similarity_scores =[]

    for record in json_data:
        # 사용자 쿼리와 레코드의 'title' 필드 간 유사도 계산
        title_similarity = calculate_similarity(user_query, record['title'])

        similarity_scores.append({'similarity': title_similarity})

    # 유사도 점수를 JSON 데이터와 매핑
    for record, score in zip(json_data, similarity_scores):
        record['similarity_score'] = score['similarity']
    #
    # 유사도 점수를 기준으로 정렬 (내림차순)
    ranked_records = sorted(json_data, key=lambda x: x['similarity_score'], reverse=True)

    # 출력 결과
    # for record in ranked_records:
    #     print(f"IDX: {record['idx']}, Title: {record['title']}, Similarity: {record['similarity_score']:.4f}")
    print(ranked_records)