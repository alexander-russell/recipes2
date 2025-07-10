import networkx as nx
import numpy as np
from django.core.cache import cache
from ..models import Unit, Conversion


def build_unit_conversion_graph():
    graph = nx.DiGraph()

    # Add units as nodes
    units = Unit.objects.all()
    for unit in units:
        graph.add_node(unit.name)

    # Add conversions as edges
    conversions = Conversion.objects.all()
    for conversion in conversions:
        # Add them in the forward direction, and then in the reverse using the reciprocal factor
        graph.add_edge(
            conversion.from_unit.name,
            conversion.to_unit.name,
            factor=conversion.factor,
            ingredient=conversion.ingredient,
        )
        graph.add_edge(
            conversion.to_unit.name,
            conversion.from_unit.name,
            factor=1 / conversion.factor,
            ingredient=conversion.ingredient,
        )

    return graph


def get_conversion_path(subgraph, start, goal, ingredient):
    # Get ingredient rule. If there is none, use simple shortest path
    try:
        ingredient_rule = Conversion.objects.get(ingredient=ingredient)
    except Conversion.DoesNotExist:
        return nx.shortest_path(subgraph, source=start, target=goal)

    # Get shortest path to ingredient rule and then shortest path from there to goal
    path_to_ingredient_rule = nx.shortest_path(
        subgraph, source=start, target=ingredient_rule.from_unit.name
    )
    path_from_ingredient_rule = nx.shortest_path(
        subgraph, source=ingredient_rule.to_unit.name, target=goal
    )

    # If ingredient rule ends at goal, return that
    print("hey1")
    print(f"goal={goal}")
    print(f"ingredient_rule={ingredient_rule}")
    print(f"ingredient_rule.to_unit.name={ingredient_rule.to_unit.name}")
    print(f"ingredient_rule.from_unit.name={ingredient_rule.from_unit.name}")
    print(f"path_to_ingredient_rule={path_to_ingredient_rule}")
    print(f"path_from_ingredient_rule={path_from_ingredient_rule}")
    print(f"path_to_ingredient_rule[:-1] + path_from_ingredient_rule={path_to_ingredient_rule[:-1] + path_from_ingredient_rule}")
    print(f"path_to_ingredient_rule + path_from_ingredient_rule={path_to_ingredient_rule + path_from_ingredient_rule}")
    print("hey2")

    if (len(path_to_ingredient_rule) == 1):
        return path_to_ingredient_rule + path_from_ingredient_rule

    return path_to_ingredient_rule[:-1] + path_from_ingredient_rule


def get_conversion_factor(start, goal, ingredient):
    # Build the graph from the database
    graph = build_unit_conversion_graph()
    # graph = cache.get("unit_conversion_graph")
    # if not graph:
    #     # If no cached graph, rebuild it and cache it
    #     graph = build_unit_conversion_graph()
    #     cache.set("unit_conversion_graph", graph, timeout=60 * 60 * 24)

    # Filter graph for this ingredient
    # filtered_nodes = [
    #     node
    #     for node, attr in graph.nodes(data=True)
    #     if attr.get("ingredient") == ingredient or attr.get("ingredient") is None
    # ]
    # subgraph = graph.subgraph(filtered_nodes)

    filtered_edges = [
        (u, v)
        for u, v, attr in graph.edges(data=True)
        if attr.get("ingredient") == ingredient or attr.get("ingredient") is None
    ]

    filtered_nodes = set(u for u, v in filtered_edges) | set(v for u, v in filtered_edges)

    subgraph = graph.subgraph(filtered_nodes)

    # Optionally, print the subgraph for debugging
    print(f"Filtered edges: {filtered_edges}")
    print(f"Filtered nodes: {filtered_nodes}")

    for node, attr in graph.nodes(data=True):
        print(node, attr.get("ingredient"))

    for node, attr in graph.nodes(data=True):
        print(f"Node: {node}, Ingredient Attribute: '{attr.get('ingredient')}', Ingredient Variable: '{ingredient}'")

    print(graph)
    print(subgraph)

    path = get_conversion_path(subgraph, start, goal, ingredient)

    print(path)

    factors = [subgraph[u][v]["factor"] for u, v in zip(path[:-1], path[1:])]

    print(factors)

    return np.prod(factors)

# to load into django shell: from manager.utils.cost_utils import *

# or:

# import manager.utils.cost_utils; import importlib; importlib.reload(manager.utils.cost_utils); from manager.utils.cost_utils import *