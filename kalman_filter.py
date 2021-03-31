import numpy as np


class KalmanFilter:
    def __init__(self, x: float, y: float):
        self.state = np.array([[x], [y],
                               [0.], [0.],
                               [0.], [0.]])
        self.F = np.array([[1., 0., 1., 0., 0.5, 0.],
                           [0., 1., 0., 1., 0., 0.5],
                           [0., 0., 1., 0., 1., 0.],
                           [0., 0., 0., 1., 0., 1.],
                           [0., 0., 0., 0., 1., 0.],
                           [0., 0., 0., 0., 0., 1.]])
        self.P = np.array([[1., 0., 0., 0., 0., 0.],
                           [0., 1., 0., 0., 0., 0.],
                           [0., 0., 1., 0., 0., 0.],
                           [0., 0., 0., 1., 0., 0.],
                           [0., 0., 0., 0., 1., 0.],
                           [0., 0., 0., 0., 0., 1.]])

        self.H = np.array([[1., 0., 0., 0., 0., 0.],
                           [0., 1., 0., 0., 0., 0.]])
        self.R = np.array([[0.00004, 0.],
                           [0., 0.00004]])

    def predict(self):
        # 1. Using the previous state, ¯xk−1 and the state transition model, F, predict the state, ˆx, at time k.
        # xˆk = F * x¯k−1
        self.state = self.F.dot(self.state)

        # 2. predict uncertainty
        # Pˆk = F * P_k−1 * Ft + Q
        self.P = self.F.dot(self.P.dot(self.F.T))

    def update(self, measured_x: float, measured_y: float):
        # 1. kalman gain
        # K = Pˆk * Ht * (H * Pˆk * Ht + R) ^ −1
        K = self.P.dot(self.H.T.dot(np.linalg.inv(self.R + self.H.dot(self.P.dot(self.H.T)))))

        # 2. update the state  based on the difference between the measurement and what the Kalman Filter
        # predicted
        # x¯_k = x¯_k + K * (¯z_k − H * x¯_k)
        z = np.array([[measured_x], [measured_y]])
        y = z - self.H.dot(self.state)
        self.state = self.state + K.dot(y)

        # 3. update the Kalman Filter’s estimate of uncertainty
        # Pk = P^_k − K * H * P^_k
        self.P = self.P - K.dot(self.H.dot(self.P))

    @property
    def location(self):
        return self.state[0][0], self.state[1][0]
