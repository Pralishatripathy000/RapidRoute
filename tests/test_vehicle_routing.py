import unittest

from src.models import (
    DeliveryScenario,
    Location,
    Order,
    Rider
)

from src.optimizers.baseline import (
    greedy_dispatch
)

from src.optimizers.vehicle_routing import (
    RoutingInfeasibleError,
    optimize_routes
)


class TestVehicleRouting(unittest.TestCase):

    def setUp(self):
        self.scenario = DeliveryScenario(
            depot=Location(0, 0),
            orders=[
                Order(
                    "O1",
                    Location(1, 1),
                    1,
                    20
                ),
                Order(
                    "O2",
                    Location(2, 1),
                    1,
                    25
                ),
                Order(
                    "O3",
                    Location(8, 8),
                    1,
                    30
                ),
                Order(
                    "O4",
                    Location(9, 8),
                    1,
                    35
                )
            ],
            riders=[
                Rider("R1", 2),
                Rider("R2", 2)
            ]
        )

    def test_assigns_every_order_once(self):
        result = optimize_routes(
            self.scenario,
            time_limit_seconds=1
        )

        assigned_orders = [
            order_id
            for route in result["routes"].values()
            for order_id in route
        ]

        self.assertCountEqual(
            assigned_orders,
            ["O1", "O2", "O3", "O4"]
        )

        self.assertEqual(
            len(assigned_orders),
            len(set(assigned_orders))
        )

    def test_respects_rider_capacity(self):
        result = optimize_routes(
            self.scenario,
            time_limit_seconds=1
        )

        order_lookup = {
            order.order_id: order
            for order in self.scenario.orders
        }

        rider_lookup = {
            rider.rider_id: rider
            for rider in self.scenario.riders
        }

        for rider_id, route in result["routes"].items():
            total_demand = sum(
                order_lookup[order_id].demand
                for order_id in route
            )

            self.assertLessEqual(
                total_demand,
                rider_lookup[rider_id].capacity
            )

    def test_not_worse_than_baseline(self):
        baseline = greedy_dispatch(
            self.scenario
        )

        optimized = optimize_routes(
            self.scenario,
            time_limit_seconds=1
        )

        rounding_tolerance_km = 0.001

        self.assertLessEqual(
            optimized["total_distance_km"],
            baseline["total_distance_km"]
            + rounding_tolerance_km
        )

    def test_infeasible_capacity(self):
        scenario = DeliveryScenario(
            depot=Location(0, 0),
            orders=[
                Order(
                    "O1",
                    Location(1, 1),
                    5,
                    20
                )
            ],
            riders=[
                Rider("R1", 2)
            ]
        )

        with self.assertRaises(
            RoutingInfeasibleError
        ):
            optimize_routes(
                scenario,
                time_limit_seconds=1
            )


if __name__ == "__main__":
    unittest.main()