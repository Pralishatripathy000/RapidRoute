from src.models import (
    DeliveryScenario,
    Location,
    Order,
    Rider
)


def create_sample_scenario():
    return DeliveryScenario(
        depot=Location(0, 0),
        orders=[
            Order(
                "O1",
                Location(1, 2),
                1,
                15
            ),
            Order(
                "O2",
                Location(2, 1),
                1,
                18
            ),
            Order(
                "O3",
                Location(4, 3),
                1,
                25
            ),
            Order(
                "O4",
                Location(5, 2),
                1,
                28
            ),
            Order(
                "O5",
                Location(7, 6),
                1,
                40
            ),
            Order(
                "O6",
                Location(8, 7),
                1,
                45
            )
        ],
        riders=[
            Rider("R1", 2),
            Rider("R2", 2),
            Rider("R3", 2)
        ],
        average_speed_kmph=30
    )