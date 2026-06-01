import heapq
import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
from math import radians, cos, sin, sqrt


class Item:
    def __init__(self, value, key):
        self.key = key
        self.value = value
    
    def __str__(self):
        return "(" + str(self.key) + "," + str(self.value) + ")"


class Heap:
    def __init__(self, data):
        self.items = data
        self.length = len(data)
        
        # add a map based on input node
        self.map = {}
        for i in range(self.length):
            self.map[self.items[i].value] = i

        self.build_heap()

    def find_left_index(self, index):
        return 2 * (index + 1) - 1

    def find_right_index(self, index):
        return 2 * (index + 1)

    def find_parent_index(self, index):
        return (index + 1) // 2 - 1  
    
    def heapify(self, index):
        smallest_known_index = index

        if self.find_left_index(index) < self.length and self.items[self.find_left_index(index)].key < self.items[index].key:
            smallest_known_index = self.find_left_index(index)

        if self.find_right_index(index) < self.length and self.items[self.find_right_index(index)].key < self.items[smallest_known_index].key:
            smallest_known_index = self.find_right_index(index)

        if smallest_known_index != index:
            self.items[index], self.items[smallest_known_index] = self.items[smallest_known_index], self.items[index]
            
            # update map
            self.map[self.items[index].value] = index
            self.map[self.items[smallest_known_index].value] = smallest_known_index

            # recursive call
            self.heapify(smallest_known_index)

    def build_heap(self):
        for i in range(self.length // 2 - 1, -1, -1):
            self.heapify(i) 



    def insert(self, node):
        if len(self.items) == self.length:
            self.items.append(node)
        else:
            self.items[self.length] = node
        self.map[node.value] = self.length
        self.length += 1
        self.swim_up(self.length - 1)

    def insert_nodes(self, node_list):
        for node in node_list:
            self.insert(node)


    def swim_up(self, index):
        while index > 0 and self.items[index].key < self.items[self.find_parent_index(index)].key:
            
            # swap values
            self.items[index], self.items[self.find_parent_index(index)] = self.items[self.find_parent_index(index)], self.items[index]
            
            #update map
            self.map[self.items[index].value] = index
            self.map[self.items[self.find_parent_index(index)].value] = self.find_parent_index(index)
            index = self.find_parent_index(index)

    def get_min(self):
        if len(self.items) > 0:
            return self.items[0]

    def extract_min(self):
        
        # exchange
        self.items[0], self.items[self.length - 1] = self.items[self.length - 1], self.items[0]
        # update map
        self.map[self.items[self.length - 1].value] = self.length - 1
        self.map[self.items[0].value] = 0

        min_node = self.items[self.length - 1]
        self.length -= 1
        self.map.pop(min_node.value)
        self.heapify(0)
        return min_node

    def decrease_key(self, value, new_key):
        if new_key >= self.items[self.map[value]].key:
            return
        index = self.map[value]
        self.items[index].key = new_key
        self.swim_up(index)

    def get_element_from_value(self, value):
        return self.items[self.map[value]]

    def is_empty(self):
        return self.length == 0


class UnDirectedWeightedGraph:
    def __init__(self):
        self.adj = {}
        self.weights = {}
        self.coordinates = {}

    def adjacent_nodes(self, node):
        return self.adj[node]
    
    def add_coordinate(self, node, lat, lon):
        self.coordinates[node] = (lat, lon)

    def add_node(self, node):
        if node not in self.adj:    # only add if not present already
            self.adj[node] = []

    def add_edge(self, node1, node2, weight):
        if node2 not in self.adj[node1]:
            self.adj[node1].append(node2)
            self.adj[node2].append(node1)
        self.weights[(node1, node2)] = weight
        self.weights[(node2, node1)] = weight

    def get_weight(self, node1, node2):
        return self.weights[(node1, node2)]
    
    def get_coordinates(self):
        return self.coordinates

    def get_graph(self):
        return self.adj
    





















def haversine(lat1, lon1, lat2, lon2):
    # convert from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # the formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    # radius of earth in km
    R = 6371  
    distance = R * c   

    return distance


def generate_graph(stations_filename, connections_filename):

    graph = UnDirectedWeightedGraph()

    # read stations' data with pandas
    stations_df = pd.read_csv(stations_filename)
    print(f"Loaded {len(stations_df)} stations")
    
    # add coordinates to graph
    for _, row in stations_df.iterrows():
        station_id = str(row['id'])
        lat = float(row['latitude'])
        lon = float(row['longitude'])
        graph.add_coordinate(station_id, lat, lon)

    # read connections with pandas
    connections_df = pd.read_csv(connections_filename)
    print(f"Loaded {len(connections_df)} connections")
    
    locations = graph.get_coordinates()
    adjacency_list = []
    


    for _, row in connections_df.iterrows():
        node1 = str(row['station1'])
        node2 = str(row['station2'])

        if node1 in locations and node2 in locations:
            lat1, lon1 = locations[node1]
            lat2, lon2 = locations[node2]
            
            weight = haversine(lat1, lon1, lat2, lon2)
            adjacency_list.append((node1, node2, weight))
    
    #build the graph
    for node1, node2, weight in adjacency_list:
        graph.add_node(node1)
        graph.add_node(node2)
        graph.add_edge(node1, node2, weight)

    return graph

# admissible hueristic, never overestimates so a* is guaranteed optimal
def heuristic_calculator(graph, destination):
    heuristic = {}
    coordinates = graph.get_coordinates()
    
    if destination not in coordinates:
        raise ValueError(f"Destination {destination} not found in graph coordinates")
    
    dst_lat, dst_lon = coordinates[destination]
    
    for src in graph.get_graph():
        if src in coordinates:
            src_lat, src_lon = coordinates[src]
            heuristic[src] = haversine(src_lat, src_lon, dst_lat, dst_lon)
        else:
            heuristic[src] = 0

    return heuristic


























def dijkstra(graph, source, target):
    
    adjacency_dict = graph.get_graph()
    visited_nodes = 0
    
    distances = {node: float('inf') for node in adjacency_dict}
    predecessors = {node: None for node in adjacency_dict}
    distances[source] = 0
    heap = Heap([])
    
    # insert all nodes with distances
    for node in adjacency_dict:
        heap.insert(Item(node, distances[node]))
    
    while not heap.is_empty():
        visited_nodes += 1
        u = heap.extract_min().value
        
        # early exit if target found
        if u == target:
            break
        
        for v in adjacency_dict[u]:
            new_distance = distances[u] + graph.get_weight(u, v)
            if new_distance < distances[v]:
                distances[v] = new_distance
                predecessors[v] = u
                heap.decrease_key(v, new_distance)
    
    # reconstruct path from source to target
    path = []
    current_node = target
    
    # if target is unreachable, return empty path
    if distances[target] == float('inf'):
        return distances, [], visited_nodes
    
    # backtrack from target to source
    while current_node is not None:
        path.append(current_node)
        current_node = predecessors[current_node]
    
    path.reverse()  # reverse to get source to target order
    

    return distances, path, visited_nodes




def a_star(graph, start, goal, heuristic):

    visited_nodes = 0
    
    # min heap
    open_set = [(heuristic[start], start)]
    
    # for some node n, came_from[n] is the node immediately preceding it
    came_from = {}
    
    # gScore stores the cost from start to each node
    g_score = {node: float('inf') for node in graph.get_graph()}

    g_score[start] = 0
    
    # fScore[n] = gScore[n] + h(n)
    f_score = {node: float('inf') for node in graph.get_graph()}
    f_score[start] = heuristic[start]

    # graph adj lists
    neighbors = graph.get_graph()
    
    while open_set:
        visited_nodes += 1
        # get node with lowest fScore value
        _, current = heapq.heappop(open_set)
        
        if current == goal:

            # reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            
            return (path, g_score[goal]), visited_nodes
        
        for neighbor in neighbors[current]:
            weight = graph.get_weight(current, neighbor)
            tentative_g_score = g_score[current] + weight
            
            if tentative_g_score < g_score[neighbor]:
                
                # this path to neighbor is better than any prev one
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic[neighbor]
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return ([], 0), visited_nodes  # no path found






























def get_station_info(stations_filename, station_id=None):

    stations_df = pd.read_csv(stations_filename)
    
    if station_id:
        station_row = stations_df[stations_df['id'] == int(station_id)]
        if not station_row.empty:
            row = station_row.iloc[0]
            return {
                'id': str(row['id']),
                'latitude': row['latitude'],
                'longitude': row['longitude'],
                'name': row['name']
            }
        return None
    
    else:

        # return all stations as dictionary
        stations = {}
        for _, row in stations_df.iterrows():
            stations[str(row['id'])] = {
                'id': str(row['id']),
                'latitude': row['latitude'],
                'longitude': row['longitude'],
                'name': row['name']
            }

        return stations




















def visualize_network(graph, stations_filename, title="Subway Network"):
    # we visualize here using matplotlib

    stations_df = pd.read_csv(stations_filename)
    
    plt.figure(figsize=(8, 6))
    plt.scatter(stations_df['longitude'], stations_df['latitude'], c='red', s=50, alpha=0.7, zorder=5)
    
    # draw connections
    coordinates = graph.get_coordinates()
    adjacency = graph.get_graph()
    

    for node1 in adjacency:
        for node2 in adjacency[node1]:
            if node1 in coordinates and node2 in coordinates:
                lat1, lon1 = coordinates[node1]
                lat2, lon2 = coordinates[node2]
                plt.plot([lon1, lon2], [lat1, lat2], 'b-', alpha=0.3, linewidth=1, zorder=1)
    

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.show()




def visualize_path(graph, path, stations_filename, title="Subway Route"):

    if len(path) < 2:
        print("Path too short to visualize")
        return

    stations_df = pd.read_csv(stations_filename)
    coordinates = graph.get_coordinates()
    
    plt.figure(figsize=(8, 6))
    # STATIONS NOT ON PATH COLOR
    plt.scatter(stations_df['longitude'], stations_df['latitude'], 
                c='lightgray', s=30, alpha=0.5, zorder=2)
    
    # STATIONS ON PATH COLOR
    path_lats = [coordinates[station][0] for station in path if station in coordinates]
    path_lons = [coordinates[station][1] for station in path if station in coordinates]
    plt.scatter(path_lons, path_lats, c='forestgreen', s=100, alpha=0.9, zorder=5)
    
    # PATH CONNECTIONS COLOR
    for i in range(len(path) - 1):
        if path[i] in coordinates and path[i+1] in coordinates:
            lat1, lon1 = coordinates[path[i]]
            lat2, lon2 = coordinates[path[i+1]]

            plt.plot([lon1, lon2], [lat1, lat2], 'limegreen', linewidth=2, zorder=4)
    
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.show()



def compare_algorithms_performance(graph, stations_filename, num_tests=10):
    # we compare dijstkra and a*

    stations_df = pd.read_csv(stations_filename)
    station_ids = stations_df['id'].astype(str).tolist()
    
    results = []
    print(f"Running {num_tests} performance tests...")
    
    for i in range(num_tests):
        start = np.random.choice(station_ids)
        end = np.random.choice([s for s in station_ids if s != start])
        
        # dijkstra
        start_time = time.perf_counter()
        distances, dijkstra_path, dijkstra_nodes = dijkstra(graph, start, end)
        dijkstra_time = time.perf_counter() - start_time
        
        # a*
        heuristic = heuristic_calculator(graph, end)
        start_time = time.perf_counter()
        (astar_path, astar_cost), astar_nodes = a_star(graph, start, end, heuristic)
        astar_time = time.perf_counter() - start_time
        
        results.append({
            'dijkstra_time': dijkstra_time,
            'dijkstra_nodes': dijkstra_nodes,
            'astar_time': astar_time,
            'astar_nodes': astar_nodes
        })

    if results:
        results_df = pd.DataFrame(results)
        
        print("\n=== PERFORMANCE COMPARISON ===")
        print(f"Average Dijkstra time: {results_df['dijkstra_time'].mean():.4f}s")
        print(f"Average A* time: {results_df['astar_time'].mean():.4f}s")
        print(f"Average Dijkstra nodes: {results_df['dijkstra_nodes'].mean():.0f}")
        print(f"Average A* nodes: {results_df['astar_nodes'].mean():.0f}")
        print(f"A* efficiency: {results_df['astar_nodes'].mean()/results_df['dijkstra_nodes'].mean():.2f}")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))
        
        ax1.bar(['Dijkstra', 'A*'], 
                [results_df['dijkstra_time'].mean(), results_df['astar_time'].mean()],
                color=['green', 'orange'], alpha=0.7)
        ax1.set_ylabel('Average Runtime (s)')
        ax1.set_title('Algorithm Runtime Comparison')
        ax1.grid(True, alpha=0.3)
        
        ax2.bar(['Dijkstra', 'A*'], 
                [results_df['dijkstra_nodes'].mean(), results_df['astar_nodes'].mean()],
                color=['green', 'orange'], alpha=0.7)
        ax2.set_ylabel('Average Nodes Visited')
        ax2.set_title('Nodes Visited Comparison')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        return results_df

































def main():

    # generate subway graph
    print("Loading London Underground network...")
    graph = generate_graph("london_stations.csv", "london_connections.csv")
    
    print(f"Graph loaded with {len(graph.get_graph())} stations")
    
    # get station info to show options to user
    stations_info = get_station_info("london_stations.csv")
    
    print("\nAvailable stations:")
    print("=" * 50)
    for station_id, info in list(stations_info.items())[:10]:  # show first 10 stations
        print(f"ID: {station_id:<3} - {info['name']}")
    print("... up until ID: 303 - Wood Green")
    print("=" * 50)
    
    # get user input for stations
    while True:
        start_station = input("\nEnter start station ID: ").strip()
        if start_station in stations_info:
            print(f"Selected start: {stations_info[start_station]['name']}")
            break
        else:
            print("Invalid station ID. Please try again.")
    
    while True:
        end_station = input("Enter destination station ID: ").strip()
        if end_station in stations_info:
            print(f"Selected destination: {stations_info[end_station]['name']}")
            break
        elif end_station == start_station:
            print("Destination cannot be the same as start station. Please choose a different one.")
        else:
            print("Invalid station ID. Please try again.")
    
    print(f"\nFinding route from {stations_info[start_station]['name']} (ID: {start_station}) to {stations_info[end_station]['name']} (ID: {end_station})")
    
    # calculate heuristic for a*
    heuristic = heuristic_calculator(graph, end_station)
    
    # run dijkstra
    distances, dijkstra_path, dijkstra_nodes = dijkstra(graph, start_station, end_station)
    
    # run a*
    (astar_path, astar_cost), astar_nodes = a_star(graph, start_station, end_station, heuristic)
    
    print(f"\nDijkstra's Algorithm:")
    print(f"  Path: {dijkstra_path}")
    print(f"  Distance: {distances[end_station]:.2f} km")
    print(f"  Nodes visited: {dijkstra_nodes}")
    
    print(f"\nA* Algorithm:")
    print(f"  Path: {astar_path}")
    print(f"  Distance: {astar_cost:.2f} km")
    print(f"  Nodes visited: {astar_nodes}")
    
    # visualize entire network
    print("\nVisualizing the subway network...")
    visualize_network(graph, "london_stations.csv", "London Underground Network")
    
    # visualize specific path
    if dijkstra_path:
        print("Visualizing the route...")
        visualize_path(graph, dijkstra_path, "london_stations.csv", 
                      f"Route from {stations_info[start_station]['name']} to {stations_info[end_station]['name']}")
    
    # performance comparison
    print("\nRunning performance comparison...")
    results_df = compare_algorithms_performance(graph, "london_stations.csv", num_tests=10)
    
    if results_df is not None:
        print(f"Performance test completed with {len(results_df)} successful runs")
    
    print("Analysis complete!")


if __name__ == "__main__":
    main()
