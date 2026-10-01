import unittest

from src.models import (
    DeliveryScenario,
    Location,
    Order,
    Rider
)

from src.utils.distance import (
    build_distance_matrix,
    build_time_matrix,
    euclidean_distance_km,
    travel_time_minutes
)


class TestDistanceUtilities(unittest.TestCase):

    def setUp(self):
        self.scenario = DeliveryScenario(
            depot=Location(0, 0),
            orders=[
                Order(
                    "O1",
                    Location(3, 4),
                    1,
                    30
                ),
                Order(
                    "O2",
                    Location(0, 4),
                    1,
                    30
                )
            ],
            riders=[
                Rider("R1", 3)
            ],
            average_speed_kmph=20
        )

    def test_euclidean_distance(self):
        distance = euclidean_distance_km(
            Location(0, 0),
            Location(3, 4)
        )

        self.assertEqual(distance, 5)

    def test_travel_time(self):
        self.assertEqual(
            travel_time_minutes(5, 20),
            15
        )

    def test_distance_matrix(self):
        matrix = build_distance_matrix(
            self.scenario
        )

        self.assertEqual(matrix[0][1], 5000)
        self.assertEqual(matrix[1][0], 5000)
        self.assertEqual(matrix[0][0], 0)

    def test_time_matrix(self):
        matrix = build_time_matrix(
            self.scenario
        )

        self.assertEqual(matrix[0][1], 15)
        self.assertEqual(matrix[0][2], 12)
        self.assertEqual(matrix[1][1], 0)


if __name__ == "__main__":
    unittest.main()