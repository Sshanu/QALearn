from file2id import file2id
from sim2id import sim2id
from simw2v import simw2v



query = 'how to apply for major'

index_list, sections = file2id('./docs/UG-Manual.txt')
# index_list, sections = file2id('./docs/DeepLearning_Bible.txt')
# index_list, sections = file2id('./docs/Elements of Statistics Learning 2e.txt')


top_n_ids, top_n_sim = sim2id(3, './docs/UG-Manual.txt', sections, index_list, query)
print(top_n_ids, top_n_sim)


top_n_ids, top_n_sim = simw2v(3, '/home/robsr/Study/6_sem/cs671/ass2/word2vec/vocab_wiki', 
                        '/home/robsr/Study/6_sem/cs671/ass2/word2vec/word_embd_wiki', 
                        './docs/UG-Manual.txt', 
                        sections, index_list, 
                        query)

print(top_n_ids, top_n_sim)
