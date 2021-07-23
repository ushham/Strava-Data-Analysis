import numpy as np
import matplotlib.pyplot as plt

class BikeModel():
    g = 9.807
    rolling_resistance = 0.005
    frontal_area = 0.509
    drag_coefficient = 0.63
    rho = 1.226
    efficiency = 0.98
    km2ms = 1/3.6

    def __init__(self, mass):
        self.mass = mass

    def force_gravity(self, slope):
        f_g = self.g * np.sin(np.arctan(slope)) * self.mass
        return f_g

    def force_rolling_resistance(self, slope):
        f_r = self.g * np.cos(np.arctan(slope)) * self.mass * self.rolling_resistance
        return f_r
    
    def force_air_drag(self, vel, include_vel=True):
        f_d = 0.5 * self.drag_coefficient * self.frontal_area * self.rho
        
        if include_vel:
            f_d = f_d * (vel ** 2)

        return f_d

    def power(self, vel, slope):
        vel_cor = vel * self.km2ms
        p = (self.efficiency ** -1) * (self.force_gravity(slope) + self.force_rolling_resistance(slope) + self.force_air_drag(vel_cor)) * vel_cor
        return p

    def vel(self, slope, power):
        # Velocity results are output in km/h

        coefs = [-power * self.efficiency, self.force_gravity(slope) + self.force_rolling_resistance(slope), 0, self.force_air_drag(0, False)]
        solutions = np.polynomial.polynomial.polyroots(coefs)
        sols = solutions[solutions.imag == 0].real / self.km2ms

        sols = sols[sols > 0]

        if sols.shape != (1,):
            print('Unexpected velocity result: ' + str(sols))
            print(np.polynomial.polynomial.Polynomial(coefs))
    
        return sols[0]

# x = BikeModel(70)
# print(x.vel(-0.05, 300))
