from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

#create a blank dictionary called map
map = {}
def explore(player, moves):
    queue = Queue()
    queue.enqueue([player.current_room.id])
    visited = set()
    while queue.size() > 0:
        route = queue.dequeue()
        last_visited = route[-1]
        if last_visited not in visited:
            visited.add(last_visited)
        # note the exits
            for exit in map[last_visited]:
                if map[last_visited][exit] == '?':
                    return route
                else:
                    been_there = list(route)
                    been_there.append(map[last_visited][exit])
                    queue.enqueue(been_there)
    return []

#create method to check for exits that haven't been tried
def untried(player, new_moves):
    exits = map[player.current_room.id]
    untried = []
    for direction in exits:
        if exits[direction] == "?":
             untried.append(direction)
    if len(untried) == 0:
        unexplored = explore(player, new_moves)
        new_room = player.current_room.id
        for room in unexplored:
            for direction in map[new_room]:
                if map[new_room][direction] == room:
                    new_moves.enqueue(direction)
                    new_room = room
                    break
    else:
        new_moves.enqueue(untried[random.randint(0, len(untried) -1)])
unexplored_room = {}
for direction in player.current_room.get_exits():
    unexplored_room[direction] = "?"
map[world.starting_room.id] = unexplored_room
new_moves = Queue()
untried(player, new_moves)
reverse_dir = {"n": "s", "s": "n", "e": "w", "w": "e"}
while new_moves.size() > 0:
    start = player.current_room.id
    move = new_moves.dequeue()
    player.travel(move)
    traversal_path.append(move)
    next_room = player.current_room.id
    map[start][move] = next_room
    if next_room not in map:
        map[next_room] = {}
        for exit in player.current_room.get_exits():
            map[next_room][exit] = "?"
    map[next_room][reverse_dir[move]] = start
    if new_moves.size() == 0:
        untried(player, new_moves)


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
