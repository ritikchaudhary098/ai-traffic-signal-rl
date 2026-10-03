import pygame


class TrafficLight:

    def __init__(self):

        # ====================================
        # CURRENT PHASE
        # ====================================

        # NS = North/South
        # EW = East/West

        self.phase = "NS"

        # ====================================
        # CURRENT SIGNAL STATE
        # ====================================

        # GREEN
        # YELLOW
        # ALL_RED

        self.state = "GREEN"

        # ====================================
        # TIMER
        # ====================================

        self.timer = 0

        # ====================================
        # SIGNAL TIMINGS
        # ====================================

        # Minimum green time:
        # 5 seconds × 60 FPS = 300 frames

        self.min_green = 5 * 60

        # Maximum green time:
        # 25 seconds × 60 FPS = 1500 frames

        self.max_green = 25 * 60

        # Yellow:
        # 3 seconds × 60 FPS = 180 frames

        self.yellow_duration = 3 * 60

        # All-red:
        # 1 second × 60 FPS = 60 frames

        self.all_red_duration = 1 * 60

        # ====================================
        # QUEUE INFORMATION
        # ====================================

        self.ns_queue = 0
        self.ew_queue = 0

    # ====================================
    # REQUEST SWITCH
    # ====================================

    def request_switch(self):

        # We can only request a switch
        # while the current signal is GREEN.

        if self.state != "GREEN":
            return False

        # Don't allow switching before
        # minimum green time has passed.

        if self.timer < self.min_green:
            return False

        # Start yellow phase.

        self.state = "YELLOW"

        self.timer = 0

        return True

    # ====================================
    # UPDATE SIGNAL
    # ====================================

    def update(self):

        self.timer += 1

        # ====================================
        # GREEN
        # ====================================

        if self.state == "GREEN":

            # Automatically switch if maximum
            # green time is reached.

            if self.timer >= self.max_green:

                self.state = "YELLOW"

                self.timer = 0

            return

        # ====================================
        # YELLOW
        # ====================================

        elif self.state == "YELLOW":

            # Wait until yellow duration finishes.

            if self.timer >= self.yellow_duration:

                self.state = "ALL_RED"

                self.timer = 0

            return

        # ====================================
        # ALL RED
        # ====================================

        elif self.state == "ALL_RED":

            # Wait until all-red duration finishes.

            if self.timer >= self.all_red_duration:

                # Switch traffic direction.

                if self.phase == "NS":

                    self.phase = "EW"

                else:

                    self.phase = "NS"

                # New phase starts with GREEN.

                self.state = "GREEN"

                self.timer = 0

            return

    # ====================================
    # CHECK GREEN
    # ====================================

    def is_green(self, direction):

        # During yellow or all-red,
        # nobody has a green signal.

        if self.state != "GREEN":
            return False

        # North/South phase.

        if self.phase == "NS":

            return direction in [
                "north",
                "south"
            ]

        # East/West phase.

        return direction in [
            "east",
            "west"
        ]

    # ====================================
    # REMAINING TIME
    # ====================================

    def get_remaining_time(self):

        if self.state == "GREEN":

            remaining = (
                self.max_green -
                self.timer
            )

        elif self.state == "YELLOW":

            remaining = (
                self.yellow_duration -
                self.timer
            )

        else:

            remaining = (
                self.all_red_duration -
                self.timer
            )

        return max(0, remaining)

    # ====================================
    # DRAW TRAFFIC LIGHTS
    # ====================================

    def draw(
        self,
        screen,
        center_x,
        center_y
    ):

        # North/South traffic lights

        self.draw_signal(
            screen,
            center_x - 25,
            55,
            self.phase == "NS"
        )

        self.draw_signal(
            screen,
            center_x + 45,
            545,
            self.phase == "NS"
        )

        # East/West traffic lights

        self.draw_signal(
            screen,
            55,
            center_y - 45,
            self.phase == "EW"
        )

        self.draw_signal(
            screen,
            895,
            center_y + 15,
            self.phase == "EW"
        )

    # ====================================
    # DRAW INDIVIDUAL SIGNAL
    # ====================================

    def draw_signal(
        self,
        screen,
        x,
        y,
        is_active_phase
    ):

        # Traffic light housing

        housing = pygame.Rect(
            x,
            y,
            35,
            90
        )

        pygame.draw.rect(
            screen,
            (30, 30, 30),
            housing,
            border_radius=6
        )

        # ====================================
        # RED LIGHT
        # ====================================

        red_color = (220, 40, 40)

        # ====================================
        # YELLOW LIGHT
        # ====================================

        yellow_color = (240, 200, 40)

        # ====================================
        # GREEN LIGHT
        # ====================================

        green_color = (40, 200, 70)

        # ====================================
        # DETERMINE ACTIVE LIGHT
        # ====================================

        if not is_active_phase:

            # This direction is not active.

            red_color = (100, 30, 30)

            yellow_color = (100, 90, 30)

            green_color = (30, 100, 40)

        else:

            if self.state == "GREEN":

                red_color = (100, 30, 30)

            elif self.state == "YELLOW":

                red_color = (100, 30, 30)

                green_color = (30, 100, 40)

            elif self.state == "ALL_RED":

                red_color = (100, 30, 30)

                green_color = (30, 100, 40)

        # ====================================
        # DRAW LIGHTS
        # ====================================

        pygame.draw.circle(
            screen,
            red_color,
            (x + 17, y + 15),
            8
        )

        pygame.draw.circle(
            screen,
            yellow_color,
            (x + 17, y + 45),
            8
        )

        pygame.draw.circle(
            screen,
            green_color,
            (x + 17, y + 75),
            8
        )