import numpy as np

def truncate_angle(angle: float):
    return ((angle + np.pi) % (2 * np.pi)) - np.pi

class MotionModel:
    def __init__(self,
                 x: float,
                 y: float,
                 angle: float = 0,
                 max_steering_angle: float = np.pi / 2,
                 max_velocity: float = 2,
                 max_acceleration: float = 2,
                ):

        self.x = x
        self.y = y
        self.angle = angle
        self.max_steering_angle = max_steering_angle
        self.max_velocity = max_velocity
        self.max_acceleration = max_acceleration

    def move(self,
             steering_angle: float,
             velocity: float = 0,
             acceleration: float = 0,
             delta_t: float = 1
            ):
            
        steering_angle = max(-self.max_steering_angle, steering_angle)
        steering_angle = min(self.max_steering_angle, steering_angle)
        self.angle = truncate_angle(self.angle + steering_angle)

        velocity = max(0, velocity)
        velocity = min(self.max_distance, velocity)
        v_x = velocity * np.cos(self.angle)
        v_y = velocity * np.sin(self.angle)

        acceleration = max(0, acceleration)
        acceleration = min(self.max_distance, acceleration)
        a_x = acceleration * np.cos(self.angle)
        a_y = acceleration * np.sin(self.angle)

        self.x = self.x + (v_x * delta_t) + (a_x * delta_t ** 2)
        self.y = self.y + (v_y * delta_t) + (a_y * delta_t ** 2)

    @property
    def location(self):
        return self.angle, self.x, self.y

    def __repr__(self):
        return f'angle:{self.angle}, x:{self.x}, y:{self.y}'
