years = ['2019','2020', '2021', '2022', '2023', '2024', '2025']


string_times = [f"{h:02d}{m:02d}" for h in range(24) for m in range(0, 60, 10)]
times = [datetime.strptime(time, '%H%M').time() for time in string_times]

# TODO:
# - WRITE CODE TO GET SELECT ALL RADARS AND YEARS
# - WRITE CODE TO SUBMIT SLURM JOB ARRAY FOR ALL RADAR/YEAR/TIME COMBINATIONS
