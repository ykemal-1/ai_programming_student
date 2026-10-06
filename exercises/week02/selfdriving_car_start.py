"""
Oefening 1: Self-Driving Car (Model-based Reflex Agent)
========================================================
Implementeer een agent die zijn voorligger volgt.
"""


class LidarSensorInput:
    def __init__(self, distance=0.0):
        self.DistanceTo = distance


class Brake:
    def __str__(self):
        return "BRAKE"


class Nothing:
    def __str__(self):
        return "NOTHING"


class SelfDrivingCar:
    def __init__(self):
        # TODO: interne state — welke variabele heb je nodig?

        self.previous_distance = None

        pass

    def process(self, sensor_input):
        # TODO: bereken relatieve snelheid en tijd tot botsing;
        #       rem als tijd < 5 seconden

        distance = sensor_input.DistanceTo

        # Bij de eerste meting is er nog geen vorige afstand
        if self.previous_distance is None:
            self.previous_distance = distance
            return Nothing()

        # Eén stap tussen metingen wordt hier als één seconde beschouwd.
        speed = self.previous_distance - distance
        self.previous_distance = distance

        # Alleen bij een positieve snelheid wordt de afstand kleiner.
        if speed > 0:
            time_to_collision = distance / speed
            if time_to_collision < 5:
                return Brake()

        action = Nothing()
        return action


if __name__ == "__main__":
    sensor = LidarSensorInput(10)
    agent = SelfDrivingCar()

    for afstand in [10, 15, 13, 10, 8, 6, 4, 3]:
        sensor.DistanceTo = afstand
        action = agent.process(sensor)
        print(f"Afstand: {afstand}m -> {action}")
