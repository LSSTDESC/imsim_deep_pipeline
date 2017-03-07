"""
Module to cache instance catalog object files.
"""
from __future__ import absolute_import, print_function
import pickle
from collections import namedtuple
import desc.imsim_deep_pipeline

__all__ = ['ObjectCacheInfo', 'ObjectCacheInfoException']

ObjectCatalog = namedtuple('ObjectCatalog', ('filename', 'ra', 'dec', 'radius'))


class ObjectCacheInfoException(RuntimeError):
    pass


class ObjectCacheInfo(object):
    """
    Class to cache large instance catalog object files.
    """
    def __init__(self):
        self.catalogs = []

    def add_obj_file(self, object_file, radius):
        self.catalogs.append(self.make_object_catalog(object_file, radius))

    @staticmethod
    def make_object_catalog(object_file, radius):
        ra, dec = ObjectCacheInfo._extract_ra_dec(object_file)
        return ObjectCatalog(object_file, ra, dec, radius)

    @staticmethod
    def _extract_ra_dec(object_file):
        ra, dec = None, None
        with open(object_file) as input_:
            for line in input_:
                if line.startswith('rightascension'):
                    ra = float(line.strip().split()[1])
                if line.startswith('declination'):
                    dec = float(line.strip().split()[1])
                if ra is not None and dec is not None:
                    break
        if ra is None or dec is None:
            raise RuntimeError("RA or Dec not found in %s" % object_file)
        return ra, dec

    def get_nearest_object_file(self, candidate_file):
        """
        Find the nearest object file to the candidate file.

        Parameters
        ----------
        candidate_file : str
            Filename of observing parameters-only instance catalog that
            needs to be covered by the cached catalogs.

        Returns
        -------
        str :
            Full path of the nearest object catalog in the cache.
        """
        candidate = self.make_object_catalog(candidate_file, 0.17)
        min_sep = None
        for catalog in self.catalogs:
            sep = desc.imsim_deep_pipeline.ang_sep(candidate.ra, candidate.dec,
                                                   catalog.ra, catalog.dec)
            if min_sep is None or sep < min_sep:
                min_sep = sep
                selected_catalog = catalog
        return selected_catalog.filename

    def get_object_files(self, candidate_file, radius):
        """
        Find the instance catalog object files that cover the candidate
        file.

        Parameters
        ----------
        candidate_file : str
            Filename of observing parameters-only instance catalog that
            needs to be covered by the cached catalogs.
        radius : float
            Radius (degrees) of the candidate instance catalog.

        Returns
        -------
        list
            A list of the covering catalog filenames.

        Raises
        ------
        ObjectCacheInfoException
            If the candidate catalog cannot be covered by the cached
            catalogs.

        Notes
        -----
        Currently, this function only returns lists containing a
        single catalog, i.e., coverage for candidate catalogs by
        multiple catalog is not yet supported.
        """
        candidate = self.make_object_catalog(candidate_file, radius)
        for catalog in self.catalogs:
            sep = desc.imsim_deep_pipeline.ang_sep(candidate.ra, candidate.dec,
                                                   catalog.ra, catalog.dec)
            if sep <= catalog.radius - candidate.radius:
                return [catalog.filename]
        message = ("Candidate catalog %s cannot be covered by cached catalogs."
                   % candidate_file)
        raise ObjectCacheInfoException(message)

    def save(self, outfile):
        with open(outfile, 'wb') as output:
            pickle.dump(self, output)

    @staticmethod
    def load(infile):
        with open(infile, 'rb') as input_:
            return pickle.load(input_)
