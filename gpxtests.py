import gpxpy as gp
import matplotlib.pyplot as plt
import numpy as np

class DataExtract():

    #data = '/Users/ushhamilton/Documents/03 Programming/Python/Mapping/Data/Mosey_in_the_Mournes.gpx'
    col_dict = {
        "time": 0,
        "latitude": 1,
        "longitude": 2,
        "elevation": 3,
        "distance": 4,
        "gradient": 5,
        "speed": 6
    }

    unit_convert = {
        "time2min": 1/60,
        "time2hr": 1/3600,
        "meter2km": 1/1000,
        "gradient2percent": 100,
        "speed2kmh": 3.6
    }

    def __init__(self, loc):
        self.loc = loc
        reader = open(self.loc, 'r')
        self.data = gp.parse(reader).tracks[0]


    def data_to_list(self, data):
        points = []
        for segment in data.segments:
            for point in segment.points:

                points.append([point.time, point.latitude, point.longitude, point.elevation])

        points.sort()
        return points

    def calcs_to_list(self, points):
        new_points = []
        for idx, pt in enumerate(points):
            if idx == 0:
                dist, grad, speed = 0, 0, 0
            else:
                dist = gp.geo.distance(pt[self.col_dict["latitude"]], pt[self.col_dict["longitude"]], pt[self.col_dict["elevation"]], prev_lat, prev_long, prev_ele)
                grad = (pt[self.col_dict["elevation"]] - prev_ele) / dist
                speed = dist / (pt[self.col_dict["time"]] - prev_time).total_seconds()

            ls = [*pt, dist, grad, speed]
            new_points.append(ls)

            prev_lat, prev_long, prev_ele, prev_time= pt[self.col_dict["latitude"]], pt[self.col_dict["longitude"]], pt[self.col_dict["elevation"]], pt[self.col_dict["time"]]
        
        return new_points

    def x_y_graph(self, xvar, yvar, time=False, culmulate=True):

        data = self.calcs_to_list(self.data_to_list(self.data))

        graph_data = []

        for idx, pt in enumerate(data):
            if idx == 0:
                culm = 0
            else:
                if time:
                    culm += (pt[self.col_dict[xvar]] - culm_prev).total_seconds()
                else:
                    if culmulate:
                        culm += pt[self.col_dict[xvar]]
                    else:
                        culm = pt[self.col_dict[xvar]]

            graph_data.append([culm, pt[self.col_dict[yvar]]])

            culm_prev = pt[self.col_dict[xvar]]
        return np.array(graph_data)

    def trend_line(self, data, rolling):
        def moving_average(x, w):
            return np.convolve(x, np.ones(w), 'valid') / w

        return moving_average(data, rolling)



# x = DataExtract()

# res = x.x_y_graph("distance", "speed", False, True)
# res2 = x.x_y_graph("distance", "gradient", False, True)

# # fig, ax1 = plt.subplots()
# # ax2 = ax1.twinx()

# # ax1.plot(res[:, 0], res[:, 1]*3.6, c='lightgrey')

# n = 60
# # ax2.plot(res[:, 0][n-1:], x.trend_line(res2[:, 1], n)*100, c='b')
# # ax1.plot(res[:, 0][n-1:], x.trend_line(res[:, 1], n)*3.6, c='red')
# plt.scatter(x.trend_line(res2[:, 1], n)*100, x.trend_line(res[:, 1], n)*3.6)
# plt.show()
