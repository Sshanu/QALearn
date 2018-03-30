from file2id import file2id
from sim2id import sim2id
from simw2v import simw2v



query = 'what are  ESO electives?'

index_list, sections, _ = file2id('/home/robsr/Study/Projects/Python/QALearn/qalearn/media/txt/UG-Manual.txt')
# index_list, sections = file2id('./docs/DeepLearning_Bible.txt')
# index_list, sections = file2id('./docs/Elements of Statistics Learning 2e.txt')

top_n_ids, top_n_sim = sim2id(3, '/home/robsr/Study/Projects/Python/QALearn/qalearn/media/txt/UG-Manual.txt', sections, index_list, query)
print(top_n_ids, top_n_sim)
print('\n\n')

top_n_ids, top_n_sim = simw2v(3, '/home/robsr/Study/6_sem/cs671/ass2/word2vec/vocab_wiki', 
                        '/home/robsr/Study/6_sem/cs671/ass2/word2vec/word_embd_wiki', 
                        '/home/robsr/Study/Projects/Python/QALearn/qalearn/media/txt/UG-Manual.txt', 
                        sections, index_list, 
                        query)

print(top_n_ids, top_n_sim)
print('\n\n')