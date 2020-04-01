import pandas as pd
import numpy as np
import requests
import re
import os
from bs4 import BeautifulSoup
import datetime

# You should use this source!
# https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Germany

RKI_url = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html'
requestRKI = requests.get(RKI_url)
soup = BeautifulSoup(requestRKI.content)
table = soup.find("table")
allP = list(soup.find_all("p"))
dateP = [p for p in allP if str(p).__contains__("online aktualisiert um")]
# old way to find date
# date = soup.find_all("div", class_="dateOfIssue")
date = re.findall('\\d+', str(dateP))
date = [int(part) for part in date]
date = datetime.date(date[2], date[1], date[0])
date = date.strftime("%d-%m-%Y")

output_rows = []
for table_row in table.findAll('tr'):
    columns = table_row.findAll('td')
    output_row = []
    for column in columns:
        output_row.append(column.text)
    output_rows.append(output_row)

output_rows = list(np.delete(output_rows, [0, 1, len(output_rows) - 1]))

headers = ['Bundesland', 'Anzahl', 'Differenz zum Vortag', 'Fälle/100.000 Einw.', 'Todesfälle']
outputTable = pd.DataFrame(output_rows, columns=headers)
outputTable.insert(0, 'Date', date)

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

outputLoc = "./raw/"
fileName = outputLoc + 'RKI_Covid19_' + date + '.csv'
outputTable.to_csv(fileName, sep=',', encoding='utf-8', index=False)
