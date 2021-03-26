import cv2
import numpy as np
import random

from player import Player

class Scene:
    def __init__(self, player: Player, points: list, shape: tuple = (720, 1280, 3)):
        self.player = player
        self.points = points
        self.playground = np.ones(shape, dtype=np.uint8) * 255

    def update_player(self, new_player: Player):
        self.player = new_player

    def render(self):
        for point in self.points:
            cv2.circle(self.playground, point, 5, (0, 0, 0), cv2.FILLED)

        start_point = (self.player.x - 5, self.player.y - 5)
        end_point = (self.player.x + 5, self.player.y + 5)
        cv2.rectangle(self.playground, start_point, end_point, (0, 0, 255), cv2.FILLED)

    def test_show(self):
        cv2.imshow("Screen", self.playground)
        cv2.waitKey(0)

if __name__ == "__main__":
    player = Player(640, 360)
    points = [(random.randrange(0, 1280), random.randrange(0, 720)) for i in range(50)]
    scene = Scene(player, points)
    scene.render()
    scene.test_show()
