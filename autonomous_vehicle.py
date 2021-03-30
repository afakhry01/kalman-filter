from motion_model import MotionModel


class AutonomousVehicleState(MotionModel):
    MIN_SAFE_DISTANCE = 1

    def __init__(self, x, y, angle):
        super().__init__(x, y, angle)
        self.score = 0

    def compute_score(self, predicted_pedestrians_location: list, starting_point: tuple, end_point: tuple):
        # 1. Penalize if getting too close to a pedestrian
        for x, y in predicted_pedestrians_location:
            dist = np.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
            if dist < self.MIN_SAFE_DISTANCE:
                self.score -= 100

        # 2. Penalize if moving away from the target
        dist_to_target = np.sqrt((end_point[0] - self.x) ** 2 + (end_point[1] - self.y) ** 2)
        self.score -= dist_to_target

        # 3. Reward if moving away from starting point
        dist_from_start = np.sqrt((starting_point[0] - self.x) ** 2 + (starting_point[1] - self.y) ** 2)
        self.score += dist_from_start

    @property
    def score(self):
        return self.score


class AutonomousVehicle:
    ACCELERATION = 0
    ANGLES = [-90, -45, 0, 45, 90] * (np.pi / 180)
    VELOCITIES = [0, 1, 2]

    def __init__(self, x: int, y: int, angle: int, starting_point: tuple, end_point: tuple):
        self.current_state = AutonomousVehicleState(x, y, angle)
        self.starting_point = starting_point
        self.end_point = end_point

    def move(self, predicted_pedestrians_location: list, delta_t: int):
        max_score = float('-inf')
        best_found_state = None

        # 1. Create and rank states: angle and velocity
        for angle in self.ANGLES:
            for velocity in self.VELOCITIES:
                x, y, angle = self.current_state.location
                new_state = AutonomousVehicleState(*self.current_state.location)
                new_state.move(angle, velocity, self.ACCELERATION, delta_t=delta_t)
                new_state.compute_score(predicted_pedestrians_location, self.starting_point, self.end_point)
                if new_state.score > max_score:
                    max_score = new_state.score
                    best_found_state = new_state

        # 2. Commit a move
        self.current_state = best_found_state

    @property
    def location(self):
        return self.current_state.location
