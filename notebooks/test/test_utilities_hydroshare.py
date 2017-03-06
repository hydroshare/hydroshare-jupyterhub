from __future__ import print_function
import unittest
import hs_restclient
from utilities.hydroshare import utilities, resource
import tempfile
import os
import shutil
import glob

class hydroshareUtilities(unittest.TestCase):


    def setUp(self):
        self.resid = '68313c40c7ff48cd9e065ceada3c8426'
        os.environ['HOME'] = os.path.dirname(__file__)

    def tearDown(self):

        # remove any leftover temp workspaces
        current_dir = os.path.dirname(__file__)
        for f in glob.glob(os.path.join(current_dir, 'tmp*')):
            shutil.rmtree(f)

    def test_sizeof(self):

        b = 1024
        res = utilities.sizeof_fmt(b)
        self.assertTrue(res == '1.0KiB')

        kb = 1024*b
        res = utilities.sizeof_fmt(kb)
        self.assertTrue(res == '1.0MiB')

        mb = 1024*kb
        res = utilities.sizeof_fmt(mb)
        self.assertTrue(res == '1.0GiB')

        gb = 1024*mb
        res = utilities.sizeof_fmt(gb)
        self.assertTrue(res == '1.0TiB')

        tb = 1024*gb
        res = utilities.sizeof_fmt(tb)
        self.assertTrue(res == '1.0PiB')

        pb = 1024*tb
        res = utilities.sizeof_fmt(pb)
        self.assertTrue(res == '1.0EiB')

        eb = 1024*pb
        res = utilities.sizeof_fmt(eb)
        self.assertTrue(res == '1.0ZiB')

    def test_resourcedir(self):

        # create a temp workspace and download the test resource
        tdir = tempfile.mkdtemp(dir='.')
        hs = hs_restclient.HydroShare()
        hs.getResource(self.resid, destination=tdir, unzip=True)

        # test resolve path by resid
        path = utilities.find_resource_directory(self.resid)

        parts = [os.environ['HOME'], tdir, self.resid]
        self.assertTrue(path == os.path.abspath(os.path.join(*parts)))

    def test_findipynb(self):

        # set testing environment vars
        os.environ['JUPYTER_HUB_IP'] = '123.456.78.910:8080'
        os.environ['JPY_BASE_URL'] = '/user/myuser'

        # create a temp workspace and download the test resource
        tdir = tempfile.mkdtemp(dir='.')
        hs = hs_restclient.HydroShare()
        hs.getResource(self.resid, destination=tdir, unzip=True)

        content = utilities.get_hs_content(self.resid)

        # test resolve ipynb files
        notebk = utilities.check_for_ipynb(content)
        expected_path = '123.456.78.910:8080/user/myuser/notebooks/notebooks/%s/%s/%s/data/contents/taudem_logan.ipynb' % (
            os.path.basename(tdir), self.resid, self.resid)

        self.assertTrue(len(notebk.keys()) == 1)
        self.assertTrue(notebk['taudem_logan.ipynb'] == expected_path)

    def test_getcontent(self):

        # create a temp workspace and download the test resource
        tdir = tempfile.mkdtemp(dir='.')
        hs = hs_restclient.HydroShare()
        hs.getResource(self.resid, destination=tdir, unzip=True)

        content = utilities.get_hs_content(self.resid)

        self.assertTrue(len(content.keys()) == 2)
        self.assertTrue('logan.tif' in content)
        self.assertTrue('taudem_logan.ipynb' in content)

    def test_displayresource(self):
        pass

    def test_runthreaded(self):
        pass


class hydroshareResource(unittest.TestCase):

    def setUp(self):
        self.resid = '68313c40c7ff48cd9e065ceada3c8426'
        pass

    def tearDown(self):
        pass

    def test_resource_object(self):
        hs = hs_restclient.HydroShare()
        sys_md = hs.getSystemMetadata(self.resid)
        sci_md = hs.getScienceMetadata(self.resid)

        self.assertTrue(type(sys_md) == dict)
        self.assertTrue(type(sci_md) == dict)

        res = resource.ResourceMetadata(sys_md, sci_md)

        self.assertTrue(res.url == sys_md['resource_url'])
        self.assertTrue(res.abstract == sci_md['description'])

        keywords = [s['value'] for s in sci_md['subjects']]
        self.assertTrue(res.keywords == keywords)



