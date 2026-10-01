import json
from pathlib import Path

from src.models import (
    DeliveryScenario,
    Location,
    Order,
    Rider
)


def load_scenario(path):
    file_path = Path(path)

    with file_path.open(
        "r",
        encoding="utf-8"
    ) as file:
        data = json.load(file)

    depot = Location(
        x=data["depot"]["x"],
        y=data["depot"]["y"]
    )

    orders = [
        Order(
            order_id=order["order_id"],
            location=Location(
                x=order["x"],
                y=order["y"]
            ),
            demand=order["demand"],
            deadline_minutes=(
                order["deadline_minutes"]
            ),
            service_minutes=order.get(
                "service_minutes",
                2
            )
        )
        for order in data["orders"]
    ]

    riders = [
        Rider(
            rider_id=rider["rider_id"],
            capacity=rider["capacity"],
            available_from=rider.get(
                "available_from",
                0
            )
        )
        for rider in data["riders"]
    ]

    return DeliveryScenario(
        depot=depot,
        orders=orders,
        riders=riders,
        average_speed_kmph=data.get(
            "average_speed_kmph",
            20
        )
    )