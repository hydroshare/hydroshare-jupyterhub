from __future__ import absolute_import, print_function
import os
import sys
import time
from . import tasks
from .compat import *
from . import progress

__all__ = []

#registered_images = ['ncar/summa', 'ncar/summa-test']

def get_invoker_id():
    try:
        # Docker version 18.05.0-ce, build f150324
        return os.popen('basename "$(head /proc/1/cgroup)"').read().strip()
    except:
        # Docker version 1.13.1, build 94f4240/1.13.1
        return os.popen('basename "$(head /proc/1/cgroup)"').read().strip().split('-')[1][:-6]
        

def get_registered_images():

    job = tasks.task_get_registered_images.delay()
    job = wait_for_task(job)
    return job.result

def is_registered(image_name):
    job = tasks.task_get_registered_images.delay()
    job = wait_for_task(job, show_progress=False)
    image_list = job.result
    if image_name in image_list:
        return True
    return False

def describe(image_name):

    # make sure the image is registered
    if not is_registered(image_name):
        print('Cannot run a non-registered container')
        return None
    
    invoker_id = get_invoker_id()

    job = tasks.task_run.delay(image_name, invoker_id, args='-d')
    job = wait_for_task(job)
    print('task complete')
    print(job.result)
    return job
    
def methods(image_name):

    # make sure the image is registered
    if not is_registered(image_name):
        print('Cannot run a non-registered container')
        return None

    invoker_id = get_invoker_id()
    job = tasks.task_run.delay(image_name, invoker_id, args='-m')
    job = wait_for_task(job)
    print('task complete')
    print(job.result)
    return job

def run(image_name, args='', vol_mount=None, mount_target=None, env_vars={}):

    # get the id, remove docker- and .scope
    invoker_id = get_invoker_id()
    
    # make sure the image is registered
    if not is_registered(image_name):
        print('Cannot run a non-registered container')
        return None

    job = tasks.task_run.delay(image_name,
                               invoker_id,
                               vol_mount,
                               mount_target,
                               env_vars,
                               args=args)
    job = wait_for_task(job)
    print('task complete')
    print(job.result)
    return job

def sanity_check(string, async=True):
    if async:
        res = tasks.task_sanity_check(string)
    else:
        res = tasks.task_sanity_check(string)
    return res

def wait_for_task(job, show_progress =True):
    msg = 'Waiting for task to finish '
    suc = 'Job finished'
    pbar = progress.progressBar(msg, type='pulse',
                                finish_message=suc)
    while not job.ready():
        if show_progress:
            pbar.writeprogress()
        time.sleep(.05)
    if show_progress:
        pbar.success()
    return job
