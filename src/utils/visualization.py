from pathlib import Path

import matplotlib.pyplot as plt


def draw_routes(
    axis,
    scenario,
    result,
    title
):
    order_lookup = {
        order.order_id: order
        for order in scenario.orders
    }

    colours = [
        "#2A9D8F",
        "#E76F51",
        "#6D597A",
        "#F4A261",
        "#457B9D"
    ]

    axis.scatter(
        scenario.depot.x,
        scenario.depot.y,
        marker="*",
        s=260,
        color="#172A3A",
        label="Dark Store",
        zorder=5
    )

    axis.annotate(
        "Dark Store",
        (
            scenario.depot.x,
            scenario.depot.y
        ),
        xytext=(8, 8),
        textcoords="offset points"
    )

    for order in scenario.orders:
        axis.scatter(
            order.location.x,
            order.location.y,
            s=90,
            color="#FFFFFF",
            edgecolor="#172A3A",
            linewidth=1.5,
            zorder=4
        )

        axis.annotate(
            order.order_id,
            (
                order.location.x,
                order.location.y
            ),
            xytext=(7, 7),
            textcoords="offset points"
        )

    for rider_index, (
        rider_id,
        route
    ) in enumerate(result["routes"].items()):
        if not route:
            continue

        colour = colours[
            rider_index % len(colours)
        ]

        locations = [
            scenario.depot,
            *[
                order_lookup[
                    order_id
                ].location
                for order_id in route
            ],
            scenario.depot
        ]

        x_values = [
            location.x
            for location in locations
        ]

        y_values = [
            location.y
            for location in locations
        ]

        axis.plot(
            x_values,
            y_values,
            marker="o",
            linewidth=2.2,
            color=colour,
            label=rider_id,
            zorder=3
        )

        for start, end in zip(
            locations[:-1],
            locations[1:]
        ):
            midpoint_x = (
                start.x + end.x
            ) / 2

            midpoint_y = (
                start.y + end.y
            ) / 2

            axis.annotate(
                "",
                xy=(
                    midpoint_x
                    + (end.x - start.x) * 0.05,
                    midpoint_y
                    + (end.y - start.y) * 0.05
                ),
                xytext=(
                    midpoint_x
                    - (end.x - start.x) * 0.05,
                    midpoint_y
                    - (end.y - start.y) * 0.05
                ),
                arrowprops={
                    "arrowstyle": "->",
                    "color": colour,
                    "linewidth": 1.8
                }
            )

    axis.set_title(
        f"{title}\n"
        f"{result['total_distance_km']:.3f} km"
    )

    axis.set_xlabel("X coordinate (km)")
    axis.set_ylabel("Y coordinate (km)")
    axis.set_aspect("equal", adjustable="box")

    axis.grid(
        True,
        linestyle="--",
        alpha=0.3
    )

    axis.legend()


def plot_route_comparison(
    scenario,
    baseline,
    optimized,
    output_path
):
    figure, axes = plt.subplots(
        1,
        2,
        figsize=(14, 7)
    )

    figure.patch.set_facecolor("white")

    draw_routes(
        axes[0],
        scenario,
        baseline,
        "Greedy Baseline"
    )

    draw_routes(
        axes[1],
        scenario,
        optimized,
        "OR-Tools Optimized"
    )

    figure.suptitle(
        "RapidRoute Delivery Comparison",
        fontsize=18,
        fontweight="bold"
    )

    figure.tight_layout()

    output = Path(output_path)
    output.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    figure.savefig(
        output,
        dpi=200,
        bbox_inches="tight",
        facecolor="white"
    )

    plt.close(figure)

    return output