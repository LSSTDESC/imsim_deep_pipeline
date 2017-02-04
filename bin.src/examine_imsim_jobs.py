from __future__ import print_function
import os
import sys
import itertools
import astropy.io.fits as fits

def sensors():
    """
    The slugified sensor ids in the LSST focal plane.

    Returns
    -------
    list of strs
        A list of the sensor ids, e.g., 'R_2_2_S_1_1'.  Corner raft sensors
        are excluded.
    """
    corners = ((0, 0), (0, 4), (4, 0), (4, 4))
    raft_ids = ['R_%i_%i' % x for x in itertools.product(range(5), range(5))
                if x not in corners]
    sensor_ids = ['S_%i_%i' % x for x in itertools.product(range(3), range(3))]
    return ['_'.join(x) for x in itertools.product(raft_ids, sensor_ids)]


vmin = 404
vmax = 606

root_dir = '/nfs/farm/g/desc/u2/data/imsim_deep/pipeline/output/full_focalplane_undithered'
visits = ['%07i' % int(x.strip()) for x in
          open(os.path.join(root_dir, 'imsim_deep_visits.txt'))]

ntot = 0
for visit in visits[404:606]:
    for sensor in sensors():
        fits_file = os.path.join(root_dir, visit, sensor,
                                 'lsst_e_%i_%s_r.fits.gz' % (int(visit),
                                                             sensor))
        try:
            foo = fits.open(fits_file)
            foo.verify()
        except:
            print(fits_file)
            sys.stdout.flush()
        ntot += 1
print(ntot)
