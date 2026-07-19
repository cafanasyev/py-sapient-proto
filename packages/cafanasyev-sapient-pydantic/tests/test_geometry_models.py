"""Round-trips for location/range_bearing/velocity models."""
import pytest
from sapient_msg.bsi_flex_335_v2_0 import location_pb2, range_bearing_pb2, velocity_pb2
from sapient_msg_pydantic._options import IcdValidationError
from sapient_msg_pydantic.bsi_flex_335_v2_0.location import Location, LocationList
from sapient_msg_pydantic.bsi_flex_335_v2_0.range_bearing import (
    LocationOrRangeBearing,
    RangeBearing,
    RangeBearingCone,
)
from sapient_msg_pydantic.bsi_flex_335_v2_0.velocity import (
    ENUVelocity,
    ENUVelocityUnits,
)

# ---------------------------------------------------------------------------
# location.Location
# ---------------------------------------------------------------------------


def _native_location_pb2() -> location_pb2.Location:
    msg = location_pb2.Location(
        x=1.5,
        y=-2.5,
        coordinate_system=location_pb2.LocationCoordinateSystem.LOCATION_COORDINATE_SYSTEM_LAT_LNG_DEG_M,
        datum=location_pb2.LocationDatum.LOCATION_DATUM_WGS84_E,
    )
    msg.z = 10.0
    msg.x_error = 0.1
    msg.y_error = 0.2
    msg.z_error = 0.3
    msg.utm_zone = "30N"
    return msg


def _native_location_model() -> Location:
    return Location(
        x=1.5,
        y=-2.5,
        z=10.0,
        x_error=0.1,
        y_error=0.2,
        z_error=0.3,
        coordinate_system=location_pb2.LocationCoordinateSystem.LOCATION_COORDINATE_SYSTEM_LAT_LNG_DEG_M,
        datum=location_pb2.LocationDatum.LOCATION_DATUM_WGS84_E,
        utm_zone="30N",
    )


def test_location_to_pb2_matches_native() -> None:
    assert _native_location_model().to_pb2() == _native_location_pb2()


def test_location_from_pb2_matches_native() -> None:
    assert Location.from_pb2(_native_location_pb2()) == _native_location_model()


def test_location_double_roundtrip() -> None:
    model = _native_location_model()
    assert Location.from_pb2(model.to_pb2()) == model


def test_location_unset_optionals_stay_unset() -> None:
    pb = Location(
        x=1.0,
        y=2.0,
        coordinate_system=location_pb2.LocationCoordinateSystem.LOCATION_COORDINATE_SYSTEM_LAT_LNG_DEG_M,
        datum=location_pb2.LocationDatum.LOCATION_DATUM_WGS84_E,
    ).to_pb2()
    assert not pb.HasField("z")
    assert Location.from_pb2(pb).z is None


# ---------------------------------------------------------------------------
# location.LocationList
# ---------------------------------------------------------------------------


def _native_location_list_pb2() -> location_pb2.LocationList:
    msg = location_pb2.LocationList()
    msg.locations.extend([_native_location_pb2()])
    return msg


def _native_location_list_model() -> LocationList:
    return LocationList(locations=[_native_location_model()])


def test_location_list_to_pb2_matches_native() -> None:
    assert _native_location_list_model().to_pb2() == _native_location_list_pb2()


def test_location_list_from_pb2_matches_native() -> None:
    assert (
        LocationList.from_pb2(_native_location_list_pb2())
        == _native_location_list_model()
    )


def test_location_list_double_roundtrip() -> None:
    model = _native_location_list_model()
    assert LocationList.from_pb2(model.to_pb2()) == model


def test_location_list_requires_locations() -> None:
    # `locations` is mandatory (empty list counts as unset); no HasField
    # exists for a repeated field, so the "stays unset" contract here is
    # enforced via _require_mandatory() instead.
    with pytest.raises(IcdValidationError, match="locations"):
        LocationList(locations=[]).to_pb2()


# ---------------------------------------------------------------------------
# range_bearing.RangeBearing
# ---------------------------------------------------------------------------


def _native_range_bearing_pb2() -> range_bearing_pb2.RangeBearing:
    msg = range_bearing_pb2.RangeBearing(
        coordinate_system=range_bearing_pb2.RangeBearingCoordinateSystem.RANGE_BEARING_COORDINATE_SYSTEM_DEGREES_M,
        datum=range_bearing_pb2.RangeBearingDatum.RANGE_BEARING_DATUM_TRUE,
    )
    msg.elevation = 1.1
    msg.azimuth = 2.2
    msg.range = 3.3
    msg.elevation_error = 0.1
    msg.azimuth_error = 0.2
    msg.range_error = 0.3
    return msg


def _native_range_bearing_model() -> RangeBearing:
    return RangeBearing(
        elevation=1.1,
        azimuth=2.2,
        range=3.3,
        elevation_error=0.1,
        azimuth_error=0.2,
        range_error=0.3,
        coordinate_system=range_bearing_pb2.RangeBearingCoordinateSystem.RANGE_BEARING_COORDINATE_SYSTEM_DEGREES_M,
        datum=range_bearing_pb2.RangeBearingDatum.RANGE_BEARING_DATUM_TRUE,
    )


def test_range_bearing_to_pb2_matches_native() -> None:
    assert _native_range_bearing_model().to_pb2() == _native_range_bearing_pb2()


def test_range_bearing_from_pb2_matches_native() -> None:
    assert (
        RangeBearing.from_pb2(_native_range_bearing_pb2())
        == _native_range_bearing_model()
    )


def test_range_bearing_double_roundtrip() -> None:
    model = _native_range_bearing_model()
    assert RangeBearing.from_pb2(model.to_pb2()) == model


def test_range_bearing_unset_optionals_stay_unset() -> None:
    pb = RangeBearing(
        coordinate_system=range_bearing_pb2.RangeBearingCoordinateSystem.RANGE_BEARING_COORDINATE_SYSTEM_DEGREES_M,
        datum=range_bearing_pb2.RangeBearingDatum.RANGE_BEARING_DATUM_TRUE,
    ).to_pb2()
    assert not pb.HasField("elevation")
    assert RangeBearing.from_pb2(pb).elevation is None


# ---------------------------------------------------------------------------
# range_bearing.RangeBearingCone
# ---------------------------------------------------------------------------


def _native_range_bearing_cone_pb2() -> range_bearing_pb2.RangeBearingCone:
    msg = range_bearing_pb2.RangeBearingCone(
        coordinate_system=range_bearing_pb2.RangeBearingCoordinateSystem.RANGE_BEARING_COORDINATE_SYSTEM_RADIANS_M,
        datum=range_bearing_pb2.RangeBearingDatum.RANGE_BEARING_DATUM_MAGNETIC,
    )
    msg.elevation = 1.1
    msg.azimuth = 2.2
    msg.range = 3.3
    msg.horizontal_extent = 4.4
    msg.vertical_extent = 5.5
    msg.horizontal_extent_error = 0.4
    msg.vertical_extent_error = 0.5
    msg.elevation_error = 0.1
    msg.azimuth_error = 0.2
    msg.range_error = 0.3
    return msg


def _native_range_bearing_cone_model() -> RangeBearingCone:
    return RangeBearingCone(
        elevation=1.1,
        azimuth=2.2,
        range=3.3,
        horizontal_extent=4.4,
        vertical_extent=5.5,
        horizontal_extent_error=0.4,
        vertical_extent_error=0.5,
        elevation_error=0.1,
        azimuth_error=0.2,
        range_error=0.3,
        coordinate_system=range_bearing_pb2.RangeBearingCoordinateSystem.RANGE_BEARING_COORDINATE_SYSTEM_RADIANS_M,
        datum=range_bearing_pb2.RangeBearingDatum.RANGE_BEARING_DATUM_MAGNETIC,
    )


def test_range_bearing_cone_to_pb2_matches_native() -> None:
    assert (
        _native_range_bearing_cone_model().to_pb2() == _native_range_bearing_cone_pb2()
    )


def test_range_bearing_cone_from_pb2_matches_native() -> None:
    assert (
        RangeBearingCone.from_pb2(_native_range_bearing_cone_pb2())
        == _native_range_bearing_cone_model()
    )


def test_range_bearing_cone_double_roundtrip() -> None:
    model = _native_range_bearing_cone_model()
    assert RangeBearingCone.from_pb2(model.to_pb2()) == model


def test_range_bearing_cone_unset_optionals_stay_unset() -> None:
    pb = RangeBearingCone(
        coordinate_system=range_bearing_pb2.RangeBearingCoordinateSystem.RANGE_BEARING_COORDINATE_SYSTEM_RADIANS_M,
        datum=range_bearing_pb2.RangeBearingDatum.RANGE_BEARING_DATUM_MAGNETIC,
    ).to_pb2()
    assert not pb.HasField("horizontal_extent")
    assert RangeBearingCone.from_pb2(pb).horizontal_extent is None


# ---------------------------------------------------------------------------
# range_bearing.LocationOrRangeBearing
# ---------------------------------------------------------------------------


def _native_location_or_range_bearing_pb2() -> range_bearing_pb2.LocationOrRangeBearing:
    msg = range_bearing_pb2.LocationOrRangeBearing()
    msg.range_bearing.CopyFrom(_native_range_bearing_cone_pb2())
    return msg


def _native_location_or_range_bearing_model() -> LocationOrRangeBearing:
    return LocationOrRangeBearing(range_bearing=_native_range_bearing_cone_model())


def test_location_or_range_bearing_to_pb2_matches_native() -> None:
    assert (
        _native_location_or_range_bearing_model().to_pb2()
        == _native_location_or_range_bearing_pb2()
    )


def test_location_or_range_bearing_from_pb2_matches_native() -> None:
    assert (
        LocationOrRangeBearing.from_pb2(_native_location_or_range_bearing_pb2())
        == _native_location_or_range_bearing_model()
    )


def test_location_or_range_bearing_double_roundtrip() -> None:
    model = _native_location_or_range_bearing_model()
    assert LocationOrRangeBearing.from_pb2(model.to_pb2()) == model


def test_location_or_range_bearing_unset_optionals_stay_unset() -> None:
    pb = _native_location_or_range_bearing_model().to_pb2()
    assert not pb.HasField("location_list")
    assert LocationOrRangeBearing.from_pb2(pb).location_list is None


def test_location_or_range_bearing_location_list_variant_roundtrips() -> None:
    model = LocationOrRangeBearing(location_list=_native_location_list_model())
    pb = model.to_pb2()
    assert pb.HasField("location_list")
    assert not pb.HasField("range_bearing")
    assert LocationOrRangeBearing.from_pb2(pb) == model


# ---------------------------------------------------------------------------
# velocity.ENUVelocity
# ---------------------------------------------------------------------------


def _native_enu_velocity_pb2() -> velocity_pb2.ENUVelocity:
    msg = velocity_pb2.ENUVelocity(east_rate=1.0, north_rate=2.0)
    msg.up_rate = 3.0
    msg.east_rate_error = 0.1
    msg.north_rate_error = 0.2
    msg.up_rate_error = 0.3
    return msg


def _native_enu_velocity_model() -> ENUVelocity:
    return ENUVelocity(
        east_rate=1.0,
        north_rate=2.0,
        up_rate=3.0,
        east_rate_error=0.1,
        north_rate_error=0.2,
        up_rate_error=0.3,
    )


def test_enu_velocity_to_pb2_matches_native() -> None:
    assert _native_enu_velocity_model().to_pb2() == _native_enu_velocity_pb2()


def test_enu_velocity_from_pb2_matches_native() -> None:
    assert (
        ENUVelocity.from_pb2(_native_enu_velocity_pb2()) == _native_enu_velocity_model()
    )


def test_enu_velocity_double_roundtrip() -> None:
    model = _native_enu_velocity_model()
    assert ENUVelocity.from_pb2(model.to_pb2()) == model


def test_enu_velocity_unset_optionals_stay_unset() -> None:
    pb = ENUVelocity(east_rate=1.0, north_rate=2.0).to_pb2()
    assert not pb.HasField("up_rate")
    assert ENUVelocity.from_pb2(pb).up_rate is None


# ---------------------------------------------------------------------------
# velocity.ENUVelocityUnits
# ---------------------------------------------------------------------------


def _native_enu_velocity_units_pb2() -> velocity_pb2.ENUVelocityUnits:
    msg = velocity_pb2.ENUVelocityUnits(
        east_north_rate_units=velocity_pb2.SpeedUnits.SPEED_UNITS_MS,
    )
    msg.up_rate_units = velocity_pb2.SpeedUnits.SPEED_UNITS_KPH
    return msg


def _native_enu_velocity_units_model() -> ENUVelocityUnits:
    return ENUVelocityUnits(
        east_north_rate_units=velocity_pb2.SpeedUnits.SPEED_UNITS_MS,
        up_rate_units=velocity_pb2.SpeedUnits.SPEED_UNITS_KPH,
    )


def test_enu_velocity_units_to_pb2_matches_native() -> None:
    assert (
        _native_enu_velocity_units_model().to_pb2()
        == _native_enu_velocity_units_pb2()
    )


def test_enu_velocity_units_from_pb2_matches_native() -> None:
    assert (
        ENUVelocityUnits.from_pb2(_native_enu_velocity_units_pb2())
        == _native_enu_velocity_units_model()
    )


def test_enu_velocity_units_double_roundtrip() -> None:
    model = _native_enu_velocity_units_model()
    assert ENUVelocityUnits.from_pb2(model.to_pb2()) == model


def test_enu_velocity_units_unset_optionals_stay_unset() -> None:
    pb = ENUVelocityUnits(
        east_north_rate_units=velocity_pb2.SpeedUnits.SPEED_UNITS_MS,
    ).to_pb2()
    assert not pb.HasField("up_rate_units")
    assert ENUVelocityUnits.from_pb2(pb).up_rate_units is None
