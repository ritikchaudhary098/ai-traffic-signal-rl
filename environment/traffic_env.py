import gymnasium as gym
from gymnasium import spaces
import numpy as np

from simulation.intersection import Intersection
from simulation.traffic_light import TrafficLight


class TrafficEnv(gym.Env):

    def __init__(self):

        super().__init__()

        # ==========================================
        # SIMULATION
        # ==========================================

        self.intersection = Intersection(
            width=1000,
            height=700
        )

        self.traffic_light = TrafficLight()

        self.intersection.traffic_light = (
            self.traffic_light
        )

        # ==========================================
        # ACTION SPACE
        # ==========================================

        # 0 = Keep current signal
        # 1 = Switch signal

        self.action_space = spaces.Discrete(2)

        # ==========================================
        # OBSERVATION SPACE
        # ==========================================

        # 12 values:
        #
        # 0  = North traffic
        # 1  = South traffic
        # 2  = East traffic
        # 3  = West traffic
        #
        # 4  = North waiting
        # 5  = South waiting
        # 6  = East waiting
        # 7  = West waiting
        #
        # 8  = Current phase
        # 9  = Signal state
        # 10 = Normalized timer
        # 11 = Switch allowed

        self.observation_space = spaces.Box(
            low=0,
            high=1,
            shape=(12,),
            dtype=np.float32
        )

        # ==========================================
        # RL SETTINGS
        # ==========================================

        # One RL decision = 60 simulation frames
        self.decision_interval = 60

        # Maximum number of RL decisions
        self.max_steps = 1000

        self.current_step = 0

    # ==========================================
    # RESET
    # ==========================================

    def reset(
        self,
        seed=None,
        options=None
    ):

        super().reset(seed=seed)

        # Reset simulation
        self.intersection = Intersection(
            width=1000,
            height=700
        )

        self.traffic_light = TrafficLight()

        self.intersection.traffic_light = (
            self.traffic_light
        )

        self.current_step = 0

        observation = self.get_observation()

        return observation, {}

    # ==========================================
    # OBSERVATION
    # ==========================================

    def get_observation(self):

        vehicles = self.intersection.vehicles

        # ------------------------------------------
        # TRAFFIC COUNTS
        # ------------------------------------------

        north_count = 0
        south_count = 0
        east_count = 0
        west_count = 0

        # ------------------------------------------
        # WAITING COUNTS
        # ------------------------------------------

        north_waiting = 0
        south_waiting = 0
        east_waiting = 0
        west_waiting = 0

        for vehicle in vehicles:

            if vehicle.direction == "north":

                north_count += 1

                if vehicle.waiting_time > 0:
                    north_waiting += 1

            elif vehicle.direction == "south":

                south_count += 1

                if vehicle.waiting_time > 0:
                    south_waiting += 1

            elif vehicle.direction == "east":

                east_count += 1

                if vehicle.waiting_time > 0:
                    east_waiting += 1

            elif vehicle.direction == "west":

                west_count += 1

                if vehicle.waiting_time > 0:
                    west_waiting += 1

        # ==========================================
        # NORMALIZE TRAFFIC COUNTS
        # ==========================================

        # The observation space expects values between
        # 0 and 1.

        north_count = min(north_count / 20, 1.0)
        south_count = min(south_count / 20, 1.0)
        east_count = min(east_count / 20, 1.0)
        west_count = min(west_count / 20, 1.0)

        north_waiting = min(north_waiting / 20, 1.0)
        south_waiting = min(south_waiting / 20, 1.0)
        east_waiting = min(east_waiting / 20, 1.0)
        west_waiting = min(west_waiting / 20, 1.0)

        # ==========================================
        # CURRENT PHASE
        # ==========================================

        # NS = 0
        # EW = 1

        if self.traffic_light.phase == "NS":
            phase = 0.0
        else:
            phase = 1.0

        # ==========================================
        # SIGNAL STATE
        # ==========================================

        # GREEN = 0
        # YELLOW = 0.5
        # ALL_RED = 1

        if self.traffic_light.state == "GREEN":

            signal_state = 0.0

        elif self.traffic_light.state == "YELLOW":

            signal_state = 0.5

        else:

            signal_state = 1.0

        # ==========================================
        # TIMER
        # ==========================================

        max_timer = max(
            self.traffic_light.max_green,
            self.traffic_light.yellow_duration,
            self.traffic_light.all_red_duration
        )

        normalized_timer = (
            self.traffic_light.timer
            / max_timer
        )

        normalized_timer = min(
            normalized_timer,
            1.0
        )

        # ==========================================
        # SWITCH ALLOWED
        # ==========================================

        switch_allowed = (
            self.traffic_light.state == "GREEN"
            and
            self.traffic_light.timer
            >= self.traffic_light.min_green
        )

        if switch_allowed:
            switch_allowed_value = 1.0
        else:
            switch_allowed_value = 0.0

        # ==========================================
        # FINAL OBSERVATION
        # ==========================================

        observation = np.array(
            [
                north_count,
                south_count,
                east_count,
                west_count,

                north_waiting,
                south_waiting,
                east_waiting,
                west_waiting,

                phase,
                signal_state,
                normalized_timer,

                switch_allowed_value
            ],
            dtype=np.float32
        )

        return observation

    # ==========================================
    # STEP
    # ==========================================

    def step(self, action):

        self.current_step += 1

        action = int(action)

        # ==========================================
        # OLD STATE
        # ==========================================

        old_ns_queue, old_ew_queue = (
            self.intersection.get_queue_length()
        )

        old_total_queue = (
            old_ns_queue +
            old_ew_queue
        )

        old_phase = self.traffic_light.phase

        # ==========================================
        # CHECK WHETHER SWITCH IS ALLOWED
        # ==========================================

        switch_allowed = (
            self.traffic_light.state == "GREEN"
            and
            self.traffic_light.timer
            >= self.traffic_light.min_green
        )

        switch_requested = False
        invalid_switch = False

        # ==========================================
        # ACTION
        # ==========================================

        if action == 1:

            if switch_allowed:

                switched = (
                    self.traffic_light.request_switch()
                )

                if switched:

                    switch_requested = True

            else:

                invalid_switch = True

        # ==========================================
        # RUN SIMULATION
        # ==========================================

        for _ in range(
            self.decision_interval
        ):

            self.traffic_light.update()

            self.intersection.update()

        # ==========================================
        # NEW QUEUE
        # ==========================================

        new_ns_queue, new_ew_queue = (
            self.intersection.get_queue_length()
        )

        new_total_queue = (
            new_ns_queue +
            new_ew_queue
        )

        # ==========================================
        # WAITING VEHICLES
        # ==========================================

        total_waiting = (
            new_total_queue
        )

        # ==========================================
        # QUEUE CHANGE
        # ==========================================

        queue_change = (
            old_total_queue -
            new_total_queue
        )

        # ==========================================
        # NEWLY PASSED VEHICLES
        # ==========================================

        current_passed = (
            self.intersection.total_vehicles_passed
        )

        # ==========================================
        # REWARD
        # ==========================================

        total_reward = 0.0

        # ------------------------------------------
        # 1. QUEUE PENALTY
        # ------------------------------------------

        total_reward -= (
            0.20 *
            new_total_queue
        )

        # ------------------------------------------
        # 2. QUEUE IMPROVEMENT
        # ------------------------------------------

        total_reward += (
            0.50 *
            queue_change
        )

        # ------------------------------------------
        # 3. VEHICLE FLOW
        # ------------------------------------------

        # Reward vehicles that leave the simulation.

        newly_passed_frame = (
            current_passed
            -
            getattr(
                self,
                "_previous_passed",
                0
            )
        )

        total_reward += (
            2.0 *
            newly_passed_frame
        )

        self._previous_passed = (
            current_passed
        )

        # ==========================================
        # 4. SWITCH REWARD
        # ==========================================

        if switch_requested:

            # Switching has a meaningful cost.
            total_reward -= 5.0

            # Reward switching when the opposite
            # direction actually has traffic.

            if old_phase == "NS":

                opposite_queue = (
                    old_ew_queue
                )

            else:

                opposite_queue = (
                    old_ns_queue
                )

            total_reward += (
                1.5 *
                opposite_queue
            )

        # ==========================================
        # 5. INVALID SWITCH PENALTY
        # ==========================================

        if invalid_switch:

            # Small penalty because the action had
            # no effect.

            total_reward -= 0.1

        # ==========================================
        # TERMINATION
        # ==========================================

        terminated = (
            self.current_step
            >= self.max_steps
        )

        truncated = False

        # ==========================================
        # OBSERVATION
        # ==========================================

        observation = (
            self.get_observation()
        )

        # ==========================================
        # INFO
        # ==========================================

        info = {

            "ns_queue":
                new_ns_queue,

            "ew_queue":
                new_ew_queue,

            "total_waiting":
                total_waiting,

            "vehicles_passed":
                current_passed,

            "vehicles_spawned":
                self.intersection.total_vehicles_spawned,

            "newly_passed":
                newly_passed_frame,

            "switch_requested":
                switch_requested,

            "switch_allowed":
                switch_allowed,

            "invalid_switch":
                invalid_switch,

            "action":
                action,

            "reward":
                total_reward
        }

        return (
            observation,
            total_reward,
            terminated,
            truncated,
            info
        )