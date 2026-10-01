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


def display_routes(title, result):
    print(f"\n{title}")
    print("-" * len(title))

    for rider_id, route in result["routes"].items():
        route_text = (
            "Depot"
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

        if "arrival_times" in result:
            arrivals = result[
                "arrival_times"
            ][rider_id]

            if arrivals:
                formatted_arrivals = ", ".join(
                    f"{order_id}: {time} min"
                    for order_id, time
                    in arrivals.items()
                )

                print(
                    f"Arrivals: {formatted_arrivals}"
                )

    print(
        f"\nTotal distance: "
        f"{result['total_distance_km']:.3f} km"
    )


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

    display_routes(
        "Greedy Baseline",
        baseline
    )

    display_routes(
        "Optimized Routing",
        optimized
    )

    distance_saved = (
        baseline["total_distance_km"]
        - optimized["total_distance_km"]
    )

    if baseline["total_distance_km"] > 0:
        improvement_percentage = (
            distance_saved
            / baseline["total_distance_km"]
        ) * 100
    else:
        improvement_percentage = 0

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


if __name__ == "__main__":
    try:
        main()

    except (
        ValueError,
        BaselineInfeasibleError,
        RoutingInfeasibleError
    ) as error:
        print(f"\nError: {error}")