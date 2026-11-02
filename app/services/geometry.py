"""Convert between frontend {lat,lng} rings and PostGIS WKT / GeoAlchemy."""
from typing import List, Sequence, Tuple

from geoalchemy2.elements import WKTElement
from geoalchemy2.shape import to_shape
from shapely.geometry import Polygon

from app.schemas.field import Coordinate


def coordinates_to_wkt(coords: Sequence[Coordinate]) -> str:
    """Build a closed WKT POLYGON from frontend coordinates (lat/lng → lng lat)."""
    points: List[Tuple[float, float]] = [(c.lng, c.lat) for c in coords]
    # Close the ring if needed
    if points[0] != points[-1]:
        points.append(points[0])
    ring = ", ".join(f"{lng} {lat}" for lng, lat in points)
    return f"POLYGON(({ring}))"


def coordinates_to_wkt_element(coords: Sequence[Coordinate]) -> WKTElement:
    return WKTElement(coordinates_to_wkt(coords), srid=4326)


def geom_to_coordinates(geom) -> List[Coordinate]:
    """Extract outer ring as [{lat, lng}, ...] (without closing point)."""
    if geom is None:
        return []
    shape = to_shape(geom)
    if not isinstance(shape, Polygon):
        return []
    # exterior.coords is (lng, lat); drop the closing point
    coords = list(shape.exterior.coords)[:-1]
    return [Coordinate(lat=lat, lng=lng) for lng, lat in coords]


def polygon_centre(coords: Sequence[Coordinate]) -> Tuple[float, float]:
    if not coords:
        return 0.0, 0.0
    lat = sum(c.lat for c in coords) / len(coords)
    lng = sum(c.lng for c in coords) / len(coords)
    return lat, lng
