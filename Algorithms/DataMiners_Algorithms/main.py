# This is a Python script for B2F2 Casus
# Authors: Arnout Smit, Luca Doenen
from typing import Tuple, Iterable
from math import sqrt
from collections import defaultdict
import matplotlib.pyplot as plt
from PIL import Image
from datetime import datetime, timedelta

# TODO: missing lifts, bushalte fietstalling, parkeergarages.
# graph = {node : [[buren], (coordinaten)]}
graph = {
        "B3-1"  : [["B3-2"]                   , (0.75, 1, 3)   ],
        "B3-2"  : [["B3-3", "B3-1"]           , (1.25, 1, 3)   ],
        "B3-3"  : [["B3-4", "B3-2"]           , (1.25, 1.5, 3) ],
        "B3-4"  : [["B3-5", "B3-3"]           , (1.25, 2.5, 3) ],
        "B3-5"  : [["B3-6", "B3-4"]           , (1.25, 3.25, 3)],
        "B3-6"  : [["B3-7", "B3-5"]           , (1.25, 3.75, 3)],
        "B3-7"  : [["B3-8", "B3-9", "B3-6"]   , (1.25, 5, 3)   ],
        "B3-8"  : [["B3-7", "B3-9", "B2-8"]   , (0.5, 6, 3)    ],
        "B3-9"  : [["B3-10", "B3-8", "B3-7"]  , (1.75, 5.5, 3) ],
        "B3-10" : [["B3-11", "B3-9"]          , (2.25, 5.5, 3) ],
        "B3-11" : [["B3-12", "B3-10"]         , (3.5, 5.5, 3)  ],
        "B3-12" : [["B3-13", "B3-11"]         , (5.25, 5.5, 3) ],
        "B3-13" : [["B3-14", "B3-12"]         , (6, 5.5, 3)    ],
        "B3-14" : [["B3-15", "B3-17", "B3-13"], (7.5, 5.5, 3)  ],
        "B3-15" : [["B3-16", "B3-14"]         , (7.75, 3, 3)   ],
        "B3-16" : [["B3-15"]                  , (8, 1, 3)      ],
        "B3-17" : [["B3-14", "B2-17"]         , (9, 5, 3)      ],

        "B2-1"  : [["B2-2"]                   , (0.75, 1, 2)],
        "B2-2"  : [["B2-3", "B2-1"]           , (1.25, 1, 2)],
        "B2-3"  : [["B2-4", "B2-2"]           , (1.25, 1.5, 2)],
        "B2-4"  : [["B2-5", "B2-3"]           , (1.25, 2.5, 2)],
        "B2-5"  : [["B2-6", "B2-4"]           , (1.25, 3.25, 2)],
        "B2-6"  : [["B2-7", "B2-5"]           , (1.25, 3.75, 2)],
        "B2-7"  : [["B2-8", "B2-9", "B2-6"]   , (1.25, 5, 2)],
        "B2-8"  : [["B2-7", "B2-9", "B1-8", "B3-8"], (0.5, 6, 2)],
        "B2-9"  : [["B2-10", "B2-8", "B2-7"]  , (1.75, 5.5, 2)],
        "B2-10" : [["B2-11", "B2-9"]          , (2.25, 5.5, 2)],
        "B2-11" : [["B2-12", "B2-10"]         , (3.5, 5.5, 2)],
        "B2-12" : [["B2-13", "B2-11"]         , (5.25, 5.5, 2)],
        "B2-13" : [["B2-14", "B2-12"]         , (6, 5.5, 2)],
        "B2-14" : [["B2-15", "B2-17", "B2-13"], (7.5, 5.5, 2)],
        "B2-15" : [["B2-16", "B2-14"]         , (7.75, 3, 2)],
        "B2-16" : [["B2-15"]                  , (8, 1, 2)],
        "B2-17" : [["B2-14", "B3-17", "B1-17"], (9, 5, 2)],

        "B1-1"  : [["B1-2"]                   , (0.75, 1, 1)],
        "B1-2"  : [["B1-3", "B1-1"]           , (1.25, 1, 1)],
        "B1-3"  : [["B1-4", "B1-2"]           , (1.25, 1.5, 1)],
        "B1-4"  : [["B1-5", "B1-3"]           , (1.25, 2.5, 1)],
        "B1-5"  : [["B1-6", "B1-4"]           , (1.25, 3.25, 1)],
        "B1-6"  : [["B1-7", "B1-5"]           , (1.25, 3.75, 1)],
        "B1-7"  : [["B1-8", "B1-9", "B1-6"]   , (1.25, 5, 1)],
        "B1-8"  : [["B1-7", "B1-9", "B2-8", "B0-8"], (0.5, 6, 1)],
        "B1-9"  : [["B1-10", "B1-8", "B1-7"]  , (1.75, 5.5, 1)],
        "B1-10" : [["B1-11", "B1-9"]          , (2.25, 5.5, 1)],
        "B1-11" : [["B1-12", "B1-10"]         , (3.5, 5.5, 1)],
        "B1-12" : [["B1-13", "B1-11"]         , (5.25, 5.5, 1)],
        "B1-13" : [["B1-14", "B1-12"]         , (6, 5.5, 1)],
        "B1-14" : [["B1-15", "B1-17", "B1-13"], (7.5, 5.5, 1)],
        "B1-15" : [["B1-16", "B1-14"]         , (7.75, 3, 1)],
        "B1-16" : [["B1-15"]                  , (8, 1, 1)],
        "B1-17" : [["B1-14", "B0-17", "B2-17"], (9, 5, 1)],

        "B0-1"  : [["B0-2"]                   , (0.75, 1, 0)],
        "B0-2"  : [["B0-3", "B0-1"]           , (1.25, 1, 0)],
        "B0-3"  : [["B0-4", "B0-2"]           , (1.25, 1.5, 0)],
        "B0-4"  : [["B0-5", "B0-3"]           , (1.25, 2.5, 0)],
        "B0-5"  : [["B0-6", "B0-4"]           , (1.25, 3.25, 0)],
        "B0-6"  : [["B0-7", "B0-5"]           , (1.25, 3.75, 0)],
        "B0-7"  : [["B0-8", "B0-9", "B0-6"]   , (1.25, 5, 0)],
        "B0-8"  : [["B0-7", "B0-9", "B1-8"]   , (0.5, 6, 0)],
        "B0-9"  : [["B0-10", "B0-8", "B0-7"]  , (1.75, 5.5, 0)],
        "B0-10" : [["B0-11", "B0-9"]          , (2.25, 5.5, 0)],
        "B0-11" : [["B0-12", "B0-10"]         , (3.5, 5.5, 0)],
        "B0-12" : [["B0-13", "B0-11"]         , (5.25, 5.5, 0)],
        "B0-13" : [["B0-14", "B0-12"]         , (6, 5.5, 0)],
        "B0-14" : [["B0-15", "B0-17", "B0-13"], (7.5, 5.5, 0)],
        "B0-15" : [["B0-16", "B0-14"]         , (7.75, 3, 0)],
        "B0-16" : [["B0-15"]                  , (8, 1, 0)],
        "B0-17" : [["B0-14", "B1-17", "B0-18", "B0-19"], (9, 5, 0)],
        "B0-18" : [["B0-17", "B0-19"]         , (10.5, 8, 0)],
        "B0-19" : [["B0-18", "B0-17"]         , (14.25, 6.25, 0)]
    }

# {lokaal: [node]}
swapped_lokalen_dict = {'B.3.309': ['B3-1'], 'B.3.311': ['B3-1'], 'NOOD3-1': ['B3-2'], 'B.3.310': ['B3-2'],
                        'B.3.305': ['B3-3', 'B3-6'], 'B.3.308': ['B3-3'], 'B.3.306': ['B3-4'], 'B.3.304': ['B3-4'],
                        'B.3.302': ['B3-5'], 'B.3.300': ['B3-6'], 'B.3.210': ['B3-7', 'B3-9', 'B3-11'],
                        'trap B3': ['B3-8'], 'B.3.221': ['B3-9'], 'B.3.217': ['B3-10', 'B3-11'], 'B.3.208': ['B3-11'],
                        'B.3.215': ['B3-11'], 'B.3.213': ['B3-12'], 'B.3.209': ['B3-13'], 'B.3.211': ['B3-13'],
                        'B.3.206': ['B3-13'], 'B.3.200': ['B3-13', 'B3-14'], 'B.3.105': ['B3-14'], 'B.3.103': ['B3-14'],
                        'B.3.107': ['B3-14'], 'B.3.104': ['B3-15'], 'NOOD3-2': ['B3-16'], 'trap C3': ['B3-17'], 'Lift C3': ['B3-17'],

                        'B.2.309': ['B2-1'], 'B.2.311': ['B2-1'], 'NOOD2-1': ['B2-2'], 'B.2.310': ['B2-2'],
                        'B.2.305': ['B2-3', 'B2-6'], 'B.2.308': ['B2-3'], 'B.2.306': ['B2-4'], 'B.2.304': ['B2-4'],
                        'B.2.302': ['B2-5'], 'B.2.300': ['B2-6'], 'B.2.210': ['B2-7', 'B2-9', 'B2-11'],
                        'trap B2': ['B2-8'], 'B.2.221': ['B2-9'], 'B.2.217': ['B2-10', 'B2-11'], 'B.2.208': ['B2-11'],
                        'B.2.215': ['B2-11'], 'B.2.213': ['B2-12'], 'B.2.209': ['B2-13'], 'B.2.211': ['B2-13'],
                        'B.2.206': ['B2-13'], 'B.2.200': ['B2-13', 'B2-14'], 'B.2.105': ['B2-14'], 'B.2.103': ['B2-14'],
                        'B.2.107': ['B2-14'], 'B.2.104': ['B2-15'], 'NOOD2-2': ['B2-16'], 'trap C2': ['B2-17'], 'Lift C2': ['B2-17'],

                        'B.1.309': ['B1-1'], 'B.1.311': ['B1-1'], 'NOOD1-1': ['B1-2'], 'B.1.310': ['B1-2'],
                        'B.1.305': ['B1-3', 'B1-6'], 'B.1.308': ['B1-3'], 'B.1.306': ['B1-4'], 'B.1.304': ['B1-4'],
                        'B.1.302': ['B1-5'], 'B.1.300': ['B1-6'], 'B.1.210': ['B1-7', 'B1-9', 'B1-11'],
                        'trap B1': ['B1-8'], 'B.1.221': ['B1-9'], 'B.1.217': ['B1-10', 'B1-11'], 'B.1.208': ['B1-11'],
                        'B.1.215': ['B1-11'], 'B.1.213': ['B1-12'], 'B.1.209': ['B1-13'], 'B.1.211': ['B1-13'],
                        'B.1.206': ['B1-13'], 'B.1.200': ['B1-13', 'B1-14'], 'B.1.105': ['B1-14'], 'B.1.103': ['B1-14'],
                        'B.1.107': ['B1-14'], 'B.1.104': ['B1-15'], 'NOOD1-2': ['B1-16'], 'trap C1': ['B1-17'], 'Lift C1': ['B1-17'],

                        'B.0.309': ['B0-1'], 'B.0.311': ['B0-1'], 'NOOD0-1': ['B0-2'], 'B.0.310': ['B0-2'],
                        'B.0.305': ['B0-3', 'B0-6'], 'B.0.308': ['B0-3'], 'B.0.306': ['B0-4'], 'B.0.304': ['B0-4'],
                        'B.0.302': ['B0-5'], 'B.0.300': ['B0-6'], 'B.0.210': ['B0-7', 'B0-9', 'B0-11'],
                        'trap B0': ['B0-8'], 'B.0.221': ['B0-9'], 'B.0.217': ['B0-10', 'B0-11'], 'B.0.208': ['B0-11'],
                        'B.0.215': ['B0-11'], 'B.0.213': ['B0-12'], 'B.0.209': ['B0-13'], 'B.0.211': ['B0-13'],
                        'B.0.206': ['B0-13'], 'B.0.200': ['B0-13', 'B0-14'], 'B.0.105': ['B0-14'], 'B.0.103': ['B0-14'],
                        'B.0.107': ['B0-14'], 'B.0.104': ['B0-15'], 'NOOD0-2': ['B0-16'], 'trap C0': ['B0-17'], 'Lift C0': ['B0-17'],
                        'Hoofdingang': ['B0-18'], 'Cafetaria': ['B0-19']}

SCHEDULE = { datetime(2024, 2, 25, 9, 0) : "Hoofdingang",
             datetime(2024, 2, 25, 9, 30) : "B.3.210",
             datetime(2024, 2, 25, 10, 30) : "B.1.104",
             datetime(2024, 2, 25, 12, 0) : "B.2.309",
             datetime(2024, 2, 25, 12, 45) : "Cafetaria",
             datetime(2024, 2, 25, 13, 15) : "B.2.309",
             datetime(2024, 2, 25, 15, 0) : "B.3.302",
             datetime(2024, 2, 25, 16, 0) : "B.3.105",
             datetime(2024, 2, 25, 17, 30) : "Hoofdingang"
             }  # TODO add coffee corner lounge for gaps in schedule

EMERGENCY_DICT = {
        3: ['B3-2', 'B3-8', 'B3-16', 'B3-17'],
        2: ['B2-2', 'B2-8', 'B2-16', 'B2-17'],
        1: ['B1-2', 'B1-8', 'B1-16', 'B1-17'],
        0: ['B0-2', 'B0-8', 'B0-16', 'B0-17']
}

def euclidian_distance(point1: Iterable[float], point2: Iterable[float]) -> float:
    """Calculate the euclidian distance between two points in space.

    A point is a euclidian coordinate packed in an iterable of arbitrary dimension.

    >>> print(round(euclidian_distance((0,0,0), (1,1,1)), 7))
    1.7320508
    >>> print (euclidian_distance((0,0), (4,0)))
    4.0
    >>> print (euclidian_distance((4,10,4), [0,10,4]))
    4.0
    >>> print (euclidian_distance((0,), (3,)))
    3.0
    """
    sum_squares = 0
    for x1, x2 in zip(point1, point2):
        sum_squares += (x1-x2)**2
    return sqrt(sum_squares)

def dijkstra_algorithm(graph, startnode, endnode):
    """Implementatie van dijkstra's algoritme conform de slides van week 4.

    Calculate the shortest path from a startnote to endnode of a given graph in the format {node: (neighbour, coordinates)}.
    Returns: (shortest_path, visited, distance, predecessor)
    """
    visited = []
    distance = dict()    # {knoop: afstand(cumulative)}
    predecessor = dict()   # {knoop: vorige_knoop}

    distance[startnode] = 0
    predecessor[startnode] = -1

    while startnode != endnode:
        visited.append(startnode)
        for neighbour in graph[startnode][0]:
            if neighbour not in visited:
                # calculate distance to neighbour
                coords1 = graph[startnode][1]
                coords2 = graph[neighbour][1]
                dist = euclidian_distance(coords1, coords2)
                # update distance dict if new shortest distance
                if (neighbour not in distance) or (distance[neighbour] > distance[startnode] + dist):
                    distance[neighbour] = distance[startnode] + dist
                    predecessor[neighbour] = startnode
        # zoek knoop met korste afstand, zet als nieuwe startnode
        distance_not_visited = {k: v for k, v in distance.items() if k not in visited}
        startnode = min(distance_not_visited, key=distance.get)

    # find shortest path through predecessors
    shortest_path = [endnode]
    while predecessor[endnode] != -1:
        shortest_path.insert(0, predecessor[endnode])
        endnode = predecessor[endnode]
    return shortest_path, visited, distance, predecessor, distance[startnode] # only really need shortest_path, distance to end (int)


# geef tijd mee, krijg terug pad naar dichtsbijzijnde trap/noodtrap.
def emergency_exit(time: datetime, schedule = SCHEDULE):
    """Find the shortest path to the nearest exit.

    Assumption: time is between highest and lowest time within schedule.

    >>> emergency_exit(datetime(2024, 2, 25, 0, 0))
    Traceback (most recent call last):
     ...
    AssertionError: Person is not scheduled to be in the building.
    """
    assert list(schedule.keys())[0] <= time <= list(schedule.keys())[-1], "Person is not scheduled to be in the building."
    # find startnode
    for schedule_t in schedule.keys():
        if time >= schedule_t:
            last_t = schedule_t
        elif time < schedule_t:
            lokaal = schedule[last_t]
            startnode = swapped_lokalen_dict[lokaal][0]
            floor = int(startnode[1])
            break

    # find shortest exit
    return min((dijkstra_algorithm(graph, startnode, exit) for exit in EMERGENCY_DICT[floor]), key=lambda x: x[4])[0]

def map_path(path, image='plattegrond_B3.png'):
    """Maps a path on a given image."""
    # Load map image
    map_img = Image.open(image)

    # prepare coordinates
    coordinates = [graph[node][1][:2] for node in path]
    coordinates_scaled = [(x*120, y*120) for x,y in coordinates]
    x_coords, y_coords = zip(*coordinates_scaled)

    # Create plot
    fig, ax = plt.subplots()
    ax.imshow(map_img)
    ax.plot(x_coords, y_coords, 'ro-')  # 'ro-' plots red dots connected by a line
    # label start and endnode (optional)
    ax.text(x_coords[0]+20, y_coords[0]+20, "start", color='red')
    ax.text(x_coords[-1] + 20, y_coords[-1] + 20, "end", color='red')

    plt.show()

def schedulestepper(schedule, lokaal):
    for entry in schedule.keys():
        user_input = input("Press Y to continue or E for emergency:")
        if user_input == 'Y':
            map_path(dijkstra_algorithm(graph, swapped_lokalen_dict[lokaal][0], schedule[entry])[0])
        elif user_input == 'E':
            map_path(emergency_exit(entry))
        else: break;




if __name__ == '__main__':
    # TODO: pytests aanmaken voor dijkstra algoritme?
    # TEST DIJKSTRA:
    print("Korste weg:",                    dijkstra_algorithm(graph, "B3-1", "B0-17")[0])
    print("Volgorde van bezochte knopen:",  dijkstra_algorithm(graph, "B3-1", "B0-17")[1])
    print("Afstanden:",                     dijkstra_algorithm(graph, "B3-1", "B0-17")[2])
    print("Predecessors:",                  dijkstra_algorithm(graph, "B3-1", "B0-17")[3])
    print("Distance to endnode:",           dijkstra_algorithm(graph, "B3-1", "B0-17")[4])
    map_path(dijkstra_algorithm(graph, "B3-1", "B0-17")[0])

    # Emergency exit test
    print("emergency exit path: ", emergency_exit(datetime(2024, 2, 25, 9, 30)))
    map_path(emergency_exit(datetime(2024, 2, 25, 9, 30)))
    schedulestepper(SCHEDULE, "Lift C0")