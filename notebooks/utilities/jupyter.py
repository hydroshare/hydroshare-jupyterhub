from os import environ
from os.path import relpath, join, dirname, abspath


def get_relative_path(p):
    """
    gets the path relative to the jupyter home directory 
    p: path to convert into relative path
    
    returns the path relative to the default jupyter home directory
    """
    
    return join('/', relpath(p, join(environ['HOME'], '../')))

def get_server_url_for_path(p):
    """
    gets the url corresponding to a given file or directory path
    p : path to convert into a url
    
    returns the url path for the filepath p
    """
    
    #http://jupyter.uwrl.usu.edu/user/tonycastronova/tree/notebooks/data/mysim
    
    load_environment()
    rel_path = relpath(p, environ['HOME'])    
    url = '%s%s/notebooks/notebooks/%s' % (':'.join(environ['JUPYTER_HUB_IP'].split(':')[:-1]),
           environ['JPY_BASE_URL'], rel_path)
    return url

def load_environment(silent=True):
    env_path = join(dirname(abspath(__file__)), 'env')
    with open(env_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            k,v = line.strip().split('=')
            environ[k] = v
        if not silent:
            print('Loading environment variables: ')
            print(' These can be accessed using [os.environ]: ')
            print(' os.environ["HS_USR_NAME"]  => %s' % environ['HS_USR_NAME'])

