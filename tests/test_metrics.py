import unittest

from src.models import (
    DeliveryScenario,
    Location,
    Order,
    Rider
)

from src.utils.metrics import (
    evaluate_routes
)


class TestRouteMetrics(unittest.TestCase):

    def test_detects_late_order(self):
        scenario = DeliveryScenario(
            depot=Location(0, 0),
            orders=[
                Order(
                    "O1",
                    Location(3, 4),
                    1,
                    14
                )
            ],
            riders=[
                Rider("R1", 2)
            ],
            average_speed_kmph=20
        )

        result = {
            "routes": {
                "R1": ["O1"]
            }
        }

        metrics = evaluate_routes(
            scenario,
            result
        )

        self.assertEqual(
            metrics["late_orders"],
            ["O1"]
        )

        self.assertEqual(
            metrics[
                "average_delivery_time_minutes"
            ],
            15
        )

        self.assertEqual(
            metrics[
                "average_rider_utilization_percentage"
            ],
            50
        )

    def test_detects_on_time_order(self):
        scenario = DeliveryScenario(
            depot=Location(0, 0),
            orders=[
                Order(
                    "O1",
                    Location(3, 4),
                    1,
                    20
                )
            ],
            riders=[
                Rider("R1", 2)
            ],
            average_speed_kmph=20
        )

        result = {
            "routes": {
                "R1": ["O1"]
            }
        }

        metrics = evaluate_routes(
            scenario,
            result
        )

        self.assertEqual(
            metrics["late_orders"],
            []
        )

        self.assertEqual(
            metrics["on_time_percentage"],
            100
        )


if __name__ == "__main__":
    unittest.main()