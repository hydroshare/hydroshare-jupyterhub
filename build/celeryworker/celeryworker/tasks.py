from __future__ import absolute_import, print_function
from celeryworker.celery import app
import time, subprocess, shlex, os
from celeryworker.compat import *


registered_images = ['castrona/jhswarm', 'jupyter/scipy-notebook']

@app.task
def task_sanity_check(string):
    time.sleep(1)
    print(string)
    image_id = os.popen('basename "$(head /proc/1/cgroup)"').read().strip()
    print(image_id)
    time.sleep(1)
    return {'success': 1,'imageid': image_id}

@app.task
def task_get_registered_images():
    res = os.popen("docker images").read()
    return res
#    cmd = 'docker images'
#    res = run_command(cmd)
#    return res
#    res = os.popen("docker images").read().split()
#    imgs = [res[i] for i in range(6,len(res),7) if res[i] in registered_images]
#    return imgs

@app.task
def task_run_container(image_name, vol_mount, mount_target, invoker_id, env_vars={}):

#    print('Name: %s' % image_name)
#    print('Local Relative Path: %s' % vol_mount)
#    print('Mount target: %s' % mount_target)
#    print('Invoking Container Id: %s' % invoker_id)

    vols = os.popen("docker inspect -f '{{ .Mounts }}' %s" % invoker_id).read()
    volumes = []
    for vol in vols.strip()[2:-2].split('} {'):
        atts = vol.split(' ')
        mnt_path = os.path.join(mount_target, atts[3].strip('/'))
        volumes.append('-v ' + (':').join([atts[2], mnt_path]))

    for v in volumes:
        print(v)

    envars = '-e %s=%s' % ('RELPATH',
     os.path.join('/tmp', vol_mount.strip('/')))
    for k, v in env_vars.items():
        envars += ' -e %s=%s' % (k, v)

    print(envars)
    run_cmd = 'docker run --rm %s %s %s' % ((' ').join(volumes),
     envars,
     image_name)
    print('RUN COMMAND: %s' % run_cmd)
    
    res = os.popen(run_cmd).read()
    return res
#    res = run_command(run_cmd)
#    print('finished.  returning output')
#    return res


def run_command(command):
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())

    rc = process.poll()
    return rc
