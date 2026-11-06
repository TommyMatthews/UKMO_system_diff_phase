# config.py

from dp_helpers import radar_number_map

# Select radars (must match keys in radar_number_map)
#radars = list(radar_number_map.keys())
radars = ['chenies']

# Select years
years = ['2019', '2020', '2021']# '2023', '2024', '2025']

# Select times (HHMM)
times = [
    f"{h:02d}{m:02d}"
    for h in [0,6,12,18]#range(24)
    for m in range(0, 60, 10)
]

# Range limits (km)
rmin = 10
rmax = 30

# Elevation angles
eles = [0, 1, 2, 3, 4]

# Maximum simultaneous jobs
max_concurrent = 20

# Maximum tasks per submitted array
chunk_size = 1000