from file2id import file2id
from sim2id import sim2id

index_list, sections = file2id('./docs/UG-Manual.txt')
top_n_ids = sim2id(3, './docs/UG-Manual.txt', sections, index_list, 'sports scholarships')
print(top_n_ids)
