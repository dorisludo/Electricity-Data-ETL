from datetime import datetime
from selenium import webdriver
import pandas as pd
import csv
import os
import numpy as np
import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import zipfile
import glob
import pytz
from pytz import timezone


country_path = "/Users/Doris/Downloads/Electri/Chile/" #Path for Holding the Initial Zip and Final Output
os.mkdir(country_path)
os.chdir(country_path)

url = 'https://www.cenace.gob.mx/SIM/VISTA/REPORTES/DemandaRealSist.aspx'


# Configuration 

chrome_options = Options()
chrome_options.headless = True #Not Launching Browser
chrome_options.add_experimental_option("prefs",{
    "download.default_directory":country_path,
    "download.prompt_for_download": False}) # Setting Download Preference
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options = chrome_options)

# HTML XPaths
datepath1 = '//*[@id="ctl00_ContentPlaceHolder1_RadDatePickerVisualizarPorBalance_dateInput"]'
buttonpath = "//input[@name='ctl00$ContentPlaceHolder1$GridRadPorBalance$ctl00$ctl04$gbccolumn' and @id ='ctl00_ContentPlaceHolder1_GridRadPorBalance_ctl00_ctl04_gbccolumn']"

# Zip XPaths
initiatepath = '//*[@id="ctl00_ContentPlaceHolder1_RadDatePickerFIVisualizarPorBalance_dateInput"]'
finalpath = '//*[@id="ctl00_ContentPlaceHolder1_RadDatePickerFFVisualizarPorBalance_dateInput"]'
zippath = '//*[@id="ctl00_ContentPlaceHolder1_DescargarArchivosCsv_PorBalance"]'

# Load URL
driver.get(url)


time.sleep(np.random.randint(20,40))

# Additional Configuration 
wait = WebDriverWait(driver,60)
element = wait.until(EC.presence_of_element_located((By.XPATH,datepath1)))
zip_button = driver.find_elements_by_xpath(zippath)[0]
click_button = driver.find_elements_by_xpath("//input[@name='ctl00$ContentPlaceHolder1$GridRadPorBalance$ctl00$ctl04$gbccolumn' and @id ='ctl00_ContentPlaceHolder1_GridRadPorBalance_ctl00_ctl04_gbccolumn']")[0]

# Fill in Initial and Final Dates
initial = wait.until(EC.presence_of_element_located((By.XPATH,initiatepath)))
initial.clear()
initial.send_keys('27/01/2016')
final = wait.until(EC.presence_of_element_located((By.XPATH,finalpath)))
final.clear()
final.send_keys('05/06/2020')

# Initiate Download
zip_button.click()


time.sleep(300)


# Check Download
files = os.listdir(country_path)
for file in files:
    if re.search(r'.zip',file) is not None:
        zip_name = file
        if os.path.getsize(zip_name) != 24550033:
            time.sleep(200)
        elif os.path.getsize(zip_name) == 24550033:
            print('Zip file downloaded is '+file)
    else:
        print('Please Inspect Directory') # Wait 3 minutes+
        assert re.search(r'.zip',file) is not None #DOUBLE CHECK

# Close Driver
driver.close()


raw_path = '/Users/Doris/Downloads/Electri/Chile/Raw/' # Path for Hosting Raw CSVs
os.mkdir(raw_path)


# Read in Zip
with zipfile.ZipFile(zip_name, 'r') as zips: 
    # printing all the contents of the zip file 
    zips.printdir() 
    # extracting all the files 
    print('Extracting all the files now...') 
    zips.extractall('/Users/Doris/Downloads/Electri/Chile/Raw/') 
    print('Done!') 


cleanpath = '/Users/Doris/Downloads/Electri/Chile/Clean/' # Path for Storing First-Stage Cleaning CSVs[Suitable for Plotting]
os.mkdir(cleanpath)


# Raw CSV Clean Function
def prepa(file):
    try:
        open(file,'r')
        print("File opened successfully")
        cleaned = clean+'_chile.csv'
        header_row_needed = True
        newheader = []
        write = []
        lines_read, lines_written = 0, 0
    except:
        print("The file could not be pulled")
    else:
        f = open(file,'r')
        for line in f:
            lines_read += 1
            # Header
            if " Generacion (MWh)" in line and header_row_needed:
                    header = line.split(",")
                    for item in header:
                        item = item.replace('"','')
                        item = item.strip()
                        newheader.append(item)
                    newheader.insert(0,'Date')
                    #print(newheader)
                    header_row_needed = False
                    write.append(newheader)
            elif header_row_needed is False:
                values = [x.strip("\"") for x in line.split(',')]
                valuesc = []
                for i in values:
                    i = i.strip()
                    i = i.strip('\"')
                    if i == '':
                        pass
                    else:
                        valuesc.append(i)
                if len(valuesc) == 0:
                    continue
                else:
                    valuesc.insert(0,clean) # Append Date
                    write.append(valuesc)
        f.close()
        with open(cleanpath+cleaned,'w') as csvfile:
            cleanedelectri = csv.writer(csvfile, delimiter = ',', dialect = 'excel')
            for row in write:
                cleanedelectri.writerow(row)
                lines_written += 1
        csvfile.close()

        print("Lines Read:" + str(lines_read))
        print("Lines Written:" + str(lines_written))



files = sorted(glob.glob(raw_path+'*'))


for file in files:
    if os.path.getsize(file) > 700:
        match = re.search('[0-9]{4}-{1}[0-9]{2}-[0-9]{2}',file)
        if match is not None:
            clean = match.group(0)
            print(clean)
            prepa(file)
    else:
        continue



finetl_path = '/Users/Doris/Downloads/Electri/Chile/FinETL/' #Path for Storing Final Individual CSVs
os.mkdir(finetl_path)

# For Time Zone Conversion
northregion = ['BCA','BCS','NES','NOR','NTE']
generegion = ['CEN','OCC','ORI','PEN']

def convert_to_local_time(row):
    return timezone(row.TimeZone).localize(row.Time)

def convert_to_dst_time(row):
    return timezone(row.TimeZone).normalize(row.Time) #Adjust for Daylight Saving

def convert_to_utc_time(row):
    return row.Time.astimezone(pytz.utc)

# Function for Final CSV
def panda_prepa(file):
    df = pd.read_csv(file)
    columnss = df.columns.to_list()
    
    for column in columnss:
        if column == 'Flujo Real de Importacion (MWh)':
            # columns.remove(column)
            df = df.drop(columns = column)
        if column == 'Importacion Total (MWh)':
            # columns.remove(column)
            df = df.drop(columns = column)
        if column == 'Intercambio neto entre Gerencias (MWh)':
            # columns.remove(column)
            df = df.drop(columns = column)
        if column == 'Flujo Real de Exportacion (MWh)':
            columnss[columnss.index(column)] = 'Exportacion (MWh)'
            # columns.remove(column)
            df = df.rename(columns = {'Flujo Real de Exportacion (MWh)':'Exportacion (MWh)'})
        if column == 'Exportacion Total (MWh)':
            columnss[columnss.index(column)] = 'Exportacion (MWh)'
            df = df.rename(columns = {'Exportacion Total (MWh)':'Exportacion (MWh)'})
            # columns.remove(column)
    
    for hour in df.Hora.unique():
        if hour >= 25:
            indexes = df[df['Hora'] == hour].index
            df.drop(indexes, inplace=True)
        else:
            continue
            
    df['Hora'] = df['Hora'].apply(lambda x: x-1)
    df['Hora'] = df['Hora'].astype(str);
    
    df['Time'] = 0
    df['Time'] = df[['Date', 'Hora']].apply(lambda x: ' '.join(x), axis=1)
    
    for hr in df['Time']:
        df.loc[df['Time'] == hr, ['Time']] = datetime.strptime(str(hr), '%Y-%m-%d %H')
    
    df['TimeZone'] = 0
    for region in df['Area']:
        if region in northregion:
            df.loc[df['Area'] == region,['TimeZone']] = 'Mexico/BajaNorte'
        elif region in generegion:
            df.loc[df['Area'] == region,['TimeZone']] = 'America/Mexico_City'
    
    df['Time'] = df.apply(convert_to_local_time, axis = 1)
    df['Time'] = df.apply(convert_to_dst_time, axis = 1)
    df['Time'] = df.apply(convert_to_utc_time, axis = 1)
    
    
    dfc = df.groupby(['Time','Area']).agg({'Estimacion de Demanda por Balance (MWh)':'sum'})
    dfc.reset_index(inplace = True)
    dfc = dfc.rename(columns = {'Estimacion de Demanda por Balance (MWh)':'load_mw'})
    dfc['pca_abbrev'] = 'Mex'
    dfc['Source'] = 'Gobierno De Mexico'
    dfc.to_csv(finetl_path+file[-20:], index = False)


filess = sorted(glob.glob(cleanpath+'*'))

for file in filess: 
    panda_prepa(file)


# Concatenate into one CSV
conc = sorted(glob.glob(finetl_path+'*'))
myli = []


for file in conc:
    df_tri = pd.read_csv(file)
    myli.append(df_tri)

dffin = pd.concat(myli, sort = False)


dffin.to_csv('MexicoElectricityData.csv', index = False)






