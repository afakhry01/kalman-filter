from motion_model import MotionModel

class Player(MotionModel):
    def __init__(self,
                 x: int,
                 y: int,
                 angle: int = 0
                ):

        super().__init__(x, y, angle)

    @property
    def location(self):
        return tuple(map(int, self.location))
