# Script

Two scripts are uploaded under the `Mexico` folder:<br>
* [200619 Data Task](https://github.com/dorisludo/Electricity-Data-ETL/blob/master/Script/Mexico/200619%20Data%20Task.py)
* [200619 Data Task Individual Dates Download](https://github.com/dorisludo/Electricity-Data-ETL/blob/master/Script/Mexico/200619%20Data%20Task%20Individual%20Dates%20Download.pyy)

## 200619 Cicala Data Task
This script allows one to scrap [Gobierno de Mexico](https://www.cenace.gob.mx/SIM/VISTA/REPORTES/DemandaRealSist.aspx), download the zip file containing hourly load data between Jan-27 2016 and Jun-05 2020, and perform the necessary cleaning. 

The script contains three parts.
> * Scraping the website
> * Raw Data Scrubbing
> * Data Transformation 

Together the `prepa` function and the `panda_prepa` function alongside time conversion functions used in `panda_prepa` transform the raw data into a clean CSV with the designated columns.

The Zip file and the final CSV could be found under the `/Data/Mexico` subdirectory.

## 200619 Cicala Data Task Individual Dates Download
This script allows one to download daily hourly load csv one by one. However, by putting the scraping process into a for-loop, [Gobierno de Mexico](https://www.cenace.gob.mx/SIM/VISTA/REPORTES/DemandaRealSist.aspx) flags the ChromeDriver as bot and redirects one to the Contact page. Measures taken to avoid bot detection, such as obscuring user-agent and randomizing elapsing time between actions, have been futile. 

However, the script is provided as a reference and could potentially be further developed or adjusted for scraping the websites of electricity wholesale market that do not provide compressed files.
