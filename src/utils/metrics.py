from src.utils.distance import (
    euclidean_distance_km,
    travel_time_minutes
)


def evaluate_routes(
    scenario,
    result
):
    order_lookup = {
        order.order_id: order
        for order in scenario.orders
    }

    rider_lookup = {
        rider.rider_id: rider
        for rider in scenario.riders
    }

    arrival_times = {}
    route_durations = {}
    rider_utilization = {}
    late_orders = []

    for rider_id, route in result["routes"].items():
        rider = rider_lookup[rider_id]

        current_location = scenario.depot
        current_time = rider.available_from
        route_demand = 0
        rider_arrivals = {}

        for order_id in route:
            order = order_lookup[order_id]

            distance = euclidean_distance_km(
                current_location,
                order.location
            )

            current_time += travel_time_minutes(
                distance,
                scenario.average_speed_kmph
            )

            rider_arrivals[order_id] = current_time

            if current_time > order.deadline_minutes:
                late_orders.append(order_id)

            current_time += order.service_minutes
            route_demand += order.demand
            current_location = order.location

        if route:
            return_distance = euclidean_distance_km(
                current_location,
                scenario.depot
            )

            current_time += travel_time_minutes(
                return_distance,
                scenario.average_speed_kmph
            )

        arrival_times[rider_id] = rider_arrivals

        route_durations[rider_id] = (
            current_time - rider.available_from
        )

        rider_utilization[rider_id] = (
            route_demand / rider.capacity * 100
        )

    all_arrivals = [
        arrival_time
        for rider_arrivals
        in arrival_times.values()
        for arrival_time
        in rider_arrivals.values()
    ]

    total_orders = len(scenario.orders)
    on_time_orders = total_orders - len(late_orders)

    average_delivery_time = (
        sum(all_arrivals) / len(all_arrivals)
        if all_arrivals
        else 0
    )

    average_utilization = (
        sum(rider_utilization.values())
        / len(rider_utilization)
        if rider_utilization
        else 0
    )

    return {
        "total_orders": total_orders,
        "on_time_orders": on_time_orders,
        "late_orders": late_orders,
        "on_time_percentage": (
            on_time_orders / total_orders * 100
        ),
        "average_delivery_time_minutes": (
            average_delivery_time
        ),
        "average_rider_utilization_percentage": (
            average_utilization
        ),
        "arrival_times": arrival_times,
        "route_durations_minutes": route_durations,
        "rider_utilization_percentage": (
            rider_utilization
        )
    }