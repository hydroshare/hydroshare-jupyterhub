#!/usr/bin/env python3

# install testing dependencies
/opt/conda/bin/pip install moto

# test xarray
/opt/conda/bin/python -m pytest --pyargs xarray

# test pandas
#/opt/conda/bin/python -m pytest --pyargs pandas


# test landlab
/opt/conda/bin/python -m pytest --pyargs landlab
