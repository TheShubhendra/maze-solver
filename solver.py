import sys

class Node:
  def __init__(self,state,parent,action):
    self.state=state
    self.parent=parent
    self.action=action
    
class StackFrontier:
  def __init__(self):
    self.frontier =[]
    
  def add(self,node):
    self.frontier.append(node)
  def empty(self):
    return len(self.frontier)==0
  def contains_state(self, state):
    return any(state==node.state for node in self.frontier)
  def remove(self):
    node = self.frontier[-1]
    self.frontier=self.frontier[:-1]
    return node
class QueueFrontier(StackFrontier):
  def remove(self):
    node = self.frontier[0]
    self.frontier=self.frontier[1:]
    return node
class Maze:
  def __init__(self, filename):
    try:
      with open(filename,"r") as f:
        contents = f.read()
      contents = contents.splitlines()
    except:
      raise Exception("Unable to read file")
    
    self.height = len(contents)
    self.width = max(len(line) for line in contents)
    self.contents=contents
    walls=[]
    for i in range(self.height):
      row=[]
      for j in range(self.width):
        try:
          if contents[i][j] == "S":
            self.start=(i,j)
            row.append(False)
          elif contents[i][j] == "E":
            self.goal=(i,j)
            row.append(False)
          elif contents[i][j]==" ":
            row.append(False)
          else:
            row.append(True)
        except IndexError:
          row.append(False)
      walls.append(row)
    self.walls = walls
    self.solution = None
    if self.start is None:
      raise Exception("Maze must have exactly one starting point")
    if self.goal is None:
      raise Exception("Maze must have exactly one goal point")
  def neighbours (self,state):
    row,col= state
    candidates =[
      ("up",(row-1,col)),
      ("down",(row+1,col)),
      ("left",(row,col-1)),
      ("right",(row,col+1))
      ]
    actions=[]
    for action ,(r,c) in candidates:
      try:
        if not self.walls[r][c]:
          actions.append((action,(r,c)))
      except:
        continue
    return actions
  def print(self):
    solution = self.solution[1] if self.solution is not None else None
    for i,row in enumerate(self.walls):
      for j,col in enumerate(row):
        if col:
          print("█",end="")
        elif (i,j)==self.start:
          print('S',end="")
        elif (i,j) == self.goal:
          print("E",end="")
        elif solution is not None and (i,j) in solution:
          print("*",end="")
        else:
          print(' ',end="")
      print("")
    print()
    
    
  def solve(self, algorithm):
    if algorithm=="BFS":
      self.frontier = QueueFrontier()
    elif algorithm=="DFS":
      self.frontier = StackFrontier()
    else:
      raise Exception("Unknown algorithm {}. Either select BFS or DFS".format(algorithm))
    node = Node(state=self.start,parent=None, action=None)
    self.num_explored = 0
    self.set_explored = set()
    self.frontier.add(node)
    while True:
      if self.frontier.empty():
        raise Exception ("No Solution")
      node = self.frontier.remove()
      self.num_explored+=1 
      if node.state ==self.goal:
        actions = []
        cells = []
        while node.parent is not None:
          actions.append(node.action)
          cells.append(node.state)
          node=node.parent
        actions.reverse()
        cells.reverse()
        self.solution = (actions,cells)
        return
      self.set_explored.add(node.state)
      for action,state in self.neighbours(node.state):
        if state not in self.set_explored and not self.frontier.contains_state(state):
          child = Node(state,node,action)
          self.frontier.add(child)
      
def main():
  maze = Maze(sys.argv[1])
  if len(sys.argv) == 3:
    algorithm = sys.argv[2]
  else:
    algorithm = "DFS"
  maze.solve(algorithm=algorithm)
  maze.print()
  print("Num Explored : ",maze.num_explored)
  print("Way length : ",len(maze.solution[1]))
if __name__ == '__main__':
  main()