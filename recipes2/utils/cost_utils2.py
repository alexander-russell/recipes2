from decimal import Decimal
import pdb
import networkx as nx
from networkx import bellman_ford_path
from networkx import NetworkXNoPath
import numpy as np
from django.core.cache import cache
from ..models import Unit, Conversion, Ingredient


def build_unit_conversion_graph():
    graph = nx.MultiDiGraph()

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
            ingredient_id=conversion.ingredient.id if conversion.ingredient else None,
        )
        graph.add_edge(
            conversion.to_unit.name,
            conversion.from_unit.name,
            factor=1 / conversion.factor,
            ingredient_id=conversion.ingredient.id if conversion.ingredient else None,
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
    # print("hey1")
    # print(f"goal={goal}")
    # print(f"ingredient_rule={ingredient_rule}")
    # print(f"ingredient_rule.to_unit.name={ingredient_rule.to_unit.name}")
    # print(f"ingredient_rule.from_unit.name={ingredient_rule.from_unit.name}")
    # print(f"path_to_ingredient_rule={path_to_ingredient_rule}")
    # print(f"path_from_ingredient_rule={path_from_ingredient_rule}")
    # print(
    #     f"path_to_ingredient_rule[:-1] + path_from_ingredient_rule={path_to_ingredient_rule[:-1] + path_from_ingredient_rule}"
    # )
    # print(
    #     f"path_to_ingredient_rule + path_from_ingredient_rule={path_to_ingredient_rule + path_from_ingredient_rule}"
    # )
    # print("hey2")

    if len(path_to_ingredient_rule) == 1:
        return path_to_ingredient_rule + path_from_ingredient_rule

    return path_to_ingredient_rule[:-1] + path_from_ingredient_rule


def get_conversion_factor(start, goal, ingredient_id):
    # Build the graph from the database
    graph = cache.get("unit_conversion_graph")
    if not graph:
        # If no cached graph, rebuild it and cache it
        graph = build_unit_conversion_graph()
        cache.set("unit_conversion_graph", graph, timeout=60 * 60 * 24)

    # Print the edges before removal
    # print("Edges before removal:", list(graph.edges(data=True)))
    # print("Edges before removal:")
    # for edge in graph.edges(data=True, keys=True):
    #     print(f"  {edge}")
    #     # print(f"  {edge}")

    # Find the ingredient edge
    ingredient_edges = [
        (u, v, key, attr)
        for u, v, key, attr in graph.edges(data=True, keys=True)
        if attr.get("ingredient_id") == ingredient_id
    ]

    # Gather edges to remove in a list first
    edges_to_remove = []
    for u, v, key, attr in graph.edges(data=True, keys=True):
        if attr["ingredient_id"] is not None and attr["ingredient_id"] != ingredient_id:
            edges_to_remove.append((u, v, key))
        elif ingredient_edges and any(
            u == edge[0] and v == edge[1] and key != edge[2]
            for edge in ingredient_edges
        ):
            edges_to_remove.append((u, v, key))

    # Now remove the edges after the iteration
    for u, v, key in edges_to_remove:
        graph.remove_edge(u, v, key)  # Remove edge using its key

    # Print the edges after removal
    # print("Edges after removal:", list(graph.edges(data=True)))
    # print("Edges after removal:")
    # for edge in graph.edges(data=True, keys=True):
    #     print(f"  {edge}")

    # for a, b, key, attr in graph.edges(data=True, keys=True):
    #     print(
    #         f"a={a}; b={b}; key={key}; ingredient={attr.get('ingredient')}; factor={attr.get('factor')}; weight={attr.get('weight')};"
    #     )

    # print(graph)

    try:
        path = nx.shortest_path(graph, start, goal)
    except NetworkXNoPath as e:
        return None

    # path = get_conversion_path(graph, start, goal, ingredient)

    print(path)

    # pdb.set_trace()

    factors = [
        Decimal(next(iter(graph[a][b].items()))[1].get("factor"))
        for a, b in zip(path[:-1], path[1:])
    ]

    # print(factors)

    return Decimal(np.prod(factors))


# to load into django shell: from recipes2.utils.cost_utils import *

# or:

# import recipes2.utils.cost_utils; import importlib; importlib.reload(recipes2.utils.cost_utils); from recipes2.utils.cost_utils import *

# or:

# import recipes2.utils.cost_utils2; import importlib; importlib.reload(recipes2.utils.cost_utils2); from recipes2.utils.cost_utils2 import *
