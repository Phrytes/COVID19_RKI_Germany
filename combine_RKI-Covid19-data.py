import os, glob
import pandas as pd
import re

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

inputLoc = ".\\raw\\"
outputLoc = ".\\"

all_files = glob.glob(os.path.join(inputLoc, "*.csv"))
all_df = []
for f in all_files:
    df = pd.read_csv(f, sep=',')
    fileDate = re.findall('\\d\\d-\\d\\d-\\d\\d\\d\\d', f)[0]
    df['Date'] = fileDate
    all_df.append(df)

combined_df = pd.concat(all_df, ignore_index=True, sort=True)
outputFileName = outputLoc + 'RKI_Covid19_ALL.csv'
combined_df.to_csv(outputFileName, sep=',', encoding='utf-8', index=False)