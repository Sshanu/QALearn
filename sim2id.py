from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# function to output top n ids for the similar paragraph based on tfidf values
def sim2id(n, sections, index_list, query):
    
    vectorizer = TfidfVectorizer(stop_words='english')
    vectorizer.fit(sections)
    
    titles = [i for i in sections]
    
    titles_vector = vectorizer.transform(titles)
    titles_arr = titles_vector.toarray()

    query_vector = vectorizer.transform([query])
    query_arr = query_vector.toarray()

    sim_mat = cosine_similarity(titles_arr, query_arr)

    top_n = [i[0] for i in sorted(enumerate(sim_mat), key=lambda x:x[1], reverse=True)][:n]
    top_sim = [i[1][0] for i in sorted(enumerate(sim_mat), key=lambda x:x[1], reverse=True)][:n]
    top_n_ids = [index_list[top_n[i]][2] for i in range(n)]    
    top_n_titles = [index_list[top_n[i]][0] for i in range(n)]
    top_n_sim = [sim_mat[top_n[i]][0] for i in range(n)]
    # print(top_n_sim)
    # for i in range(n):
    #     print(i+1, "section ids:", top_n_ids[i], " section: ", top_n_titles[i])
    print(top_n_ids)
    print(top_n_titles)
    # print('\n\n\n')
    # print(sections[top_n[0]])
    
    return top_n, top_sim