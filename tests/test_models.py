import unittest

from src.models import (
    DeliveryScenario,
    Location,
    Order,
    Rider
)


class TestModels(unittest.TestCase):

    def test_valid_scenario(self):
        scenario = DeliveryScenario(
            depot=Location(0, 0),
            orders=[
                Order(
                    order_id="O1",
                    location=Location(2, 3),
                    demand=1,
                    deadline_minutes=20
                )
            ],
            riders=[
                Rider(
                    rider_id="R1",
                    capacity=3
                )
            ]
        )

        self.assertEqual(len(scenario.orders), 1)
        self.assertEqual(len(scenario.riders), 1)

    def test_invalid_order_demand(self):
        with self.assertRaises(ValueError):
            Order(
                order_id="O1",
                location=Location(2, 3),
                demand=0,
                deadline_minutes=20
            )

    def test_duplicate_order_ids(self):
        with self.assertRaises(ValueError):
            DeliveryScenario(
                depot=Location(0, 0),
                orders=[
                    Order(
                        "O1",
                        Location(1, 2),
                        1,
                        15
                    ),
                    Order(
                        "O1",
                        Location(3, 4),
                        1,
                        20
                    )
                ],
                riders=[
                    Rider("R1", 3)
                ]
            )


if __name__ == "__main__":
    unittest.main()