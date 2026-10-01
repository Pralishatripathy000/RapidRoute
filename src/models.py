from dataclasses import dataclass, field


@dataclass(frozen=True)
class Location:
    x: float
    y: float


@dataclass(frozen=True)
class Order:
    order_id: str
    location: Location
    demand: int
    deadline_minutes: int
    service_minutes: int = 2

    def __post_init__(self):
        if not self.order_id:
            raise ValueError("Order ID cannot be empty.")

        if self.demand <= 0:
            raise ValueError("Order demand must be positive.")

        if self.deadline_minutes <= 0:
            raise ValueError("Delivery deadline must be positive.")

        if self.service_minutes < 0:
            raise ValueError("Service time cannot be negative.")


@dataclass(frozen=True)
class Rider:
    rider_id: str
    capacity: int
    available_from: int = 0

    def __post_init__(self):
        if not self.rider_id:
            raise ValueError("Rider ID cannot be empty.")

        if self.capacity <= 0:
            raise ValueError("Rider capacity must be positive.")

        if self.available_from < 0:
            raise ValueError("Availability time cannot be negative.")


@dataclass
class DeliveryScenario:
    depot: Location
    orders: list[Order] = field(default_factory=list)
    riders: list[Rider] = field(default_factory=list)
    average_speed_kmph: float = 20.0

    def __post_init__(self):
        if not self.orders:
            raise ValueError("At least one order is required.")

        if not self.riders:
            raise ValueError("At least one rider is required.")

        if self.average_speed_kmph <= 0:
            raise ValueError("Average speed must be positive.")

        order_ids = [
            order.order_id
            for order in self.orders
        ]

        rider_ids = [
            rider.rider_id
            for rider in self.riders
        ]

        if len(order_ids) != len(set(order_ids)):
            raise ValueError("Order IDs must be unique.")

        if len(rider_ids) != len(set(rider_ids)):
            raise ValueError("Rider IDs must be unique.")