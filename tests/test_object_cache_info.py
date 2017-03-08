"""
Unit tests for instance catalog caching code.
"""
import os
import unittest
import desc.imsim_deep_pipeline

class ObjectCacheInfoTest(unittest.TestCase):
    "Test case for ObjectCacheInfo class."
    def setUp(self):
        self.object_info_cache = desc.imsim_deep_pipeline.ObjectCacheInfo()

        ra, dec = 93.1078762, -29.9663229
        self.large_file = 'large_object_file.txt'
        self.large_file_radius = 0.1
        self._make_instcat_file(self.large_file, ra, dec)
        self.object_info_cache.add_obj_file(self.large_file,
                                            self.large_file_radius)

        self.offset = self.large_file_radius/2.
        self.offset_file = 'offset_object_file.txt'
        self._make_instcat_file(self.offset_file, ra, dec + self.offset)

        self.disjoint_file = 'disjoint_object_file.txt'
        self._make_instcat_file(self.disjoint_file, ra,
                                dec + 2*self.large_file_radius)

    def tearDown(self):
        del self.object_info_cache
        for cat_file in (self.large_file, self.offset_file, self.disjoint_file):
            try:
                os.remove(cat_file)
            except OSError:
                pass

    @staticmethod
    def _make_instcat_file(filename, ra, dec):
        with open(filename, 'w') as output:
            output.write('rightascension %.7f\n' % ra)
            output.write('declination %.7f\n' % dec)

    def test_get_nearest_object_file(self):
        """
        Test for retrieving the nearest object file.
        """
        self.object_info_cache.add_obj_file(self.offset_file, 0.2)

        candidate_file = 'candidate_file.txt'
        self._make_instcat_file(candidate_file, 93.1078762, -29.9663229)

        object_file \
            = self.object_info_cache.get_nearest_object_file(candidate_file)
        self.assertEqual(object_file, self.large_file)
        os.remove(candidate_file)

    def test_caching(self):
        """
        Test for caching based on file pointing directions and trim
        radius of object list.
        """
        # Test for matching file
        radius = self.large_file_radius
        object_files \
            = self.object_info_cache.get_object_files(self.large_file, radius)
        self.assertEqual(object_files[0], self.large_file)

        # Test for centered contained file.
        radius = self.large_file_radius/2.
        object_files \
            = self.object_info_cache.get_object_files(self.large_file, radius)
        self.assertEqual(object_files[0], self.large_file)

        # Test for offset contained file.
        radius = self.offset/10.
        object_files \
            = self.object_info_cache.get_object_files(self.offset_file, radius)
        self.assertEqual(object_files[0], self.large_file)

        # Test for file which is larger than cached file.
        radius = self.large_file_radius*2.
        self.assertRaises(desc.imsim_deep_pipeline.ObjectCacheInfoException,
                          self.object_info_cache.get_object_files,
                          self.large_file, radius)

        # Test for uncontained offset file.
        radius = self.large_file_radius
        self.assertRaises(desc.imsim_deep_pipeline.ObjectCacheInfoException,
                          self.object_info_cache.get_object_files,
                          self.offset_file, radius)

        # Test for disjoint file.
        radius = self.large_file_radius
        self.assertRaises(desc.imsim_deep_pipeline.ObjectCacheInfoException,
                          self.object_info_cache.get_object_files,
                          self.disjoint_file, radius)

    def test_add_object_file(self):
        "Test the addition of another object file to the cache."
        radius = 2.1
        self.object_info_cache.add_obj_file(self.disjoint_file, radius)
        object_files \
            = self.object_info_cache.get_object_files(self.disjoint_file,
                                                      radius/2.)

        self.assertEqual(len(object_files), 1)
        self.assertEqual(object_files[0], self.disjoint_file)

    def test_persistence(self):
        "Test methods to save and load the caching data to and from disk."
        radius = 2.1
        self.object_info_cache.add_obj_file(self.disjoint_file, radius)
        cache_file = 'my_object_catalog_cache'
        self.object_info_cache.save(cache_file)
        my_object_cache \
            = desc.imsim_deep_pipeline.ObjectCacheInfo.load(cache_file)

        object_files \
            = self.object_info_cache.get_object_files(self.disjoint_file,
                                                      radius/2.)
        self.assertEqual(len(object_files), 1)
        self.assertEqual(object_files[0], self.disjoint_file)
        os.remove(cache_file)

if __name__ == '__main__':
    unittest.main()
