from examples.sample_scenario import (
    create_sample_scenario
)

from src.models import (
    Location,
    Order
)

from src.simulation.dynamic_dispatch import (
    insert_order_and_reoptimize
)


def display_routes(title, routes):
    print(f"\n{title}")
    print("-" * len(title))

    for rider_id, route in routes.items():
        route_text = (
            "No assigned orders"
            if not route
            else "Depot -> "
            + " -> ".join(route)
            + " -> Depot"
        )

        print(f"{rider_id}: {route_text}")


def main():
    scenario = create_sample_scenario()

    new_order = Order(
        order_id="O7",
        location=Location(3, 2),
        demand=1,
        deadline_minutes=35
    )

    result = insert_order_and_reoptimize(
        scenario,
        new_order,
        time_limit_seconds=3
    )

    display_routes(
        "Routes Before New Order",
        result["previous_result"]["routes"]
    )

    print(
        f"\nNew order received: "
        f"{new_order.order_id}"
    )

    print(
        f"Location: "
        f"({new_order.location.x}, "
        f"{new_order.location.y})"
    )

    print(
        f"Deadline: "
        f"{new_order.deadline_minutes} minutes"
    )

    display_routes(
        "Routes After Reoptimization",
        result["updated_result"]["routes"]
    )

    print(
        f"\nNew order assigned to: "
        f"{result['new_order_rider']}"
    )

    print(
        f"Distance change: "
        f"{result['distance_change_km']:.3f} km"
    )

    if result["reassigned_orders"]:
        print("\nReassigned Existing Orders")

        for order_id, change in (
            result["reassigned_orders"].items()
        ):
            print(
                f"{order_id}: "
                f"{change['previous_rider']} -> "
                f"{change['updated_rider']}"
            )
    else:
        print(
            "\nNo existing orders were reassigned."
        )


if __name__ == "__main__":
    main()