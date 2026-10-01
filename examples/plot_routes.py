from examples.sample_scenario import (
    create_sample_scenario
)

from src.optimizers.baseline import (
    greedy_dispatch
)

from src.optimizers.vehicle_routing import (
    optimize_routes
)

from src.utils.visualization import (
    plot_route_comparison
)


def main():
    scenario = create_sample_scenario()

    baseline = greedy_dispatch(scenario)

    optimized = optimize_routes(
        scenario,
        time_limit_seconds=3
    )

    output = plot_route_comparison(
        scenario,
        baseline,
        optimized,
        "visuals/route_comparison.png"
    )

    print(
        f"Visualization saved to {output}"
    )


if __name__ == "__main__":
    main()