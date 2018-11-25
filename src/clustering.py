
from gensim.parsing.preprocessing import remove_stopwords
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.parsing.porter import PorterStemmer
from gensim.utils import simple_preprocess
from gensim.corpora import dictionary
from nltk.cluster import KMeansClusterer
from sklearn import cluster, metrics
from sklearn.cluster import KMeans
from os import scandir
import multiprocessing
import json
import gc
import nltk
import time
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

class MyCorpus():
    def __iter__(self):
        p = PorterStemmer()
        for entry in scandir("./dblpfiledir"):
            with open(entry.path, "r", encoding="utf-8") as f:
                jsoncontent = json.load(f)
                doc = jsoncontent["abstract"]
                if len(doc) > 0:
                    doc = remove_stopwords(doc)
                    doc = p.stem_sentence(doc)
                    words = simple_preprocess(doc, deacc=True)
                    yield TaggedDocument(words=words, tags=[jsoncontent['index']])

def Doc2VecTrain():
    t0 = time.time()
    cores = multiprocessing.cpu_count()
    print('num of cores is %s' % cores)
    gc.collect()
    corpus_data = MyCorpus()
    model = Doc2Vec(window=3, min_count=3, sample=1e-4, negative=5, workers=cores, dm=1)
    print('building vocabulary...')
    model.build_vocab(corpus_data)
    model.train(corpus_data, total_examples=model.corpus_count, epochs=20)
    model.save("./d2vmodel.bin")
    t1 = time.time()
    print(t1)

def Kmeans():
    d2v_model = Doc2Vec.load("./d2vmodel.bin")
    kmeans_model = KMeans(n_clusters=3, init='k-means++', max_iter=100)  
    X = kmeans_model.fit(d2v_model.docvecs.doctag_syn0)
    labels=kmeans_model.labels_.tolist()
    l = kmeans_model.fit_predict(d2v_model.docvecs.doctag_syn0)
    pca = PCA(n_components=2).fit(d2v_model.docvecs.doctag_syn0)
    datapoint = pca.transform(d2v_model.docvecs.doctag_syn0)
    plt.figure
    label1 = ["#FFFF00", "#008000", "#0000FF"]
    color = [label1[i] for i in labels]
    plt.scatter(datapoint[:, 0], datapoint[:, 1], c=color)

    centroids = kmeans_model.cluster_centers_
    centroidpoint = pca.transform(centroids)
    plt.scatter(centroidpoint[:, 0], centroidpoint[:, 1], marker='^', s=150, c='#000000')
    plt.show()

Kmeans()