import unittest

from src.models import (
    DeliveryScenario,
    Location,
    Order,
    Rider
)

from src.optimizers.baseline import (
    BaselineInfeasibleError,
    greedy_dispatch
)


class TestGreedyBaseline(unittest.TestCase):

    def test_assigns_every_order(self):
        scenario = DeliveryScenario(
            depot=Location(0, 0),
            orders=[
                Order(
                    "O1",
                    Location(1, 0),
                    1,
                    10
                ),
                Order(
                    "O2",
                    Location(5, 0),
                    1,
                    20
                )
            ],
            riders=[
                Rider("R1", 1),
                Rider("R2", 1)
            ]
        )

        result = greedy_dispatch(scenario)

        assigned_orders = [
            order_id
            for route in result["routes"].values()
            for order_id in route
        ]

        self.assertCountEqual(
            assigned_orders,
            ["O1", "O2"]
        )

        self.assertEqual(
            result["routes"]["R1"],
            ["O1"]
        )

        self.assertEqual(
            result["routes"]["R2"],
            ["O2"]
        )

        self.assertEqual(
            result["total_distance_km"],
            12
        )

    def test_insufficient_capacity(self):
        scenario = DeliveryScenario(
            depot=Location(0, 0),
            orders=[
                Order(
                    "O1",
                    Location(1, 1),
                    3,
                    15
                )
            ],
            riders=[
                Rider("R1", 2)
            ]
        )

        with self.assertRaises(
            BaselineInfeasibleError
        ):
            greedy_dispatch(scenario)


if __name__ == "__main__":
    unittest.main()