import numpy as np
import re


# function which takes text file as input and returns index_list and corresponding sections
def file2id(text_file_loc):
    with open(text_file_loc, 'r') as f:
        test_str = f.read()
    flag = 0
    # retrieving indexes
    regex = r"((\d{1,2})[\d.]*) ([^}].+)"
    matches = re.finditer(regex, test_str)
    contents = []
    ids = []
    parents = []
    count = 0
    last = None
    for matchNum, match in enumerate(matches):
        matchNum = matchNum + 1

        id = match.group(1)
        if(id in ids):
            break

        count = max(count, int(match.group(2)))
        contents.append(match.group(3))
        parents.append(match.group(2))
        ids.append(id)
        last = match.end(3) 
    regex = "[.…]{2,}\s*\d*"
    for i,c in enumerate(contents):
        contents[i] = re.sub(regex, "", c)
        
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
    
    final_str = test_str[last:]    
    
    regex = "(" + index_list[0][2] + ")"  + "?\s*" + index_list[0][1] 
    match  = re.search(regex, final_str)
    start = match.start()
    sections = []
    for i in range(len(index_list)-1):

        try:
            regex = "(" + index_list[i+1][2] + ")"  + "\s*" + index_list[i+1][1] 
            match  = re.search(regex, final_str)
            end = match.start()
        except AttributeError:
            try:
                regex = "(" + index_list[i+1][2] + ")"  + "\s*"
                match  = re.search(regex, final_str)
                end = match.start()
            except AttributeError:
                try:
                    regex = "(" + index_list[i+1][1]  + ")"  + "\s*" 
                    match  = re.search(regex, final_str)
                    end = match.start()
                except AttributeError:
                    print("error, i")

        if(end>start):
            sections.append(final_str[start:end])
        else:  
            flag = 1
            print("error", i, start, end)

        start = end
    sections.append(final_str[start:])
    
    return index_list, sections, flag