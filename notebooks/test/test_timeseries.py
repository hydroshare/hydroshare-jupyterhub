import os, sys
import unittest

# todo: remove this sys.path call.  The docker container should have the utilities dir in the system path

sys.path.append(os.path.abspath('../'))
os.environ['DATA'] = '.'

# todo:-------------------------------------------

import numpy as np
import itertools as it
from datetime import datetime
from utilities import hydroshare
import shutil

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
    input = raw_input
else:
    from unittest.mock import patch


class TaudemNotebook(unittest.TestCase):

    def setUp(self):

        # with patch('__builtin__.raw_input', return_value='hydro') as _raw_input:
        self.hs = hydroshare.hydroshare(username='tonytest2', password='hydro')
        self.resid = '927094481da54af38ffb6f0c39ad8787'

    def tearDown(self):
        outfile = 'beaver_divide_temp_daily_agg.csv'
        if os.path.exists(outfile):
            os.remove(outfile)
        if os.path.exists(self.resid):
            shutil.rmtree(self.resid)


    def testNotebookOperations(self):

        # operations for timeseries.ipynb

        with patch.object(hydroshare, 'input', return_value='y'):
            content = self.hs.getResourceFromHydroShare('927094481da54af38ffb6f0c39ad8787')
        self.assertTrue(os.path.exists('./927094481da54af38ffb6f0c39ad8787'))

        self.assertTrue('BeaverDivideTemp.csv' in self.hs.content)
        air_temp_csv = self.hs.content['BeaverDivideTemp.csv']
        f = open(self.hs.content['BeaverDivideTemp.csv'])
        self.assertFalse(f.closed)

        data = np.genfromtxt(air_temp_csv, comments='#', delimiter=',',autostrip=True,
                             converters={0: lambda x: datetime.strptime(x.decode("utf-8"),
                                                               '%m-%d-%Y %H:%M:%S')})

        # ----------------------------------------------
        start = data[0][0]
        lenperiod = 1
        grouped_data = []
        grouped_dates = []
        ind = 0
        for k, g in it.groupby(data,lambda data: (data[0]-start).days // lenperiod):
            group = list(g)
            grouped_dates.append(group[0][0])
            d = [g[1] for g in group if g[1] != -9999]
            grouped_data.append(d)

        # ----------------------------------------------

        t_min = np.full((len(grouped_dates), 1),  9999, dtype=np.float)
        t_max = np.full((len(grouped_dates), 1), -9999, dtype=np.float)
        t_ave = np.full((len(grouped_dates), 1), 0, dtype=np.float)
        for i in range(len(grouped_dates)):
            temp_count = 0
            for temp in grouped_data[i]:
                if temp > -80:
                    if temp < t_min[i]:
                        t_min[i] = temp
                    if temp > t_max[i]:
                        t_max[i] = temp
                    t_ave[i] += temp
                    temp_count += 1
            t_ave[i] = (t_ave[i] / temp_count).round(2)

        # ----------------------------------------------

        # set the save path for the aggregated values
        temp_agg = os.path.join(os.environ['DATA'], 'beaver_divide_temp_daily_agg.csv')

        # write the derived temperatures to a csv file
        with open(temp_agg, 'w') as f:
            f.write('Date, Ave Temp (C), Min Temp (C), Max Temp (C)\n')
            for i in range(len(grouped_dates)):
                f.write('%s,%3.2f,%3.2f,%3.2f\n' %
                       (grouped_dates[i].strftime('%m-%d-%Y'), t_ave[i], t_min[i], t_max[i]))

        # ---------------------------------------------- 

