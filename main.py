from math import *
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
        self.focus = f  # focal length(mm) ---> convert to metres
        self.matrix_x = m_a  # matrix side, px
        self.matrix_y = m_b  # matrix side, px
        self.pixel_x = px  # px - matrix_x/2  # pixel X coordinate in the image, px
        self.pixel_y = py  # (py - matrix_y/2) * (-1)  # pixel Y coordinate in the image, px

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
        #camera_coordinates = camera_coordinates  * self.alt
        #camera_coordinates[0][0] /= 1000
        #camera_coordinates[1][0] /= 1000
        return camera_coordinates

    # Точка в мировых координатах
    def get_world_coordinates(self):
        yaw = 0
        pitch = 0
        roll = 0
        drone_x_ecef, drone_y_ecef, drone_z_ecef = ECEF.from_wgs84_to_ecef(self.lat, self.lon, self.alt)
        # coordinates of camera in world coordinates
        t = np.array([
            [drone_x_ecef],
            [drone_y_ecef],
            [drone_z_ecef]
        ])
        # ecef 2 ned
        rotate_matrix = np.array([
            [-sin(self.lat)*cos(self.lon), -sin(self.lat)*sin(self.lon), cos(self.lat)],
            [-sin(self.lon), cos(self.lon), 0],
            [-cos(self.lat)*cos(self.lon), -cos(self.lat)*sin(self.lon), -sin(self.lat)]
        ])

        camera_coordinates = camera.get_camera_coordinates()
        camera_coordinates_ecef = rotate_matrix.dot(camera_coordinates)

        world_coordinates_ecef = camera_coordinates_ecef + t

        return world_coordinates_ecef


if __name__ == "__main__":
    f = 60  # in mm
    matrix_x, matrix_y = 1920, 1080  # in px
    px = 200
    py = 1000
    lat = 59.973017 # degrees
    lon = 30.220557  # degrees
    alt = 50
    roll = 0
    pitch = 0
    yaw = 0
    camera = Camera(lat, lon, alt, roll, pitch, yaw, px, py, f, matrix_x, matrix_y)
    print("\n Coordinates relative to the camera\n", *camera.get_camera_coordinates())
    print("\n", *camera.get_world_coordinates())
    print("\n", *ECEF.from_ecef_to_wgs84(camera.get_world_coordinates()[0], camera.get_world_coordinates()[1],
                                         camera.get_world_coordinates()[2]))