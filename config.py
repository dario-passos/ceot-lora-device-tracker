LHT65_FIELDS = {
    'bat':'device_frmpayload_data_BatV',
    'hum':'device_frmpayload_data_Hum_SHT',
    'tmp':'device_frmpayload_data_TempC_SHT',
    'ilx':'device_frmpayload_data_ILL_lux'
}

MAX_LHT65_DEVICES = 25


LSE01_FIELDS = {
    'bat': 'device_frmpayload_data_Bat',
    'soil_hum': 'device_frmpayload_data_water_SOIL',
    'soil_cond': 'device_frmpayload_data_conduct_SOIL',
    'soil_tmp':'device_frmpayload_data_temp_SOIL'
}

MAX_LSE01_DEVICES = 6


SIGNAL_FIELDS = ['rssi', 'snr']

MEASUREMENT_OPTIONS = ['mean', 'max', 'min', 'median', 'stddev']


WS_FIELDS = {
    'outsidetmp': 'device_frmpayload_data_OUTSIDETEMPERATURE',
    'outsidehum': 'device_frmpayload_data_OUTSIDEHUMIDITY',
    'solarrad'  : 'device_frmpayload_data_SOLARADIATION',
    'pressure'  : 'device_frmpayload_data_PRESSURE',
    'dayrain'   : 'device_frmpayload_data_DAYRAIN',
    'windspeed' : 'device_frmpayload_data_WINDSPEED',
    'winddir'   : 'device_frmpayload_data_WINDDIRECTION',
    '10minavg'  : 'device_frmpayload_data_TENMINUTESAVGWINDSPEED',
}