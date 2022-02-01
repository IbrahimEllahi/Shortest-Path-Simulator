import pygame as pg
from typing import *
from pprint import pprint
import pickle


pg.init()

# Display Settings
TILESIZE = 48



#Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)
BLUE = (0, 255, 255)
RED = (255,0,0)
SILVER = (192,192,192)
GRAY = (128,128,128)
FOREST_GREEN = (34, 139, 34)




# Software Settings
FPS = 60
clock = pg.time.Clock()

# Initialize display


WIDTH, HEIGHT = 1300, 800
WINDOW = pg.display.set_mode(
  (WIDTH, HEIGHT)
)

GRIDW, GRIDH  = WIDTH//TILESIZE, HEIGHT//TILESIZE



Node = TypeVar('Node')
Weight = int


class WeightedGraph(Generic[Node]):    
    def __init__(self, graph: Dict[Node, List[Tuple[Node, Weight]]]):
        self._graph = graph
        self._paths: List[Tuple[List[Node], Weight]] = []

    def _all_paths(self, start: Node, end: Node, current_weight: Weight = 0, visited: Tuple[List[Node], Weight] = None):
        current_nodes, accumulated_weight = visited = visited or ([], 0)

        if start == end:
            return (current_nodes + [end], accumulated_weight + current_weight)

        for connected_node, weight in self._graph[start]:
            if connected_node in current_nodes:
                continue
            
            visited = (current_nodes + [start], accumulated_weight + current_weight)
            data = self._all_paths(connected_node, end, current_weight=weight, visited=visited)

            if data and isinstance(data, tuple):
                self._paths.append(data)

        return self._paths

    def path(self, start: Node, end: Node) -> List[Node]:
        self._all_paths(start, end)
        shortest_path, _ = min(self._paths, key=lambda tupl: tupl[1])

        self._paths = []
        return shortest_path

Location = Tuple[int, int]
Connections = List[Tuple[Node, Weight]]

def pather(graph: Dict[Node, Tuple[Location, Connections]]) -> Callable[[Node, Node], Dict[Node, Location]]:
    weighted = WeightedGraph({node: connections for node, (_, connections) in graph.items()})

    def wrapper(start: Node, end: Node) -> Dict[Node, Location]:
        nodes = weighted.path(start, end)
        return {
            node: graph[node][0]
            for node in nodes
        }
    
    return wrapper


class Graph:

  def __init__(self):

      self.lines = []
      self.nodes = []
      self.selected_nodes = []
      self.graph_mode = False


  def get_neighbours(self, node):

    if not node:
      return None

    neighbours = []
    for line, n in self.lines:
      if node in n:
        n_list = n.copy()
        n_list.remove(node)
        neighbours.append(n_list[0].id)

    return neighbours

  def get_node(self, num):

    for node in self.nodes:
      if node.id == num:
        return node
    
    return None

  def find_distance(self, point1, point2):
    return abs((point1.rect.x - point2.rect.x) + (point1.rect.y - point2.rect.y))

  def get_data(self, dimensions = None):
    coords = None
    data = {}

    for node in self.nodes:
      
      if dimensions:
        coords = [
          (
            node.rect.center[0] * WIDTH
          ) 
          / dimensions[0], 
          (
            node.rect.center[1] * HEIGHT
          ) 
          / dimensions[1]
        ]

      neighbours_id = [str(n) for n in self.get_neighbours(node)]

      distance = [self.find_distance(node, self.get_node(neighbour)) for neighbour in neighbours_id]

      data[str(node.id)] = [coords, list(zip(neighbours_id, distance))]

    return data

  def save(self):

    with open("graph.pkl", "wb") as file:

      pickle.dump([self.nodes, self.lines], file)


  def load(self):

    with open("graph.pkl", "rb") as file:

      self.nodes, self.lines = pickle.load(file)

  def move_to_tile(self, position):
    difference = position % TILESIZE

    return position - difference

graph = Graph()



# Node class draws graph.nodes onto the screen and helps detect if we are hovering over the node

class Node:

  def __init__(self, id, color, x, y, width, height):

    self.color = color
    self.static_color = self.color
    self.hover_color = WHITE
    self.id = str(id)
    self.rect = pg.Rect(x, y , width, height)



  def draw(self,win,outline=WHITE):


    if outline:
      pg.draw.circle(win, outline, (self.rect.center), self.rect.width/2+1)
        
    pg.draw.circle(win, self.color, (self.rect.center), self.rect.width/2)

    font = pg.font.SysFont('comicsans', 35)
    text = font.render(str(self.id), 1, WHITE)

    win.blit(text, (self.rect.x + (self.rect.width/2 - text.get_width()/2), self.rect.y + (self.rect.height/2 - text.get_height()/2)))
      

  def is_over(self, pos):
    
    # Checks if mouse cursor over the node

    if pos[0] > self.rect.x and pos[0] < self.rect.x + self.rect.width:
      if pos[1] > self.rect.y and pos[1] < self.rect.y + self.rect.height:
        return True
        
    return False

# Use this class to create line objects and store them in a list
class Line:
  def __init__(self, color, startpoint, endpoint, width):
    self.color = color
    self.start = startpoint
    self.end = endpoint
    self.width = width

    


def update(win):

  WINDOW.fill(BLACK)

  if graph.graph_mode:
  
    for tile_num in range(GRIDW):

      x = tile_num * TILESIZE
      pg.draw.line(WINDOW, RED, (x,0), (x,HEIGHT),1)

    for tile_num in range(GRIDH):

      y = tile_num * TILESIZE
      pg.draw.line(WINDOW ,RED, (0,y), (WIDTH,y), 1)

  for line, (first, second) in graph.lines:

    line.start, line.end = first.rect.center, second.rect.center
    pg.draw.line(win, line.color, line.start, line.end, line.width)

  for node in graph.nodes:


    node.draw(WINDOW, YELLOW)



  pg.display.update()


allow_keys = [str(i) for i in range(10)] + ['backspace']

while (run := True):
  
  clock.tick(FPS)

  for event in pg.event.get():
    pos = pg.mouse.get_pos()


    if event.type == pg.QUIT:
        run = False
        pg.quit()



    if event.type == pg.KEYDOWN:

      if pg.key.name(event.key) in allow_keys and graph.selected_nodes:
        edit = 0 if len(graph.selected_nodes) == 1 else 1

        if event.key != pg.K_BACKSPACE:
          graph.selected_nodes[edit].id += pg.key.name(event.key)
        
        else: graph.selected_nodes[edit].id = graph.selected_nodes[edit].id[:-1]


      if event.key == pg.K_SPACE:

        for node in graph.nodes:
          
          node.rect.x, node.rect.y = [graph.move_to_tile(xy) for xy in node.rect.center]

      if event.key == pg.K_c and not graph.selected_nodes:

        tiled_pos = [graph.move_to_tile(xy) for xy in pos]

        graph.nodes.append(
          Node(
            len(graph.nodes) + 1,
            RED, 
            tiled_pos[0], 
            tiled_pos[1], 
            TILESIZE, 
            TILESIZE
          )
        )

      if event.key == pg.K_l:
        graph.load()
        
      if event.key == pg.K_LCTRL and graph.selected_nodes:

        select = 0 if len(graph.selected_nodes) == 1 else 1

        lines_remove = []
        node = graph.selected_nodes[select]

        for line in graph.lines:


          con, (first, second) = line
          if node == first or node == second:
            lines_remove.append(line)

        for line in lines_remove:
          graph.lines.remove(line)

        graph.nodes.remove(node)

      if event.key == pg.K_r:

        graph.graph_mode = False if graph.graph_mode else True

      if event.key == pg.K_s:
        graph.save()

      if event.key == pg.K_q and len(graph.selected_nodes) == 2:

        pathfinder = pather(graph.get_data())
        
        selection = [str(node.id) for node in graph.selected_nodes]

        print(pathfinder(selection[0], selection[1]))


      # Detects if two graph.nodes are selected
      if len(graph.selected_nodes) == 2 and event.key == pg.K_f:
        line_remove = False

        # Checks if a line already exists between the two graph.nodes, if yes, the line will be removed
        for line in graph.lines:
          line_exists = [line[0].start, line[0].end] == [graph.selected_nodes[0].rect.center, graph.selected_nodes[1].rect.center]

          if line_exists:
            graph.lines.remove(line)
            line_remove = True
            break

        # If no such line already exists, it will create one instead
        if not line_remove:
          graph.lines.append(
          (
            Line(
              BLUE,
              graph.selected_nodes[0].rect.center,
              graph.selected_nodes[1].rect.center,
              1
            ), 
            graph.selected_nodes.copy()
          )
        )




    for node in graph.nodes:

      if len(graph.selected_nodes) > 2:
          graph.selected_nodes.pop(0)

      # Changes graph.nodes color if we hover over it
      if node.is_over(pos):
        node.color = node.hover_color
    
        if pg.mouse.get_pressed()[0]:

          # Selects/Deselects already existing graph.nodes
          
          

          if node not in graph.selected_nodes:
            graph.selected_nodes.append(node)
          
          else: graph.selected_nodes.remove(node)

          # Check if we already have a node selected, this way we won't pick up multiple at a time
          selected = 0
          for n in graph.nodes:
            if n.color == n.hover_color and n != node:
              selected += 1

          # Moves the node to the mouse pos if we have no other graph.nodes selected
          if not selected:
            node.rect.center = pos
      
      # Changes colors of graph.nodes when Selected
      else: node.color = node.static_color if node not in graph.selected_nodes else FOREST_GREEN
      
      
      

  update(WINDOW)