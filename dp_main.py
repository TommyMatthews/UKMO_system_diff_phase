import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import pandas as pd
import h5py as h5
import glob
from datetime import datetime
from diff_phase_estimator import get_drizzly_phiDPs
from nimrod_reader import read_nimrod_aggregated_odim_h5, _get_radar_name_from_radar_numer
from dp_helpers import get_date, get_radar_number
import argparse
import os
import re


def list_of_ints(arg):
    return list(map(int, arg.split(',')))

def get_arguments():
    """
    Retrieve four arguments from user input:
    - radar (r)
    - year (y)
    - day of year (d)
    - time (t)
    - r_min (rmin)
    - r_max (rmax)
    - elevation angles (e):list of elevation angles
    """
    parser = argparse.ArgumentParser(description='Retrieve radar file and time arguments')
    
    parser.add_argument('-r', '--radar', 
                       dest='radar',
                       type=str, 
                       required=True,
                       help='radar name')
    
    parser.add_argument('-y', '--year',
                       dest='year',
                       type=str,
                       required=True,
                       help='year')
    
    parser.add_argument('-d', '--day_of_year',
                       dest='day',
                       type=str,
                       required=True,
                       help='day of year in format mmdd')
    
    parser.add_argument('-t', '--time',
                       dest='time',
                       type=str,
                       required=True,
                       help='time of scan (e.g. 1050)')

    parser.add_argument('-rmin', '--r_min',
                       dest='rmin',
                       type=int,
                       required=True,
                       help='minimum range in km')

    parser.add_argument('-rmax', '--r_max',
                       dest='rmax',
                       type=int,
                       required=True,
                       help='maximum range in km')
    
    
    parser.add_argument('-e', '--elevation_angles',
                       dest='elev_angles',
                       type=list_of_ints,
                       required=True,
                       help='list of elevation angles e.g "0,1,2"')
    
    args = parser.parse_args()

    return args.radar, args.year, args.day, args.time, args.rmin, args.rmax, args.elev_angles


def generate_radar_file_path(radar, year, day, number):
    
    file_path= f'/gws/ssde/j25a/ncas_radar/vol2/avocet/ukmo-nimrod/raw_h5_data_final/single-site/{radar}/{year}/{year}{day}_polar_pl_radar{number}_aggregate.h5'

    return file_path


#TODO edit to allow for r_min r_max
def get_specific_time_phiDP_ds(file, year, time, r_min, r_max, ele):
    '''
    ranges in km! 
    '''

    date = get_date(year, file)
    try:
        radar = read_nimrod_aggregated_odim_h5(file, 'lp', time)
    except KeyError as exc:
        raise FileNotFoundError(
            f'Could not read radar data: {file}, time {time}'
        ) from exc

    r_min_m = r_min*1000
    r_max_m = r_max*1000
    
    phiDP, ranges, azimuths, Ze, Zdr, Rhv = get_drizzly_phiDPs(radar, r_min_m, r_max_m, ele)

    # Flatten PhiDP
    phiDP_1d = phiDP.flatten()
    # Ze_1d = Ze.flatten()
    # Zdr_1d = Zdr.flatten()
    # Rhv_1d = Rhv.flatten()

    # Expand range and azimuth labels to match PhiDP
    ranges_1d = np.repeat(ranges, len(azimuths))
    azimuths_1d = np.tile(azimuths, len(ranges))

    full_times = np.full(len(phiDP_1d), time, dtype=object)
    full_date = np.full(len(phiDP_1d), date)
    full_elevation = np.full(len(phiDP_1d), ele)

    ds = xr.Dataset(
        data_vars={
            'PhiDP': (['measurement_index'], phiDP_1d),
            # 'Ze': (['measurement_index'], Ze_1d),
            # 'Zdr': (['measurement_index'], Zdr_1d),
            # 'Rhv': (['measurement_index'], Rhv_1d)
        },
        coords={
            'range': ('measurement_index', ranges_1d),
            'azimuth': ('measurement_index', azimuths_1d),
            'time': ('measurement_index', full_times),
            'date': ('measurement_index', full_date),
            'elevation' : ('measurement_index', full_elevation),
        }
    )

    return ds

def generate_folder_path(radar, year,day,time):
    base_path = '/gws/ssde/j25a/ncas_radar/vol1/tommy/sys_diff_phase_estimates/raw_extracts/'
    path_elements = [radar, year, day, time] 
    save_path = os.path.join(base_path, *path_elements)
    
    if not os.path.isdir(save_path):
        os.makedirs(save_path)
    
    return save_path
    
# TODO: write this
def save_ds(ds, save_path, r_min, r_max, ele):
    file_name = f'phidp_vals_{r_min}km_to_{r_max}km_{ele}_ele.nc'
    file_path = os.path.join(save_path, file_name)
    ds.to_netcdf(file_path)


if __name__ == '__main__':

    r, y, d, t, rmin, rmax, e_list = get_arguments()
    radar_num = get_radar_number(r)
    file_path = generate_radar_file_path(r, y, d, radar_num)

    folder_save_path = generate_folder_path(r,y,d,t)
    for e in e_list:
        print(f'Running elevation {e}')
        ds = get_specific_time_phiDP_ds(file_path, y, t, rmin, rmax, e)
        print(f'Saving elevation {e}')
        save_ds(ds, folder_save_path, rmin, rmax, e)
        