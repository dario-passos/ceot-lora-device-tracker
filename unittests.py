import unittest
import config
from device import DeviceProfile


class TestDeviceProfile(unittest.TestCase):


    def setUp(self):
        # LHT65_FIELDS = {
        #     'bat':'device_frmpayload_data_BatV',
        #     'hum':'device_frmpayload_data_Hum_SHT',
        #     'tmp':'device_frmpayload_data_TempC_SHT',
        #     'ilx':'device_frmpayload_data_ILL_lux'
        # }
        self.dp = DeviceProfile('LHT65', config.LHT65_FIELDS)
    
    def test_field_names(self):
        fieldnames = ['bat', 'hum', 'tmp', 'ilx']
        self.assertEqual(self.dp.get_fieldnames(), fieldnames)

    def test_query_fields(self):
        queryfields = ['device_frmpayload_data_BatV', 'device_frmpayload_data_Hum_SHT', 'device_frmpayload_data_TempC_SHT', 'device_frmpayload_data_ILL_lux']
        self.assertEqual(self.dp.get_queryfields(), queryfields)


if __name__ == '__main__':
    unittest.main()