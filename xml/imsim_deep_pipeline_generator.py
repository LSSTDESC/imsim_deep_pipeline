"""
Script to generate xml for the imsim_deep_pipeline simulation pipeline.
"""
from __future__ import absolute_import, print_function
import os
import desc.workflow_engine.workflow_engine as engine

pipeline = engine.Pipeline('imsim_deep_pipeline', '0.1')

main_task = pipeline.main_task
main_task.notation = 'imsim Deep Execution Pipeline'

main_task.set_variables()

slac_root_dir = '/nfs/farm/g/desc/u1/imsim_deep/pipeline'
slac_path = lambda x: os.path.join(slac_root_dir, x)

main_task.set_variable('SLAC_OUTPUT_DATA_DIR', slac_path('output'))
main_task.set_variable('SLAC_SCRIPT_LOCATION', slac_path('scripts'))
main_task.set_variable('SCRIPT_NAME', 'imsim_deep_pipeline.py')

# Prepare a list of visits.
make_visit_list = main_task.create_process('make_visit_list')

# Parent process for looping over visit subtasks.
submit_visits = main_task.create_process('submit_visits',
                                         job_type='script',
                                         requirements=[make_visit_list])
# For each visit,
# * generate the instance catalog for the focal plane,
# * loop over sensors, submitting an imsim.py job for each.
visit_task = engine.Task('visit_task')
submit_visits.add_subtask(visit_task)
make_instcat = visit_task.create_process('make_instcat')
submit_imsim_jobs = visit_task.create_process('submit_imsim_jobs',
                                              job_type='script',
                                              requirements=[make_instcat])
imsim_task = engine.Task('imsim_task')
submit_imsim_jobs.add_subtask(imsim_task)
run_imsim = imsim_task.create_process('run_imsim')
register_imsim_files = imsim_task.create_process('register_imsim_files',
                                                 job_type='script',
                                                 requirements=[run_imsim])

with open('imsim_deep_pipeline.xml', 'w') as output:
    output.write(pipeline.toxml() + '\n')

pipeline.write_python_module()
pipeline.write_process_scripts()
