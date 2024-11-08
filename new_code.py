from collections import defaultdict,deque
import heapq,random


class Graph:
    def __init__(self) -> None:
        self.graph=defaultdict(list)
        self.weights={}
        self.heuristic={}
        self.and_nodes={'B'}
        self.or_nodes={}
        

    def addedges(self,u,v,weight: int=1):
        self.graph[u].append(v)
        self.graph[v].append(u)
        self.weights[(u,v)]=weight
        self.weights[(v,u)]=weight
    def set_heurtistics(self,node,value):
        self.heuristic[node]=value
    def print_graph(self):
        for node,neighbors in self.graph.items():
            print(f"{node}:{', '.join(neighbors)}")

    def bfs(self,start,goal):
        queue=deque([[start]])
        visited =set([start])

        while queue:
                path=queue.popleft()
                node=path[-1]

                if node==goal:
                      return path

                for neighbour in self.graph[node]:
                      if neighbour not in visited:
                            visited.add(neighbour)
                            new_path=list(path)
                            new_path.append(neighbour)
                            queue.append(new_path)
                            print(f"Exploring path:{new_path}")
        return []
    
    
    
    def bms(self,start,goal,max_iterations: int=1000):
          best_path=None
          best_length=float('inf')

          for _ in range(max_iterations):
                current=start
                path=[start]
                visited={start}

                while current!=goal and len(self.graph[current])>0:
                        for n in self.graph[current]:
                            if n not in visited:
                                  neighbors=[n]
                                  if not neighbors:
                                        break
                        current=random.choice(neighbors)
                        path.append(current)
                        visited.add(current)

                if current==goal and len(path)<best_length:
                      best_path=path
                      best_length=len(path)
          return best_path if best_path else []
    
    def dfs(self,start,goal):
      stack=[(start,[start])]
      visited=set()

      while stack:
            node,path=stack.pop()

            if node==goal:
                  return path
            visited.add(node)
            print(f"Visited:{node}")
            for neighbors in reversed(self.graph[node]):
                  if neighbors not in visited:
                        stack.append((neighbors,path+[neighbors]))
                        print(f"Path:{path+[neighbors]}")

      return []
    

    def branch_bound(self,start,goal):
        queue=[(0,start,[start])]
        visited=set()
        while queue:
            cost,node,path=heapq.heappop(queue)
            if node==goal:
                return path
            if node not in visited:
                visited.add(node)
                for neighbor in self.graph[node]:
                    if neighbor not in visited:
                        new_cost=cost+self.weights.get((node,neighbor),1)
                        heapq.heappush(queue,(new_cost,neighbor,path+[neighbor]))
        return []
    
    def branch_bound_hue(self,start,goal):
        queue=[(self.heuristic.get(start,0),0,start,[start])]
        visited=set()
        while queue:
            _,cost,node,path=heapq.heappop(queue)
            if node==goal:
                return path
            if node not in visited:
                visited.add(node)
                for neighbor in self.graph[node]:
                    if neighbor not in visited:
                        new_cost=cost+self.weights.get((node,neighbor),1)
                        estimate=cost+self.heuristic.get(neighbor,0)
                        heapq.heappush(queue,(estimate,new_cost,neighbor,path+[neighbor]))
        return []
    
    
    
    def hill_climb(self,start,goal):
        current=start
        path=[start]
        while current!=goal:
                
            neighbor=self.graph[current]
            if not neighbor:
                    break
            next_node=min(neighbor,key=lambda x:self.heuristic.get(x,float('inf')))
            if(self.heuristic.get(next_node,float('inf')))>(self.heuristic.get(current,float('inf'))):
                    break
            current=next_node
            path.append(next_node)
        return path if path[-1]==goal else []
    
    def a_star(self,start,goal):
        queue=[(self.heuristic.get(start,0),0,start,[start])]
        extended_list=set()
        visited=set()
        while queue:
            _,cost,node,path=heapq.heappop(queue)
            if node==goal:
               return path
            
           

            if node not in visited:
              visited.add(node)
              for neighbor in self.graph[node]:
                if neighbor not in visited:
                    new_cost=cost+self.weights.get((node,neighbor),1)
                    estimate=new_cost+self.heuristic.get(neighbor,0)
                    heapq.heappush(queue,(estimate,new_cost,neighbor,path+[neighbor]))
               

        
        return[]
            
    
        
    def ao_star(self,start,goal):
        def calculate_cost(node,visited):
            if node==goal:
               return 0,[node]
            if node in visited:
                return float('inf'),[]
            visited.add(node)

            if node in self.and_nodes:
                total_cost=0
                total_path=[node]
                for neighbor in self.graph[node]:
                    
                        cost,path=calculate_cost(neighbor,visited.copy())
                        total_cost+=cost+self.weights.get((node,neighbor),1)
                        total_path.extend(path)
                return total_cost,total_path
            else:
                min_cost=float('inf')
                best_path=[]
                for neighbor in self.graph[node]:
                    cost,path=calculate_cost(neighbor,visited.copy())
                    total_cost=cost+self.weights.get((node,neighbor),1)
                    if total_cost<min_cost:
                        min_cost=total_cost
                        best_path=[node]+path
                return min_cost,best_path
        _,path=calculate_cost(start,set())
        return path if path else []
    
    def oracle_search(self,start,goal,oracle):
        
        stack=[(0,start,[start])]
        

        while stack:
            total_cost,node,path=stack.pop()

            if node==goal and total_cost<=oracle:
                 return path
            for neighbor in self.graph[node]:
                cost_so_far=total_cost+self.weights.get((node,neighbor),1)
                if cost_so_far<=oracle:
                    stack.append((cost_so_far,neighbor,path+[neighbor]))
        return []
    def oracle_search_hue(self,start,goal,oracle):
        stack=[(0,start,[start])]
        while stack:
            total_cost,node,path=stack.pop()
            if node==goal and total_cost<=oracle:
                return path
            for neighbor in self.graph[node]:
                cost_so_far=total_cost+self.weights.get((node,neighbor),1)+self.heuristic.get((node,neighbor),0)
                if cost_so_far<=oracle:
                    stack.append((cost_so_far,neighbor,path+[neighbor]))
        return []
    
    def beam_search(self,start,goal,beam):
      queue=deque()
      queue.append((start,[start]))

      while queue:
            level_nodes=[]
            while queue:
                  node,path=queue.popleft()
                  if node==goal:
                        return path
                  for neighbor in self.graph[node]:
                        level_nodes.append((neighbor,path+[neighbor]))
            level_nodes=sorted(level_nodes,key=lambda x: self.heuristic.get(x[0]))[:beam]
            queue.extend(level_nodes)
      return []


    
     
g=Graph()

edges=[('A','B',4),('A','C',3),
       ('C','E',10),('C','D',7),
       ('D','E',2),
       ('B','E',12),('B','F',5),
       ('F','Z',16),
       ('E','Z',5)]
heuristics={
       'A':14,'B':12,'C':11,'E':4,'D':6,'F':11,'Z':0
}

oracle=17

for edge in edges:
    g.addedges(*edge)

for node,value in heuristics.items():
    g.set_heurtistics(node,value)



start,goal='A','Z'
print("The graph:\n")
g.print_graph()
print("\nPath:")
path=g.beam_search(start,goal,oracle)

print(f"AO*:{'->'.join(path)}")




