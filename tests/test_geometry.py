from app.schemas.field import Coordinate
from app.services.geometry import coordinates_to_wkt, polygon_centre


def test_coordinates_to_wkt_closes_ring():
    coords = [
        Coordinate(lat=-1.14, lng=36.96),
        Coordinate(lat=-1.15, lng=36.96),
        Coordinate(lat=-1.15, lng=36.97),
    ]
    wkt = coordinates_to_wkt(coords)
    assert wkt.startswith("POLYGON((")
    assert wkt.endswith("))")
    # Closed: first point repeated
    assert "36.96 -1.14" in wkt


def test_polygon_centre():
    coords = [
        Coordinate(lat=0.0, lng=0.0),
        Coordinate(lat=0.0, lng=2.0),
        Coordinate(lat=2.0, lng=2.0),
        Coordinate(lat=2.0, lng=0.0),
    ]
    lat, lng = polygon_centre(coords)
    assert lat == 1.0
    assert lng == 1.0
