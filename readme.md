# HydroShare Jupyterhub Notebook Server

The HydroShare Jupyterhub Notebook Server is an environment specifically designed to link HydroShare resources to user-generated web computations (e.g. Python notebooks). It extends the FOSS [JupyerHub](https://github.com/jupyterhub/jupyterhub) project to incorporate libraries designed to provided seamless interaction with HydroShare web resources and core functionality.  This project also leverages [docker](https://www.docker.com/) containers to provide users with isolated linux environments where they can build, modify, and store custom Jupyter notebooks and data.  While this software can be deployed as a stand-alone application, it is intended to interact with HydroShare resources via WebApps that invoke a REST API, e.g. [Jupyer-NCSA](https://www.hydroshare.org/resource/80d9f3b4bc914628a2d1df4ebebcc3fd/) (an instance deployed at the Resourcing Open Geo-spatial Education and Research (ROGER) supercomputer).


See [setup.md](setup.md) for detailed installation instructions.
