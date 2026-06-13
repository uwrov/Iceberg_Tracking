import argparse
import math
import sys

NM_PER_DEG_LAT = 60.0  # 1 minute of latitude = 1 nautical mile
PLATFORM_COUNT = 4


def lat_lon_to_nm(lat, lon, origin_lat, origin_lon):
    mean_lat_rad = math.radians((lat + origin_lat) / 2.0)
    east_nm = (lon - origin_lon) * NM_PER_DEG_LAT * math.cos(mean_lat_rad)
    north_nm = (lat - origin_lat) * NM_PER_DEG_LAT
    return east_nm, north_nm


def track_distance_nm( iceberg_lat, iceberg_lon, heading_deg, platform_lat, platform_lon):
    east_nm, north_nm = lat_lon_to_nm(
        platform_lat, platform_lon, iceberg_lat, iceberg_lon
    )
    heading_rad = math.radians(heading_deg)
    track_east = math.sin(heading_rad)
    track_north = math.cos(heading_rad)

    along_track = east_nm * track_east + north_nm * track_north
    closest_east = along_track * track_east
    closest_north = along_track * track_north
    perp_east = east_nm - closest_east
    perp_north = north_nm - closest_north
    return math.hypot(perp_east, perp_north)


def surface_threat(distance_nm, keel_m, water_depth_m):
    if keel_m / water_depth_m >= 1.10:
        return "GREEN"
    if distance_nm > 10:
        return "GREEN"
    if distance_nm >= 5:
        return "YELLOW"
    return "RED"


def subsea_threat(distance_nm, keel_m, water_depth_m):
    if distance_nm > 25:
        return "GREEN"
    ratio = keel_m / water_depth_m
    if ratio >= 1.10:
        return "GREEN"
    if ratio >= 0.90:
        return "RED"
    if ratio >= 0.70:
        return "YELLOW"
    return "GREEN"

def parse_platform(value):

    parts = [part.strip() for part in value.split(",")]
    name, lat, lon, depth = parts[0], float(parts[1]), float(parts[2]), float(parts[3])
    return {
        "name": name,
        "lat": lat,
        "lon": lon,
        "depth_m": abs(depth),
    }


def evaluate(iceberg_lat, iceberg_lon, heading_deg, keel_m, platforms):
    results = []
    for platform in platforms:
        distance = track_distance_nm(
            iceberg_lat,
            iceberg_lon,
            heading_deg,
            platform["lat"],
            platform["lon"],
        )
        depth = platform["depth_m"]
        keel_ratio = keel_m / depth
        results.append(
            {
                "platform": platform["name"],
                "distance_nm": distance,
                "water_depth_m": depth,
                "keel_ratio": keel_ratio,
                "surface": surface_threat(distance, keel_m, depth),
                "subsea": subsea_threat(distance, keel_m, depth),
            }
        )
    return results


def print_results(results):
    for row in results:
        print(
            f"{row['platform']}: Surface {row['surface']}, Subsea {row['subsea']}"
        )


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Calculate iceberg threat levels for MATE ROV 2026 oil platforms."
    )
    parser.add_argument("--lat", type=float, required=True, help="Iceberg latitude (deg N)")
    parser.add_argument("--lon", type=float, required=True, help="Iceberg longitude (deg W)")
    parser.add_argument(
        "--heading",
        type=float,
        required=True,
        help="Iceberg heading in degrees from true north, clockwise",
    )
    parser.add_argument("--keel", type=float, required=True, help="Iceberg keel depth (m)")
    parser.add_argument(
        "--platform",
        action="append",
        type=parse_platform,
        required=True,
        metavar="NAME,LAT,LON,DEPTH",
        help=(
            "Platform data as name,lat,lon,depth. "
            "Repeat 4 times (example: --platform Hibernia,43.7504,-48.7819,78)"
        ),
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv or sys.argv[1:])

    if len(args.platform) != PLATFORM_COUNT:
        print(
            f"Error: provide exactly {PLATFORM_COUNT} --platform entries "
            f"(got {len(args.platform)}).",
            file=sys.stderr,
        )
        return 1

    results = evaluate(args.lat, args.lon, args.heading, args.keel, args.platform)
    print_results(results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
