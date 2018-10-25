from distutils.core import setup

setup(name='JupyterhubRestServer',
      version='1.0',
      description='A rest server for HydroShare-JupyterHub',
      author='Tony Castronova',
      author_email='acastronova@cuahsi.org',
      url='www.cuahsi.org',
      packages=['jupyterhub_rest_server'],
      install_requires= ['tornado==4.4.2'],
     )

