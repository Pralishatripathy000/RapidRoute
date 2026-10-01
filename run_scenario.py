import argparse

from src.optimizers.baseline import (
    greedy_dispatch
)

from src.optimizers.vehicle_routing import (
    RoutingInfeasibleError,
    optimize_routes
)

from src.utils.io import load_scenario

from src.utils.metrics import (
    evaluate_routes
)


def display_result(title, result, metrics):
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

        print(f"{rider_id}: {route_text}")

    print(
        f"Total distance: "
        f"{result['total_distance_km']:.3f} km"
    )

    print(
        f"On-time deliveries: "
        f"{metrics['on_time_percentage']:.1f}%"
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
    parser = argparse.ArgumentParser(
        description=(
            "Optimize a quick-commerce "
            "delivery scenario."
        )
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to the scenario JSON file."
    )

    parser.add_argument(
        "--time-limit",
        type=int,
        default=5,
        help="Solver time limit in seconds."
    )

    arguments = parser.parse_args()

    scenario = load_scenario(
        arguments.input
    )

    baseline = greedy_dispatch(scenario)

    optimized = optimize_routes(
        scenario,
        time_limit_seconds=(
            arguments.time_limit
        )
    )

    baseline_metrics = evaluate_routes(
        scenario,
        baseline
    )

    optimized_metrics = evaluate_routes(
        scenario,
        optimized
    )

    display_result(
        "Greedy Baseline",
        baseline,
        baseline_metrics
    )

    display_result(
        "Optimized Routing",
        optimized,
        optimized_metrics
    )

    distance_saved = (
        baseline["total_distance_km"]
        - optimized["total_distance_km"]
    )

    improvement = (
        distance_saved
        / baseline["total_distance_km"]
        * 100
        if baseline["total_distance_km"] > 0
        else 0
    )

    print("\nComparison")
    print("----------")

    print(
        f"Distance saved: "
        f"{distance_saved:.3f} km"
    )

    print(
        f"Relative improvement: "
        f"{improvement:.2f}%"
    )


if __name__ == "__main__":
    try:
        main()

    except (
        ValueError,
        FileNotFoundError,
        RoutingInfeasibleError
    ) as error:
        print(f"\nError: {error}")