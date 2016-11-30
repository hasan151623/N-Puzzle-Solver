from math import *
import sys
goal=[]
class State(object):
    def __init__(self,n):
        #global goal
        self.state=[x[:] for x in goal]

    def size(self):
        return len(self.state)

    def __str__(self):
        string=[]
        for i in self.state:
            for c in i:
                string.append(str(c)+"\t")
            string.append("\n")
        string.pop()
        return "".join(string)

    def __eq__(self,other):
        return self.state == other.state

    def __ne__(self,other):
        return self.state != other.state

    def __hash__(self):
        return hash(self.__str__())

    def startState(self,start):
        self.state=[x[:] for x in start]

    def get_tile(self,row,col):
        return self.state[row][col]

    def set_tile(self,row ,col,value):
        self.state[row][col]=value

    def copy(self):
        newState = State(self.size())
        for r in range(self.size()):
            for c in range(self.size()):
                newState.set_tile(r,c,self.state[r][c])
        return newState

    def eucledian_distance(self):
        ed=0
        
        for (i,row) in enumerate(self.state):
            for (j,value) in enumerate(row):
                for (k,row1) in enumerate(goal):
                    for (l,value1) in enumerate(row1):
                        if value==value1 and value!=0:
                            d2=(i-k)**2 + (j-l)**2
                            ed+=sqrt(d2)
                            break
        return ed

    def heuristic_cost_estimate(self):
    
        r_out=0
        c_out=0
        transpose_st=[[ self.state[row][col] for row in range(0,n) ] for col in range(0,n) ]
        #global goal
        for i in range(self.size()):
            for j in range(self.size()):
                if goal[i][j]!=0 and goal[i][j] not in self.state[i]:
                    r_out+=1
                if goal[j][i]!=0 and goal[j][i] not in transpose_st[i]:
                    c_out+=1
        return r_out+c_out

    def swap_tile(self,r,c,new_r,new_c):
        temp= self.state[r][c]
        self.state[r][c] = self.state[new_r][new_c]
        self.state[new_r][new_c]=temp

    def successors(self):
        neighbors=[]
        n=self.size()
        for r in range(n):
            for c in range(n):
                if self.state[r][c]==0:
                    if r!=0:
                        neighbor=self.copy()
                        neighbor.swap_tile(r,c,r-1,c)
                        neighbors.append(neighbor)
                    if c!=0:
                        neighbor=self.copy()
                        neighbor.swap_tile(r,c,r,c-1)
                        neighbors.append(neighbor)
                    if r!=n-1:
                        neighbor=self.copy()
                        neighbor.swap_tile(r,c,r+1,c)
                        neighbors.append(neighbor)
                    if c!=n-1:
                        neighbor=self.copy()
                        neighbor.swap_tile(r,c,r,c+1)
                        neighbors.append(neighbor)
                    break
                
        return neighbors
                        

    
class NPuzzle(object):
    def __init__(self,start,n):
        self.state = State(n)
        self.state.startState(start)
        self.nodes_explored=0

    def __str__(self):
        return str(self.state)
    def __repr__(self):
        return str(self.state)

    def a_star_search(self):
        start=self.state.copy()
    
        gl = State(self.state.size())
        closedSet=set()
        openSet=set([start])
        cameFrom={}

        gScore={start:0}
        fScore = {start: gScore[start] + start.heuristic_cost_estimate()}

        while len(openSet) != 0:
            current=min(openSet, key=fScore.get)
            if current == gl:
                return self.reconstruct_path(cameFrom,current)

            openSet.remove(current)
            closedSet.add(current)
            neighbors=current.successors()
            for neighbor in neighbors:
                if neighbor in closedSet:
                    continue
                tentative_gScore = gScore[current] + 1
                if neighbor not in openSet:
                    openSet.add(neighbor)
                elif tentative_gScore >= gScore[neighbor]:
                    continue
                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = gScore[neighbor] + neighbor.heuristic_cost_estimate()
 
                self.nodes_explored+=1
        return None
    

    def reconstruct_path(self,cameFrom,current):
        total_path=[current]
        while current in cameFrom:
            current = cameFrom[current]
            total_path.append(current)
        return total_path


if __name__=="__main__":
    #sys.stdout=open("puzzle.txt", "w")

    N = int(input().strip())
    n = int(sqrt(int(N)+1))
    
    s = [int(i) for i in input().strip().split()]
    start = [s[i:i+n] for i in range(0,len(s),n)]
  
    g = [int(i) for i in input().strip().split()]
    goal = [g[i:i+n] for i in range(0,len(g),n)]

    puzzle = NPuzzle(start,n)
    explored_nodes = puzzle.a_star_search()

    print("Moves Required: ",len(explored_nodes))
    print("Nodes Explored : ", puzzle.nodes_explored)

    for node in reversed(explored_nodes):
        print(node)
        print()
    #sys.stdout.close()
        
                    

