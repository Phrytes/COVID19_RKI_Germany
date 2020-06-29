#!/usr/bin/python 3
import pandas as pd
import numpy as np
import requests
import re
import os
from bs4 import BeautifulSoup
import datetime
import traceback

# You should use this source!
# https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Germany
RKI_url = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html'
requestRKI = requests.get(RKI_url)
soup = BeautifulSoup(requestRKI.content, features="html.parser")
table = soup.find("table")
allP = list(soup.find_all("p"))

## Filter the html soup for column headers automatically,
## removing empty table header cells and multiline headers (colspan > 1)
allcols = list(soup.find_all("th"))
def rppl(tx):
	"""some shortening of the html"""
	tx=tx.replace("\n"," ")
	tx=tx.replace("\xad","")
	return tx

rh = [re.sub('<[^<]+?>', '', rppl(str(p))) for p in allcols if str(p).__contains__('colspan="1"')]
RKIColumnHeaders = [y for y in rh if len(y)>0]
##

dateP = [p for p in allP if str(p).__contains__("online aktualisiert um")]
#find footnote under table
RKIFootnotes = [re.sub('<[^<]+?>', '', str(p)) for p in allP if str(p).__contains__("*")]

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
output_rows.append(RKIFootnotes)

#Recently RKI switched to these headers:
#headers = ['Bundesland', 'Anzahl', 'Differenz zum Vortag', 'Fälle in den letzten 7 Tagen', '7-Tage-Inzidenz', 'Todesfälle']
#Former headers:
#headers = ['Bundesland', 'Anzahl', 'Differenz zum Vortag', 'Fälle/100.000 Einw.', 'Todesfälle']

#use gathered headers
headers = RKIColumnHeaders


try:
	outputTable = pd.DataFrame(output_rows, columns=headers)
	outputTable.insert(0, 'Date', date)
	
	abspath = os.path.abspath(__file__)
	dname = os.path.dirname(abspath)
	os.chdir(dname)

	outputLoc = "./raw/"
	if not os.path.exists(outputLoc):
		os.makedirs(outputLoc)
	fileName = outputLoc + 'RKI_Covid19_' + date + '.csv'
	outputTable.to_csv(fileName, sep=',', encoding='utf-8', index=False)
except ValueError:
	print(f"You see this because pandas receaved an error.\nReason may be that RKI changed the column header format.\nThis may happen if two values under one column header with colspan=2 as an option")
	traceback.print_exc()
