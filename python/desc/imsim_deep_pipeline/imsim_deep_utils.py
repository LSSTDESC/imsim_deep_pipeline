"""
Utilities for the imsim_deep pipeline python code.
"""
from __future__ import absolute_import
import os
import itertools
from collections import namedtuple
import lsst.obs.lsstSim as obs_lsstSim
from lsst.sims.coordUtils import raDecFromPixelCoords
from lsst.sims.photUtils import LSSTdefaults
from lsst.sims.utils import ObservationMetaData
import desc.imsim
from .instcat_utils import sky_cone_select

__all__ = ['get_visit_info', 'sensors', 'obs_metadata', 'trim_instcat']

VisitInfo = namedtuple('VisitInfo',
                       ('obsHistId', 'instcat_file', 'instcat_radius'))


def get_visit_info():
    """
    Get the desired obsHistId, as set by the driving jython script and
    build the instance catalog filepath.

    Returns
    -------
    tuple : obsHistId, instcat_file, instcat_radius
    """
    obsHistId = int(os.environ['OBSHISTID'])
    lsst_band = os.environ['LSST_BAND']
    instcat_radius = float(os.environ['INSTCAT_RADIUS'])
    instcat_dir = os.path.join(os.environ['OUTPUT_DATA_DIR'],
                               '%07i' % obsHistId)
    if not os.path.isdir(instcat_dir):
        os.mkdir(instcat_dir)
    instcat_file = os.path.join(instcat_dir, 'instcat_%07i_%s_%.1f.txt'
                                % (obsHistId, lsst_band, instcat_radius))
    return VisitInfo(obsHistId, instcat_file, instcat_radius)


def sensors():
    """
    The sensor ids in the LSST focal plane.

    Returns
    -------
    list of strs
        A list of the sensor ids, e.g., 'R:2,2 S:1,1'.  Corner raft sensors
        are excluded.
    """
    corners = ((0, 0), (0, 4), (4, 0), (4, 4))
    raft_ids = ['R:%i,%i' % x for x in itertools.product(range(5), range(5))
                if x not in corners]
    sensor_ids = ['S:%i,%i' % x for x in itertools.product(range(3), range(3))]
    return [' '.join(x) for x in itertools.product(raft_ids, sensor_ids)]


def obs_metadata(commands):
    """
    Create an ObservationMetaData instance from phosim commands.
    Parameters
    ----------
    commands : dict
        Dictionary of phosim instance catalog commands.
    Returns:
    lsst.sims.utils.ObservationMetaData
    """
    return ObservationMetaData(pointingRA=commands['rightascension'],
                               pointingDec=commands['declination'],
                               mjd=commands['mjd'],
                               rotSkyPos=commands['rotskypos'],
                               bandpassName=commands['bandpass'],
                               m5=LSSTdefaults().m5(commands['bandpass']),
                               seeing=commands['seeing'])


def trim_instcat(chipname, infile, outfile, radius=0.18):
    """
    Trim an instance catalog to an acceptance cone centered on the
    specified sensor.

    Parameters
    ----------
    chipname : str
        The name of the sensor, e.g., 'R:2,2 S:1,1'.
    infile : str
        The filename of the instance catalog to be trimmed.
    outfile : str
        The output filename for the trimmed data.
    radius : float, optional
        The radius of the acceptance cone in degrees.  Default: 0.18;
        this includes some buffer to account for differing pixel
        geometries for ITL vs e2v sensors.

    Notes
    -----
    This function depends on the optional ImSimDeep package.
    """
    camera = obs_lsstSim.LsstSimMapper().camera
    instcat = desc.imsim.parsePhoSimInstanceFile(infile, numRows=100)
    obs_md = obs_metadata(instcat.commands)
    # Get the chip sensor coordinates in degrees.
    ra, dec = raDecFromPixelCoords(2036, 2000, chipname, camera=camera,
                                   obs_metadata=obs_md)
    sky_cone_select(infile, ra, dec, radius, outfile)
