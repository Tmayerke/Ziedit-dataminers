# This is a Python script for B2F2 Casus
# Authors: Arnout Smit, Luca Doenen
from typing import Tuple, Iterable
from math import sqrt

def euclidian_distance(point1: Iterable[float], point2: Iterable[float]) -> float:
    """Calculate the euclidian distance between two points in space.

    A point is an iterable euclidian coordinate of arbitrary dimension.

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
    """Implementatie van dijkstra's algortime conform de slides van week 4."""
    visited = []
    distance = dict()    # {knoop: afstand(cumulative)}
    predeccesor = dict()   # {knoop: vorige_knoop}

    distance[startnode] = 0
    predeccesor[startnode] = -1

    while startnode != endnode:
        visited.append(startnode)
        for neighbour, dist in graph[startnode].items():
            if neighbour not in visited:
                if neighbour not in distance:
                    distance[neighbour] = distance[startnode] + graph[startnode][neighbour] #new distance neigbour = dist startnode + distance start-neighbour
                    predeccesor[neighbour] = startnode
                elif distance[neighbour] > distance[startnode] + graph[startnode][neighbour]:
                    distance[neighbour] = distance[startnode] + graph[startnode][neighbour]
                    predeccesor[neighbour] = startnode
        # zoek knoop met korste afstand, zet als nieuwe startnode
        distance_not_visted = {k: v for k,v in distance.items() if k not in visited}
        startnode = min(distance_not_visted, key=distance.get)

    # find shortest path through predecessors
    shortest_path = [endnode]
    while predeccesor[endnode] != -1:
        shortest_path.insert(0, predeccesor[endnode])
        endnode = predeccesor[endnode]
    return distance, visited, predeccesor, shortest_path


if __name__ == '__main__':

    graaf1 = {  # vorm: {node: {neighbornode: value}}
        1 : {3: 7, 2: 12},
        2 : {1: 12, 10: 13, 6: 14, 9: 3},
        3 : {1: 7, 5: 9, 4: 15, 10: 9},
        4 : {3:15, 8:12},
        5 : {3:9, 7: 10},
        6 : {8:7, 2:14},
        7 : {10:11, 9:10, 8:6},
        8 : {4:12, 6:7, 7:6},
        9 : {2:3, 7:10},
        10: {3:9, 7:11, 2:13}
    }

    print("Korste weg:", dijkstra_algorithm(graaf1, 3, 6)[3])
    print("Volgorde van bezochte knopen:", dijkstra_algorithm(graaf1, 3, 6)[1])
    print("Predeccesors:", dijkstra_algorithm(graaf1, 3, 6)[2])
    print("Afstanden:", dijkstra_algorithm(graaf1, 3, 6)[0])

    plattegrond = {
        (18.75, 31),
        (19.25, 31),
        (19.25, 30.5),
        (19.25, 29.5),
        (19.25, 28.5),
        (19.25, 28),
        (19.25, 27.5),
        (19.25, 27),
        (19.25, 26.5),
        (19.25, 26),
        (19.25, 25.5),
        (19.25, 25),
        (19.25, 24.5),
        (19.25, 24),
        (19.25, 23.5),
        (19.25, 23),
        (19.25, 22.5),
        (19.25, 22),
        (19.25, 21.5)
    }

# node : coordinates
    nodes_coords = {
        "B3-1":  (0.75, 1)   ,
        "B3-2":  (1.25, 1)   ,
        "B3-3":  (1.25, 1.5) ,
        "B3-4":  (1.25, 2.5) ,
        "B3-5":  (1.25, 3.25),
        "B3-6":  (1.25, 3.75),
        "B3-7":  (1.25, 5)   ,
        "B3-8":  (0.5, 6)    ,
        "B3-9":  (1.75, 5.5) ,
        "B3-10": (2.25, 5.5) ,
        "B3-11": (3.5, 5.5)  ,
        "B3-12": (5.25, 5.5) ,
        "B3-13": (6, 5.5)    ,
        "B3-14": (7.5, 5.5)  ,
        "B3-15": (7.75, 3)   ,
        "B3-16": (8, 1)      ,
        "B3-17": (9, 5)      ,
    }

    # graph = {node : [[lokalen], [buren], (coordinaten)]}
    graph_B3 = {
        "B3-1"  : [["B.3.309", "B.3.311"]                       , ["B3-2"]          , (0.75, 1)   ],
        "B3-2"  : [["B.3.n1" , "B.3.310"]                       , ["B3-3"]          , (1.25, 1)   ],
        "B3-3"  : [["B.3.305", "B.3.308"]                       , ["B3-4"]          , (1.25, 1.5) ],
        "B3-4"  : [["B.3.306", "B.3.304"]                       , ["B3-5"]          , (1.25, 2.5) ],
        "B3-5"  : [["B.3.302"           ]                       , ["B3-6"]          , (1.25, 3.25)],
        "B3-6"  : [["B.3.305", "B.3.300"]                       , ["B3-7"]          , (1.25, 3.75)],
        "B3-7"  : [["B.3.210"           ]                       , ["B3-8", "B3-9"]  , (1.25, 5)   ],
        "B3-8"  : [["trap B.3.1"        ]                       , []                , (0.5, 6)    ],    #buren?
        "B3-9"  : [["B.3.210", "B.3.221"]                       , ["B3-10"]         , (1.75, 5.5) ],
        "B3-10" : [["B.3.217"           ]                       , ["B3-11"]         , (2.25, 5.5) ],
        "B3-11" : [["B.3.210", "B.3.208", "B.3.217", "B.3.215" ], ["B3-12"]         , (3.5, 5.5)  ],
        "B3-12" : [["B.3.213" ]                                 , ["B3-13"]         , (5.25, 5.5) ],
        "B3-13" : [["B.3.209", "B.3.211", "B.3.206", "B.3.200"] , ["B3-14"]         , (6, 5.5)    ],
        "B3-14" : [["B.3.105", "B.3.103", "B.3.200", "B.3.107"] , ["B3-15", "B3-17"], (7.5, 5.5)  ],
        "B3-15" : [["B.3.104"]                                  , ["B3-16"]         , (7.75, 3)   ],
        "B3-16" : [["B3.n2"]                                    , []                , (8, 1)      ],
        "B3-17" : [["trap C.3.1"]                               , []                , (9, 5)      ],   #buren?
    } # Hans zegt over nooduitgang-functie: vraag korste route naar een (nood)trap gebruik, noodtrap als eindnode.

    # x = {key: {value[1]: value[0] for _ in range(len(value[1]))} for key, value in graph_B3.items()}
    # print(x)
    #graph_B3[value[1][0]][2]

    # Python code to demonstrate dictionary
    # comprehension

    # Lists to represent keys and values
    keys = ['a', 'b', 'c', 'd', 'e']
    values = [1, 2, 3, 4, 5]

    # but this line shows dict comprehension here
    myDict = {k: v for (k, v) in zip(keys, values)}

    # We can use below too
    # myDict = dict(zip(keys, values))

    print(myDict)

    # kleine lokaaltjes en lokalen die aan elkaar verbonden zijn hebben we genegeerd. Het is unlikely dat een klein lokaaltje wordt gebruikt voor een presentatie en een route die dwars door een ander lokaal gaat is in de meeste gevallen ongewest.