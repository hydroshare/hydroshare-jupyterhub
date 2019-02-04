import os
import inspect
import shutil
import sys
import itertools

def save_script(fname):

    frame = inspect.stack()[1]
    print(frame)

    module = inspect.getmodule(frame[0])
    print(module)

    print(module.__name__)

def create_workspace(folder_name):

    # get the data directory (this is an environment variable that is provided to you)
    data_directory = os.path.join(os.environ['DATA'], folder_name)
    create_dir = True
    if os.path.exists(data_directory):
        print('This directory already exists.')
        tree(data_directory)
        res = input('\nDo you want to overwrite these data [Y/n]? ')
        if res != 'n':
            shutil.rmtree(data_directory)
        else:
            create_dir = False
            print('Directory creation aborted')
            
    if create_dir:
        os.mkdir(data_directory)
        print('A clean directory has been created')  
    
    return data_directory

class heartbeat(object):

    def __init__(self, progress_message, finish_message='Finished', error_message='An error has occurred'):

        # create a simple progress bar
        pulse_array  = ['___________________']*20
        pulse_array = [pulse_array[i][:i] + '/\\' + pulse_array[i][i:] for i in range(len(pulse_array))]
        pulse_array = pulse_array + pulse_array[-2:0:-1]
        self.pulse = itertools.cycle(pulse_array)

        self.msg = '\r' + progress_message
        self.fin = '\r' + finish_message 
        self.err = '\r' + error_message 
        
        self.overwrite_progress_length = len(self.msg) + 21
    
    def clearLine(self):
        chars = len(self.msg) +  27
        sys.stdout.write('\r%s' % (chars * ' '))
        sys.stdout.flush()

    def updateProgressMessage(self, msg):
        self.msg = '\r' + msg

    def writeprogress(self):
        self.clearLine()
        sys.stdout.write(' '.join([self.msg, next(self.pulse)]))
        sys.stdout.flush()
    
    def success(self):
        self.clearLine()
        sys.stdout.write(self.fin + '\n')
        sys.stdout.flush()
    
    def error(self):
        self.clearLine()
        sys.stdout.write(self.err + '\n')
        sys.stdout.flush()

    def update(self, *args):
        self.clearLine()
        msg = self.msg + ' %s  '
        args += tuple([next(self.pulse)])
        sys.stdout.write(msg % args)
        sys.stdout.flush()
        
        
def _realname(path, root=None):
    if root is not None:
        path=os.path.join(root, path)
    result=os.path.basename(path)
    if os.path.islink(path):
        realpath=os.readlink(path)
        result= '%s -> %s' % (os.path.basename(path), realpath)
    return result

def tree(startpath, depth=-1):
    prefix=0
    if startpath != '/':
        if startpath.endswith('/'): startpath=startpath[:-1]
        prefix=len(startpath)
    for root, dirs, files in os.walk(startpath):
        level = root[prefix:].count(os.sep)
        if depth >-1 and level > depth: continue
        indent=subindent =''
        if level > 0:
            indent = '|   ' * (level-1) + '|-- '
        subindent = '|   ' * (level) + '|-- '
        print('{}{}/'.format(indent, _realname(root)))
        # print dir only if symbolic link; otherwise, will be printed as root
        for d in dirs:
            if os.path.islink(os.path.join(root, d)):
                print('{}{}'.format(subindent, _realname(d, root=root)))
        for f in files:
            print('{}{}'.format(subindent, _realname(f, root=root)))