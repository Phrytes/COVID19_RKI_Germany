import pandas as pd
import numpy as np
import requests
import re
import os
from bs4 import BeautifulSoup

RKI_url = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html'
requestRKI = requests.get(RKI_url)
soup = BeautifulSoup(requestRKI.content)
table = soup.find("table")
date = soup.find_all("div", class_="dateOfIssue")
date = re.findall('\\d\\d\\.\\d\\d\\.\\d\\d\\d\\d', str(date))[0]
date = date.replace(".", "-")

output_rows = []
for table_row in table.findAll('tr'):
    columns = table_row.findAll('td')
    output_row = []
    for column in columns:
        output_row.append(column.text)
    output_rows.append(output_row)

output_rows = list(np.delete(output_rows, [0, 1, len(output_rows) - 1]))

headers = ['Bundesland', 'Anzahl', 'Differenz zum Vortag', 'Fälle/100.000 Einw.', 'Todesfälle', 'Besonders betroffene Gebiete']
outputTable = pd.DataFrame(output_rows, columns=headers)
outputTable.insert(0, 'Date', date)

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

outputLoc = "./raw/"
fileName = outputLoc + 'RKI_Covid19_' + date + '.csv'
outputTable.to_csv(fileName, sep=',', encoding='utf-8', index=False)
