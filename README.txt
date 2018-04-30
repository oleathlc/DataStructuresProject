READMEConor Lawlor (17203166)This is a my solution for the term project of COMP20230.Prerequisites----------------------This project was created in a Python 3.6 environment, using Eclipse (Version: Oxygen.2 
Release (4.7.2)). It will be easier to set up the project if you install [Anaconda](https://conda.io/docs/user-guide/install/download.html) or [Miniconda](https://conda.io/miniconda.html). Other options, such as [PyEnv](https://github.com/pyenv/pyenv) and classic virtual environment (i.e. `venv`), will also work.Project Structure
-------------------
The project files (programs and input files) are contained in the Airport_Project
folder. Within this folder, there are two subfolders, input and project. All project programs are contained within the project subfolder and all the input files that are required to run these programs are contained within the input subfolder.
Setup
----------------------

Run the following commands in Terminal:

```
git clone https://github.com/oleathlc/DataStructuresProject.git && cd /project
```Running the Program-------------------There are two main programs, with two different algorithms, BFS.py and DFS.py.All csv files are stored in the input subfolder, while the project files are stored in the project subfolder. To run the project files correctly, ensure to replace the sample testroute.csv file in the input subfolder with the your own one.From the project directory (in Terminal), run this command```python BFS.py run   		-> to run the BFS.py program```Or```python DFS.py run   		-> to run the DFS.py program```Running the Tests------------------I have my tests set up to run with the pytest package, so this may need to be installed on your system, if it isn't already. This can be done using 'pip install pytest'. From the project directory (in Terminal), run this command```python -m pytest --verbose tests.py ```