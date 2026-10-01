from math import ceil
from random import Random

from src.models import (
    DeliveryScenario,
    Location,
    Order,
    Rider
)


def generate_scenario(
    order_count,
    rider_count,
    seed=42,
    area_size_km=8
):
    if order_count <= 0:
        raise ValueError(
            "Order count must be positive."
        )

    if rider_count <= 0:
        raise ValueError(
            "Rider count must be positive."
        )

    random = Random(seed)

    orders = [
        Order(
            order_id=f"O{index + 1}",
            location=Location(
                round(
                    random.uniform(
                        0.5,
                        area_size_km
                    ),
                    2
                ),
                round(
                    random.uniform(
                        0.5,
                        area_size_km
                    ),
                    2
                )
            ),
            demand=1,
            deadline_minutes=120,
            service_minutes=2
        )
        for index in range(order_count)
    ]

    rider_capacity = (
        ceil(order_count / rider_count) + 2
    )

    riders = [
        Rider(
            rider_id=f"R{index + 1}",
            capacity=rider_capacity
        )
        for index in range(rider_count)
    ]

    return DeliveryScenario(
        depot=Location(0, 0),
        orders=orders,
        riders=riders,
        average_speed_kmph=25
    )