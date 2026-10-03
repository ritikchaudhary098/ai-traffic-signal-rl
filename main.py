import pygame

from stable_baselines3 import PPO

from simulation.intersection import Intersection
from simulation.traffic_light import TrafficLight


# ====================================
# INITIALIZE PYGAME
# ====================================

pygame.init()

WIDTH = 1000
HEIGHT = 700

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(
    "AI Traffic Signal Optimization - PPO"
)

clock = pygame.time.Clock()


# ====================================
# CREATE SIMULATION
# ====================================

intersection = Intersection(
    width=WIDTH,
    height=HEIGHT
)

traffic_light = TrafficLight()

intersection.traffic_light = traffic_light


# ====================================
# LOAD TRAINED PPO MODEL
# ====================================

model = PPO.load(
    "models/traffic_ppo"
)


# ====================================
# FONT
# ====================================

font = pygame.font.SysFont(
    "Arial",
    21
)

small_font = pygame.font.SysFont(
    "Arial",
    17
)


# ====================================
# PPO DECISION TIMER
# ====================================

decision_timer = 0

decision_interval = 60

last_action = 0


# ====================================
# MAIN LOOP
# ====================================

running = True

while running:

    # --------------------------------
    # EVENTS
    # --------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False


    # --------------------------------
    # GET CURRENT TRAFFIC
    # --------------------------------

    ns_queue, ew_queue = (
        intersection.get_queue_length()
    )


    # --------------------------------
    # COUNT VEHICLES
    # --------------------------------

    north = 0
    south = 0
    east = 0
    west = 0

    north_waiting = 0
    south_waiting = 0
    east_waiting = 0
    west_waiting = 0


    for vehicle in intersection.vehicles:

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


    # --------------------------------
    # NORMALIZE TRAFFIC COUNTS
    # --------------------------------

    north_obs = min(north / 20.0, 1.0)
    south_obs = min(south / 20.0, 1.0)
    east_obs = min(east / 20.0, 1.0)
    west_obs = min(west / 20.0, 1.0)

    north_waiting_obs = min(
        north_waiting / 20.0,
        1.0
    )

    south_waiting_obs = min(
        south_waiting / 20.0,
        1.0
    )

    east_waiting_obs = min(
        east_waiting / 20.0,
        1.0
    )

    west_waiting_obs = min(
        west_waiting / 20.0,
        1.0
    )


    # --------------------------------
    # CURRENT PHASE
    # --------------------------------

    if traffic_light.phase == "NS":
        phase = 0
    else:
        phase = 1


    # --------------------------------
    # SIGNAL STATE
    # --------------------------------

    if traffic_light.state == "GREEN":

        signal_state = 0.0

    elif traffic_light.state == "YELLOW":

        signal_state = 0.5

    else:

        signal_state = 1.0


    # --------------------------------
    # NORMALIZED TIMER
    # --------------------------------

    timer = (
        traffic_light.timer
        / traffic_light.max_green
    )

    timer = min(
        timer,
        1.0
    )


    # --------------------------------
    # SWITCH ALLOWED
    # --------------------------------

    if (
        traffic_light.state == "GREEN"
        and traffic_light.timer
        >= traffic_light.min_green
    ):

        switch_allowed = 1.0

    else:

        switch_allowed = 0.0


    # --------------------------------
    # BUILD 12-VALUE OBSERVATION
    # --------------------------------

    observation = [

        north_obs,
        south_obs,
        east_obs,
        west_obs,

        north_waiting_obs,
        south_waiting_obs,
        east_waiting_obs,
        west_waiting_obs,

        phase,
        signal_state,
        timer,
        switch_allowed
    ]


    # --------------------------------
    # PPO DECISION
    # --------------------------------

    decision_timer += 1


    if decision_timer >= decision_interval:

        action, _states = model.predict(
            observation,
            deterministic=True
        )

        last_action = int(action)

        decision_timer = 0


        # ----------------------------
        # APPLY PPO ACTION
        # ----------------------------

        if last_action == 1:

            traffic_light.request_switch()


    # --------------------------------
    # UPDATE TRAFFIC LIGHT
    # --------------------------------

    traffic_light.update()


    # --------------------------------
    # UPDATE CARS
    # --------------------------------

    intersection.update()


    # --------------------------------
    # DRAW SIMULATION
    # --------------------------------

    intersection.draw(screen)


    # --------------------------------
    # GET METRICS
    # --------------------------------

    ns_total, ew_total = (
        intersection.get_traffic_counts()
    )

    ns_queue, ew_queue = (
        intersection.get_queue_length()
    )

    metrics = intersection.get_metrics()


    # =================================
    # INFORMATION PANEL
    # =================================

    panel = pygame.Surface(
        (350, 390),
        pygame.SRCALPHA
    )

    panel.fill(
        (0, 0, 0, 180)
    )

    screen.blit(
        panel,
        (10, 10)
    )


    # --------------------------------
    # TITLE
    # --------------------------------

    title = font.render(
        "AI TRAFFIC MANAGEMENT",
        True,
        (255, 255, 255)
    )

    screen.blit(
        title,
        (25, 20)
    )


    # --------------------------------
    # PPO INFORMATION
    # --------------------------------

    if last_action == 0:

        action_text = "KEEP PHASE"

    else:

        action_text = "REQUEST SWITCH"


    if switch_allowed == 1.0:

        switch_text = "YES"

    else:

        switch_text = "NO"


    lines = [

        "Controller       : PPO",

        f"NS Traffic       : {ns_total}",

        f"EW Traffic       : {ew_total}",

        f"NS Queue         : {ns_queue}",

        f"EW Queue         : {ew_queue}",

        "",

        f"Phase            : {traffic_light.phase}",

        f"Signal           : {traffic_light.state}",

        f"AI Action        : {action_text}",

        f"Switch Allowed   : {switch_text}",

        f"Remaining        : {traffic_light.get_remaining_time() // 60}s",

        "",

        "----- PERFORMANCE -----",

        f"Spawned          : {metrics['vehicles_spawned']}",

        f"Passed           : {metrics['vehicles_passed']}",

        f"Average Queue    : {metrics['average_queue']:.2f}",

        f"Maximum Queue    : {metrics['maximum_queue']}",

        f"Avg Waiting      : {metrics['average_waiting_time']:.2f}"
    ]


    # --------------------------------
    # DRAW TEXT
    # --------------------------------

    y = 52

    for line in lines:

        text = small_font.render(
            line,
            True,
            (255, 255, 255)
        )

        screen.blit(
            text,
            (25, y)
        )

        y += 20


    # --------------------------------
    # UPDATE SCREEN
    # --------------------------------

    pygame.display.flip()

    clock.tick(60)


# ====================================
# CLOSE
# ====================================

pygame.quit()