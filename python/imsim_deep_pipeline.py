"""
Jython functions to be run in the imsim_deep_pipeline.xml scripts.
"""
import java.util import HashMap

def submit_visits():
    job_vars = HashMap()
    visit_file = open(VISIT_LIST_FILE)
    for line in visit_file:
        obsHistID = int(line.strip())
        job_vars.put('OBSHISTID', obsHistID)
        pipeline.createSubstream("visit_task", obsHistID, job_vars)
    visit_file.close()

def submit_imsim_jobs():
    job_vars = HashMap()
    num_sensors = int(NUM_SENSORS)
    for sensor_number in range(num_sensors):
        job_vars.put('SENSOR_NUMBER', sensor_number)
        pipeline.createSubstream('imsim_task', sensor_number, job_vars)

def register_imsim_files():
    pass
