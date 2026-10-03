class FixedTimeController:

    def __init__(self, traffic_light):
        self.traffic_light = traffic_light

    def update(self):

        if (
            self.traffic_light.state == "GREEN"
            and self.traffic_light.timer
            >= self.traffic_light.max_green
        ):
            self.traffic_light.request_switch()