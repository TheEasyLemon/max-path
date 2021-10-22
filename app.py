"""
Main app functionality for project management.

Query user for a list of tasks, their dependencies, and
the cost of doing the task.

Create a directed acyclic graph to represent it.

Use mathematical programming to solve for the
longest path and critical tasks.
"""
from Wdgraph import Wdgraph

json = {
    "data": [
        {
            "task_name": "A",
            "dependencies": [],
            "cost": 2
        },
        {
            "task_name": "B",
            "dependencies": [],
            "cost": 5
        },
        {
            "task_name": "C",
            "dependencies": [],
            "cost": 8
        },
        {
            "task_name": "D",
            "dependencies": ["B", "C"],
            "cost": 14
        },
        {
            "task_name": "E",
            "dependencies": ["D", "A"],
            "cost": 7
        },
        {
            "task_name": "F",
            "dependencies": ["A", "B"],
            "cost": 30
        },
        {
            "task_name": "G",
            "dependencies": ["E", "F", "D"],
            "cost": 6
        },
        {
            "task_name": "H",
            "dependencies": ["D"],
            "cost": 3
        },
    ],
}

def generate_graph():
    data = [(task["task_name"], task["dependencies"], task["cost"]) for task in json["data"]]
    all_names = set([name for name, _, _ in data])

    graph = Wdgraph()

    is_dependency = set()

    for task in data:
        task_name, dependencies, cost = task

        for dep in dependencies:
            is_dependency.add(dep)
            graph.set_edge(dep, task_name, cost)

        if dependencies == []:
            # If no dependencies, must be a starting task
            graph.set_edge("s", task_name, cost)

    terminals = list(all_names - is_dependency)

    for terminal in terminals:
        graph.set_edge(terminal, "t", 0)

    return graph

def kahns_algorithm(graph):
    # Slow, but necessary
    G = graph.copy()
    # Will return L, contains sorted nodes
    L = []
    # S is set of nodes with no incoming edge
    S = G.get_nodes_without_incoming()

    while len(S) != 0:
        n = S.pop()
        L.append(n)
        for m, weight in G.get_outneighbors(n):
            G.remove_edge(n, m)
            if G.get_inneighbors(m) == []:
                S.add(m)

    if G.all_edges() != []:
        raise Exception("Graph has a cycle")
    else:
        return L


def solve_max_path(G):
    """
    Find the maximum network path (s -> t) on weighted directed graph G using
    topological ordering.

    1. Find a topological ordering of the DAG
    2. For each vertex of the topologically sorted list,
       set the distance to that vertex as the maximum of the distances
       of the incoming nodes plus the distance to the current node.
       We traverse the graph backwards to find the critical path.
    """
    # Topologically sort the DAG
    sorted_nodes = kahns_algorithm(G)

    dist = dict(zip(sorted_nodes, [0 for i in range(G.len)]))

    # Construct max distance from start to every other node
    for target in sorted_nodes:
        max_dist = 0
        max_source = None

        for source, weight in G.get_inneighbors(target):
            d = dist[source] + weight
            if d > max_dist:
                max_dist = d
                max_source = source

        dist[target] = max_dist

    critical_path = ["t"]
    current = "t"

    # Traverse backwards through graph to get critical path
    while current != "s":
        max_dist = float("-inf")
        max_node = None

        for source, _ in G.get_inneighbors(current):
            d = dist[source]
            if d > max_dist:
                max_dist = d
                max_node = source

        critical_path.append(max_node)
        current = max_node

    critical_path = list(reversed(critical_path))
    return dist["t"], critical_path


def main():
    graph = generate_graph()

    max_path_length, critical_path = solve_max_path(graph)

    print(f"The critical path is {critical_path}, and its length is {max_path_length}")


if __name__ == '__main__':
    main()
