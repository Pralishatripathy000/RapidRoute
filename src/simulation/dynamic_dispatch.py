from src.models import (
    DeliveryScenario,
    Order
)

from src.optimizers.vehicle_routing import (
    optimize_routes
)


class DuplicateOrderError(Exception):
    pass


def get_order_assignments(routes):
    return {
        order_id: rider_id
        for rider_id, route in routes.items()
        for order_id in route
    }


def insert_order_and_reoptimize(
    scenario: DeliveryScenario,
    new_order: Order,
    time_limit_seconds=5
):
    existing_order_ids = {
        order.order_id
        for order in scenario.orders
    }

    if new_order.order_id in existing_order_ids:
        raise DuplicateOrderError(
            f"Order {new_order.order_id} "
            f"already exists."
        )

    previous_result = optimize_routes(
        scenario,
        time_limit_seconds
    )

    updated_scenario = DeliveryScenario(
        depot=scenario.depot,
        orders=[
            *scenario.orders,
            new_order
        ],
        riders=scenario.riders[:],
        average_speed_kmph=(
            scenario.average_speed_kmph
        )
    )

    updated_result = optimize_routes(
        updated_scenario,
        time_limit_seconds
    )

    previous_assignments = get_order_assignments(
        previous_result["routes"]
    )

    updated_assignments = get_order_assignments(
        updated_result["routes"]
    )

    reassigned_orders = {
        order_id: {
            "previous_rider": previous_rider,
            "updated_rider": (
                updated_assignments[order_id]
            )
        }
        for order_id, previous_rider
        in previous_assignments.items()
        if updated_assignments[order_id]
        != previous_rider
    }

    new_order_rider = updated_assignments[
        new_order.order_id
    ]

    distance_change = (
        updated_result["total_distance_km"]
        - previous_result["total_distance_km"]
    )

    return {
        "updated_scenario": updated_scenario,
        "previous_result": previous_result,
        "updated_result": updated_result,
        "new_order_rider": new_order_rider,
        "reassigned_orders": reassigned_orders,
        "distance_change_km": distance_change
    }