import pygame


class Vehicle:

    def __init__(self, x, y, direction, speed=2.5):

        self.x = float(x)
        self.y = float(y)

        self.direction = direction
        self.speed = speed

        # Vehicle size
        if direction in ["north", "south"]:
            self.width = 18
            self.height = 32
        else:
            self.width = 32
            self.height = 18

        # --------------------------------------------------
        # Vehicle state
        # --------------------------------------------------

        self.waiting_time = 0

        # True after the front of the vehicle crosses
        # the stop line.
        self.passed_stop_line = False

        # Count whether this vehicle has entered the
        # intersection.
        self.entered_intersection = False

    # ======================================================
    # RECTANGLE
    # ======================================================

    def get_rect(self):

        return pygame.Rect(
            int(self.x),
            int(self.y),
            self.width,
            self.height
        )

    # ======================================================
    # FRONT POSITION
    # ======================================================

    def get_front_position(self):

        if self.direction == "south":
            return self.y + self.height

        elif self.direction == "north":
            return self.y

        elif self.direction == "east":
            return self.x + self.width

        elif self.direction == "west":
            return self.x

        return 0

    # ======================================================
    # MOVE
    # ======================================================

    def move(self):

        if self.direction == "south":
            self.y += self.speed

        elif self.direction == "north":
            self.y -= self.speed

        elif self.direction == "east":
            self.x += self.speed

        elif self.direction == "west":
            self.x -= self.speed

    # ======================================================
    # DRAW
    # ======================================================

    def draw(self, screen):

        rect = self.get_rect()

        # --------------------------------------------------
        # CAR BODY
        # --------------------------------------------------

        pygame.draw.rect(
            screen,
            (40, 120, 220),
            rect,
            border_radius=4
        )

        # --------------------------------------------------
        # WINDSHIELD
        # --------------------------------------------------

        if self.direction == "south":

            windshield = pygame.Rect(
                int(self.x + 3),
                int(self.y + 4),
                self.width - 6,
                7
            )

        elif self.direction == "north":

            windshield = pygame.Rect(
                int(self.x + 3),
                int(self.y + self.height - 11),
                self.width - 6,
                7
            )

        elif self.direction == "east":

            windshield = pygame.Rect(
                int(self.x + self.width - 11),
                int(self.y + 3),
                7,
                self.height - 6
            )

        else:

            windshield = pygame.Rect(
                int(self.x + 4),
                int(self.y + 3),
                7,
                self.height - 6
            )

        pygame.draw.rect(
            screen,
            (190, 225, 240),
            windshield,
            border_radius=2
        )