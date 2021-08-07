import nltk
from text_unidecode import unidecode
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('portuguese')

for i, word in enumerate(stopwords):
    stopwords[i] = unidecode(word)

def treinar(resps):
    vectorizer = CountVectorizer(strip_accents='unicode', stop_words=stopwords)
    X = vectorizer.fit_transform([resposta['texto'] for resposta in resps])
    y = [resposta['nota'] for resposta in resps]

    modelo = LogisticRegression()
    modelo.fit(X, y)

    return pickle.dumps(modelo), pickle.dumps(vectorizer)

    

def avaliar(modelo, vetorizador, texto):
    modelo = pickle.loads(modelo)
    vetorizador = pickle.loads(vetorizador)
    return modelo.predict(vetorizador.transform([texto]))