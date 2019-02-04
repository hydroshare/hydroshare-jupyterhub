from __future__ import absolute_import
from celeryworker.celery import app
import time
import subprocess
import shlex
import os
from .compat import *

@app.task
def longtime_add(x, y):
    print 'long time task begins'
    time.sleep(5)
    print 'long time task finished'
    return x + y


@app.task
def run_container(image_name, vol_mount, mount_target, invoker_id, env_vars={}):
    print 'long time task begins'
    print "Name: %s" % image_name
    print "Local Relative Path: %s" % vol_mount
    print "Mount target: %s" % mount_target
    print "Invoking Container Id: %s" % invoker_id

    # get the invoker volume mounts
    vols = os.popen("docker inspect -f '{{ .Mounts }}' %s" % invoker_id).read()
    volumes = []
    for vol in vols.strip()[2:-2].split('} {'):
        atts = vol.split(' ')
        mnt_path = os.path.join(mount_target, atts[3].strip('/'))
        volumes.append('-v ' + ':'.join([atts[2], mnt_path]))
    for v in volumes:
        print(v)

    # set the path to data (inside the tmp dir)
    envars = '-e %s=%s' % ('RELPATH', os.path.join('/tmp',
                                                   vol_mount.strip('/')))
    # this assumes that env_vars are relative paths
    for k, v in env_vars.items():
        envars += ' -e %s=%s' % (k, v)
    print(envars)

    run_cmd = 'docker run --rm %s %s %s' % (' '.join(volumes),
                                            envars,
                                            image_name)
    print('RUN COMMAND: %s' % run_cmd)
    res = run_command(run_cmd)
    print 'finished.  returning output'
    return res


@app.task
def run_task_test(name, host_volume, param):
    print 'long time task begins'
    time.sleep(5)
    print "Name: %s" % name
    print "Volume: %s" % host_volume
    print "Param: %s" % param
    print 'long time task finished'
    return 1


def run_command(command):
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print output.strip()
    rc = process.poll()
    return rc
