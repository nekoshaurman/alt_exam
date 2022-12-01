from math import *
import numpy as np
import ECEF as ECEF

# 1 mm = 3.793627 px
alpha = 1 / 3.793627  # coefficient for translation mm ---> px


# (0,0) ---> (1920/2, 1080/2) new center (960, 540)

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

    # Точка в координатах камеры
    def get_camera_coordinates(self):
        intrinsic_matrix = np.array([
            [self.focus, 0, self.matrix_x / 2],
            [0, self.focus, self.matrix_y / 2],
            [0, 0, 1]
        ])
        # print("\n", intrinsic_matrix)
        intrinsic_matrix_inverse = np.linalg.inv(intrinsic_matrix)
        # print("\n", intrinsic_matrix_inverse)
        pixel_coord = np.array([
            [self.pixel_x],
            [self.pixel_y],
            [1]
        ])
        # print("\n", pixel_coord)
        camera_coordinates = intrinsic_matrix_inverse.dot(pixel_coord)
        # print("\n", from_pixel_to_camera)
        camera_coordinates = camera_coordinates * self.alt
        # print("\n", from_pixel_to_camera)
        camera_coordinates[0][0] /= 1000
        camera_coordinates[1][0] /= 1000
        return camera_coordinates

    # Точка в мировых координатах
    def get_world_coordinates(self):
        a = self.yaw  # Надо прикрутить им всем коррекцию по ECEF либо новые переменные для этого юзать
        b = self.pitch
        g = self.roll
        camera_x_ecef, camera_y_ecef, camera_z_ecef = ECEF.from_wgs84_to_ecef(self.lat, self.lon, self.alt)
        # coordinates of camera in world coordinates
        t = np.array([
            [camera_x_ecef],
            [camera_y_ecef],
            [camera_z_ecef]
        ])
        # clockwise yaw
        r_z = np.array([
            [cos(a), -sin(a), 0],
            [sin(a), cos(a), 0],
            [0, 0, 1]
        ])
        # counterclockwise pitch
        r_y = np.array([
            [cos(b), 0, sin(b)],
            [0, 1, 0],
            [-sin(b), 0, cos(b)]
        ])
        # counterclockwise roll
        r_x = np.array([
            [1, 0, 0],
            [0, cos(g), -sin(g)],
            [0, sin(g), cos(g)]
        ])
        rotate_matrix = (r_z.dot(r_y)).dot(r_x)
        rotate_matrix_inverse = np.linalg.inv(rotate_matrix)
        camera_coordinates = camera.get_camera_coordinates()
        world_coordinates = (rotate_matrix_inverse.dot(camera_coordinates)) + t
        print("\n", t)
        return world_coordinates


if __name__ == "__main__":
    f = 530  # 50mm
    matrix_x, matrix_y = 1920, 1080  # in px
    px = 450
    py = 580
    lat = 59.973017000000006  # degrees
    lon = 30.220557  # degrees
    alt = 50
    roll = 0
    pitch = 0
    yaw = 0
    camera = Camera(lat, lon, alt, roll, pitch, yaw, px, py, f, matrix_x, matrix_y)
    print("\n Coordinates relative to the camera\n", camera.get_camera_coordinates())  # координаты одинаковые т.к. нужно скорректировать матрицу поворота
    print("\n", camera.get_world_coordinates())
    print("\n", ECEF.from_wgs84_to_ecef(lat, lon, alt))
    print("\n", ECEF.from_ecef_to_wgs84(*camera.get_world_coordinates()[0], *camera.get_world_coordinates()[1], *camera.get_world_coordinates()[2]))

    # Что-то почти доделал, надо разобраться какие тестовые ролл питч и йа установить
