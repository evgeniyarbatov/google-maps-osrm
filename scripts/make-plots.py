import gpxpy
import sys
import os

import pandas as pd

import matplotlib.pyplot as plt
import contextily as ctx


def parse_gpx(filepath):
    gpx_file = open(filepath, "r")
    gpx = gpxpy.parse(gpx_file)

    data = []

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                lat, lng = (
                    point.latitude,
                    point.longitude,
                )

                data.append(
                    {
                        "latitude": lat,
                        "longitude": lng,
                    }
                )

    df = pd.DataFrame(data)

    return df


GPX_DIR = "../gpx/"


def main(args):
    destinations = os.listdir(GPX_DIR)

    for destination in destinations:
        dir = os.path.join(GPX_DIR, destination)

        maps_df = parse_gpx(dir + "/google-maps/route.gpx")
        osrm_df = parse_gpx(dir + "/osrm/route.gpx")

        plt.figure(figsize=(15, 8))

        plt.plot(
            maps_df["longitude"], maps_df["latitude"], color="blue", label="Google Maps"
        )
        plt.plot(osrm_df["longitude"], osrm_df["latitude"], color="red", label="OSRM")
        ctx.add_basemap(
            plt.gca(), crs="EPSG:4326", source=ctx.providers.OpenStreetMap.Mapnik
        )

        plt.legend()
        plt.xticks([], [])
        plt.yticks([], [])
        plt.tick_params(
            axis="both", which="both", bottom=False, top=False, left=False, right=False
        )

        plt.savefig(dir + "/" + "maps.png", bbox_inches="tight", pad_inches=0)


if __name__ == "__main__":
    main(sys.argv[1:])
