
import numpy as np
import pandas as pd
from pathlib import Path
from typing import List

data_dir = Path('../data')

dat = pd.read_csv(data_dir/'ids.csv', header=0)

def complete_ra(N:int,m:int,conditions:List[int]) -> pd.Series:
    assignment = np.random.permutation(np.repeat(conditions,[N-m,m],axis=0))
    return assignment

dat2 = dat.assign(trt=complete_ra(len(dat),np.floor(len(dat)/2),conditions=[0,1]))

## Make sure that dat2 is the same number of rows as dat
assert(len(dat2)==len(dat))
## Make sure that we have randomly assigned half to treatment
assert(sum(dat2['trt'])==np.floor(len(dat)/2))

## Save new csv
dat2.to_csv(data_dir/'ids_plus_treatment.csv')

