"""
Utilities for creating object catalogs via CatSim for imSim.
"""
from __future__ import absolute_import, print_function
import copy
import sys
import logging
import warnings
import numpy as np
with warnings.catch_warnings():
    warnings.filterwarnings('ignore', 'Duplicate object type id', UserWarning)
    warnings.filterwarnings('ignore', 'duplicate object identifie', UserWarning)
    from lsst.sims.utils import arcsecFromRadians
    from lsst.sims.catalogs.db import CatalogDBObject
    from lsst.sims.catUtils.utils import ObservationMetaDataGenerator
    from lsst.sims.catUtils.exampleCatalogDefinitions \
        import DefaultPhoSimHeaderMap
    from lsst.sims.catUtils.exampleCatalogDefinitions.phoSimCatalogExamples \
        import PhoSimCatalogPoint, PhoSimCatalogSersic2D

__all__ = ['PhoSimPointICRS', 'PhoSimSersic2dICRS', 'make_obs_par_file',
           'make_instance_catalog', 'apply_dithering']

logging.basicConfig(format="%(message)s", level=logging.INFO,
                    stream=sys.stdout)
logger = logging.getLogger()

class PhoSimPointICRS(PhoSimCatalogPoint):

    catalog_type = 'phoSim_catalog_POINT_ICRS'

    column_outputs = ['prefix', 'uniqueId', 'raJ2000', 'decJ2000',
                      'phoSimMagNorm', 'sedFilepath',
                      'redshift', 'shear1', 'shear2', 'kappa', 'raOffset', 'decOffset',
                      'spatialmodel', 'internalExtinctionModel',
                      'galacticExtinctionModel', 'galacticAv', 'galacticRv',
                      'properMotionRa', 'properMotionDec', 'parallax', 'radialVelocity']


    transformations = {'raJ2000': np.degrees, 'decJ2000': np.degrees,
                       'properMotionRa': arcsecFromRadians,
                       'properMotionDec': arcsecFromRadians,
                       'parallax': arcsecFromRadians}


class PhoSimSersic2dICRS(PhoSimCatalogSersic2D):

    catalog_type = 'phoSim_catalog_SERSIC2D_ICRS'

    column_outputs = ['prefix', 'uniqueId', 'raJ2000', 'decJ2000', 'phoSimMagNorm', 'sedFilepath',
                      'redshift', 'shear1', 'shear2', 'kappa', 'raOffset', 'decOffset',
                      'spatialmodel', 'majorAxis', 'minorAxis', 'positionAngle', 'sindex',
                      'internalExtinctionModel', 'internalAv', 'internalRv',
                      'galacticExtinctionModel', 'galacticAv', 'galacticRv',]

    transformations = {'raJ2000': np.degrees, 'decJ2000': np.degrees, 'positionAngle': np.degrees,
                       'majorAxis': arcsecFromRadians, 'minorAxis': arcsecFromRadians}


def make_obs_par_file(obs_md, db_config, phosim_header_map, outfile):
    """
    Create an observing parameter-only instance catalog.

    Parameters
    ----------
    obs_md : ObservationMetaData
        Data describing the observation, especially telescope orientation.
    db_config : dict
        Dictionary of connection parameters to CatSim database.
    phosim_header_map : PhoSimHeaderMap
        Object containing phosim observing parameters.
    outfile : str
        Filename of the instance catalog.
    """
    db_obj = CatalogDBObject.from_objid('msstars', **db_config)
    phosim_object = PhoSimPointICRS(db_obj, obs_metadata=obs_md)
    phosim_object.phoSimHeaderMap = phosim_header_map
    with open(outfile, 'w') as output:
        phosim_object.write_header(output)

def make_instance_catalog(obs_md, db_config, phosim_header_map, outfile,
                          stars_only=False, logger=logger):
    """
    Create an instance catalog for stars and galaxies.

    Parameters
    ----------
    obs_md : ObservationMetaData
        Data describing the observation, especially telescope orientation.
    db_config : dict
        Dictionary of connection parameters to CatSim database.
    phosim_header_map : PhoSimHeaderMap
        Object containing phosim observing parameters.
    outfile : str
        Filename of the instance catalog.
    stars_only : bool, optional
        Set to True if only stars should be included.  Default: False
    """
    star_objs = ['msstars', 'bhbstars', 'wdstars', 'rrlystars', 'cepheidstars']
    gal_objs = ['galaxyBulge', 'galaxyDisk']

    do_header = True
    for objid in star_objs:
        logger.info("processing %s", objid)
        db_obj = CatalogDBObject.from_objid(objid, **db_config)
        phosim_object = PhoSimPointICRS(db_obj, obs_metadata=obs_md)
        if do_header:
            phosim_object.phoSimHeaderMap = phosim_header_map
            phosim_object.write_catalog(outfile, write_mode='w',
                                        write_header=True, chunk_size=20000)
            do_header = False
        else:
            phosim_object.write_catalog(outfile, write_mode='a',
                                        write_header=False, chunk_size=20000)

    if not stars_only:
        for objid in gal_objs:
            logger.info("processing %s", objid)
            db_obj = CatalogDBObject.from_objid(objid, **db_config)
            phosim_object = PhoSimSersic2dICRS(db_obj, obs_metadata=obs_md)
            phosim_object.write_catalog(outfile, write_mode='a',
                                        write_header=False, chunk_size=20000)

def apply_dithering(obs_md):
    """
    Apply dithering.  If any of the dithered summary table columns
    are missing, emit a warning, so that the user knows.

    Parameters
    ----------
    obs_md : ObservationMetaData
        Data from the OpSim db file for the desired visit.

    Returns
    -------
    (obs_md, phosim_header_map) : (ObservationMetaData, PhoSimHeaderMap)
        The updated obs_md object and the PhoSimHeaderMap to be used by
        the PhoSimCatalog.write_catalog method.
    """
    dithered_ra_name = 'randomDitherFieldPerVisitRA'
    dithered_dec_name = 'randomDitherFieldPerVisitDec'
    dithered_rot_tel_pos_name = 'ditheredRotTelPos'

    # dither RA
    try:
        obs_md.pointingRA = np.degrees(obs_md.OpsimMetaData[dithered_ra_name])
    except KeyError:
        warnings.warn('ObservationMetaData does not contain %s data'
                      % dithered_ra_name)

    # dither Dec
    try:
        obs_md.pointingDec = np.degrees(obs_md.OpsimMetaData[dithered_dec_name])
    except KeyError:
        warnings.warn('ObservationMetaData does not contain %s data'
                      % dithered_dec_name)

    # dither rotTelPos and rotSkyPos
    from lsst.sims.utils import _getRotSkyPos
    phosim_header_map = copy.deepcopy(DefaultPhoSimHeaderMap)
    phosim_header_map['rawSeeing'] = ('rawSeeing', None)
    phosim_header_map['FWHMgeom'] = ('FWHMgeom', None)
    phosim_header_map['FWHMeff'] = ('FWHMeff', None)

    try:
        dithered_rot_tel = obs_md.OpsimMetaData[dithered_rot_tel_pos_name]
        dithered_rot_sky = _getRotSkyPos(obs_md._pointingRA,
                                         obs_md._pointingDec,
                                         obs_md, dithered_rot_tel)

        obs_md.rotSkyPos = np.degrees(dithered_rot_sky)
        phosim_header_map['rottelpos'] = (dithered_rot_tel_pos_name, np.degrees)
    except KeyError:
        warnings.warn('ObservationMetaData does not contain %s data'
                      % dithered_rot_tel_pos_name)

    return obs_md, phosim_header_map
