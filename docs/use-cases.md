<!--
When writing use cases keep the following in mind:

* Why should CUAHSI be doing this? 
* What is CUAHSI’s role?  
* Why is it our “job”?

* Make the Benefit of accomplishing this use case clear
   - How would a scientist accomplish this task right now (without this tech)?
   - What is the relative benefit of this tech to the user and to CUAHSI?  

* Convey the cost of accomplishing this use case
  - Minimal development tasks as a checklist.  
-->


HydroShare JupyterHub Use-Cases

Anthony Castronova  
Hydrologic Scientist  
Consortium of Universities for the Advancement of Hydrologic Science, Inc  


This document outlines development use cases for the HydroShare JupyterHub software stack. Its purpose is to clearly identify directions for future development that can be presented to the CUAHSI board of directors for feedback and prioritization.  The use cases are expressed using the document structure outlined below with goal of accurately and concisely conveying their motivation, tasks, and amount of effort required to complete.  The framework and terminology for these use cases was adopted from Alistair Cockburn and summarized in the following document: http://lyle.smu.edu/~lghuang/CSE7316/paper/gettingstartedwithusecasemodeling.pdf

      
### Document Structure

**Motivation**    

* Summary of activity
  * Background
  * Identify target actor(s)
  * Limitations of current approaches (i.e. justify the importance)
* Summary of our role in this effort
  * Why is it our responsibility to support this use case?
  * Explain the value added to the community
     * Benefit to the user(s)  
     * Benefit to HydroShare/CUAHSI   

**Preconditions**   
A list of conditions that we assume are true at the start of the use case.
   
**User Tasks**   
An ordered list of tasks that a user must complete to satisfy the use case.  
   
**Minimal Tasks to Satisfy the Use Case**  
A list of the items that still need to be implemented to achieve minimal success of the use case.   
   
**Potential Future Extensions**  
A list of the items could be implemented to extend the initial use case.

## 1. Execute Computationally Intensive Python Notebooks  
### Motivation  
Scientists typically develop algorithms and software routines for hydrologic analysis that are limited to small or moderate computational scales due to the compute limitations. These scales are often acceptable for development and testing purposes, however many studies require analysis at computational scales that exceed the capabilities of personal computers.  Executing full-scale analysis on a personal computer can consume all hardware resources thereby stagnating all other research until analysis has completed and effectively stalling research progress.  For example, executing a distributed hydrologic model at a regional scale or running data intensive algorithms across a collection of datasets would completely consume a typical personal computer. To satisfy these computational limitations, researchers must invest in compute resources such as workstations, cloud servers, or HPC cycles which must be maintained over time.  Instead, scientists should have access to tools and libraries to facilitate the execution of these prototype routines using community hosted and FOSS software. One approach for providing such functionality is the HydroShare JupyterHub initiative which provides compute cycles capable of supporting most small to medium scale hydrologic routines and is ideal for prototyping.  The development of the JupyterHub software and infrastructure supports CUAHSI's mission to foster hydrologic research by providing a community-based portal for scientists to prototype, collaborate, and validate published results.  Moreover, linking this environment with the HydroShare search and discovery interface enables scientists to host their published results and workflows in a manner that supports reproducible science and generally satisfies NSF's requirement for funded work to disseminate and sharing research results.


### Preconditions
* The scientist has developed their routine as a Python notebook
* All required libraries are installed on the JupyterHub server

### User Tasks
1. A Python notebook is developed and tested locally by the user.  
2. The notebook and supporting data is uploaded to the cloud using standard JupyterHub interface functionality.  
3. The notebook is executed through the JupyterHub interface.  
4. Results are saved to the local userspace on the JupyterHub cloud.  
5. Using built-in libraries, a new HydroShare resource is created from within the Python notebook.  
6. Results are downloaded by the user from the JupyterHub interface or via HydroShare.

### Minimal Tasks to Satisfy the Use Case

* [x] Deploy a JupyterHub server instance on NCSA
  * [x] Install scientific libraries
* [x] Setup Python 2 and 3 kernels
* [x] Establish a connection with HydroShare using OAuth
* [x] Build libraries 
   * [x] HydroShare library - uses `hs_restclient` to transfer files between JupyterHub and HydroShare
* [x] Provide examples for running Python notebooks using HydroShare data

### Potential Future Extensions  
* [ ] Implement quotas so that users do not hog server resources
   * [ ] use docker settings to adjust CPU, RAM, HDD quotas.
* [ ] Enable HPC execution 
   * [ ] Create a library to facilitate the execution of jobs on ROGER  
   * [ ] Create a library to facilitate the execution of jobs using RADII
* [ ] Support large file transfer between HydroShare and JupyterHub.  This is necessary to enable scientists to work with large datasets, including those that may result from scaling algorithms.
   * [ ] Mount iRODs disk storage to connect the user with large HydroShare datasets (i.e. beyond 2 GB)  

---

## 2. Execute Data Intensive Python Notebooks

### Motivation
Routines for hydrologic analysis are often developed and tested at partial scales before they are deployed at full scale (e.g. national or continental spatial scales). Typically the full scale execution of these scripts requires considerable data to be downloaded for processing which can be automated using web services. However, many consecutive data queries and downloads can consume a significant portion of CPU as well as considerable disk space.  This is problematic for researchers that rely on a single computer for their research for which data download and analysis will consume significant CPU, and HDD resources. Moreover, much of these "raw" data are not used after analysis is complete but they consume a considerable amount of hard drive storage.  The overall download and processing requirements of these data intensive analysis deter community validation of results.  Scientists should have access to community designed/developed cloud services to overcome these limitations.  One solution is to allow scientist to uploaded and/or download hydrologic data to the HydroShare JupyterHub server and  execute their routines remotely on cloud infrastructure. The development of the JupyterHub software to support data intensive research activities using JupyterHub supports CUAHSI's mission to facilitate water science research by providing FOSS platform for scientists to analyze datasets that exceed the resources of their personal computers.  Furthermore, this activity enables researchers to collaborate and validate the findings and analysis of large datasets without the time and CPU intensive data collection process occurring on their computer.  Moreover, linking this environment with the HydroShare search and discovery interface enables scientists to host their published results and workflows in a manner that supports reproducible science and generally satisfies NSF's requirement for funded work to disseminate and sharing research results.


### Preconditions  
* The scientist has prototyped and tested their algorithm as a Python notebook  
* Data is downloaded within the Python notebook via web services  
* All required libraries are already installed on the JupyterHub server  

### User Tasks  
1. A Python notebook is developed and tested locally  
2. The notebook is uploaded directly to the cloud using standard JupyterHub functionality  
3. The notebook is executed through the JupyterHub interface  
4. Results are saved to the local userspace on the JupyterHub cloud.  
5. Using the hsutils built-in library, a new HydroShare resource is created from within the Python notebook.  
6. Results are downloaded by the user from the JupyterHub interface or via HydroShare.  

### Minimal Tasks to Satisfy the Use Case
* [x] Deploy a JupyterHub server instance on NCSA
  * [x] Install scientific libraries
* [x] Setup Python 2 and 3 kernels
* [x] Establish a connection with HydroShare using OAuth
* [x] Build libraries 
   * [x] HydroShare library - uses `hs_restclient` to transfer files between JupyterHub and HydroShare
   * [ ] Utility for cleaning data from userspace
* [ ] Provide examples
   * [ ] Collecting and processing a large amount of data  
   * [ ] Moving large amounts of data between JupyterHub and HydroShare  

### Potential Future Extensions
* [ ] Implement quotas so that users do not hog server resources
   * [ ] use docker settings to adjust CPU, RAM, HDD quotas.
* [ ] Enable HPC execution 
   * [ ] Create a library to facilitate the execution of jobs on ROGER  
   * [ ] Create a library to facilitate the execution of jobs using RADII
* [ ] Support large file transfer between HydroShare and JupyterHub.  This is necessary to enable scientists to work with large datasets, including those that may result from scaling algorithms.
   * [ ] Mount iRODs disk storage to connect the user with large HydroShare datasets (i.e. beyond 2 GB)  
