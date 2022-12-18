import navpy as nv


def from_wgs84_to_ecef(lat, lon, alt):
    ecef = nv.lla2ecef(lat, lon, alt)
    return ecef[0], ecef[1], ecef[2]


def from_ecef_to_wgs84(x, y, z):
    ecef = [x, y, z]
    lla = nv.ecef2lla(ecef)
    return lla[0], lla[1], lla[2]


def from_ecef_to_ned(x, y, z, lat, lon, alt):
    ecef = [x, y, z]
    ned = nv.ecef2ned(ecef, lat, lon, alt)
    return ned[0], ned[1], ned[2]
# 34.00000048333403, -117.33356934722197, 251.70201122574508
# 34.0000534361111, -117.333547744444, 234.052

# print(nv.lla2ned(34.0000534361111, -117.333547744444, 234.052, 34.00000048333403, -117.33356934722197, 251.70201122574508))
