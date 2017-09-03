"""
Unit tests for SensorLists class.
"""
import os
import unittest
import desc.imsim_deep_pipeline

class SensorListsTestCase(unittest.TestCase):
    """
    Test case class for SensorLists.
    """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sensors_function(self):
        "Test the SensorList function object."
        # Default case: return all science sensors.
        sensors = desc.imsim_deep_pipeline.SensorLists()
        for obsHistID in (0, 10, 100, 1000):
            self.assertEqual(len(sensors(obsHistID)), 189)

        # Pass a truncated list of invalid FITS files.
        infile = os.path.join(os.environ['IMSIM_DEEP_PIPELINE_DIR'], 'tests',
                              'invalid_file_list_example.txt')
        sensors = desc.imsim_deep_pipeline.SensorLists(infile)
        self.assertEqual(set(sensors(193223)),
                         set(('R:0,2 S:2,1', 'R:4,1 S:2,0')))
        self.assertEqual(len(sensors(195755)), 2)
        self.assertEqual(len(sensors(201793)), 11)
        self.assertEqual(len(sensors(32910)), 0)

if __name__ == '__main__':
    unittest.main()
