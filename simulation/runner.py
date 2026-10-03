import random

from simulation.intersection import Intersection
from simulation.traffic_light import TrafficLight


class SimulationRunner:

    def __init__(self, seed=None):

        self.width = 1000
        self.height = 700

        self.seed = seed

        self.reset()

    # ==========================================
    # RESET
    # ==========================================

    def reset(self):

        # Same seed = same traffic pattern
        if self.seed is not None:
            random.seed(self.seed)

        self.intersection = Intersection(
            width=self.width,
            height=self.height
        )

        self.traffic_light = TrafficLight()

        self.intersection.traffic_light = (
            self.traffic_light
        )

    # ==========================================
    # STEP
    # ==========================================

    def step(self, action=0):

        if action == 1:
            self.traffic_light.request_switch()

        self.traffic_light.update()

        self.intersection.update()

    # ==========================================
    # QUEUES
    # ==========================================

    def get_queues(self):

        ns_queue, ew_queue = (
            self.intersection.get_queue_length()
        )

        return ns_queue, ew_queue

    # ==========================================
    # METRICS
    # ==========================================

    def get_metrics(self):

        return self.intersection.get_metrics()

    # ==========================================
    # TRAFFIC COUNTS
    # ==========================================

    def get_traffic_counts(self):

        return self.intersection.get_traffic_counts()

    # ==========================================
    # OBSERVATION
    # ==========================================

    def get_observation(self):

        north = 0
        south = 0
        east = 0
        west = 0

        north_waiting = 0
        south_waiting = 0
        east_waiting = 0
        west_waiting = 0

        for vehicle in self.intersection.vehicles:

            if vehicle.direction == "north":

                north += 1

                if vehicle.waiting_time > 0:
                    north_waiting += 1

            elif vehicle.direction == "south":

                south += 1

                if vehicle.waiting_time > 0:
                    south_waiting += 1

            elif vehicle.direction == "east":

                east += 1

                if vehicle.waiting_time > 0:
                    east_waiting += 1

            elif vehicle.direction == "west":

                west += 1

                if vehicle.waiting_time > 0:
                    west_waiting += 1

        # Signal phase

        if self.traffic_light.phase == "NS":
            phase = 0
        else:
            phase = 1

        # Signal state

        if self.traffic_light.state == "GREEN":

            signal_state = 0

        elif self.traffic_light.state == "YELLOW":

            signal_state = 1

        else:

            signal_state = 2

        observation = [

            north,
            south,
            east,
            west,

            north_waiting,
            south_waiting,
            east_waiting,
            west_waiting,

            phase,
            signal_state,

            self.traffic_light.timer
        ]

        return observation