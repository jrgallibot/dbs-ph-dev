from transformers import T5Config, T5ForConditionalGeneration, T5Tokenizer
import nltk
import re
import numpy as np
import re
from scipy.sparse.linalg import svds
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import networkx
import datetime


def Questions(textlist):
    model_name = "allenai/t5-small-squad2-question-generation"
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)

    def run_model(input_string, **generator_args):
        input_ids = tokenizer.encode(input_string, return_tensors="pt")
        res = model.generate(input_ids, **generator_args)
        output = tokenizer.batch_decode(res, skip_special_tokens=True)
        #print(output)
        return output 
    q = list()
    a =list()
    for i in textlist.split('\n'):
        t = run_model(i,)
        if 'is ' in t[0]:
            print(t[0].split('is ')[1][:-1].title())
            qt = t[0].split('is ')[1][:-1].title()
            q.append(qt)
            a.append(f"{t[0]} {i}")
        elif 'are ' in t[0]:
            print(t[0].split('are ')[1][:-1].title())
            qt = t[0].split('are ')[1][:-1].title()
            q.append(qt)
            a.append(f"{t[0]} {i}")
    
    return [q,a]
def QandA(DOCUMENT,topic):
    nltk.download('punkt')
    def normalize_document(doc):
        # lower case and remove special characters\whitespaces
        doc = re.sub(r'[^a-zA-Z\s]', '', doc, re.I|re.A)
        doc = doc.lower()
        doc = doc.strip()
        # tokenize document
        tokens = nltk.word_tokenize(doc)
        # filter stopwords out of document
        try:
            stop_words = nltk.corpus.stopwords.words('english')
        except:
            nltk.download('stopwords')
            stop_words = nltk.corpus.stopwords.words('english')
        filtered_tokens = [token for token in tokens if token not in stop_words]
        # re-create document from filtered tokens
        doc = ' '.join(filtered_tokens)
        return doc


    def low_rank_svd(matrix, singular_count=2):
        u, s, vt = svds(matrix, k=singular_count)
        return u, s, vt

    DOCUMENT = re.sub(r'\n|\r', ' ', DOCUMENT)
    DOCUMENT = re.sub(r' +', ' ', DOCUMENT)
    DOCUMENT = DOCUMENT.strip()
    sentences = nltk.sent_tokenize(DOCUMENT)
    print(len(sentences))

    #stop_words = nltk.corpus.stopwords.words('english')


    print('Line 71')
    normalize_corpus = np.vectorize(normalize_document)

    norm_sentences = normalize_corpus(sentences)



    tv = TfidfVectorizer(min_df=0., max_df=1., use_idf=True)
    dt_matrix = tv.fit_transform(norm_sentences)
    dt_matrix = dt_matrix.toarray()

    vocab = tv.get_feature_names()
    td_matrix = dt_matrix.T

    num_sentences = 8
    num_topics = 3
    print('Line 87')
    u, s, vt = low_rank_svd(td_matrix, singular_count=num_topics)  
    print(u.shape, s.shape, vt.shape)
    term_topic_mat, singular_values, topic_document_mat = u, s, vt

    # remove singular values below threshold                                         
    sv_threshold = 0.5
    min_sigma_value = max(singular_values) * sv_threshold
    singular_values[singular_values < min_sigma_value] = 0

    salience_scores = np.sqrt(np.dot(np.square(singular_values), 
                                    np.square(topic_document_mat)))

    top_sentence_indices = (-salience_scores).argsort()[:num_sentences]
    top_sentence_indices.sort()

    
    similarity_matrix = np.matmul(dt_matrix, dt_matrix.T)
    print(similarity_matrix.shape)
    np.round(similarity_matrix, 3)
    similarity_graph = networkx.from_numpy_array(similarity_matrix)
    scores = networkx.pagerank(similarity_graph)
    ranked_sentences = sorted(((score, index) for index, score 
                                                in scores.items()), 
                            reverse=True)

    top_sentence_indices = [ranked_sentences[index][1] 
                            for index in range(len(ranked_sentences))]
    top_sentence_indices.sort()
    print('Line 116')
    textlist = list()
    for i in range(len((np.array(sentences)[top_sentence_indices]))):
        if len((np.array(sentences)[top_sentence_indices])[i]) > 150:
            #print(np.array(sentences)[top_sentence_indices][i])
            textlist.append(np.array(sentences)[top_sentence_indices][i])
        else:
            print('Did not match')
    print('Line 124')
    textcontent = '\n'.join(textlist)
    return textcontent


    #print(f"{t[0]} {i}")