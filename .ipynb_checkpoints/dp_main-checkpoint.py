import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import pandas as pd
import h5py as h5
import glob
from datetime import datetime
from diff_phase_estimator import get_drizzly_phiDPs
from nimrod_reader import read_nimrod_aggregated_odim_h5
from dp_helpers import get_date

#TODO: write get radar num function
radar = ' '
file = ' '
time = ' ' 

def get_specific_time_phiDP_ds(file, time):

    date = get_date(year, file)

    try:
        radar = read_nimrod_aggregated_odim_h5(file, 'lp', time)
    except KeyError:
        return None

    phiDP, ranges, azimuths = get_drizzly_phiDPs(radar, 10000, 30000)

    # Flatten PhiDP
    phiDP_1d = phiDP.flatten()

    # Expand range and azimuth labels to match PhiDP
    ranges_1d = np.repeat(ranges, len(azimuths))
    azimuths_1d = np.tile(azimuths, len(ranges))

    time = datetime.strptime(time, '%H%M').time()
    full_times = np.full(len(phiDP_1d), time, dtype=object)
    full_date = np.full(len(phiDP_1d), date)

    ds = xr.Dataset(
        data_vars={
            'PhiDP': (['measurement_index'], phiDP_data)
        },
        coords={
            'range': ('measurement_index', day_level_ranges),
            'azimuth': ('measurement_index', day_level_azimuths),
            'time': ('measurement_index', day_level_times),
            'date': ('measurement_index', full_date),
        }
    )

    return ds
  

if __name__ == '__main__':

# TODO: 
# - call function
# - check directory exisits
# - save to radar/year/time folder