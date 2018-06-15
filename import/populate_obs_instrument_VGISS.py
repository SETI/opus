################################################################################
# populate_obs_instrument_VGISS.py
#
# Routines to populate fields specific to VGISS. It may change fields in
# obs_general, obs_mission_voyager, or obs_instrument_VGISS.
################################################################################

import numpy as np

import julian
import pdsfile

import import_util

from populate_obs_mission_voyager import *

# Data from: https://pds-rings.seti.org/voyager/iss/inst_cat_wa1.html#inst_info
# (WL MIN, WL MAX)
_VGISS_FILTER_WAVELENGTHS = { # XXX
    'CLEAR':  (280, 640),
    'VIOLET': (350, 450),
    'GREEN':  (530, 640),
    'ORANGE': (590, 640),
    'SODIUM': (588, 590),
    'UV':     (280, 370),
    'BLUE':   (430, 530),
    'CH4_JS': (614, 624),
    'CH4_U':  (536, 546),
}


################################################################################
# THESE NEED TO BE IMPLEMENTED FOR EVERY INSTRUMENT
################################################################################

### OBS_GENERAL TABLE ###

def _VGISS_file_spec_helper(**kwargs):
    metadata = kwargs['metadata']
    index_row = metadata['index_row']
    # Format: "DATA/C13854XX/C1385455_CALIB.LBL"
    file_spec = index_row['FILE_SPECIFICATION_NAME']
    volume_id = kwargs['volume_id']
    return volume_id + '/' + file_spec

def populate_obs_general_VGISS_opus_id(**kwargs):
    file_spec = _VGISS_file_spec_helper(**kwargs)
    pds_file = pdsfile.PdsFile.from_filespec(file_spec)
    try:
        opus_id = pds_file.opus_id
    except:
        metadata = kwargs['metadata']
        index_row = metadata['index_row']
        index_row_num = metadata['index_row_num']
        import_util.announce_nonrepeating_error(
            f'Unable to create OPUS_ID for FILE_SPEC "{file_spec}"',
            index_row_num)
        return file_spec
    return opus_id

# Format: "VOYAGER 1" or "VOYAGER 2"
def populate_obs_general_VGISS_inst_host_id(**kwargs):
    metadata = kwargs['metadata']
    index_row = metadata['index_row']
    inst_host = index_row['INSTRUMENT_HOST_NAME']

    assert inst_host in ['VOYAGER 1', 'VOYAGER 2']

    return 'VG'+inst_host[-1]

def populate_obs_general_VGISS_time1(**kwargs):
    metadata = kwargs['metadata']
    supp_index_row = metadata['supp_index_row']
    if supp_index_row is None:
        return None
    start_time = import_util.safe_column(supp_index_row, 'START_TIME')

    return start_time

def populate_obs_general_VGISS_time2(**kwargs):
    metadata = kwargs['metadata']
    supp_index_row = metadata['supp_index_row']
    if supp_index_row is None:
        return None
    stop_time = import_util.safe_column(supp_index_row, 'STOP_TIME')

    return stop_time

def populate_obs_general_VGISS_target_name(**kwargs):
    target_name = helper_voyager_target_name(**kwargs)
    if target_name is None:
        target_name = 'NONE'
    return target_name

def populate_obs_general_VGISS_observation_duration(**kwargs):
    metadata = kwargs['metadata']
    index_row = metadata['index_row']
    exposure = import_util.safe_column(index_row, 'EXPOSURE_DURATION')

    if exposure is None or exposure < 0:
        # There's one exposure somewhere that has duration -0.09999
        return None

    return exposure / 1000

def populate_obs_general_VGISS_quantity(**kwargs):
    metadata = kwargs['metadata']
    index_row = metadata['index_row']
    filter_name = index_row['FILTER_NAME']

    if filter_name == 'UV':
        return 'EMISSION'
    return 'REFLECT'

def populate_obs_general_VGISS_spatial_sampling(**kwargs):
    return '2D'

def populate_obs_general_VGISS_wavelength_sampling(**kwargs):
    return 'N'

def populate_obs_general_VGISS_time_sampling(**kwargs):
    return 'N'

def populate_obs_general_VGISS_note(**kwargs):
    metadata = kwargs['metadata']
    index_row = metadata['index_row']
    return index_row['NOTE']

def populate_obs_general_VGISS_primary_file_spec(**kwargs):
    return _VGISS_file_spec_helper(**kwargs)

# Format: "VG1/VG2-J-ISS-2/3/4/6-PROCESSED-V1.0"
def populate_obs_general_VGISS_data_set_id(**kwargs):
    # For VGISS the DATA_SET_ID is provided in the volume label file,
    # not the individual observation rows
    metadata = kwargs['metadata']
    index_label = metadata['index_label']
    dsi = index_label['DATA_SET_ID']
    return (dsi, dsi)

def populate_obs_general_VGISS_product_creation_time(**kwargs):
    metadata = kwargs['metadata']
    supp_index_row = metadata['supp_index_row']
    if supp_index_row is None:
        return None
    pct = supp_index_row['PRODUCT_CREATION_TIME']
    return pct

# Format: "C1385455_CALIB.IMG"
def populate_obs_general_VGISS_product_id(**kwargs):
    metadata = kwargs['metadata']
    index_row = metadata['index_row']
    product_id = index_row['PRODUCT_ID']

    return product_id

def populate_obs_general_VGISS_right_asc1(**kwargs):
    metadata = kwargs['metadata']
    ring_geo_row = metadata.get('ring_geo_row', None)
    if ring_geo_row is not None:
        return import_util.safe_column(ring_geo_row, 'MINIMUM_RIGHT_ASCENSION')

    return None

def populate_obs_general_VGISS_right_asc2(**kwargs):
    metadata = kwargs['metadata']
    ring_geo_row = metadata.get('ring_geo_row', None)
    if ring_geo_row is not None:
        return import_util.safe_column(ring_geo_row, 'MAXIMUM_RIGHT_ASCENSION')

    return None

def populate_obs_general_VGISS_declination1(**kwargs):
    metadata = kwargs['metadata']
    ring_geo_row = metadata.get('ring_geo_row', None)
    if ring_geo_row is not None:
        return import_util.safe_column(ring_geo_row, 'MINIMUM_DECLINATION')

    return None

def populate_obs_general_VGISS_declination2(**kwargs):
    metadata = kwargs['metadata']
    ring_geo_row = metadata.get('ring_geo_row', None)
    if ring_geo_row is not None:
        return import_util.safe_column(ring_geo_row, 'MAXIMUM_DECLINATION')

    return None


# Format: "JUPITER ENCOUNTER"
def populate_obs_mission_voyager_VGISS_mission_phase_name(**kwargs):
    metadata = kwargs['metadata']
    index_row = metadata['index_row']
    mp = index_row['MISSION_PHASE_NAME']
    return mp.replace('_', ' ')


### OBS_TYPE_IMAGE TABLE ###

def populate_obs_type_image_VGISS_image_type_id(**kwargs):
    return 'FRAM'

def populate_obs_type_image_VGISS_duration(**kwargs):
    metadata = kwargs['metadata']
    obs_general_row = metadata['obs_general_row']
    return obs_general_row['observation_duration']

# XXX
def populate_obs_type_image_VGISS_levels(**kwargs):
    return 256

def _VGISS_pixel_size_helper(**kwargs):
    metadata = kwargs['metadata']
    supp_index_row = metadata['supp_index_row']
    if supp_index_row is None:
        return None, None
    line1 = supp_index_row['FIRST_LINE']
    line2 = supp_index_row['LAST_LINE']
    sample1 = supp_index_row['FIRST_SAMPLE']
    sample2 = supp_index_row['LAST_SAMPLE']

    return line2-line1+1, sample2-sample1+1

def populate_obs_type_image_VGISS_lesser_pixel_size(**kwargs):
    pix1, pix2 = _VGISS_pixel_size_helper(**kwargs)
    if pix1 is None or pix2 is None:
        return None
    return min(pix1, pix2)

def populate_obs_type_image_VGISS_greater_pixel_size(**kwargs):
    pix1, pix2 = _VGISS_pixel_size_helper(**kwargs)
    if pix1 is None or pix2 is None:
        return None
    return max(pix1, pix2)


### OBS_WAVELENGTH TABLE ###

def _wavelength_helper(**kwargs):
    metadata = kwargs['metadata']
    index_row_num = metadata['index_row_num']
    index_row = metadata['index_row']
    instrument_id = index_row['INSTRUMENT_NAME'][0]
    filter_name = index_row['FILTER_NAME']

    if filter_name not in _VGISS_FILTER_WAVELENGTHS:
        import_util.announce_nonrepeating_error(
            f'Unknown VGISS filter name "{filter_name}" [line {index_row_num}]')
        return 0

    return _VGISS_FILTER_WAVELENGTHS[filter_name]

def populate_obs_wavelength_VGISS_wavelength1(**kwargs):
    return _wavelength_helper(**kwargs)[0] / 1000 # microns

def populate_obs_wavelength_VGISS_wavelength2(**kwargs):
    return _wavelength_helper(**kwargs)[1] / 1000 # microns

def populate_obs_wavelength_VGISS_wave_res1(**kwargs):
    metadata = kwargs['metadata']
    wl_row = metadata['obs_wavelength_row']
    wl1 = wl_row['wavelength1']
    wl2 = wl_row['wavelength2']
    if wl1 is None or wl2 is None:
        return None
    return wl2 - wl1

def populate_obs_wavelength_VGISS_wave_res2(**kwargs):
    metadata = kwargs['metadata']
    wl_row = metadata['obs_wavelength_row']
    wl1 = wl_row['wavelength1']
    wl2 = wl_row['wavelength2']
    if wl1 is None or wl2 is None:
        return None
    return wl2 - wl1

def populate_obs_wavelength_VGISS_wave_no1(**kwargs):
    metadata = kwargs['metadata']
    wavelength_row = metadata['obs_wavelength_row']
    return 10000 / wavelength_row['wavelength2'] # cm^-1

def populate_obs_wavelength_VGISS_wave_no2(**kwargs):
    metadata = kwargs['metadata']
    wavelength_row = metadata['obs_wavelength_row']
    return 10000 / wavelength_row['wavelength1'] # cm^-1

def populate_obs_wavelength_VGISS_wave_no_res1(**kwargs):
    metadata = kwargs['metadata']
    wl_row = metadata['obs_wavelength_row']
    wno1 = wl_row['wave_no1']
    wno2 = wl_row['wave_no2']
    if wno1 is None or wno2 is None:
        return None
    return wno2 - wno1

def populate_obs_wavelength_VGISS_wave_no_res2(**kwargs):
    metadata = kwargs['metadata']
    wl_row = metadata['obs_wavelength_row']
    wno1 = wl_row['wave_no1']
    wno2 = wl_row['wave_no2']
    if wno1 is None or wno2 is None:
        return None
    return wno2 - wno1

def populate_obs_wavelength_VGISS_spec_flag(**kwargs):
    metadata = kwargs['metadata']
    index_row = metadata['obs_general_row']
    return index_row['wavelength_sampling']

def populate_obs_wavelength_VGISS_spec_size(**kwargs):
    return None

def populate_obs_wavelength_VGISS_polarization_type(**kwargs):
    return 'NONE'


################################################################################
# THESE NEED TO BE IMPLEMENTED FOR EVERY VOYAGER INSTRUMENT
################################################################################

def populate_obs_mission_voyager_VGISS_spacecraft_clock_count1(**kwargs):
    metadata = kwargs['metadata']
    supp_index_row = metadata['supp_index_row']
    if supp_index_row is None:
        return None
    partition = import_util.safe_column(supp_index_row,
                                        'SPACECRAFT_CLOCK_PARTITION_NUMBER')
    start_time = supp_index_row['SPACECRAFT_CLOCK_START_COUNT']

    return str(partition) + '/' + start_time

def populate_obs_mission_voyager_VGISS_spacecraft_clock_count2(**kwargs):
    metadata = kwargs['metadata']
    supp_index_row = metadata['supp_index_row']
    if supp_index_row is None:
        return None
    partition = import_util.safe_column(supp_index_row,
                                        'SPACECRAFT_CLOCK_PARTITION_NUMBER')
    stop_time = supp_index_row['SPACECRAFT_CLOCK_STOP_COUNT']

    return str(partition) + '/' + stop_time



################################################################################
# THESE ARE SPECIFIC TO OBS_INSTRUMENT_VGISS
################################################################################

def populate_obs_instrument_VGISS_camera(**kwargs):
    metadata = kwargs['metadata']
    index_row = metadata['index_row']
    obs_general_row = metadata['obs_general_row']
    camera = index_row['INSTRUMENT_NAME']

    assert camera in ['NARROW ANGLE CAMERA', 'WIDE ANGLE CAMERA']

    return camera[0]

def populate_obs_instrument_VGISS_ert(**kwargs):
    metadata = kwargs['metadata']
    index_row = metadata['index_row']
    start_time = index_row['EARTH_RECEIVED_TIME']

    if start_time.startswith('UNK'):
        return None

    return start_time

def populate_obs_instrument_VGISS_ert_sec(**kwargs):
    metadata = kwargs['metadata']
    index_row_num = metadata['index_row_num']
    index_row = metadata['index_row']
    start_time = index_row['EARTH_RECEIVED_TIME']

    if start_time.startswith('UNK'):
        return None

    try:
        ert = julian.tai_from_iso(start_time)
    except (ValueError,TypeError):
        import_util.announce_nonrepeating_error(
            f'"{start_time}" is not a valid date-time format in '+
            f'instrument_VGISS_ert_sec [line {index_row_num}]')
        ert = None
    return ert

def populate_obs_instrument_VGISS_usable_lines(**kwargs):
    metadata = kwargs['metadata']
    supp_index_row = metadata['supp_index_row']
    if supp_index_row is None:
        return None
    line1 = supp_index_row['FIRST_LINE']
    line2 = supp_index_row['LAST_LINE']

    return line2-line1+1

def populate_obs_instrument_VGISS_usable_samples(**kwargs):
    metadata = kwargs['metadata']
    supp_index_row = metadata['supp_index_row']
    if supp_index_row is None:
        return None
    sample1 = supp_index_row['FIRST_SAMPLE']
    sample2 = supp_index_row['LAST_SAMPLE']

    return sample2-sample1+1
