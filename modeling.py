from datetime import datetime
from gensim.models import Word2Vec
from matplotlib import font_manager, rc
from sklearn.manifold import TSNE
from PIL import Image
from wordcloud import WordCloud
import collections
import gensim
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import pandas as pd
import time


def initialize_font():
    font_path = './env/malgun.ttf'
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    mpl.rcParams['axes.unicode_minus'] = False
    rc('font', family=font_name)
    plt.rc('font', family=font_name)


def create_word2vec_model():
    start_time = time.time()
    options = {'size': 100, 'window': 4, 'min_count': 5, 'workers': 6, 'cycle': 100, 'sg': 1}
    save_filename = f'Word2VecModel_{datetime.now().strftime("%y%m%d_%H%M%S")}.model'

    data = pd.read_csv(f'./crawling_data/cleaned_disease_content.csv')
    cleaned_token_content = list(data['cleaned_content'])
    cleaned_tokens = []
    for content in cleaned_token_content:
        token = content.split()
        cleaned_tokens.append(token)
    print(f'create "cleaned_tokens" variable.\t\truntime is {time.time() - start_time:.3f} seconds.')

    # 모델 학습
    # gensim 패키지 버전에 따라 매개변수명 이름이 다르기 때문에 아래와 같이 선언하였음.
    start_time = time.time()
    if gensim.__version__ < '4.0.0':
        embedding_model = Word2Vec(cleaned_tokens, size=options['size'], window=options['window'],
                                   min_count=options['min_count'], workers=options['workers'],
                                   iter=options['cycle'], sg=options['sg'])
    else:
        embedding_model = Word2Vec(cleaned_tokens, size=options['size'], window=options['window'],
                                   min_count=options['min_count'], workers=options['workers'],
                                   epochs=options['cycle'], sg=options['sg'])
    # gensim 패키지 버전에 따라 출력 방식에 차이가 있어 아래와 같이 선언하였음.
    if gensim.__version__ < '4.0.0':
        save_filename = f'Word2VecModel_{len(embedding_model.wv.vocab.keys())}words.model'
        print(embedding_model.wv.vocab.keys())
        print(len(embedding_model.wv.vocab.keys()))
    else:
        save_filename = f'Word2VecModel_{len(list(embedding_model.wv.vocab.key))}words.model'
        print(list(embedding_model.wv.vocab.key))
        print(len(list(embedding_model.wv.vocab.key)))
    # 모델 저장
    embedding_model.save(f'./models/{save_filename}')
    print(f'"{save_filename}" is saved.\t\truntime is {time.time() - start_time:.3f} seconds.')


def visualize_word2vec_model(**kwargs):
    cloud_flag = kwargs['cloud'] if 'cloud' in kwargs else False
    # 폰트 설정
    initialize_font()
    # 모델 불러오기
    read_filename = None
    for file in os.listdir((os.getcwd() + '/models/').replace('\\', '/')):
        if file.split('.')[-1] == 'model':
            read_filename = file
            break

    embedding_model = Word2Vec.load(f'./models/{read_filename}')

    keyword = '가래'
    sim_word = embedding_model.wv.most_similar(keyword, topn=10)

    vectors, labels = [], []
    for label, _ in sim_word:
        vectors.append(embedding_model.wv[label])
        labels.append(label)
    df_vectors = pd.DataFrame(vectors)

    # t-SNE 모델 선언
    tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500)
    new_value = tsne_model.fit_transform(df_vectors)
    # 결과 확인
    xy = pd.DataFrame({'words': labels, 'x': new_value[:, 0], 'y': new_value[:, 1]})
    print(xy.tail(10))

    # Plot 그리기
    xy.loc[xy.shape[0]] = (keyword, 0, 0)           # keyword 로 사용하고있는 단어의 중심 좌표 설정
    plt.figure(figsize=(10, 10))
    plt.scatter(0, 0, s=1500, marker='*')           # (0, 0) 좌표에 별 모양을 가진 마커를 1500의 크기로 그린다.
    for i in range(len(xy.x) - 1):
        a = xy.loc[[i, (len(xy.x) - 1)], :]
        plt.plot(a.x, a.y, '-D', linewidth=2)
        plt.annotate(xy.words[i], xytext=(1, 1), xy=(xy.x[i], xy.y[i]), textcoords='offset points', ha='right', va='bottom')
    plt.show()

    if cloud_flag:
        # 키워드 매개변수에는 병명(Disease)을 입력하셔야 합니다.
        sketch_word_cloud(keyword='황열')


def sketch_word_cloud(keyword):
    font_path = './env/malgun.ttf'
    df_contents = pd.read_csv('./crawling_data/cleaned_disease_content.csv')

    words = df_contents[df_contents['Disease'] == keyword]['cleaned_content']
    words = words.iloc[0].split()
    word_dict = dict(collections.Counter(words))
    word_cloud_img = WordCloud(background_color='white', max_words=2000, font_path=font_path).generate_from_frequencies(word_dict)
    plt.figure(figsize=(12, 12))
    plt.imshow(word_cloud_img, interpolation='bilinear')
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    create_word2vec_model()
    # visualize_word2vec_model(cloud=True)
