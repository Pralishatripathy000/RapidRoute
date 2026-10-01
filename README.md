# RapidRoute

**A Quick-Commerce Delivery Optimization Experiment**

RapidRoute began with curiosity: Operations Research looks elegant on paper, but what happens when its models are asked to handle riders, deadlines, capacities and orders arriving mid-route?

This project is my attempt to find out—by turning textbook optimization into progressively more realistic quick-commerce experiments. The current version is a working foundation built with synthetic locations and Euclidean distances. The mathematics is real; the roads are currently suspiciously straight.

RapidRoute is under active development. The next stage will introduce real geographic coordinates, road-network travel distances and more realistic delivery conditions. It is not trying to become another delivery app—it is a laboratory for understanding what makes one work.

## Core Capabilities

- Models a depot, customer orders and delivery riders
- Solves a Capacitated Vehicle Routing Problem using Google OR-Tools
- Handles rider capacity, availability, service time and delivery deadlines
- Compares optimized routes against a greedy baseline
- Inserts new orders and reoptimizes active routes
- Reports distance, delivery time, delays and rider utilization
- Generates benchmark data and route visualizations
- Supports JSON scenarios through a command-line interface
- Includes automated tests and GitHub Actions

## Optimization Model

RapidRoute currently minimizes total route distance while respecting:

- Each order must be served exactly once
- Every route starts and ends at the depot
- Rider capacity cannot be exceeded
- Delivery deadlines must be respected
- Service time contributes to route duration
- Unavailable riders cannot be assigned orders

The current version uses Cartesian coordinates and Euclidean distance, with travel time estimated using a constant rider speed.

## Verified Sample Experiment

| Metric | Greedy Baseline | Optimized Routing |
|---|---:|---:|
| Total distance | 33.380 km | 33.284 km |
| On-time deliveries | 100% | 100% |
| Average delivery time | 15.50 min | 16.33 min |
| Average rider utilization | 66.67% | 66.67% |

**Distance saved:** 0.096 km  
**Relative improvement:** 0.29%

The small improvement is intentional evidence rather than a disappointing result: for this tiny scenario, the greedy baseline was already close to the best distance-based solution. RapidRoute does not manufacture dramatic percentages where the data does not support them.

The optimized route has a slightly higher average delivery time because the current objective minimizes total distance—not average ETA.

## Dynamic Order Experiment

When a new order `O7` is inserted:

- It is assigned to rider `R2`
- Total distance increases by `3.102 km`
- Existing orders `O4`, `O5` and `O6` are reassigned

This demonstrates complete route reoptimization after a new order arrives rather than simply attaching it to the nearest rider.

## Benchmark Results

| Orders | Riders | Baseline | Optimized | Distance Saved | Runtime |
|---:|---:|---:|---:|---:|---:|
| 10 | 2 | 48.009 km | 35.642 km | 25.76% | 2.007 s |
| 20 | 3 | 79.503 km | 48.047 km | 39.57% | 2.002 s |
| 30 | 4 | 104.095 km | 62.749 km | 39.72% | 2.002 s |

These results come from reproducible synthetic scenarios. They demonstrate optimization behaviour, not production performance claims.

## Visual Results

![Route comparison](visuals/route_comparison.png)

![Benchmark comparison](visuals/benchmark_comparison.png)

## Installation

```bash
git clone https://github.com/Pralishatripathy000/RapidRoute.git
cd RapidRoute
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

Run the sample comparison:

```bash
python main.py
```

Run a JSON scenario:

```bash
python main.py --scenario examples/sample_scenario.json
```

Run the dynamic-dispatch experiment:

```bash
python examples/dynamic_order_demo.py
```

Generate benchmarks and charts:

```bash
python examples/benchmark.py
python examples/plot_routes.py
python examples/plot_benchmark.py
```

Run all tests:

```bash
python -m unittest discover -s tests -v
```

## Project Structure

```text
RapidRoute/
├── src/
│   ├── models/
│   ├── optimizers/
│   ├── simulation/
│   ├── metrics/
│   └── utils/
├── examples/
├── tests/
├── results/
├── visuals/
├── main.py
└── requirements.txt
```

## Current Limitations

- Uses synthetic Cartesian coordinates
- Uses Euclidean rather than road-network distance
- Assumes constant rider speed
- Reoptimizes the complete scenario after a new order
- Does not yet model live traffic, batching or pickup preparation time

## Where It Goes Next

Planned experiments include:

- Real latitude and longitude coordinates
- OpenStreetMap-based road networks
- Road-distance and travel-time matrices
- Routes drawn along actual streets
- Traffic-aware travel-time estimation
- Multi-objective optimization across distance, ETA and rider balance
- Smarter partial reoptimization for live orders
- ML-assisted travel-time or demand prediction

RapidRoute is intentionally an evolving OR experiment—not a polished delivery platform. For now, it is learning to choose better routes. Real roads and real chaos come next.