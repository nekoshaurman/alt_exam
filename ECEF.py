import pyproj as proj


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
