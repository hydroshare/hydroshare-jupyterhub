import inspect
import shutil


print ('utils imported')

def save_script(fname):

    frame = inspect.stack()[1]
    print(frame)

    module = inspect.getmodule(frame[0])
    print(module)

    print(module.__name__)
