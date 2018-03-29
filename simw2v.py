import numpy as np
import re, string
import pickle
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



def simw2v(n, w2v_vocab_path, w2v_emb_path, raw_text_file, sections, index_list, query):    
    
    with open(w2v_vocab_path, 'rb') as f:
        w2v_vocab = pickle.load(f)

    with open(w2v_emb_path, 'rb') as f:
        w2v_emb = pickle.load(f)
        
    with open(raw_text_file, 'r') as f:
        text = f.readlines()
    
    vectorizer = TfidfVectorizer(stop_words='english')
    vectorizer.fit(text)
    idf_list=vectorizer.idf_
    dict_map = dict(zip(vectorizer.vocabulary_.keys(), vectorizer.vocabulary_.values()))

    
    titles_avg = [para.split() for para in sections]
    avg_vec=[]
    
    dict2_map = dict(zip(w2v_vocab,w2v_emb[0]))
    
    for i in titles_avg:
        temp=np.zeros(len(w2v_emb[0][0]))
        summ=0
        for j in i:
            try:
                temp+=idf_list[dict_map[j]]*dict2_map[j]
                summ+=idf_list[dict_map[j]]
            except:
                pass
        avg_vec.append(temp/summ)
    
    avg_vec = np.array(avg_vec)

    ttemp=np.zeros(len(w2v_emb[0][0]))
    summm=0
    for j in query.split():
        try:
            ttemp+=idf_list[dict_map[j]]*dict2_map[j]
            summm+=idf_list[dict_map[j]]
        except:
            pass
    ttemp =( ttemp/summm).reshape(1,-1)
    
    sim_mat = cosine_similarity(avg_vec, ttemp)

    top_n = [i[0] for i in sorted(enumerate(sim_mat), key=lambda x:x[1], reverse=True)][:n]
    top_sim = [i[1][0] for i in sorted(enumerate(sim_mat), key=lambda x:x[1], reverse=True)][:n]
    top_n_ids = [index_list[top_n[i]][2] for i in range(n)]    
    top_n_titles = [index_list[top_n[i]][0] for i in range(n)]
    top_n_sim = [sim_mat[top_n[i]][0] for i in range(n)]
    # print(top_n_sim)
    # print(top_n_ids)
    print(top_n_titles)
    # print('\n\n\n')
    # print(sections[top_n[0]])
    
    return top_n_ids, top_sim