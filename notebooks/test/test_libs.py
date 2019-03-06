from os.path import abspath, join, dirname
import unittest
import nbrunner
import sys
import os
import subprocess
from utilities import hydroshare
import pkg_resources as p

"NOTE: If running inside a conda container, make sure that Jupyter is installed in the base environment or else" \
"the nbconvert command will fail with a 'file not found' exception"

"""
REQUIREMENTS

Todo: execute the unit test inside the docker container!!!!!

"""

class TestExamples(unittest.TestCase):

    def setUp(self):
        pass
#        self.examples_path = abspath(dirname(__file__))
#        sys.path.append(abspath(join(self.examples_path, '../')))
#        self.env = os.environ.copy()
#        self.env["PATH"] = "/usr/sbin:/sbin:" + '/'

    def tearDown(self):
        pass

    def test_lib_imports(self):
        self.assertTrue(pkg_resources.get_distribution("gdal").version == "2.1.3")
        self.assertTrue(pkg_resources.get_distribution("h5py").version =="2.7.0")
        self.assertTrue(pkg_resources.get_distribution("hdf4").version == "4.2.12")
        self.assertTrue(pkg_resources.get_distribution("hdf5").version == "1.8.17")
        self.assertTrue(pkg_resources.get_distribution("landlab").version == "1.0.3")
        self.assertTrue(pkg_resources.get_distribution("libspatialite").version == "4.3.0a")
        self.assertTrue(pkg_resources.get_distribution("matplotlib").version == "2.0.0")
        self.assertTrue(pkg_resources.get_distribution("netcdf4").version =="1.2.7")          
        self.assertTrue(pkg_resources.get_distribution("numpy").version == "1.11.3")
        self.assertTrue(pkg_resources.get_distribution("pandas").version == "0.19.2")
        self.assertTrue(pkg_resources.get_distribution("pillow").version == "4.1.0")
        self.assertTrue(pkg_resources.get_distribution("pyshp").version == "1.2.10")
        self.assertTrue(pkg_resources.get_distribution("qt").version == "5.6.2")
        self.assertTrue(pkg_resources.get_distribution("scipy").version == "0.19.0")
        self.assertTrue(pkg_resources.get_distribution("seaborn").version == "0.7.1")
        self.assertTrue(pkg_resources.get_distribution("sqlalchemy").version == "1.1.5")
        self.assertTrue(pkg_resources.get_distribution("suds-jurko").version == "0.6")
        self.assertTrue(pkg_resources.get_distribution("ulmo").version == "0.8.4")
