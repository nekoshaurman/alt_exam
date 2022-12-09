import pyproj as proj
import numpy as np
import scipy.spatial.transform


def from_wgs84_to_ecef(lat, lon, alt):
    transformer = proj.Transformer.from_crs(
        {"proj": 'latlong', "ellps": 'WGS84', "datum": 'WGS84'},
        {"proj": 'geocent', "ellps": 'WGS84', "datum": 'WGS84'},
    )
    x, y, z = transformer.transform(lat, lon, alt, radians=False)
    return x, y, z


def from_ecef_to_wgs84(x, y, z):
    transformer = proj.Transformer.from_crs(
        {"proj": 'geocent', "ellps": 'WGS84', "datum": 'WGS84'},
        {"proj": 'latlong', "ellps": 'WGS84', "datum": 'WGS84'},
    )
    lat, lon, alt = transformer.transform(x, y, z, radians=False)
    return lat, lon, alt


def from_wgs84_to_enu(lat_pixel, lon_pixel, alt_pixel, lat_drone, lon_drone, alt_drone):
    transformer = proj.Transformer.from_crs(
        {"proj": 'latlong', "ellps": 'WGS84', "datum": 'WGS84'},
        {"proj": 'geocent', "ellps": 'WGS84', "datum": 'WGS84'},
    )
    x_drone, y_drone, z_drone = transformer.transform(lon_drone, lat_drone, alt_drone, radians=False)
    x_pixel, y_pixel, z_pixel = transformer.transform(lon_pixel, lat_pixel, alt_pixel, radians=False)
    vec = np.array([[x_pixel - x_drone, y_pixel - y_drone, z_pixel - z_drone]]).T

    rot1 = scipy.spatial.transform.Rotation.from_euler('x', -(90 - lat_pixel),
                                                       degrees=True).as_matrix()  # angle*-1 : left handed *-1
    rot3 = scipy.spatial.transform.Rotation.from_euler('z', -(90 + lon_pixel),
                                                       degrees=True).as_matrix()  # angle*-1 : left handed *-1

    rotMatrix = rot1.dot(rot3)

    enu = rotMatrix.dot(vec).T.ravel()
    return enu.T


def from_enu_to_wgs84(e, n, u, lat_drone, lon_drone, alt_drone):
    transformer1 = proj.Transformer.from_crs(
        {"proj": 'latlong', "ellps": 'WGS84', "datum": 'WGS84'},
        {"proj": 'geocent', "ellps": 'WGS84', "datum": 'WGS84'},
    )
    transformer2 = proj.Transformer.from_crs(
        {"proj": 'geocent', "ellps": 'WGS84', "datum": 'WGS84'},
        {"proj": 'latlong', "ellps": 'WGS84', "datum": 'WGS84'},
    )

    x_drone, y_drone, z_drone = transformer1.transform(lon_drone, lat_drone, alt_drone, radians=False)
    ecef_org = np.array([[x_drone, y_drone, z_drone]]).T

    rot1 = scipy.spatial.transform.Rotation.from_euler('x', -(90 - lat_drone),
                                                       degrees=True).as_matrix()  # angle*-1 : left handed *-1
    rot3 = scipy.spatial.transform.Rotation.from_euler('z', -(90 + lon_drone),
                                                       degrees=True).as_matrix()  # angle*-1 : left handed *-1

    rotMatrix = rot1.dot(rot3)

    ecefDelta = rotMatrix.T.dot(np.array([[e, n, u]]).T)
    ecef = ecefDelta + ecef_org
    lon, lat, alt = transformer2.transform(ecef[0, 0], ecef[1, 0], ecef[2, 0], radians=False)

    return lat, lon, alt


#e, n, u = from_wgs84_to_enu(59.96, 30.20, 0, 59.973017, 30.220557, 50)
#print(e, n, u)
#lat, lon, alt = from_enu_to_wgs84(e, n, u, 59.973017, 30.220557, 50)
#print(lat, lon, alt)