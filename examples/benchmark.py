import csv
from math import ceil
from pathlib import Path
from time import perf_counter

from src.optimizers.baseline import (
    greedy_dispatch
)

from src.optimizers.vehicle_routing import (
    optimize_routes
)

from src.simulation.generator import (
    generate_scenario
)


def run_benchmark():
    results = []

    for order_count in [10, 20, 30]:
        rider_count = max(
            2,
            ceil(order_count / 8)
        )

        scenario = generate_scenario(
            order_count=order_count,
            rider_count=rider_count,
            seed=100 + order_count
        )

        baseline = greedy_dispatch(scenario)

        start_time = perf_counter()

        optimized = optimize_routes(
            scenario,
            time_limit_seconds=2
        )

        runtime_seconds = (
            perf_counter() - start_time
        )

        distance_saved = (
            baseline["total_distance_km"]
            - optimized["total_distance_km"]
        )

        savings_percentage = (
            distance_saved
            / baseline["total_distance_km"]
            * 100
        )

        results.append({
            "orders": order_count,
            "riders": rider_count,
            "baseline_distance_km": round(
                baseline["total_distance_km"],
                3
            ),
            "optimized_distance_km": round(
                optimized["total_distance_km"],
                3
            ),
            "distance_saved_km": round(
                distance_saved,
                3
            ),
            "savings_percentage": round(
                savings_percentage,
                2
            ),
            "runtime_seconds": round(
                runtime_seconds,
                3
            )
        })

    return results


def save_results(results, output_path):
    output = Path(output_path)

    output.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with output.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=results[0].keys()
        )

        writer.writeheader()
        writer.writerows(results)

    return output


def display_results(results):
    print("\nRapidRoute Benchmark")
    print("-" * 76)

    header = (
        f"{'Orders':>8}"
        f"{'Riders':>10}"
        f"{'Baseline':>14}"
        f"{'Optimized':>14}"
        f"{'Saved %':>12}"
        f"{'Runtime':>12}"
    )

    print(header)
    print("-" * 76)

    for result in results:
        print(
            f"{result['orders']:>8}"
            f"{result['riders']:>10}"
            f"{result['baseline_distance_km']:>14.3f}"
            f"{result['optimized_distance_km']:>14.3f}"
            f"{result['savings_percentage']:>12.2f}"
            f"{result['runtime_seconds']:>12.3f}"
        )


def main():
    results = run_benchmark()

    display_results(results)

    output = save_results(
        results,
        "results/benchmark.csv"
    )

    print(f"\nResults saved to {output}")


if __name__ == "__main__":
    main()