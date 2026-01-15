# 🚇 SubwayRouter

A high-performance pathfinding system for the London Underground network, implementing both Dijkstra's and A\* algorithms with real-time visualization and performance analysis.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.3+-green.svg)](https://pandas.pydata.org)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.10+-orange.svg)](https://matplotlib.org)
[![NumPy](https://img.shields.io/badge/NumPy-2.4+-red.svg)](https://numpy.org)

## 📋 Overview

SubwayRouter is a route-finding application that calculates the optimal paths between London Underground stations. The project demonstrates advanced graph theory concepts by implementing two fundamental pathfinding algorithms:

- **Dijkstra's Algorithm**
- **A\* Algorithm**

The system processes real London Underground data with 302 stations and 406 connections, providing both algorithmic analysis and geographic visualizations.

## 📊 Data Used

The project uses two main CSV datasets:

### `london_stations.csv`

Contains 302 London Underground stations with:

- Station ID, name, and display name
- Latitude and longitude coordinates
- Zone information and rail connectivity

### `london_connections.csv`

Contains 406 connections between stations with:

- Station pair mappings
- Line information
- Travel time data

## 🚀 Getting Started

1. Clone this repository:

```bash
git clone https://github.com/oakflow/SubwayRouter.git
cd SubwayRouter
```

2. Ensure you have dependencies:

```bash
# (Recommended) Create virtual environment
python -m venv venv

# Activate
venv\Scripts\activate        # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
python -m pip install -r requirements.txt
```

3. Run the application:

```bash
python router.py
```

## 🕹️ Usage

### Interactive Mode

1. **Launch the program**: Run `python router.py`
2. **Select stations**: Choose start and destination by station ID
3. **View results**: Compare both algorithm outputs
4. **Visualizations**: Automatic network and route maps
5. **Performance data**: Runtime and efficiency analysis

### Example Session

```
Loading London Underground network...
Loaded 302 stations
Loaded 406 connections
Graph loaded with 302 stations

Available stations:
==================================================
ID: 1   - Acton Town
ID: 2   - Aldgate
ID: 3   - Aldgate East
ID: 4   - All Saints
ID: 5   - Alperton
ID: 7   - Angel
ID: 8   - Archway
ID: 9   - Arnos Grove
ID: 10  - Arsenal
ID: 11  - Baker Street
... up until ID: 303 - Wood Green
==================================================

Enter start station ID: 157
Selected start: London Bridge
Enter destination station ID: 41
Selected destination: Canada Water

Finding route from London Bridge (ID: 157) to Canada Water (ID: 41)

Dijkstra's Algorithm:
  Path: ['157', '23', '41']
  Distance: 2.70 km
  Nodes visited: 20

A* Algorithm:
  Path: ['157', '23', '41']
  Distance: 2.70 km
  Nodes visited: 3

Visualizing the subway network...
Visualizing the route...

Running performance comparison...
Running 10 performance tests...

=== PERFORMANCE COMPARISON ===
Average Dijkstra time: 0.0011s
Average A* time: 0.0001s
Average Dijkstra nodes: 177
Average A* nodes: 45
A* efficiency: 0.26
Performance test completed with 10 successful runs
Analysis complete!
```

## ⚙️ Algorithm Implementation

### Dijkstra's Algorithm

- **Time Complexity**: O((V + E) log V)
- **Space Complexity**: O(V)
- **Guarantee**: Always finds shortest path
- **Use Case**: When exploring all possibilities is acceptable

### A\* Algorithm

- **Time Complexity**: O(E) in best case
- **Heuristic**: Haversine distance (admissible)
- **Optimization**: Reduces search space significantly
- **Use Case**: When efficiency matters with guaranteed optimality

### Custom Data Structures

#### Min-Heap Implementation

- Efficient priority queue operations
- O(log n) insertion and extraction
- Supports decrease-key operations for Dijkstra's algorithm

#### Weighted Graph Structure

- Adjacency list representation
- Coordinate storage for geographic calculations
- Bidirectional edge support

## 📈 Performance Analysis

The system includes comprehensive performance benchmarking:

- **Runtime Comparison**: Millisecond precision timing
- **Node Visitation**: Algorithm efficiency metrics
- **Visual Analytics**: Automatic chart generation
- **Statistical Analysis**: Multiple test averaging

Typical results show A\* visiting ~60% fewer nodes than Dijkstra and having ~85% faster runtime while maintaining optimal solutions.

## 🗺️ Visualizations

### Network Overview

- Complete London Underground map
- Station plotting with geographic coordinates
- Connection line rendering

### Reference Map

The project includes `london_underground.png` - a London Underground network map for visual comparison with the generated network visualizations.

### Route Highlighting

- Path visualization in distinctive colors
- Clear route progression

### Performance Charts

- Side-by-side algorithm comparison
- Runtime and efficiency bar charts
- Statistical significance display

## 📐 Mathematical Foundation

### Haversine Distance Formula

Calculates great-circle distances between coordinate pairs:

```
a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
c = 2 ⋅ atan2(√a, √(1−a))
d = R ⋅ c
```

Where φ is latitude, λ is longitude, R is Earth's radius (6,371 km)

### A\* Heuristic

Uses straight-line geographic distance as admissible heuristic:

- Never overestimates actual path cost (since actual can't be shorter than straight)
- Guides search toward goal efficiently
- Maintains optimality guarantee

---
