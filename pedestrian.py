import uuid
import random

from motion_model import MotionModel

class Pedestrian(MotionModel):
    STEERING_ANGLE = 0
    ACCELERATION = 0

    def __init__(self,
                 x: int,
                 y: int,
                 angle: int = 0
                ):

        super().__init__(x, y, angle)
        self.id = str(uuid.uuid4())
        self.velocity = random.randrange(0, 5)

    @property
    def location(self) -> tuple:
        return tuple(map(int, self.location))

    def move(self):
        super().move(self.STEERING_ANGLE, self.velocity, self.ACCELERATION)


class Pedestrians:
    def __init__(self, pedestrians_list: list):
        self.pedestrians_list = pedestrians_list

    @classmethod
    def init_random(cls, count: int) -> Pedestrians:
        pedestrians_list = []
        for i in range(count):
            x = random.randrange(0, 1280)
            y = random.randrange(0, 720)
            angle = random.choice([90, -90])
            pedestrians_list.append(Pedestrian(x, y, angle))

        return cls(pedestrians_list)

    def move(self):
        for ndx in range(len(self.pedestrians_list)):
            self.pedestrians_list[ndx].move()

    def get_true_locations(self) -> list:
        locations = []
        for pedestrian in self.pedestrians_list:
            locations.append(pedestrian.location)

        return locations

    def get_noisy_locations(self, noise: float) -> list:
        locations = []
        for pedestrian in self.pedestrians_list:
            angle, x, y = pedestrian.location
            x += random.gauss(0.0, noise)
            y += random.gauss(0.0, noise)

            locations.append((angle, x, y))

        return locations        
