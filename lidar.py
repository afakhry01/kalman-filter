from pedestrian import Pedestrians
from kalman_filter import KalmanFilter


class Lidar:
    NOISE = 5

    def __init__(self, pedestrians_kf_list: list):
        self.pedestrians_kf_list = pedestrians_kf_list

    @classmethod
    def init_from_pedestrians(cls, pedestrians: Pedestrians) -> Lidar:
        pedestrians_kf_list = []
        for x, y in pedestrians.get_noisy_locations(cls.NOISE):
            pedestrians_kf_list.append(KalmanFilter(x, y))

        return cls(pedestrians_kf_list)

    def predict_pedestrians_location(self):
        predicted_pedestrians_location = []
        for ndx in range(len(self.pedestrians_kf_list)):
            pedestrians_kf_list[ndx].predict()
            predicted_pedestrians_location.append(pedestrians_kf_list[ndx].location)

        return predicted_pedestrians_location

    def update_pedestrians_location(self, pedestrians: Pedestrians):
        new_measurements = pedestrians.get_noisy_locations(self.NOISE)
        if len(self.pedestrians_kf_list) != len(new_measurements):
            raise ValueError

        for ndx in range(len(self.pedestrians_kf_list)):
            measured_x, measured_y = new_measurements[ndx]
            pedestrians_kf_list[ndx].update(measured_x, measured_y)
