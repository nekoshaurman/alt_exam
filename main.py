from math import *
import numpy as np
import ECEF as ECEF
import scipy.spatial.transform


class Camera:
    def __init__(self, lat, lon, alt, roll, pitch, yaw, px, py, f, m_a, m_b):
        self.lat = lat  # radians(lat)  # latitude(deg)
        self.lon = lon  # radians(lon)  # longitude(deg)
        self.alt = alt  # altitude(meters)
        self.roll = roll  # roll(degrees)
        self.pitch = pitch  # pitch(degrees)
        self.yaw = yaw  # yaw(°degrees)
        self.focus = f  # focal length(mm) ---> convert to metres
        self.matrix_x = m_a  # matrix side, px
        self.matrix_y = m_b  # matrix side, px
        self.pixel_x = px  # pixel X coordinate in the image, px
        self.pixel_y = py  # pixel Y coordinate in the image, px

    # Точка в координатах камеры
    def get_camera_coordinates(self):
        skew = 0
        intrinsic_matrix = np.array([
            [self.focus, skew, self.matrix_x / 2],
            [0, self.focus, self.matrix_y / 2],
            [0, 0, 1]
        ])
        intrinsic_matrix_inverse = np.linalg.inv(intrinsic_matrix)
        pixel_coord = np.array([
            [self.pixel_x],
            [self.pixel_y],
            [1]
        ])
        camera_coordinates = intrinsic_matrix_inverse.dot(pixel_coord)
        camera_coordinates = camera_coordinates * self.alt
        camera_coordinates[0][0] /= 1000
        camera_coordinates[1][0] /= 1000
        return camera_coordinates

    # Точка в мировых координатах
    def get_world_coordinates(self):

        camera_coordinates = camera.get_camera_coordinates()

        world_coordinates = ECEF.sed2geodetic(camera_coordinates[0], camera_coordinates[1], camera_coordinates[2], self.lat, self.lon, self.alt)

        return world_coordinates


if __name__ == "__main__":
    f = 200  # in mm
    matrix_x, matrix_y = 1920, 1080  # in px
    px = 1000
    py = 200
    lat = 59.973017  # degrees
    lon = 30.220557  # degrees
    alt = 50
    roll = 0
    pitch = 0
    yaw = 0
    camera = Camera(lat, lon, alt, roll, pitch, yaw, px, py, f, matrix_x, matrix_y)
    print("\n Coordinates relative to the camera\n", *camera.get_camera_coordinates())
    print("\n", *camera.get_world_coordinates()) #59.972753, 30.220076
