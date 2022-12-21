import navpy as nv
import pyproj
import scipy
import numpy as np
from pyproj import proj


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


def sed2geodetic(x, y, z, lat_org, lon_org, alt_org):
    transformer1 = pyproj.Transformer.from_crs(
        {"proj": 'latlong', "ellps": 'WGS84', "datum": 'WGS84'},
        {"proj": 'geocent', "ellps": 'WGS84', "datum": 'WGS84'},
    )
    transformer2 = pyproj.Transformer.from_crs(
        {"proj": 'geocent', "ellps": 'WGS84', "datum": 'WGS84'},
        {"proj": 'latlong', "ellps": 'WGS84', "datum": 'WGS84'},
    )

    x_org, y_org, z_org = transformer1.transform(lon_org, lat_org, alt_org, radians=False)
    ecef_org = np.array([[x_org, y_org, z_org]]).T

    rot1 = scipy.spatial.transform.Rotation.from_euler('x', -(90-lat_org),
                                                       degrees=True).as_matrix()  # angle*-1 : left handed *-1
    rot3 = scipy.spatial.transform.Rotation.from_euler('z', -(90+lon_org),
                                                       degrees=True).as_matrix()  # angle*-1 : left handed *-1

    rotMatrix = rot1.dot(rot3)

    ecefDelta = rotMatrix.T.dot(np.array([[x, y, z]]).T)
    ecef = ecefDelta + ecef_org
    lon, lat, alt = transformer2.transform(ecef[0, 0], ecef[1, 0], ecef[2, 0], radians=False)

    return [lat, lon, alt]
