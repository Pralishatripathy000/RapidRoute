# RapidRoute

Quick commerce promises delivery in minutes. The routes, unfortunately, do not optimize themselves.

RapidRoute is an Operations Research experiment for rider assignment, order batching and delivery-route optimization from a single dark store.

## Core Capabilities

- Capacitated multi-rider routing
- Delivery deadline constraints
- Rider availability and service time
- Greedy dispatch baseline
- OR-Tools route optimization
- Dynamic insertion of new orders
- Route reoptimization
- JSON-based scenario input
- Delivery and utilization metrics
- Reproducible benchmark experiments
- Static route and benchmark visualizations

## Optimization Model

RapidRoute models delivery planning as a Capacitated Vehicle Routing Problem with delivery deadlines.

The optimizer minimizes total route distance while ensuring:

- Every order is assigned exactly once
- Rider capacities are respected
- Every order meets its delivery deadline
- Routes begin and end at the dark store

A deadline-first greedy dispatcher provides the baseline.

## Verified Sample Experiment

| Metric | Greedy baseline | Optimized routing |
|---|---:|---:|
| Total distance | 33.380 km | 33.284 km |
| On-time deliveries | 100% | 100% |
| Average delivery time | 15.50 min | 16.33 min |
| Average rider utilization | 66.67% | 66.67% |

The optimized route reduced distance by **0.096 km or 0.29%**. The small difference indicates that the greedy solution was already near-optimal for this six-order scenario.

Average delivery time increased slightly because the current objective minimizes total distance rather than average ETA. All delivery deadlines remained satisfied.

## Dynamic Order Experiment

A seventh order was inserted after the initial routes were generated.

- New order assigned to: `R2`
- Additional distance: `3.102 km`
- Existing orders reassigned: `O4`, `O5` and `O6`
- Routes successfully reoptimized under the existing constraints

## Benchmark Results

The benchmarks use seeded synthetic scenarios, Euclidean distances and a two-second solver limit.

| Orders | Riders | Greedy baseline | Optimized | Distance saved | Runtime |
|---:|---:|---:|---:|---:|---:|
| 10 | 2 | 48.009 km | 35.642 km | 25.76% | 2.007 s |
| 20 | 3 | 79.503 km | 48.047 km | 39.57% | 2.002 s |
| 30 | 4 | 104.095 km | 62.749 km | 39.72% | 2.002 s |

These measurements describe the included scenarios and are not claims about production delivery networks.

## Visual Results

![Route comparison](visuals/route_comparison.png)

![Benchmark comparison](visuals/benchmark_comparison.png)

## Installation

```bash
python -m pip install -r requirements.txt
```

## Usage

Run the standard experiment:

```bash
python main.py
```

Solve a JSON scenario:

```bash
python run_scenario.py --input data/sample_scenario.json --time-limit 3
```

Run dynamic order insertion:

```bash
python -m examples.dynamic_order_demo
```

Run and visualize the benchmarks:

```bash
python -m examples.benchmark
python -m examples.plot_routes
python -m examples.plot_benchmark
```

Run all tests:

```bash
python -m unittest discover tests
```

## Project Structure

```text
src/optimizers/   Greedy and OR-Tools routing algorithms
src/simulation/   Scenario generation and dynamic dispatch
src/utils/        Distance, input, metrics and visualization utilities
data/             JSON delivery scenarios
examples/         Runnable experiments
tests/            Automated tests
results/          Benchmark outputs
visuals/          Generated plots
```

## Current Limitations

- Coordinates and orders are synthetic
- Distance is currently Euclidean
- Travel speed is constant
- Dynamic insertion reoptimizes complete routes
- The objective minimizes distance rather than multiple delivery metrics

RapidRoute is intentionally a focused OR experiment rather than a production delivery platform—one route, constraint and questionable deadline at a time.