"""
Jython functions to be run in the imsim_deep_pipeline.xml scripts.
"""
from java.util import HashMap

def submit_visits():
    """
    Loop over obsHistIds in the VISIT_LIST_FILE and submit the
    associated visit_task.
    """
    job_vars = HashMap()
    visit_file = open(VISIT_LIST_FILE)
    vmin = int(VISIT_NUM_MIN)
    vmax = int(VISIT_NUM_MAX)
    for line in visit_file.readlines()[vmin:vmax]:
        obsHistID = int(line.strip())
        job_vars.put('OBSHISTID', obsHistID)
        pipeline.createSubstream("visit_task", obsHistID, job_vars)
    visit_file.close()

def submit_imsim_jobs():
    """
    Loop over the sensors and submit the imsim_tasks.
    """
    job_vars = HashMap()
    num_sensors = int(NUM_SENSORS)
    for sensor_number in range(num_sensors):
        job_vars.put('SENSOR_NUMBER', sensor_number)
        pipeline.createSubstream('imsim_task', sensor_number, job_vars)

def register_imsim_files():
    """
    Register the imsim.py data products with the Data Catalog.
    """
    pass
