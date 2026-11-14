
import json
from pathlib import Path

# ==========================================
# 1. Load Heatmap Result
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent
RESULT_PATH = PROJECT_DIR / "heatmap_result.json"

with open(RESULT_PATH, "r", encoding="utf-8") as file:
    data = json.load(file)

print("File loaded successfully!")

# ==========================================
# 2. Inspect Result Structure
# ==========================================

print("\n========== RESULT STRUCTURE ==========")

result = data.get("result", {})

print("Result type:", type(result).__name__)

if isinstance(result, dict):
    print("Result keys:", list(result.keys()))

# ==========================================
# 3. Inspect Map Data
# ==========================================

print("\n========== MAP DATA ==========")

map_data = result.get("map_data")

if isinstance(map_data, dict):
    print("Map type:", map_data.get("type"))

    features = map_data.get("features", [])

    print("Number of features:", len(features))

    if features:
        print("\nFirst feature:")
        print(json.dumps(features[0], indent=4)[:2000])

else:
    print("Map data type:", type(map_data).__name__)

# ==========================================
# 4. Inspect Temperature Statistics
# ==========================================

print("\n========== STATISTICS DATA ==========")

stats_data = result.get("stats_data")

if isinstance(stats_data, dict):
    print("Statistics keys:", list(stats_data.keys()))

    print("\nStatistics content:")
    print(json.dumps(stats_data, indent=4)[:5000])

else:
    print("Stats data type:", type(stats_data).__name__)
    print("Stats data:", stats_data)


# ==========================================
# 5. Deep Data Quality Analysis
# ==========================================

print("\n========== DATA QUALITY CHECK ==========")

features = map_data.get("features", [])

# Extract temperature properties
avg_temps = []
min_temps = []
max_temps = []

missing_properties = 0

for feature in features:
    properties = feature.get("properties", {})

    avg = properties.get("average_temperature")
    min_temp = properties.get("min_temperature")
    max_temp = properties.get("max_temperature")

    if avg is not None:
        avg_temps.append(avg)

    if min_temp is not None:
        min_temps.append(min_temp)

    if max_temp is not None:
        max_temps.append(max_temp)

    if avg is None or min_temp is None or max_temp is None:
        missing_properties += 1

print("Total features:", len(features))
print("Features with missing temperature fields:", missing_properties)

if avg_temps:
    print("\nAverage Temperature Across Features:")
    print("Minimum:", min(avg_temps))
    print("Maximum:", max(avg_temps))
    print("Mean:", sum(avg_temps) / len(avg_temps))

if min_temps:
    print("\nLocal Minimum Temperature:")
    print("Minimum:", min(min_temps))
    print("Maximum:", max(min_temps))

if max_temps:
    print("\nLocal Maximum Temperature:")
    print("Minimum:", min(max_temps))
    print("Maximum:", max(max_temps))

# Compare with aggregated statistics
if stats_data and avg_temps:
    api_stats = stats_data.get("temperature_stats", {})

    calculated_mean = sum(avg_temps) / len(avg_temps)
    api_mean = api_stats.get("mean")

    print("\n========== AGGREGATE COMPARISON ==========")
    print("Calculated feature mean:", calculated_mean)
    print("API aggregate mean:", api_mean)

    if api_mean is not None:
        print("Mean difference:", abs(calculated_mean - api_mean))

# Check GeoJSON geometry
invalid_geometries = 0

for feature in features:
    geometry = feature.get("geometry", {})

    if geometry.get("type") != "Polygon":
        invalid_geometries += 1
        continue

    coordinates = geometry.get("coordinates", [])

    if not coordinates or not coordinates[0]:
        invalid_geometries += 1
        continue

    ring = coordinates[0]

    if ring[0] != ring[-1]:
        invalid_geometries += 1

print("\nInvalid geometries:", invalid_geometries)

# Distribution array lengths
distribution = stats_data.get(
    "normal_temperature_distribution", {}
)

x_axis = distribution.get("x_axis", [])
y_axis = distribution.get("y_axis", [])

print("\n========== DISTRIBUTION CHECK ==========")
print("X-axis values:", len(x_axis))
print("Y-axis values:", len(y_axis))
print("Same length:", len(x_axis) == len(y_axis))

# ==========================================
# 6. Data Visualization
# ==========================================

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from matplotlib.collections import PolyCollection

# Get data from the API result
map_data = result.get("map_data", {})
stats_data = result.get("stats_data", {})

features = map_data.get("features", [])

# Save charts in a separate folder
OUTPUT_DIR = Path(__file__).resolve().parent / "visualizations"
OUTPUT_DIR.mkdir(exist_ok=True)

# Extract valid average temperatures
tile_temperatures = [
    feature["properties"]["average_temperature"]
    for feature in features
    if isinstance(feature.get("properties", {}).get("average_temperature"), (int, float))
]

# ------------------------------------------
# Chart 1: Temperature Histogram
# ------------------------------------------

plt.figure(figsize=(10, 5))

plt.hist(tile_temperatures, bins=15, edgecolor="black")

plt.title("Temperature Distribution - Lower Manhattan")
plt.xlabel("Average Temperature (°C)")
plt.ylabel("Number of Tiles")
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "temperature_histogram.png", dpi=150)
plt.show()
plt.close()


# ------------------------------------------
# Chart 2: Normal Temperature Distribution
# ------------------------------------------

distribution = stats_data.get("normal_temperature_distribution", {})

x_axis = distribution.get("x_axis", [])
y_axis = distribution.get("y_axis", [])

if len(x_axis) == len(y_axis) and len(x_axis) > 0:

    plt.figure(figsize=(10, 5))

    plt.plot(x_axis, y_axis)

    plt.title("Normal Temperature Distribution")
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Distribution Density")
    plt.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "normal_distribution.png", dpi=150)
    plt.show()
    plt.close()


# ------------------------------------------
# Chart 3: Geographic Heatmap
# ------------------------------------------

polygons = []
polygon_temperatures = []

for feature in features:

    geometry = feature.get("geometry", {})
    properties = feature.get("properties", {})

    if geometry.get("type") != "Polygon":
        continue

    coordinates = geometry.get("coordinates", [])

    if not coordinates:
        continue

    # GeoJSON coordinates are [longitude, latitude]
    outer_ring = coordinates[0]

    temperature = properties.get("average_temperature")

    if temperature is None:
        continue

    polygons.append(outer_ring)
    polygon_temperatures.append(temperature)


fig, ax = plt.subplots(figsize=(10, 10))

collection = PolyCollection(
    polygons,
    array=np.array(polygon_temperatures),
    cmap="coolwarm",
    edgecolors="black",
    linewidths=0.15
)

ax.add_collection(collection)
ax.autoscale_view()

ax.set_title("Temperature Heatmap - Lower Manhattan")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_aspect("equal", adjustable="datalim")

colorbar = fig.colorbar(collection, ax=ax)
colorbar.set_label("Average Temperature (°C)")

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "geographic_heatmap.png", dpi=150)
plt.show()
plt.close()

print("\nAll visualizations saved in:", OUTPUT_DIR)
