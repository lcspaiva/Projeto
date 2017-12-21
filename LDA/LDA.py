import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import gensim
from gensim import corpora, models


docs_raw = []
noticia = ""

#extraindo as noticias dos txts para memoria
for i in range (1, 11):
    with open ("doc" + str(i) + ".txt", "r") as documento:
        for linha in documento:
            noticia += linha.rstrip()
        docs_raw.append(noticia)
        noticia=""

#tokenizando e removendo as palavras indesejadas
docs_ts = [] #lista com listas dos documentos tokenizados e sem stopwords
for doc in docs_raw:
    tokens = [w for w in word_tokenize(doc.lower()) if w.isalpha()]
    no_stops = [t for t in tokens if t not in stopwords.words('portuguese')]
    docs_ts.append(no_stops)


#lemantizando os tokens
lemmatizer = nltk.stem.snowball.PortugueseStemmer()
docs_lm = [] #documentos lemantizados
for doc in docs_ts:
    lemmatized = [lemmatizer.stem(t) for t in doc]
    docs_lm.append(lemmatized)


dictionary = corpora.Dictionary(docs_ts)
corpus = [dictionary.doc2bow(texts) for texts in docs_ts]

ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=6, id2word = dictionary, passes=20)
#print(ldamodel.print_topics(num_topics=8, num_words=15))
topicos = ldamodel.print_topics(num_topics=6, num_words=10)

for topico in topicos:
    print(topico)
