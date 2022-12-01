import pyproj as proj


def from_wgs84_to_ecef(lat, lon, alt):
    transformer = proj.Transformer.from_crs(
        {"proj": 'latlong', "ellps": 'WGS84', "datum": 'WGS84'},
        {"proj": 'geocent', "ellps": 'WGS84', "datum": 'WGS84'},
    )
    x, y, z = transformer.transform(lon, lat, alt, radians=False)
    return x, y, z
