import unittest

from src.utils.io import load_scenario


class TestScenarioLoader(unittest.TestCase):

    def test_loads_sample_scenario(self):
        scenario = load_scenario(
            "data/sample_scenario.json"
        )

        self.assertEqual(
            len(scenario.orders),
            6
        )

        self.assertEqual(
            len(scenario.riders),
            3
        )

        self.assertEqual(
            scenario.average_speed_kmph,
            30
        )

        self.assertEqual(
            scenario.orders[0].order_id,
            "O1"
        )


if __name__ == "__main__":
    unittest.main()