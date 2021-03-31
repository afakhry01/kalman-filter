import cv2
import numpy as np
import random

from autonomous_vehicle import AutonomousVehicle
from pedestrian import Pedestrians
from lidar import Lidar

class Scene:
    SHAPE = (720, 1280, 3)

    def __init__(self, autonomous_vehicle: AutonomousVehicle, pedestrians: Pedestrians):
        self.autonomous_vehicle = autonomous_vehicle
        self.pedestrians = pedestrians
        self.playground = None
        self.predicted_pedestrians_location = None
        self.true_pedestrians_location = None

    def next(self, delta_t):
        self.pedestrians.move(delta_t)
        self.predicted_pedestrians_location = self.autonomous_vehicle.move(delta_t)
        self.true_pedestrians_location = self.pedestrians.get_true_locations()

        # correct/improve KF predictions by taking a new measurement and comparing
        # it with the predicted values
        self.autonomous_vehicle.lidar.update_pedestrians_location(self.pedestrians)

    def render(self):
        self.playground = np.ones(self.SHAPE, dtype=np.uint8) * 255

        for x, y in self.predicted_pedestrians_location:
            cv2.circle(self.playground, (int(x), int(y)), 5, (0, 0, 255), cv2.FILLED)

        for x, y in self.true_pedestrians_location:
            cv2.circle(self.playground, (x, y), 5, (0, 0, 0), cv2.FILLED)

        vehicle_x, vehicle_y, _ = self.autonomous_vehicle.location
        start_point = (int(vehicle_x) - 5, int(vehicle_y) - 5)
        end_point = (int(vehicle_x) + 5, int(vehicle_y) + 5)
        cv2.rectangle(self.playground, start_point, end_point, (0, 255, 0), cv2.FILLED)

    def test_show(self):
        cv2.imshow("Screen", self.playground)
        cv2.waitKey(0)

if __name__ == "__main__":
    pedestrians = Pedestrians.init_random(30)
    lidar = Lidar.init_from_pedestrians(pedestrians)
    autonomous_vehicle = AutonomousVehicle(360, 640, 0, lidar, (360, 640), (0, 0))
    scene = Scene(autonomous_vehicle, pedestrians)
    for i in range(30):
        scene.next(i)
        scene.render()
        scene.test_show()
