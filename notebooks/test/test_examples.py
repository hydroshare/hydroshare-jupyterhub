from os.path import abspath, join, dirname
import unittest
import nbrunner
import sys
import os
import subprocess
from utilities import hydroshare

"NOTE: If running inside a conda container, make sure that Jupyter is installed in the base environment or else" \
"the nbconvert command will fail with a 'file not found' exception"

"""
REQUIREMENTS

Todo: execute the unit test inside the docker container!!!!!

PYTHON 3
sudo pip3 install nbformat
sudo pip3 install pyyaml
sudo pip3 install hs_restclient

"""

class TestExamples(unittest.TestCase):

    def setUp(self):
        self.examples_path = abspath(dirname(__file__))
        sys.path.append(abspath(join(self.examples_path, '../')))


        self.env = os.environ.copy()

        self.env["PATH"] = "/usr/sbin:/sbin:" + '/'

    def tearDown(self):
        pass

    def test_generic_timeseries(self):
        # notebook_path = join(self.examples_path, 'timeseries.ipynb')
        # notebook_path = join(self.examples_path, '../help/timeseries.ipynb')
        # nb, errors = nbrunner._notebook_run(notebook_path, self.env)
        # assert errors == []
        pass
