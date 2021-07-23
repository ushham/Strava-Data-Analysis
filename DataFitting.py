import numpy as np
import gpxtests as gpt
import BikeCalculator as bc

import matplotlib.pyplot as plt

class DataFitting():
    def __init__(self, bikecomputer, data) -> None:
        self.data = data
        self.bike_com = bikecomputer
        self.num_divisions = 20

    def slope_to_speed(self):
        ave_parm = 100

        vel = self.data.x_y_graph("distance", "speed", False, True)
        grad = self.data.x_y_graph("distance", "gradient", False, True)

        #Average the data to smooth results
        vel_ave = self.data.trend_line(vel[:, 1], ave_parm) * self.data.unit_convert["speed2kmh"]
        grad_ave = self.data.trend_line(grad[:, 1], ave_parm) * self.data.unit_convert["gradient2percent"]

        return [grad_ave, vel_ave]

    def linspace(self, data):
        d_min, d_max = np.min(data), np.max(data)
        lin = np.linspace(d_min, d_max, self.num_divisions)
        return lin

    def ave_speed_from_power(self, grad, power):
        grad_lin = self.linspace(grad)
        vel = []
        for i in grad_lin:
            vel.append(self.bike_com.vel(i / self.data.unit_convert["gradient2percent"], power))
        return [grad_lin, np.array(vel)]

    def average_speed_from_grad(self, grad, vel):
        grad_lin = self.linspace(grad)
        
        ave_speed = []
        for i in range(grad_lin.shape[0]-1):
            ave_speed.append(np.mean(vel[np.logical_and(grad>=grad_lin[i], grad<grad_lin[i+1])]))

        return [grad_lin[:-1], np.array(ave_speed)]

    def power_from_vel(self, vel, grad):
        power = self.bike_com.power(vel,  grad / self.data.unit_convert["gradient2percent"])
        print(vel[-1], grad[-1], power)
        return power

loc = '/Users/ushhamilton/Documents/03 Programming/Python/Mapping/Data/Mosey_in_the_Mournes.gpx'
x = DataFitting(bc.BikeModel(70), gpt.DataExtract(loc))
data = x.slope_to_speed()
line = x.ave_speed_from_power(data[0], 270)
ave_grad, ave_speed = x.average_speed_from_grad(*data)
ave_power = x.power_from_vel(ave_speed, ave_grad)

plt.scatter(*data)
plt.plot(*line, c='r')
plt.plot(ave_grad, ave_speed, c='g')
plt.plot(ave_grad, ave_power, c='grey')

plt.show()
