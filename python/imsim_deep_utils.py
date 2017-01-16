import os
import itertools

def get_visit_info(band='r', radius=1.8):
    obsHistId = os.environ['OBSHISTID']
    instcat_file \
        = os.path.join(os.environ['IMSIM_DEEP_INSTCAT_DIR'],
                       'instcat_%07i_%s_%.1f.txt' % (obsHistID, band, radius))
    return obsHistId, instcat_file

def sensors():
    corners = ((0, 0), (0, 4), (4, 0), (4, 4))
    raft_ids = ['R:%i,%i' % x for x in itertools.product(range(5), range(5))
                if x not in corners]
    sensor_ids = ['S:%i,%i' % x for x in itertools.product(range(3), range(3))]
    return ['%s %s' %x for x in itertools.product(raft_ids, sensor_ids)]
