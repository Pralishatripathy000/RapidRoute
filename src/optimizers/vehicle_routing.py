from ortools.constraint_solver import (
    pywrapcp,
    routing_enums_pb2
)

from src.models import DeliveryScenario

from src.utils.distance import (
    build_distance_matrix,
    build_time_matrix
)


class RoutingInfeasibleError(Exception):
    pass


def optimize_routes(
    scenario: DeliveryScenario,
    time_limit_seconds=5
):
    distance_matrix = build_distance_matrix(
        scenario
    )

    time_matrix = build_time_matrix(
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

    service_times = [
        0,
        *[
            order.service_minutes
            for order in scenario.orders
        ]
    ]

    def time_callback(
        from_index,
        to_index
    ):
        from_node = manager.IndexToNode(
            from_index
        )

        to_node = manager.IndexToNode(
            to_index
        )

        return (
            service_times[from_node]
            + time_matrix[from_node][to_node]
        )

    time_callback_index = (
        routing.RegisterTransitCallback(
            time_callback
        )
    )

    latest_deadline = max(
        order.deadline_minutes
        for order in scenario.orders
    )

    latest_availability = max(
        rider.available_from
        for rider in scenario.riders
    )

    time_horizon = max(
        latest_deadline,
        latest_availability
    ) + 120

    routing.AddDimension(
        time_callback_index,
        60,
        time_horizon,
        False,
        "Time"
    )

    time_dimension = routing.GetDimensionOrDie(
        "Time"
    )

    for order_index, order in enumerate(
        scenario.orders,
        start=1
    ):
        index = manager.NodeToIndex(order_index)

        time_dimension.CumulVar(index).SetRange(
            0,
            order.deadline_minutes
        )

    for vehicle_index, rider in enumerate(
        scenario.riders
    ):
        start_index = routing.Start(vehicle_index)

        time_dimension.CumulVar(
            start_index
        ).SetRange(
            rider.available_from,
            rider.available_from
        )

        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(
                routing.End(vehicle_index)
            )
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
            "No feasible routing solution found."
        )

    routes = {}
    route_distances_meters = {}
    arrival_times = {}
    route_durations_minutes = {}

    for vehicle_index, rider in enumerate(
        scenario.riders
    ):
        index = routing.Start(vehicle_index)
        route = []
        route_distance = 0
        rider_arrival_times = {}

        start_time = solution.Value(
            time_dimension.CumulVar(index)
        )

        while not routing.IsEnd(index):
            node = manager.IndexToNode(index)

            if node != 0:
                order = scenario.orders[node - 1]

                route.append(order.order_id)

                rider_arrival_times[
                    order.order_id
                ] = solution.Value(
                    time_dimension.CumulVar(index)
                )

            next_index = solution.Value(
                routing.NextVar(index)
            )

            route_distance += (
                routing.GetArcCostForVehicle(
                    index,
                    next_index,
                    vehicle_index
                )
            )

            index = next_index

        end_time = solution.Value(
            time_dimension.CumulVar(index)
        )

        routes[rider.rider_id] = route

        route_distances_meters[
            rider.rider_id
        ] = route_distance

        arrival_times[
            rider.rider_id
        ] = rider_arrival_times

        route_durations_minutes[
            rider.rider_id
        ] = end_time - start_time

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
        ),
        "arrival_times": arrival_times,
        "route_durations_minutes": (
            route_durations_minutes
        )
    }