# Assess the random assignments: we want half of each upload to be assigned to
# treatment and half to control When we have an odd number of units, we should
# have a difference of no more than 1 unit.  Across 10 randomizations to 3
# units, for example, we should see 15 in treatment and 15 in control even if
# each individual randomization has either 1 or 2 in treatment

# building on https://stackoverflow.com/questions/20906474/import-multiple-csv-files-into-pandas-and-concatenate-into-one-dataframe

import pandas as pd
import glob
import re

path = r'./results' # use your path
all_files = glob.glob(path + "/*.csv")

##

li = []
i = 1
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    df['filen'] = i
    df['fileabbrv'] = re.search('- ids_(.+?) -',filename).group(1)
    df['n'] = len(df)
    li.append(df)
    i = i + 1

dfbig = pd.concat(li, axis=0, ignore_index=True)

## These don't have to be exactly equal because of different sample sizes
pd.crosstab(index = dfbig["Assigned Arm"],columns="count")

## But we should see close to equal here
pd.crosstab(index = dfbig["Assigned Arm"],columns=dfbig["n"],margins=True)

## And here
pd.crosstab(index = dfbig["Assigned Arm"],columns=dfbig["fileabbrv"],margins=True)


##
