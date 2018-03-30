import numpy as np
import re


# function which takes text file as input and returns index_list and corresponding sections
def file2id(text_file_loc):
    with open(text_file_loc, 'r') as f:
        test_str = f.read()
    
    flag = 0

    # retrieving indexes
    test_str = test_str.lower()
    regex = r"(Contents)|(contents)"

    match = re.search(regex, test_str)
    start = match.end()

    test_str = test_str[start:]

    regex = r"[.…]{2,}\s+\d+"

    test_str = re.sub(regex, "", test_str)

    
    regex = r")[\d.]*)\s+([^}].+)"
    contents = []
    ids = []
    parents = []
    count = 1
    content_flag = 1
    final_str = test_str
    while(content_flag):
        match = re.search("\s*((" + str(count) +"|"+ str(count+1) + "|"+ str(count+2)+ regex, final_str)
        print(match)
        id = match.group(1)
        if(id in ids):
            content_flag = 0
            break
        count = max(count, int(match.group(2)))
        contents.append(match.group(3))
        parents.append(match.group(2))
        ids.append(id)
        final_str = final_str[match.end():]
        print(count, parents[-1], ids[-1], contents[-1])

    
    id2ids = dict((w, i) for i, w in enumerate(ids))

    def find_section(final_str, section_id, section_title):
        try:
    #         regex = "(" + section_id + "|" + str(int(section_id)+1)+ ")"  + "\s*" +section_title 
            regex = "(" + section_id + ")"  + "\s*" +section_title 
            match  = re.search(regex, final_str)
            end = match.start()
            print(1)
            
        except AttributeError:
            
            if(re.search("\.", section_id) == None):
                regex = "(" + section_title  + ")"  + "\s*" 
            else:
                regex = "(" + section_id + ")"  + "\s*"
                
            try:
                match  = re.search(regex, final_str)
                end = match.start()
                print(2)
                
            except AttributeError:
                print("error")
                return -1
            
        print(match)
        return end

    for i,c in enumerate(contents):
        contents[i]  = " ".join(c.split())

    # Graph Class
    class Graph:

        def __init__(self,v):
            self.graph = [list() for i in range(v)]

        def addEdge(self,u,v):
            self.graph[u].append(v)

        def DFSUtil(self, v, visited,res,ans):
            visited[v]= True
            res.append(contents[v])
            #print(v)
            count=0
            for i in self.graph[v]:
                count+=1
                if visited[i] == False:
                    self.DFSUtil(i, visited,res,ans)
            if count==0:
                final_res=[' '.join(res),res[-1],ind2id[v]]
                #print(final_res)
                ans.append(final_res)
            res.pop()    

        def DFS(self):
            res=[]
            ans=[]
            V = len(self.graph) 
            visited =V*[False]
            for i in range(V):
                if visited[i] == False:
                    self.DFSUtil(i, visited,res,ans)
                    res=[]

            return ans

    id2ind = dict([(w,i) for i,w in enumerate(ids)])
    ind2id = dict([(i,w) for i,w in enumerate(ids)])
    nodes=[]
    for it in contents:
        nodes.append(it.split())
    parents=[int(i) for i in parents]
    g=Graph(len(ids))
    for i in ids:
        if i not in [str(i) for i in set(parents)]:
            g.addEdge(id2ind['.'.join(i.split('.')[:-1])],id2ind[i])

    index_list = g.DFS()

    # print(index_list)
    # final_str = test_str[last:]    

    start = find_section(final_str, index_list[0][2], index_list[0][1])

    sections = []
    for i in range(len(index_list)-1):

        
        end = find_section(final_str, index_list[i+1][2], index_list[i+1][1])
        if(end>start):
            sections.append(final_str[start:end])
            
            for j in range(id2ids[index_list[i+1][2]]):
                regex = ids[j] + "\s+" + contents[j]
                sections[-1] = re.sub(regex, "", sections[-1])
            sections[-1] = re.sub(r'\n{2,}', '', sections[-1])
                
            final_str = final_str[end:]
            start = 0
        else:  
            flag = 1
            print("error", i, start, end)
            
        print(start, end)
    sections.append(final_str[start:])
    
    return index_list, sections, flag