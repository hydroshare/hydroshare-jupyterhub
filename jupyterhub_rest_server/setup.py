import os, sys
from distutils.core import setup

setup(name='JupyterhubRestServer',
      version='1.0',
      description='A rest server for HydroShare-JupyterHub',
      author='Tony Castronova',
      author_email='acastronova@cuahsi.org',
      url='www.cuahsi.org',
      packages=['jupyterhub_rest_server'],
      install_requires= [
	'appdirs==1.4.2',
	'ipgetter==0.6',
	'pyparsing==2.1.10',
	'six==1.10.0',
	'tornado==4.4.2'
      ],
     )

