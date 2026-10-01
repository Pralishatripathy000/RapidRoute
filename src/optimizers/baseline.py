from src.models import DeliveryScenario
from src.utils.distance import euclidean_distance_km


class BaselineInfeasibleError(Exception):
    pass


def calculate_route_distance(
    scenario,
    route
):
    if not route:
        return 0.0

    order_lookup = {
        order.order_id: order
        for order in scenario.orders
    }

    current_location = scenario.depot
    total_distance = 0.0

    for order_id in route:
        order = order_lookup[order_id]

        total_distance += euclidean_distance_km(
            current_location,
            order.location
        )

        current_location = order.location

    total_distance += euclidean_distance_km(
        current_location,
        scenario.depot
    )

    return total_distance


def greedy_dispatch(
    scenario: DeliveryScenario
):
    routes = {
        rider.rider_id: []
        for rider in scenario.riders
    }

    remaining_capacity = {
        rider.rider_id: rider.capacity
        for rider in scenario.riders
    }

    current_locations = {
        rider.rider_id: scenario.depot
        for rider in scenario.riders
    }

    sorted_orders = sorted(
        scenario.orders,
        key=lambda order: (
            order.deadline_minutes,
            order.order_id
        )
    )

    for order in sorted_orders:
        eligible_riders = [
            rider
            for rider in scenario.riders
            if remaining_capacity[rider.rider_id]
            >= order.demand
        ]

        if not eligible_riders:
            raise BaselineInfeasibleError(
                f"No rider has capacity for order "
                f"{order.order_id}."
            )

        selected_rider = min(
            eligible_riders,
            key=lambda rider: (
                euclidean_distance_km(
                    current_locations[rider.rider_id],
                    order.location
                ),
                rider.rider_id
            )
        )

        rider_id = selected_rider.rider_id

        routes[rider_id].append(order.order_id)

        remaining_capacity[rider_id] -= (
            order.demand
        )

        current_locations[rider_id] = (
            order.location
        )

    route_distances = {
        rider_id: calculate_route_distance(
            scenario,
            route
        )
        for rider_id, route in routes.items()
    }

    return {
        "routes": routes,
        "route_distances_km": route_distances,
        "total_distance_km": sum(
            route_distances.values()
        ),
        "remaining_capacity": remaining_capacity
    }