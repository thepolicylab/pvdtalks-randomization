import csv
import numpy as np
import pandas as pd

ids_dat = pd.DataFrame(np.random.randint(10000,99999,50), columns=['ParticipantID'])

ids_dat.to_csv('ids_n_50.csv', index_label=False, index=False)

