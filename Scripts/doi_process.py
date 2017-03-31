import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

sample = 'http://doi.acm.org/10.1145/2884781.2884828'
DIR = os.path.abspath(os.path.dirname(__file__))
input_csv = os.path.join(DIR, os.pardir, 'Paper', 'all_v8.csv')

# DOI_URL
original_data = pd.read_csv(input_csv)
original_data['DOI'] = original_data['DOI_URL'].apply(lambda x: x.split('.org/')[-1])
print original_data['DOI']
