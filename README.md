# RapidRoute

Quick commerce promises delivery in minutes. The routes, unfortunately, do not optimize themselves.

RapidRoute is an Operations Research experiment focused on assigning orders to riders, batching compatible deliveries and finding efficient routes from a single dark store.

## Problem

A quick-commerce system must decide:

- Which rider should handle each order?
- Which orders can be delivered together?
- In what sequence should deliveries occur?
- Can capacity and delivery deadlines be satisfied?

## Planned Scope

- Single dark store
- Multiple riders and customer orders
- Rider capacity constraints
- Delivery deadlines
- Order-to-rider assignment
- Order batching
- Vehicle route optimization
- Dynamic insertion of new orders
- Comparison with a simple delivery baseline

## Evaluation Metrics

- Total delivery distance
- Average delivery time
- Delayed orders
- Rider utilization
- Optimization runtime

## Technology

- Python
- Google OR-Tools
- NumPy
- pandas
- Matplotlib

## Project Structure

```text
src/optimizers/   Assignment and routing algorithms
src/simulation/   Orders, riders and delivery simulation
src/utils/        Shared utilities
data/             Input and generated datasets
examples/         Example scenarios
tests/            Automated tests
results/          Experiment results
visuals/          Route visualizations
```

## Status

Currently under development—one route, constraint and questionable delivery deadline at a time.