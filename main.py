from examples.sample_scenario import (
    create_sample_scenario
)

from src.optimizers.baseline import (
    BaselineInfeasibleError,
    greedy_dispatch
)

from src.optimizers.vehicle_routing import (
    RoutingInfeasibleError,
    optimize_routes
)

from src.utils.metrics import (
    evaluate_routes
)


def display_routes(title, result):
    print(f"\n{title}")
    print("-" * len(title))

    for rider_id, route in result["routes"].items():
        route_text = (
            "No assigned orders"
            if not route
            else "Depot -> "
            + " -> ".join(route)
            + " -> Depot"
        )

        distance = result[
            "route_distances_km"
        ][rider_id]

        print(
            f"{rider_id}: {route_text}"
        )

        print(
            f"Distance: {distance:.3f} km"
        )

    print(
        f"\nTotal distance: "
        f"{result['total_distance_km']:.3f} km"
    )


def display_metrics(metrics):
    print(
        f"On-time deliveries: "
        f"{metrics['on_time_orders']}/"
        f"{metrics['total_orders']} "
        f"({metrics['on_time_percentage']:.1f}%)"
    )

    print(
        f"Average delivery time: "
        f"{metrics['average_delivery_time_minutes']:.2f} "
        f"minutes"
    )

    print(
        f"Average rider utilization: "
        f"{metrics['average_rider_utilization_percentage']:.2f}%"
    )

    if metrics["late_orders"]:
        print(
            "Late orders: "
            + ", ".join(metrics["late_orders"])
        )
    else:
        print("Late orders: None")


def main():
    print("\nRapidRoute")
    print(
        "Quick-Commerce Delivery "
        "Optimization Experiment"
    )

    scenario = create_sample_scenario()

    baseline = greedy_dispatch(scenario)

    optimized = optimize_routes(
        scenario,
        time_limit_seconds=3
    )

    baseline_metrics = evaluate_routes(
        scenario,
        baseline
    )

    optimized_metrics = evaluate_routes(
        scenario,
        optimized
    )

    display_routes(
        "Greedy Baseline",
        baseline
    )

    display_metrics(
        baseline_metrics
    )

    display_routes(
        "Optimized Routing",
        optimized
    )

    display_metrics(
        optimized_metrics
    )

    distance_saved = (
        baseline["total_distance_km"]
        - optimized["total_distance_km"]
    )

    improvement_percentage = (
        distance_saved
        / baseline["total_distance_km"]
        * 100
        if baseline["total_distance_km"] > 0
        else 0
    )

    print("\nComparison")
    print("----------")

    print(
        f"Distance difference: "
        f"{distance_saved:.3f} km"
    )

    print(
        f"Relative improvement: "
        f"{improvement_percentage:.2f}%"
    )

    print(
        f"Late-order reduction: "
        f"{len(baseline_metrics['late_orders'])} -> "
        f"{len(optimized_metrics['late_orders'])}"
    )


if __name__ == "__main__":
    try:
        main()

    except (
        ValueError,
        BaselineInfeasibleError,
        RoutingInfeasibleError
    ) as error:
        print(f"\nError: {error}")