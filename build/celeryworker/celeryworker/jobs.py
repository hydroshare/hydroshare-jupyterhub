from __future__ import absolute_import, print_function
import time
from .tasks import *
from .compat import * 

registered_images = ['castrona/jhswarm', 'jupyter/scipy-notebook', 'summa']

def get_registered_images():

    task = task_get_registered_images.delay()
    task = wait_for_task(task)
    res = task.result.split('\n')
    imgs = [res[i].split()[0] for i in range(1,len(res)-1) if res[i].split()[0] in registered_images]
    return imgs

def run(image_name, vol_mount, mount_target, env_vars={}):

    invoker_id = os.popen('basename "$(head /proc/1/cgroup)"').read().strip()   
    print('Name: %s' % image_name)
    print('Local Relative Path: %s' % vol_mount)
    print('Mount target: %s' % mount_target)
    print('Invoking Container Id: %s' % invoker_id)
 
    # make sure the image is registered
    if image_name not in registered_images:
        print('Cannot run a non-registered container')
        return None

    task = task_run_container.delay(image_name, vol_mount, mount_target, invoker_id, env_vars)
    task = wait_for_task(task)
    print('task complete')
    print(task.result)
    return task



def sanity_check(string, async=True):
    if async:
        task = task.sanity_check(string)
        res = task.result
    else:
        res = task.sanity_check(string)
    return res

def wait_for_task(task):
    print('waiting for task to finish', end='')
    while not task.ready():
#        print(task.info)
        print('.', end='')
        time.sleep(.25)
    print(' done')
    return task
