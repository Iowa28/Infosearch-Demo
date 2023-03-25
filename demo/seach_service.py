import operator
import os

import pymorphy2
from numpy import dot
from numpy.dual import norm


class SearchService(object):

    def __init__(self):
        self.movie_vectors = self.__read_vectors()
        self.morph = pymorphy2.MorphAnalyzer()

    def __read_vectors(self):
        vectors = {}

        k = 100
        for i in range(1, k + 1):
            filename = 'tf-idf/lemmas/' + str(i) + '.txt'
            file = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)
            with open(file, encoding="utf-8") as f:
                vectors[i] = f.readlines()

        return vectors

    def __lemmatize(self, word):
        p = self.morph.parse(word)[0]
        return p.normal_form

    def __calc_cos_similarity(self, tf_idf_vector, tf_idf_movie_vector):
        query_vector = list(tf_idf_vector.values())
        movie_vector = list(tf_idf_movie_vector.values())

        if norm(query_vector) == 0 or norm(movie_vector) == 0:
            return 0

        return dot(query_vector, movie_vector) / (norm(query_vector) * norm(movie_vector))

    def search(self, query):
        query_terms = [self.__lemmatize(x) for x in query.split()]
        unique_terms = set(query_terms)

        tf_vector = {}
        for term in unique_terms:
            word_count = len([x for x in query_terms if x == term])
            tf = word_count / len(query_terms)
            tf_vector[term] = tf

        cos_sim_result = {}

        for i, lines in self.movie_vectors.items():
            tf_idf_vector = {}
            tf_idf_movie_vector = {}
            movie_terms = []

            for line in lines:
                line_data = line.split()
                term = line_data[0]
                idf = line_data[1]
                tf_idf = line_data[2]

                if term in unique_terms:
                    movie_terms.append(term)
                    tf_idf_vector[term] = tf_vector[term] * float(idf)
                    tf_idf_movie_vector[term] = float(tf_idf)

            for term in unique_terms:
                if term not in movie_terms:
                    tf_idf_vector[term] = 1
                    tf_idf_movie_vector[term] = 0

            cos_sim = self.__calc_cos_similarity(tf_idf_vector, tf_idf_movie_vector)
            if cos_sim != 0:
                cos_sim_result[i] = cos_sim

        sorted_result = sorted(cos_sim_result.items(), key=operator.itemgetter(1), reverse=True)
        result = dict(sorted_result)
        return result
