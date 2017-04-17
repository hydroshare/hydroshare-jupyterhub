from os import environ
from os.path import relpath, join, dirname, abspath, exists


def get_relative_path(p):
    """
    gets the path relative to the jupyter home directory 
    p: path to convert into relative path
    
    returns the path relative to the default jupyter home directory
    """
    
    return join('/', relpath(p, join(environ['NOTEBOOK_HOME'], '../')))

def get_server_url_for_path(p):
    """
    gets the url corresponding to a given file or directory path
    p : path to convert into a url
    
    returns the url path for the filepath p
    """
    
    #http://jupyter.uwrl.usu.edu/user/tonycastronova/tree/notebooks/data/mysim
    
    load_environment()
    rel_path = relpath(p, environ['NOTEBOOK_HOME'])    
    url = '%s%s/notebooks/notebooks/%s' % (':'.join(environ['JUPYTER_HUB_IP'].split(':')[:-1]),
           environ['JPY_BASE_URL'], rel_path)
    return url

def load_environment(env_path=None, silent=True):

    # load the environment path (if it exists)
    if env_path is None:
        if 'NOTEBOOK_HOME' in environ.keys():
            env_path = join(environ['NOTEBOOK_HOME'], '.env')

    if not exists(env_path):
        print('\nEnvironment file could not be found.  Make sure that the JUPYTER_ENV variable is set properly')
        return

    with open(env_path, 'r') as f:
        lines = f.readlines()
        print('Adding the following system variables:')
        for line in lines:
            k, v = line.strip().split('=')
            environ[k] = v
            print('   %s = %s' % (k, v))
        print('\nThese can be accessed using the following command: ')
        print('   os.environ[key]')
        print('\n   (e.g.)\n   os.environ["HS_USR_NAME"]  => %s' % environ['HS_USR_NAME'])


