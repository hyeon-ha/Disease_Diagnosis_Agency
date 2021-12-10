from gensim.models import Word2Vec
from scipy.io import mmwrite, mmread
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import pandas as pd
import pickle


def create_tfidf():
    data = pd.read_csv('./crawling_data/cleaned_disease_content.csv')
    tfidf = TfidfVectorizer(sublinear_tf=True)
    tfidf_matrix = tfidf.fit_transform(data['cleaned_content'])
    with open ('./models/tfidf.pickle', 'wb') as f:
        pickle.dump(tfidf, f)

    save_filename = 'tfidf_disease_detected_agency.mtx'
    mmwrite(f'./models/{save_filename}', tfidf_matrix)
    print(f'"{save_filename}" is saved.')


def getRecommendation(cosine_sim, view_count):
    data = pd.read_csv('./crawling_data/cleaned_disease_content.csv')
    sim_score = list(enumerate(cosine_sim[-1]))
    sim_score = sorted(sim_score, key=lambda x: x[1], reverse=True)
    sim_score = sim_score[1:view_count + 1]
    disease_index = [i[0] for i in sim_score]
    recommend_disease_list = data.iloc[disease_index]
    return recommend_disease_list


def main_function(keyword_flag, keywords, elements):
    data = pd.read_csv('./crawling_data/cleaned_disease_content.csv')
    tfidf_matrix = mmread('./models/tfidf_disease_detected_agency.mtx').tocsr()
    with open('./models/tfidf.pickle', 'rb') as f:
        tfidf = pickle.load(f)

    # 병명(Disease)을 이용하여 유사 워드 찾기
    if not keyword_flag:
        keyword = '(장관감염증)\n살모넬라균 감염증'
        disease_index = data[data['Disease'] == keyword].index[0]
        print(f'disease_index: {disease_index}')
        print(f'result: {data["Disease"][209]}')

        cosine_sim = linear_kernel(tfidf_matrix[disease_index], tfidf_matrix)
        recommendation = getRecommendation(cosine_sim, view_count=elements)
        print(recommendation.iloc[:, 0])

        return None
    else:
        # 증상(Symptom)을 이용하여 유사 워드 찾기
        # Embedding 모델 불러오기
        read_filename = None
        for file in os.listdir((os.getcwd() + '/models/').replace('\\', '/')):
            if file.split('.')[-1] == 'model':
                read_filename = file
                break
        embedding_model = Word2Vec.load(f'./models/{read_filename}')

        keyword = '가래'
        sentence = [keywords] * 10
        sim_word = embedding_model.wv.most_similar(keywords, topn=elements)
        words = []
        for word, _ in sim_word:
            words.append(word)

        for i, word in enumerate(words):
            sentence += [word] * (10 - i)
        sentence = ' '.join(sentence)

        sentence_vec = tfidf.transform([sentence])
        cosine_sim = linear_kernel(sentence_vec, tfidf_matrix)
        recommendation = getRecommendation(cosine_sim, view_count=elements)
        return recommendation['cleaned_content']


if __name__ == '__main__':
    # create_tfidf()
    ret_val = main_function(keyword_flag=True, keywords='가래', elements=10)
