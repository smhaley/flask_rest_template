
from models import Location
from flask import abort


def get_lim_offset(params):
    """Simple helper to extract offset and limite q params"""
    
    if 'limit' in params:
        if params['limit'] > 100 or params['limit'] < 0:
            limit = 100
        else:
            limit = int(params['limit'])
    else:
        limit = None

    if 'offset' in params:
        offset = int(params['offset'])
    else:
        offset = None

    return limit, offset


def loc_by_bbox(south_west, north_east, limit, offset, subquery=False, **kwargs):
    """
    Helper function to clean and return location subquery
    south_west: coord string (lat, long)
    north_east: coord string (lat, long)
    return: sql query of locations within bbox
    """

    try:
        sw = south_west.replace(' ', '').strip('(').strip(')').split(',')
        ne = north_east.replace(' ', '').strip('(').strip(')').split(',')
        lon_min = float(sw[0])
        lat_min = float(sw[1])
        lon_max = float(ne[0])
        lat_max = float(ne[1])

        if subquery:
            locations = Location.query.with_entities(Location.id).filter(
                Location.lat >= lat_min, Location.lat <= lat_max, Location.lon >= lon_min, Location.lon <= lon_max).limit(limit).offset(offset).subquery()
        else:
            locations = Location.query.filter(
                Location.lat >= lat_min, Location.lat <= lat_max, Location.lon >= lon_min, Location.lon <= lon_max).limit(limit).offset(offset).all()

        return locations

    except ValueError:
        abort(404, "Outside expected format. Use (lat, lon)")
