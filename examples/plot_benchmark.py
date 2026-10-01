import csv
from pathlib import Path

import matplotlib.pyplot as plt


def load_results(path):
    with Path(path).open(
        "r",
        encoding="utf-8"
    ) as file:
        reader = csv.DictReader(file)

        return [
            {
                "orders": int(row["orders"]),
                "baseline": float(
                    row["baseline_distance_km"]
                ),
                "optimized": float(
                    row["optimized_distance_km"]
                ),
                "saved_percentage": float(
                    row["savings_percentage"]
                )
            }
            for row in reader
        ]


def plot_results(results, output_path):
    order_counts = [
        result["orders"]
        for result in results
    ]

    baseline_values = [
        result["baseline"]
        for result in results
    ]

    optimized_values = [
        result["optimized"]
        for result in results
    ]

    savings_values = [
        result["saved_percentage"]
        for result in results
    ]

    positions = list(
        range(len(order_counts))
    )

    width = 0.35

    figure, axis = plt.subplots(
        figsize=(10, 6)
    )

    baseline_bars = axis.bar(
        [
            position - width / 2
            for position in positions
        ],
        baseline_values,
        width,
        label="Greedy Baseline",
        color="#E76F51"
    )

    optimized_bars = axis.bar(
        [
            position + width / 2
            for position in positions
        ],
        optimized_values,
        width,
        label="OR-Tools Optimized",
        color="#2A9D8F"
    )

    axis.set_title(
        "RapidRoute: Baseline vs Optimized Distance",
        fontsize=15,
        fontweight="bold"
    )

    axis.set_xlabel("Number of Orders")
    axis.set_ylabel("Total Distance (km)")

    axis.set_xticks(
        positions,
        order_counts
    )

    axis.grid(
        axis="y",
        linestyle="--",
        alpha=0.3
    )

    axis.legend()

    axis.bar_label(
        baseline_bars,
        fmt="%.1f",
        padding=3
    )

    axis.bar_label(
        optimized_bars,
        fmt="%.1f",
        padding=3
    )

    for position, saving in zip(
        positions,
        savings_values
    ):
        height = max(
            baseline_values[position],
            optimized_values[position]
        )

        axis.text(
            position,
            height + 2,
            f"{saving:.1f}% saved",
            ha="center",
            fontweight="bold",
            color="#264653"
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


def main():
    results = load_results(
        "results/benchmark.csv"
    )

    output = plot_results(
        results,
        "visuals/benchmark_comparison.png"
    )

    print(
        f"Benchmark chart saved to {output}"
    )


if __name__ == "__main__":
    main()