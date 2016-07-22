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