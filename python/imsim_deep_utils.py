"""
Utilities for the imsim_deep pipeline python code.
"""
from __future__ import absolute_import
import os
import itertools
from collections import namedtuple

visit_info = namedtuple('visit_info',
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
    return visit_info(obsHistId, instcat_file, instcat_radius)

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
    return ['%s %s' %x for x in itertools.product(raft_ids, sensor_ids)]
