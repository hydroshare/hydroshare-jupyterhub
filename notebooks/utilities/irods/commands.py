import os
from subprocess import Popen, PIPE, STDOUT
import getpass
import zipfile
import shutil
from .compat import *


class iCommands(object):
    def __init__(self, hydroshare):
        self.irods_dir = os.environ['DATA']
        self.hs = hydroshare

        # force an update of the system environment variables
        # export the irods environment vars if they don't already exist
        if 'IRODS_PLUGINS_HOME' not in os.environ.keys():
            os.environ['PATH'] += ':%s/icommands' % self.irods_dir
            os.environ['IRODS_PLUGINS_HOME'] = '%s/icommands/plugins/' \
                % self.irods_dir
            os.environ['IRODS_ENVIRONMENT_FILE'] = '%s/.irods/' \
                'irods_environment.json' % self.irods_dir
            os.environ['IRODS_AUTHENTICATION_FILE'] = '%s/.irods/.irodsA' \
                % self.irods_dir

        chk = Popen(['ienv'], stdout=PIPE, stderr=STDOUT, shell=True)
        chk.communicate()
        chk_returncode = chk.returncode
        if chk_returncode != 0:
            print('iCommands not found on the system, preparing to install.')

            # need to install icommands
            print('Downloading iCommands...', end='', flush=True)
            if not os.path.exists('/home/jovyan/libs/icommands.sh'):
                get_cmd = 'wget --no-http-keep-alive -O'
                '/home/jovyan/libs/icommands.sh https://pods.'
                'iplantcollaborative.org/wiki/download/attachments/'
                '28117338/irods-icommands-4.1.9-ubuntu-12.installer?'
                'version=1&modificationDate=1473720729000&api=v2'
                download_icommands = Popen([get_cmd], stdout=PIPE,
                                           stderr=STDOUT, shell=True)
                download_icommands.communicate()
            print('done', flush=True)

            print('Installing iCommands...', end='', flush=True)
            install_cmd = 'chmod +x /home/jovyan/libs/icommands.sh;'
            'echo "%s" | /home/jovyan/libs/icommands.sh ' % self.irods_dir
            installicommands = Popen(install_cmd, stdout=PIPE,
                                     stderr=STDOUT, shell=True)
            installicommands.communicate()
            get_returncode = installicommands.returncode
            if get_returncode != 0:
                print('ERROR.\nCould not install icommands :(', flush=True)
            else:
                print('done', flush=True)

            print('Configuring iCommands', flush=True)
            self._init_icommands()

    def _init_icommands(self):
        irods_config = os.path.join(self.irods_dir, '.irods')
        print(irods_config)

        if not os.path.exists(irods_config):
            os.makedirs(irods_config)

        username = input('Please enter your HydroShare username: ')
        json = os.path.join(irods_config, 'irods_environment.json')
        print('Writing irods environment file', flush=True)
        with open(json, 'w') as f:
            f.write('{\n"irods_host": "users.hydroshare.org",\n \
                     "irods_zone_name": "hydroshareuserZone",\n \
                     "irods_port": 1247,\n \
                     "irods_user_name": "%s"\n \
                     }' % username)
        os.putenv("IRODS_ENVIRONMENT_FILE", json)
        os.environ["IRODS_ENVIRONMENT_FILE"] = json
        with open('/home/jovyan/.bashrc', 'a') as f:
            f.write('export IRODS_ENVIRONMENT_FILE=%s' % json)

        print('Initializing environment', flush=True)
        p = getpass.getpass('Please enter your iRODS password: ')
        os.system('iinit %s' % (p))

    def ils(self):
        """lists contents of hydroshare irods userspace

        args:
        -- None

        returns:
        -- list of files in hydroshare userspace
        """
        cmd = Popen(['ils'], stdout=PIPE, stderr=STDOUT, shell=True)
        stdout = cmd.communicate()[0].decode('ascii')
        if cmd.returncode != 0:
            print('Failed to fetch irods file list: %s' % stdout)
            return []
        return [s.replace('C-', '').strip() for s in
                stdout.split('\n')[1:] if s != '']

        print('Not Implemented')

    def iget(self, filename, destination=None, unzip=True):
        """gets a file from the hydroshare irods userspace

        args:
        -- filename: name of file to retrieve
        -- destination: location to save the file, defaults to data directory
        -- unzip: specify if the file should be unzipped (where applicable)

        returns:
        -- path to file
        """

        # build the destination
        if destination is None:
            destination = os.environ['DATA']

        irods_cmd = 'iget -f -r %s %s' % (filename, destination)
        cmd = Popen([irods_cmd], stdout=PIPE, stderr=STDOUT, shell=True)
        stdout = cmd.communicate()[0].decode('ascii')
        if cmd.returncode != 0:
            print('Failed to fetch irods file: %s' % stdout)
            return []

        infile = os.path.join(destination, filename)
        # unzip
        if unzip and filename[-3:] == 'zip':
            zdestination = os.path.join(destination, filename[:-4])
            if os.path.exists(zdestination):
                res = input('This directory already exists, '
                            'do you want to overwrite it [Y/n]?')
                if res.strip().lower() != 'y':
                    return infile
                else:
                    shutil.rmtree(zdestination)
            os.makedirs(zdestination)
            zip_ = zipfile.ZipFile(infile, 'r')
            zip_.extractall(destination)
            zip_.close()
            return zdestination
        return infile

    def irsync(self, source, target, source_irods=False, target_irods=True,
               dryrun=False):
        """sync files between Jupyter and iRODs

        args:
        -- source: name of the source sync file
        -- target: name of the target sync file
        -- source_irods: specifies if the source exists in HydroShare iRODs
                         (boolean), default False
        -- target_irods: specifies if the target exists in HydroShare iRODs
                         (boolean), default True
        -- dryrun: execute a dry run before proceeding

        returns:
        -- boolean, True if successful otherwise False
        """
        liverun = True
        source = 'i:%s' % source if source_irods else source
        target = 'i:%s' % target if target_irods else target
        irods_cmd = 'irsync -r %s %s' % (source, target)

        if dryrun:
            liverun = False
            cmd = Popen(['%s -l' % irods_cmd], stdout=PIPE,
                        stderr=STDOUT, shell=True)
            stdout = cmd.communicate()[0].decode('ascii')
            if cmd.returncode != 0:
                print('Failed during syncronization dry run: %s' % stdout,
                      flush=True)
                return False
            if stdout.strip() == '':
                print('No changes detected', flush=True)
                return False
            print(stdout, flush=True)
            res = input('Would you like to continue with syncronization '
                        '[Y/n]?')
            if res.strip().lower() != 'n':
                liverun = True

        if liverun:
            cmd = Popen([irods_cmd], stdout=PIPE, stderr=STDOUT, shell=True)
            stdout = cmd.communicate()[0].decode('ascii')
            if cmd.returncode != 0:
                print('Failed during syncronization, %s: %s' % (cmd, stdout))
                return False

        return True

    def getResourceFromHydroshare(self, resid, destination=None):
        """transfers a large file from hydroshare.

        args:
        -- resid: hydroshare resource id
        -- destination: path to save file, defaults to data directory

        returns:
        -- None
        """
        print('Not Implemented')
