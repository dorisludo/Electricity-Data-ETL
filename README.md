# README

## Requirements
All requirements must be installed and set up for command line usage. For further detail, see the **Command Line Usage** section below.

* Python (3.7)
* pip (>=10.0)
* Homebrew

To run the scripts as-is in `Script`, the following packages should be installed in your Python environment: 

* pandas
* seaborn 
* matplotlib
* selenium
* pytz
* numpy
* chromedriver 

The packages and are used by the scripts contained in the repository. 

## Setup
**If you are using Windows, you will need to run all bash commands in administrator mode. To do so, open your terminal by right clicking and selecting `Run as administrator`. To set administrator mode on permanently, refer to the [RA manual](https://github.com/gentzkow/template/wiki/Repository-Usage#Administrator-Mode).**

**For Windows set-up of selenium and ChromeDriver:** please refer to `Detailed instructions for Windows users` [here](https://selenium-python.readthedocs.io/installation.html).

1. Install Python dependencies listed above using pip. 

2. Install ChromeDriver with the following terminal command:
```
brew cask install chromedriver
```

3. Download the associated script files from the `Script` subdirectory and save them in the directory of your Python environment.

4. For Running Jupyter Notebook, Launch Jupyter Notebook with the following command in your terminal
```
   $ jupyter notebook
```

5. Modify the file paths to their respective paths in your working environment. 
