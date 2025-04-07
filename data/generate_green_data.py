import pandas as pd

data = {
    "Neighborhood": [
        "Central Park", "Midtown", "Riverside", "North Hill", "Southgate", "Old Town",
        "Lakeside", "West End", "East Village", "Harbor Bay", "Maple Heights", "Hillview"
    ],
    "Population": [120000, 85000, 70000, 65000, 90000, 50000, 40000, 60000, 75000, 48000, 55000, 68000],
    "Area_km2": [3.2, 2.5, 3.5, 2.8, 3.0, 1.9, 2.1, 2.4, 2.9, 2.6, 2.0, 3.1],
    "Green_Area_km2": [1.2, 0.6, 2.0, 0.7, 0.5, 0.4, 0.8, 1.0, 0.9, 0.3, 0.6, 0.5],
    "Lat": [40.78, 40.75, 40.79, 40.80, 40.74, 40.73, 40.81, 40.76, 40.72, 40.77, 40.79, 40.71],
    "Lon": [-73.97, -73.99, -73.95, -73.93, -73.98, -74.00, -73.91, -73.96, -73.94, -73.90, -73.92, -74.01]
}

df = pd.DataFrame(data)

df["Green_Cover_%"] = (df["Green_Area_km2"] / df["Area_km2"]) * 100
df["People_per_green_km2"] = df["Population"] / df["Green_Area_km2"]

df["Recommendation"] = df.apply(
    lambda row: "Add Green Space" if row["Green_Cover_%"] < 30 or row["People_per_green_km2"] > 50000 else "Sufficient",
    axis=1
)

df.to_csv("data/green_space_data.csv", index=False)
print("✅ green_space_data.csv regenerated with coordinates.")
