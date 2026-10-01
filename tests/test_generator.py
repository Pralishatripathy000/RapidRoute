import unittest

from src.simulation.generator import (
    generate_scenario
)


class TestScenarioGenerator(unittest.TestCase):

    def test_generates_requested_size(self):
        scenario = generate_scenario(
            order_count=10,
            rider_count=3,
            seed=42
        )

        self.assertEqual(
            len(scenario.orders),
            10
        )

        self.assertEqual(
            len(scenario.riders),
            3
        )

    def test_is_reproducible(self):
        first = generate_scenario(
            order_count=5,
            rider_count=2,
            seed=42
        )

        second = generate_scenario(
            order_count=5,
            rider_count=2,
            seed=42
        )

        first_locations = [
            order.location
            for order in first.orders
        ]

        second_locations = [
            order.location
            for order in second.orders
        ]

        self.assertEqual(
            first_locations,
            second_locations
        )


if __name__ == "__main__":
    unittest.main()