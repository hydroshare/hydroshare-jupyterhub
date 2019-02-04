from distutils.core import setup

setup(name='HydroSharePythonUtilities',
      version='1.0',
      description='Convenience functions for accessing HydroShare resources',
      author='Tony Castronova',
      author_email='acastronova@cuahsi.org',
      url='www.cuahsi.org',
      packages=['utilities', 'utilities.hydroshare', 'utilities.irods', 'utilities.plotting'],
      install_requires=[
            'matplotlib',
            'pandas'
            ],
      )
