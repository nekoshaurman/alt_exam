 import main
import numpy as np
import ECEF as ECEF


class Camera:
    def __init__(self, lat, lon, alt, roll, pitch, yaw, px, py, f, m_a, m_b):
        self.lat = lat  # radians(lat)  # latitude(deg)
        self.lon = lon  # radians(lon)  # longitude(deg)
        self.alt = alt  # altitude(meters)
        self.roll = roll  # roll(degrees)
        self.pitch = pitch  # pitch(degrees)
        self.yaw = yaw  # yaw(°degrees)
        self.focus = f / 1000  # focal length(mm) ---> convert to metres
        self.matrix_x = m_a  # matrix side, px
        self.matrix_y = m_b  # matrix side, px
        self.pixel_x = px  # px - matrix_x/2  # pixel X coordinate in the image, px
        self.pixel_y = py  # (py - matrix_y/2) * (-1)  # pixel Y coordinate in the image, px


    def get_camera_coordinates(self):
        skew = 0
        intrinsic_matrix = np.array([[self.focus, skew, self.matrix_x / 2],
                                     [0, self.focus, self.matrix_y / 2],
                                     [0, 0, 1]])
        x_ecef, y_ecef, z_ecef = ECEF.from_wgs84_to_ecef(self.lat, self.lon, self.alt)
        world_coordinates_ecef = np.array([[x_ecef],
                                           [y_ecef],
                                           [z_ecef],
                                           1])
        pixel_coord = np.array([[self.pixel_x],
                                [self.pixel_y],
                                [1]])

        extrinsic_matrix = np.array([])

        pixel_coord = (intrinsic_matrix.dot(extrinsic_matrix)).dot(world_coordinates_ecef)


if __name__ == "__main__":
    f = 1000
    matrix_x, matrix_y = 1920, 1080 # in px
    px = 1000
    py = 1000
    lat = 59.973017  # degrees
    lon = 30.220557  # degrees
    alt = 50
    roll = 0
    pitch = 0
    yaw = 0
    camera = main.Camera(lat, lon, alt, roll, pitch, yaw, px, py, f, matrix_x, matrix_y)