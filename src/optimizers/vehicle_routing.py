from ortools.constraint_solver import (
    pywrapcp,
    routing_enums_pb2
)

from src.models import DeliveryScenario
from src.utils.distance import build_distance_matrix


class RoutingInfeasibleError(Exception):
    pass


def optimize_routes(
    scenario: DeliveryScenario,
    time_limit_seconds=5
):
    distance_matrix = build_distance_matrix(
        scenario
    )

    rider_count = len(scenario.riders)
    location_count = len(distance_matrix)

    manager = pywrapcp.RoutingIndexManager(
        location_count,
        rider_count,
        0
    )

    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(
        from_index,
        to_index
    ):
        from_node = manager.IndexToNode(
            from_index
        )

        to_node = manager.IndexToNode(
            to_index
        )

        return distance_matrix[from_node][to_node]

    distance_callback_index = (
        routing.RegisterTransitCallback(
            distance_callback
        )
    )

    routing.SetArcCostEvaluatorOfAllVehicles(
        distance_callback_index
    )

    demands = [
        0,
        *[
            order.demand
            for order in scenario.orders
        ]
    ]

    def demand_callback(index):
        node = manager.IndexToNode(index)
        return demands[node]

    demand_callback_index = (
        routing.RegisterUnaryTransitCallback(
            demand_callback
        )
    )

    capacities = [
        rider.capacity
        for rider in scenario.riders
    ]

    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,
        capacities,
        True,
        "Capacity"
    )

    search_parameters = (
        pywrapcp.DefaultRoutingSearchParameters()
    )

    search_parameters.first_solution_strategy = (
        routing_enums_pb2
        .FirstSolutionStrategy
        .PATH_CHEAPEST_ARC
    )

    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2
        .LocalSearchMetaheuristic
        .GUIDED_LOCAL_SEARCH
    )

    search_parameters.time_limit.seconds = (
        time_limit_seconds
    )

    solution = routing.SolveWithParameters(
        search_parameters
    )

    if solution is None:
        raise RoutingInfeasibleError(
            "No feasible vehicle-routing solution found."
        )

    routes = {}
    route_distances_meters = {}

    for vehicle_index, rider in enumerate(
        scenario.riders
    ):
        index = routing.Start(vehicle_index)
        route = []
        route_distance = 0

        while not routing.IsEnd(index):
            node = manager.IndexToNode(index)

            if node != 0:
                order = scenario.orders[node - 1]
                route.append(order.order_id)

            next_index = solution.Value(
                routing.NextVar(index)
            )

            route_distance += routing.GetArcCostForVehicle(
                index,
                next_index,
                vehicle_index
            )

            index = next_index

        routes[rider.rider_id] = route

        route_distances_meters[
            rider.rider_id
        ] = route_distance

    total_distance_meters = sum(
        route_distances_meters.values()
    )

    return {
        "routes": routes,
        "route_distances_km": {
            rider_id: distance / 1000
            for rider_id, distance
            in route_distances_meters.items()
        },
        "total_distance_km": (
            total_distance_meters / 1000
        )
    }