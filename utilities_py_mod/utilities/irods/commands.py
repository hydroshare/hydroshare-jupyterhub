import os
from subprocess import Popen, PIPE, STDOUT
import getpass
import zipfile
import shutil
import time
from .compat import *


class iCommands(object):
    def __init__(self, hydroshare):
        self.irods_dir = os.environ['DATA']
        self.hs = hydroshare

        self.icmd = os.path.join(self.irods_dir, 'icommands.sh')
        self.iplug = os.path.join(self.irods_dir, 'icommands/plugins/')
        self.iauth = os.path.join(self.irods_dir, '.irods/.irodsA')
        self.ienv = os.path.join(self.irods_dir, '.irods/irods_environment.json')

        if not os.path.exists(self.ienv):
            print('iRODS not configuration found')
            sys.stdout.flush()
            time.sleep(.25)
            self._init_icommands()
        else:
            print('iRODS configuration found:')
            with open(self.ienv, 'r') as f:
                for line in f.readlines():
                    print(line.strip())
        print('\nTo connect to a different iRODS host use:')
        print('   iCommands.iinit()')


    def _init_icommands(self):
        irods_config = os.path.join(self.irods_dir, '.irods')

        if not os.path.exists(irods_config):
            os.makedirs(irods_config)
        
        if not os.path.exists(self.ienv):
            irods_host = input('iRODs host: ')
            irods_zone = input('iRODs zone: ')
            irods_port = input('iRODs port: ')
            username = input('iRODs username: ')
            home_dir = input('iRODs home directory (leave blank if unknown): ') or None
            json = os.path.join(irods_config, 'irods_environment.json')
            print('Writing irods environment file')
            sys.stdout.flush()
            print(json)
            with open(json, 'w') as f:
                f.write('{\n')
                f.write(' "irods_host": "%s",\n' % irods_host)
                f.write(' "irods_zone_name": "%s",\n'% irods_zone)
                f.write(' "irods_port": %s,\n' % irods_port)
                f.write(' "irods_user_name": "%s"' % username)
                if home_dir is not None:
                    f.write(',\n "irods_home": "%s"\n' % home_dir)
                f.write('\n}')
            
            
        print('Initializing environment')
        sys.stdout.flush()
        p = getpass.getpass('Please enter your iRODS password: ')
        irods_cmd = 'iinit -V %s' % (p)
        cmd = Popen([irods_cmd], stdout=PIPE, stderr=STDOUT, shell=True)
        stdout = cmd.communicate()[0].decode('ascii')
        if cmd.returncode != 0:
            print('Failed to fetch irods file: %s' % stdout)
            return []
        else:
            print('Authentication Successful')
            sys.stdout.flush()
            
        
    def iinit(self):
        """initializes the icommands for an irods userzone
        
        args: 
        -- None
        
        returns:
        -- None
        """
        
        # remove old irods settings if they exist
        if os.path.exists(self.ienv):
            os.remove(self.ienv)
        if os.path.exists(self.iauth):
            os.remove(self.iauth)
            
        self._init_icommands()
        
        pass
        
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
        
        filename = os.path.basename(filename)
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

