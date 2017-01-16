"""
Utilities for the imsim_deep pipeline python code.
"""
import os
import itertools

def get_visit_info(band='r', radius=1.8):
    """
    Get the desired obsHistId, as set by the driving jython script and
    build the instance catalog filepath.

    Parameters
    ----------
    band : str, optional
        The filter band to use. Default: 'r'
    radius : float, optional
        The radius of the sky cone in degrees for the instance catalog
        generation. Default: 1.8

    Returns
    -------
    tuple : obsHistId, instcat_file
    """
    obsHistId = os.environ['OBSHISTID']
    instcat_file \
        = os.path.join(os.environ['IMSIM_DEEP_INSTCAT_DIR'],
                       'instcat_%07i_%s_%.1f.txt' % (obsHistId, band, radius))
    return obsHistId, instcat_file

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
