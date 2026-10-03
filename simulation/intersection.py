import random
import pygame

from simulation.vehicle import Vehicle


class Intersection:

    def __init__(self, width=1000, height=700):

        self.width = width
        self.height = height

        # ==========================================
        # INTERSECTION CENTER
        # ==========================================

        self.center_x = width // 2
        self.center_y = height // 2

        # ==========================================
        # ROAD SETTINGS
        # ==========================================

        self.road_width = 220
        self.lane_offset = 45

        # Distance before intersection where
        # vehicles stop
        self.stop_distance = 125

        # ==========================================
        # TRAFFIC LIGHT
        # ==========================================

        self.traffic_light = None

        # ==========================================
        # VEHICLES
        # ==========================================

        self.vehicles = []

        self.frame_count = 0

        # ==========================================
        # VEHICLE SPAWNING
        # ==========================================

        self.spawn_interval = 70

        self.traffic_weights = {
            "south": 0.35,
            "north": 0.35,
            "east": 0.15,
            "west": 0.15
        }

        # ==========================================
        # METRICS
        # ==========================================

        self.total_vehicles_spawned = 0
        self.total_vehicles_passed = 0

        # Total waiting frames across vehicles
        self.total_waiting_time = 0

        self.maximum_queue = 0
        self.queue_measurements = 0
        self.total_queue_length = 0

    # ==========================================
    # TRAFFIC COUNTS
    # ==========================================

    def get_traffic_counts(self):

        ns_total = 0
        ew_total = 0

        for vehicle in self.vehicles:

            if vehicle.direction in ["north", "south"]:
                ns_total += 1
            else:
                ew_total += 1

        return ns_total, ew_total

    # ==========================================
    # QUEUE LENGTH
    # ==========================================

    def get_queue_length(self):

        ns_queue = 0
        ew_queue = 0

        for vehicle in self.vehicles:

            if vehicle.waiting_time > 0:

                if vehicle.direction in ["north", "south"]:
                    ns_queue += 1
                else:
                    ew_queue += 1

        return ns_queue, ew_queue

    # ==========================================
    # SPAWN VEHICLE
    # ==========================================

    def spawn_vehicle(self):

        direction = random.choices(
            list(self.traffic_weights.keys()),
            weights=list(self.traffic_weights.values())
        )[0]

        if direction == "south":

            x = self.center_x - self.lane_offset - 9
            y = -50

        elif direction == "north":

            x = self.center_x + self.lane_offset - 9
            y = self.height + 50

        elif direction == "east":

            x = -50
            y = self.center_y + self.lane_offset - 9

        else:

            x = self.width + 50
            y = self.center_y - self.lane_offset - 9

        vehicle = Vehicle(
            x=x,
            y=y,
            direction=direction,
            speed=2.5
        )

        self.vehicles.append(vehicle)

        self.total_vehicles_spawned += 1

    # ==========================================
    # CHECK STOP LINE
    # ==========================================

    def has_reached_stop_line(self, vehicle):

        front = vehicle.get_front_position()

        if vehicle.direction == "south":

            stop_line = self.center_y - self.stop_distance

            return front >= stop_line

        elif vehicle.direction == "north":

            stop_line = self.center_y + self.stop_distance

            return front <= stop_line

        elif vehicle.direction == "east":

            stop_line = self.center_x - self.stop_distance

            return front >= stop_line

        elif vehicle.direction == "west":

            stop_line = self.center_x + self.stop_distance

            return front <= stop_line

        return False

    # ==========================================
    # FIND VEHICLE AHEAD
    # ==========================================

    def get_vehicle_ahead(self, vehicle):

        closest_vehicle = None
        closest_distance = float("inf")

        for other in self.vehicles:

            if other is vehicle:
                continue

            if other.direction != vehicle.direction:
                continue

            if vehicle.direction == "south":

                distance = other.y - vehicle.y

                if distance > 0 and distance < closest_distance:

                    closest_distance = distance
                    closest_vehicle = other

            elif vehicle.direction == "north":

                distance = vehicle.y - other.y

                if distance > 0 and distance < closest_distance:

                    closest_distance = distance
                    closest_vehicle = other

            elif vehicle.direction == "east":

                distance = other.x - vehicle.x

                if distance > 0 and distance < closest_distance:

                    closest_distance = distance
                    closest_vehicle = other

            elif vehicle.direction == "west":

                distance = vehicle.x - other.x

                if distance > 0 and distance < closest_distance:

                    closest_distance = distance
                    closest_vehicle = other

        return closest_vehicle

    # ==========================================
    # CHECK VEHICLE AHEAD
    # ==========================================

    def should_stop_for_vehicle(self, vehicle):

        vehicle_ahead = self.get_vehicle_ahead(vehicle)

        if vehicle_ahead is None:
            return False

        safe_distance = 12

        if vehicle.direction == "south":

            distance = (
                vehicle_ahead.y
                - vehicle.get_front_position()
            )

        elif vehicle.direction == "north":

            distance = (
                vehicle.get_front_position()
                - (vehicle_ahead.y + vehicle_ahead.height)
            )

        elif vehicle.direction == "east":

            distance = (
                vehicle_ahead.x
                - vehicle.get_front_position()
            )

        else:

            distance = (
                vehicle.get_front_position()
                - (vehicle_ahead.x + vehicle_ahead.width)
            )

        return distance <= safe_distance

    # ==========================================
    # CHECK TRAFFIC SIGNAL
    # ==========================================

    def should_stop_at_signal(self, vehicle):

        if vehicle.passed_stop_line:
            return False

        if self.traffic_light is None:
            return False

        current_front = vehicle.get_front_position()

        if vehicle.direction == "south":

            next_front = current_front + vehicle.speed

            stop_line = self.center_y - self.stop_distance

            would_cross = next_front >= stop_line

        elif vehicle.direction == "north":

            next_front = current_front - vehicle.speed

            stop_line = self.center_y + self.stop_distance

            would_cross = next_front <= stop_line

        elif vehicle.direction == "east":

            next_front = current_front + vehicle.speed

            stop_line = self.center_x - self.stop_distance

            would_cross = next_front >= stop_line

        elif vehicle.direction == "west":

            next_front = current_front - vehicle.speed

            stop_line = self.center_x + self.stop_distance

            would_cross = next_front <= stop_line

        else:

            return False

        if would_cross:

            return not self.traffic_light.is_green(
                vehicle.direction
            )

        return False

    # ==========================================
    # UPDATE ONE VEHICLE
    # ==========================================

    def update_vehicle(self, vehicle):

        # ------------------------------------------
        # VEHICLE ALREADY PASSED STOP LINE
        # ------------------------------------------

        if vehicle.passed_stop_line:

            if self.should_stop_for_vehicle(vehicle):

                vehicle.waiting_time += 1

                return

            vehicle.waiting_time = 0

            vehicle.move()

            return

        # ------------------------------------------
        # TRAFFIC SIGNAL
        # ------------------------------------------

        if self.should_stop_at_signal(vehicle):

            vehicle.waiting_time += 1

            return

        # ------------------------------------------
        # VEHICLE AHEAD
        # ------------------------------------------

        if self.should_stop_for_vehicle(vehicle):

            vehicle.waiting_time += 1

            return

        # ------------------------------------------
        # VEHICLE CAN MOVE
        # ------------------------------------------

        vehicle.waiting_time = 0

        vehicle.move()

        # ------------------------------------------
        # CHECK STOP LINE
        # ------------------------------------------

        if self.has_reached_stop_line(vehicle):

            vehicle.passed_stop_line = True
            vehicle.entered_intersection = True

    # ==========================================
    # UPDATE METRICS
    # ==========================================

    def update_metrics(self):

        ns_queue, ew_queue = self.get_queue_length()

        current_queue = ns_queue + ew_queue

        # ------------------------------------------
        # QUEUE METRICS
        # ------------------------------------------

        self.total_queue_length += current_queue

        self.queue_measurements += 1

        if current_queue > self.maximum_queue:

            self.maximum_queue = current_queue

        # ------------------------------------------
        # WAITING TIME METRIC
        # ------------------------------------------
        #
        # IMPORTANT:
        #
        # Count ONE waiting frame for each vehicle
        # that is currently waiting.
        #
        # Do NOT add vehicle.waiting_time here.
        #
        # Example:
        #
        # Vehicle waits for 10 frames
        #
        # Correct total = 10
        #
        # Old incorrect calculation:
        #
        # 1 + 2 + 3 + ... + 10 = 55
        #
        # ------------------------------------------

        for vehicle in self.vehicles:

            if vehicle.waiting_time > 0:

                self.total_waiting_time += 1

    # ==========================================
    # UPDATE SIMULATION
    # ==========================================

    def update(self):

        self.frame_count += 1

        # ------------------------------------------
        # SPAWN VEHICLE
        # ------------------------------------------

        if self.frame_count % self.spawn_interval == 0:

            self.spawn_vehicle()

        # ------------------------------------------
        # UPDATE VEHICLES
        # ------------------------------------------

        for vehicle in self.vehicles:

            self.update_vehicle(vehicle)

        # ------------------------------------------
        # UPDATE METRICS
        # ------------------------------------------

        self.update_metrics()

        # ------------------------------------------
        # REMOVE VEHICLES OUTSIDE SCREEN
        # ------------------------------------------

        remaining_vehicles = []

        for vehicle in self.vehicles:

            outside_screen = (

                vehicle.x < -100

                or vehicle.x > self.width + 100

                or vehicle.y < -100

                or vehicle.y > self.height + 100

            )

            if outside_screen:

                self.total_vehicles_passed += 1

                continue

            remaining_vehicles.append(vehicle)

        self.vehicles = remaining_vehicles

    # ==========================================
    # GET METRICS
    # ==========================================

    def get_metrics(self):

        # ------------------------------------------
        # AVERAGE WAITING TIME
        # ------------------------------------------

        if self.total_vehicles_spawned > 0:

            average_waiting_frames = (
                self.total_waiting_time
                / self.total_vehicles_spawned
            )

            average_waiting_time = (
                average_waiting_frames / 60
            )

        else:

            average_waiting_time = 0

        # ------------------------------------------
        # AVERAGE QUEUE
        # ------------------------------------------

        if self.queue_measurements > 0:

            average_queue = (
                self.total_queue_length
                / self.queue_measurements
            )

        else:

            average_queue = 0

        # ------------------------------------------
        # RETURN METRICS
        # ------------------------------------------

        return {

            "vehicles_spawned":
                self.total_vehicles_spawned,

            "vehicles_passed":
                self.total_vehicles_passed,

            "average_waiting_time":
                average_waiting_time,

            "average_queue":
                average_queue,

            "maximum_queue":
                self.maximum_queue
        }

    # ==========================================
    # DRAW ROADS
    # ==========================================

    def draw_roads(self, screen):

        screen.fill((40, 140, 70))

        # ------------------------------------------
        # HORIZONTAL ROAD
        # ------------------------------------------

        pygame.draw.rect(
            screen,
            (60, 60, 60),
            (
                0,
                self.center_y - self.road_width // 2,
                self.width,
                self.road_width
            )
        )

        # ------------------------------------------
        # VERTICAL ROAD
        # ------------------------------------------

        pygame.draw.rect(
            screen,
            (60, 60, 60),
            (
                self.center_x - self.road_width // 2,
                0,
                self.road_width,
                self.height
            )
        )

        # ------------------------------------------
        # ROAD LINES
        # ------------------------------------------

        pygame.draw.line(
            screen,
            (220, 220, 220),
            (0, self.center_y),
            (
                self.center_x
                - self.road_width // 2,
                self.center_y
            ),
            2
        )

        pygame.draw.line(
            screen,
            (220, 220, 220),
            (
                self.center_x
                + self.road_width // 2,
                self.center_y
            ),
            (self.width, self.center_y),
            2
        )

        pygame.draw.line(
            screen,
            (220, 220, 220),
            (self.center_x, 0),
            (
                self.center_x,
                self.center_y
                - self.road_width // 2
            ),
            2
        )

        pygame.draw.line(
            screen,
            (220, 220, 220),
            (
                self.center_x,
                self.center_y
                + self.road_width // 2
            ),
            (self.center_x, self.height),
            2
        )

        # ------------------------------------------
        # STOP LINES
        # ------------------------------------------

        # South

        pygame.draw.line(
            screen,
            (255, 255, 255),
            (
                self.center_x + 5,
                self.center_y - self.stop_distance
            ),
            (
                self.center_x
                + self.road_width // 2 - 5,
                self.center_y - self.stop_distance
            ),
            5
        )

        # North

        pygame.draw.line(
            screen,
            (255, 255, 255),
            (
                self.center_x
                - self.road_width // 2 + 5,
                self.center_y + self.stop_distance
            ),
            (
                self.center_x - 5,
                self.center_y + self.stop_distance
            ),
            5
        )

        # East

        pygame.draw.line(
            screen,
            (255, 255, 255),
            (
                self.center_x - self.stop_distance,
                self.center_y + 5
            ),
            (
                self.center_x - self.stop_distance,
                self.center_y
                + self.road_width // 2 - 5
            ),
            5
        )

        # West

        pygame.draw.line(
            screen,
            (255, 255, 255),
            (
                self.center_x + self.stop_distance,
                self.center_y
                - self.road_width // 2 + 5
            ),
            (
                self.center_x + self.stop_distance,
                self.center_y - 5
            ),
            5
        )

    # ==========================================
    # DRAW EVERYTHING
    # ==========================================

    def draw(self, screen):

        self.draw_roads(screen)

        # ------------------------------------------
        # TRAFFIC LIGHT
        # ------------------------------------------

        if self.traffic_light is not None:

            self.traffic_light.draw(
                screen,
                self.center_x,
                self.center_y
            )

        # ------------------------------------------
        # VEHICLES
        # ------------------------------------------

        for vehicle in self.vehicles:

            vehicle.draw(screen)