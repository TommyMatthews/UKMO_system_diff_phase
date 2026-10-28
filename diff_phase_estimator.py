import matplotlib.pyplot as plt
import numpy
import xarray
import pandas as pd

import pyart
import netCDF4
import h5py as h5
from glob import glob
import os
import numpy as np
import cartopy.crs as ccrs
import warnings
import time
import cartopy.feature as cfeature
import cartopy.io.img_tiles as cimgt
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
#import rasterio
import matplotlib
import wradlib
warnings.filterwarnings("ignore", category=DeprecationWarning)

def clutter_filter(radar):

    full_exclusion_conditions = np.array(
        [
            # radar.fields['SQI']['data'].data < 0.5,
            # radar.fields['normalized_coherent_power']['data'].data > 0.8,
            radar.fields['reflectivity']['data'].data > 35,
            radar.fields['differential_reflectivity']['data'].data>12,
            #radar.fields['differential_reflectivity']['data'].data<=-8
            
            radar.fields['reflectivity']['data'].data < -10,
        ]     
    )  

    excluded =  np.max(full_exclusion_conditions, axis = 0)

    radar.fields['reflectivity']['data'].data[excluded]=np.nan
    radar.fields['differential_reflectivity']['data'].data[excluded]=np.nan
    radar.fields['cross_correlation_ratio']['data'].data[excluded]=np.nan
    radar.fields['differential_phase']['data'].data[excluded]=np.nan
    radar.fields['velocity']['data'].data[excluded]=np.nan
    # radar.fields['normalized_coherent_power']['data'].data[excluded]=np.nan

    return radar

def get_range_restricted_data(radar, field_name, R_min, R_max, ele_index):
    min_gate_index = np.argmin(np.abs(radar.range['data'] - R_min))
    max_gate_index = np.argmin(np.abs(radar.range['data'] - R_max))

    range_indices = np.arange(min_gate_index, max_gate_index + 1)

    start_ray = radar.sweep_start_ray_index['data'][ele_index]
    end_ray = radar.sweep_end_ray_index['data'][ele_index] + 1
    azimuths = radar.azimuth['data'][start_ray:end_ray]
    values_array = np.zeros((len(range_indices),len(azimuths),))
    values_array[:]=np.nan
    range_labels = []

    masks = np.zeros((len(range_indices), len(azimuths)))
    
    for index, gate in enumerate(range_indices):
            field_values = radar.fields[field_name]['data'][start_ray:end_ray, gate]
            values_array[index, :] = field_values[:]
            masks[index, :] = field_values.mask
            range_label = radar.range['data'][gate]/1000
            range_labels.append(range_label)

    masked_values = np.ma.array(values_array,mask=masks)

    return masked_values, range_labels, azimuths
    


def get_drizzly_phiDPs(radar, R_min, R_max):
    
    filtered_radar = clutter_filter(radar)
    Zdr, _,_ = get_range_restricted_data(radar, 'differential_reflectivity', R_min, R_max, 1)
    Rhv, _,_ = get_range_restricted_data(radar, 'cross_correlation_ratio', R_min, R_max, 1)
    PhiDP, _,_ = get_range_restricted_data(radar, 'differential_phase', R_min, R_max, 1)

    full_drizzle_conditions = np.array(
    [
        Zdr < 1,
        Zdr > -1,
        Rhv >0.9
    ]     
    )  

    drizzle_mask = np.min(full_drizzle_conditions, axis = 0)
    PhiDP[~drizzle_mask] = np.nan

    return PhiDP

    
    
    