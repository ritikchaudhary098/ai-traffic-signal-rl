class AdaptiveController:

    def __init__(self, traffic_light, intersection):

        self.traffic_light = traffic_light
        self.intersection = intersection

    def update(self):

        # ------------------------------------------
        # Only make a decision when the light is
        # currently GREEN.
        # ------------------------------------------

        if self.traffic_light.state != "GREEN":
            return

        # ------------------------------------------
        # Get current queues
        # ------------------------------------------

        ns_queue, ew_queue = (
            self.intersection.get_queue_length()
        )

        # ------------------------------------------
        # Check whether minimum green time
        # has passed.
        # ------------------------------------------

        if (
            self.traffic_light.timer
            < self.traffic_light.min_green
        ):
            return

        # ------------------------------------------
        # If NS is green and EW has significantly
        # more traffic, switch.
        # ------------------------------------------

        if self.traffic_light.phase == "NS":

            if ew_queue > ns_queue + 2:
                self.traffic_light.request_switch()

        # ------------------------------------------
        # If EW is green and NS has significantly
        # more traffic, switch.
        # ------------------------------------------

        else:

            if ns_queue > ew_queue + 2:
                self.traffic_light.request_switch()