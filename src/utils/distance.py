from math import ceil, hypot

from src.models import DeliveryScenario, Location


def euclidean_distance_km(
    first: Location,
    second: Location
):
    return hypot(
        second.x - first.x,
        second.y - first.y
    )


def distance_to_meters(distance_km):
    return int(round(distance_km * 1000))


def travel_time_minutes(
    distance_km,
    speed_kmph
):
    if speed_kmph <= 0:
        raise ValueError("Speed must be positive.")

    if distance_km == 0:
        return 0

    return ceil(
        (distance_km / speed_kmph) * 60
    )


def get_scenario_locations(
    scenario: DeliveryScenario
):
    return [
        scenario.depot,
        *[
            order.location
            for order in scenario.orders
        ]
    ]


def build_distance_matrix(
    scenario: DeliveryScenario
):
    locations = get_scenario_locations(scenario)

    return [
        [
            distance_to_meters(
                euclidean_distance_km(
                    origin,
                    destination
                )
            )
            for destination in locations
        ]
        for origin in locations
    ]


def build_time_matrix(
    scenario: DeliveryScenario
):
    locations = get_scenario_locations(scenario)

    return [
        [
            travel_time_minutes(
                euclidean_distance_km(
                    origin,
                    destination
                ),
                scenario.average_speed_kmph
            )
            for destination in locations
        ]
        for origin in locations
    ]