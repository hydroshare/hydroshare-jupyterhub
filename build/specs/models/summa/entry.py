#!/usr/bin/env python3

import os
import shutil

####################################
# Author: Tony Castronova
# Email:  acastronova.cuahsi.org
# Date:   10.23.2017
# Org:    CUAHSI
# Desc:   Entrypoint for executing the summa model
####################################


basedir = '/tmp/summa'

# these paths come in as absolute.  Grab everything after the initial "\"


def prepare():
#    print('Preparing execution environment')

    # copy summa to temp location
    
    summa_masterpath = os.environ['MASTERPATH']

    # remove leading '/' to make sure path join is correct
#    print('SUMMA_MASTERPATH: %s' % summa_masterpath)
    if summa_masterpath[0] == '/':
        summa_masterpath = summa_masterpath[1:]

#    print('ABS_SUMMA_MASTERPATH: %s' % summa_masterpath)
    summa_masterpath = os.path.join(basedir, summa_masterpath)
    tmp_fm = summa_masterpath+'_tmp'
#    tmp_fm = os.path.join(basedir, summa_masterpath+'_tmp')
    assert os.path.exists(summa_masterpath), 'Could not find masterfile at %s' % summa_masterpath

    # removing leading '/' to make sure path join is correct
    localbase = os.environ['LOCALBASEDIR']
#    print('BASEDIR: %s' % localbase)
    if localbase[0] == '/':
        localbase = localbase[1:]
    localbase = os.path.join(basedir, localbase)
#    print('NEW_BASEDIR: %s' % localbase)


#    print('PATH: %s' % basedir)
#    print('FM PATH: %s' % summa_masterpath)
#    print('TMP_FM PATH: %s' % tmp_fm)

#    print('Creating the tmp Filemanager')
    args = {}
    with open(tmp_fm, 'w') as w:
        with open(summa_masterpath, 'r') as r:
            lines = r.readlines()
            for line in lines:
                l = line.replace('<BASEDIR>', localbase)
                w.write(l)

                # save masterpath args
                path, id = l.split('!')
                path = path.strip().replace("'", "")
                id = id.strip()
                args[id] = path

    # modify paths without BASEDIR to be relative to setting_path
    # this is just for validating the filepaths in the next step
    settings_path = args['setting_path'].replace(localbase,'')
    if settings_path[0] == '/':
        settings_path = settings_path[1:]
#    print('SETTING PATH: %s' % settings_path)
    for k, v in args.items():
        if basedir not in v:
            args[k] = os.path.join(localbase, settings_path, v)
#            print('%s + %s + %s = %s' %(localbase, settings_path, v, args[k]))

    # create the output path, if it doesn't already exist
    if not os.path.exists(args['output_path']):
        os.makedirs(args['output_path'])


    # make sure all these paths exist
    for k, v in args.items():
        print('{:20s} -> '.format(k), end='')
#        print('checking %s ->' % k, end='')
        if k in ['fman_ver', 'output_prefix']:
            pass
        elif 'path' in k:
            assert os.path.exists(v), "Error in masterfile. Could not find " \
                                      "%s: %s" % (k, v)
        else:
            p = os.path.join(args['setting_path'], v)
            assert os.path.exists(p), "Error in masterfile. Could not find " \
                                      "%s: %s" % (k, v)
        print('OK')
#    print('SUMMA PREP COMPLETE')
    return tmp_fm


def rm_tmp_dir(tmp):
    # remove the temporary directory
    if os.path.exists(tmp):
        print('Cleaning execution environment')
        shutil.rmtree(tmp)


def mk_output_dir(d):
    if not os.path.exists(d):
        os.makedirs(d)


def run(masterp):
    print('Running SUMMA simulation')
    os.system('/code/bin/summa.exe -m %s' % masterp)

def clean(masterp):
    os.remove(masterp)

# entry point steps
masterp = prepare()
run(masterp)
clean(masterp)
