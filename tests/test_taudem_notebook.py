


import os, sys
import unittest
import shutil

# todo: remove this sys.path call.  The docker container should have the utilities dir in the system path

sys.path.append(os.path.abspath('../'))
os.environ['DATA'] = '.'

# todo:-------------------------------------------

from utilities import hydroshare, taudem

"""
----------
Lib Notes
----------

Python 2
pip install mock

"""


is_py2 = sys.version[0] == '2'
if is_py2:
    from mock import patch
else:
    from unittest.mock import patch


class TaudemNotebook(unittest.TestCase):

    def setUp(self):

        is_py2 = sys.version[0] == '2'
        if is_py2:
            input = raw_input

        # with patch('__builtin__.raw_input', return_value='hydro') as _raw_input:
        self.hs = hydroshare.hydroshare(username='tonytest2', password='hydro')

        # content = self.hs.getResourceFromHydroShare('6ee06abb2ed8414f9b66d229c8e9a129')

    def testUserSpaceCreation(self):

        # test creating the userspace
        with patch.object(taudem, 'input', return_value='yes'):
            data_directory = taudem.create_workspace('test_processing_env')
        self.assertTrue(os.path.exists(data_directory))

        # test recreating the userspace
        with patch.object(taudem, 'input', return_value='yes'):
            data_directory = taudem.create_workspace('test_processing_env')
        self.assertTrue(os.path.exists(data_directory))

        # test not recreating the userspace
        with patch.object(taudem, 'input', return_value='no'):
            data_directory = taudem.create_workspace('test_processing_env')
        self.assertTrue(os.path.exists(data_directory))

        # remove the test userspace
        os.removedirs(data_directory)
        self.assertTrue(not os.path.exists(data_directory))

    def testNotebookOperations(self):

        with patch.object(hydroshare, 'input', return_value='y'):
            content = self.hs.getResourceFromHydroShare('6ee06abb2ed8414f9b66d229c8e9a129')
        self.assertTrue(os.path.exists('./6ee06abb2ed8414f9b66d229c8e9a129'))

        with patch.object(taudem, 'input', return_value='no'):
            data_directory = taudem.create_workspace('temp')
        self.assertTrue(os.path.exists(data_directory))

        raw_dem_path = self.hs.content['logan.tif']

        fill = os.path.join(data_directory, 'loganfel.tif')
        cmd = 'pitremove -z %s -fel %s' % (raw_dem_path, fill)
        taudem.run_cmd(cmd, processors=4)
        self.assertTrue(os.path.exists(fill))

        fdr = os.path.join(data_directory, 'fdr.tif')  # flowdir
        sd8 = os.path.join(data_directory, 'sd8.tif')  # slope
        cmd = 'd8flowdir -fel %s -sd8 %s -p %s' % (fill, sd8, fdr)
        taudem.run_cmd(cmd, processors=4)
        self.assertTrue(os.path.exists(fdr))
        self.assertTrue(os.path.exists(sd8))

        ang = os.path.join(data_directory, 'loganang.tif')  # flow angle
        slp = os.path.join(data_directory, 'loganslp.tif')  # flow slope
        cmd = 'dinfflowdir -fel %s -ang %s -slp %s' % (fill, ang, slp)
        taudem.run_cmd(cmd, processors=4)
        self.assertTrue(os.path.exists(ang))
        self.assertTrue(os.path.exists(slp))

        ad8 = os.path.join(data_directory, 'loganad8.tif')  # D8 contributing area
        cmd = 'aread8 -p %s -ad8 %s' % (fdr, ad8)
        taudem.run_cmd(cmd, processors=4)
        self.assertTrue(os.path.exists(ad8))

        sca = os.path.join(data_directory, 'logansca.tif')  # D-Infinity contributing area
        cmd = 'areadinf -ang %s -sca %s' % (ang, sca)
        taudem.run_cmd(cmd, processors=4)
        self.assertTrue(os.path.exists(sca))

        shutil.rmtree('./6ee06abb2ed8414f9b66d229c8e9a129')
        self.assertTrue(not os.path.exists('./6ee06abb2ed8414f9b66d229c8e9a129'))

        shutil.rmtree(data_directory)
        self.assertTrue(not os.path.exists(data_directory))



#
# #
# # def answer():
# #     ans = raw_input('enter yes or no')
# #     if ans == 'yes':
# #         return 'you entered yes'
# #     if ans == 'no':
# #         return 'you entered no'
#
#
# import shutil
# def create_workspace(folder_name):
#     # get the data directory (this is an environment variable that is provided to you)
#     data_directory = os.path.join(os.environ['DATA'], folder_name)
#     create_dir = True
#     if os.path.exists(data_directory):
#         res = input('This directory already exists.\nWould you like to remove it [Y/n]? ')
#         if res != 'n':
#             shutil.rmtree(data_directory)
#         else:
#             create_dir = False
#             print('Directory creation aborted')
#
#     if create_dir:
#         os.mkdir(data_directory)
#         print('A clean directory has been created')
#
#     return data_directory
#
# class TestAnswer(unittest.TestCase):
#
#     # def setUp(self):
#         # is_py2 = sys.version[0] == '2'
#         # if is_py2:
#         #     input = raw_input
#
#
#     def test_yes(self):
#         with patch('raw_input', return_value='yes') as _raw_input:
#             data_directory = taudem.create_workspace('test_processing_env')
# #             self.assertEqual(answer(), 'you entered yes')
# #             _raw_input.assert_called_once_with('enter yes or no')
# #
#     # def test_no(self):
#     #     with patch('__builtin__.raw_input', return_value='no') as _raw_input:
#     #         a = answer()
#     #         self.assertEqual(answer(), 'you entered no')
#             # _raw_input.assert_called_once_with('enter yes or no')

