import unittest

from examples.sample_scenario import (
    create_sample_scenario
)

from src.models import (
    Location,
    Order
)

from src.simulation.dynamic_dispatch import (
    DuplicateOrderError,
    insert_order_and_reoptimize
)


class TestDynamicDispatch(unittest.TestCase):

    def setUp(self):
        self.scenario = create_sample_scenario()

        self.new_order = Order(
            order_id="O7",
            location=Location(3, 2),
            demand=1,
            deadline_minutes=35
        )

    def test_inserts_new_order(self):
        result = insert_order_and_reoptimize(
            self.scenario,
            self.new_order,
            time_limit_seconds=1
        )

        updated_routes = result[
            "updated_result"
        ]["routes"]

        assigned_orders = [
            order_id
            for route in updated_routes.values()
            for order_id in route
        ]

        self.assertIn(
            self.new_order.order_id,
            assigned_orders
        )

        self.assertEqual(
            assigned_orders.count(
                self.new_order.order_id
            ),
            1
        )

    def test_preserves_original_scenario(self):
        insert_order_and_reoptimize(
            self.scenario,
            self.new_order,
            time_limit_seconds=1
        )

        original_order_ids = [
            order.order_id
            for order in self.scenario.orders
        ]

        self.assertNotIn(
            self.new_order.order_id,
            original_order_ids
        )

    def test_reports_assigned_rider(self):
        result = insert_order_and_reoptimize(
            self.scenario,
            self.new_order,
            time_limit_seconds=1
        )

        self.assertIn(
            result["new_order_rider"],
            ["R1", "R2", "R3"]
        )

    def test_rejects_duplicate_order(self):
        duplicate_order = Order(
            order_id="O1",
            location=Location(3, 2),
            demand=1,
            deadline_minutes=35
        )

        with self.assertRaises(
            DuplicateOrderError
        ):
            insert_order_and_reoptimize(
                self.scenario,
                duplicate_order,
                time_limit_seconds=1
            )


if __name__ == "__main__":
    unittest.main()