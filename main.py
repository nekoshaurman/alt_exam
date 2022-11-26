from math import *
# 1 mm = 3.793627 px
alpha = 1/3.793627  # coefficient for translation mm ---> px

# (0,0) ---> (1920/2, 1080/2) new center (960, 540)

class Camera:
    def __init__(self, lat, lon, alt, roll, pitch, yaw, px, py, f, m_a, m_b):
        self.lat = radians(lat)  # latitude(deg)
        self.lon = radians(lon)  # longitude(deg)
        self.alt = alt  # altitude(meters)
        self.roll = roll  # roll(degrees)
        self.pitch = pitch  # pitch(degrees)
        self.yaw = yaw  # yaw(°degrees)
        self.f = f/1000  # focal length(mm) ---> convert to metres
        self.matrix_x = m_a  # matrix side, px
        self.matrix_y = m_b  # matrix side, px
        self.px = px - matrix_x/2  # pixel X coordinate in the image, px
        self.py = (py - matrix_y/2) * (-1)  # pixel Y coordinate in the image, px
        self.bearing = 0
        self.x = self.get_x_position()  # coordinates of the object relative to the projection of the camera on the ground
        self.y = self.get_y_position()  # coordinates of the object relative to the projection of the camera on the ground

    # Camera position x
    def get_x_position(self):
        if self.f != 0:
            return (self.px * alpha * self.alt)/(1000 * self.f)
        else:
            return 0

    # Camera position y
    def get_y_position(self):
        if self.f != 0:
            return (self.py * alpha * self.alt)/(1000 * self.f)
        else:
            return 0

    # Distance to object
    def get_distance(self):
        ix = self.lat + self.x
        iy = self.lon + self.y
        return sqrt(pow(ix, 2)+pow(iy, 2))


if __name__ == "__main__":
    f = 530  # 50mm
    matrix_x, matrix_y = 1920, 1080  # in px
    px = 80
    py = 320
    lat = 59.973017 # degrees
    lon = 30.220557 # degrees
    alt = 50
    roll = 0
    pitch = 0
    yaw = 0
    camera = Camera(lat, lon, alt, roll, pitch, yaw, px, py, f, matrix_x, matrix_y)