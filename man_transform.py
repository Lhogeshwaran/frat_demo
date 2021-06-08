import pandas as pd
import fratutils

resp = pd.read_csv('data/sfs_resp.csv')

resp['is_core'] = resp['resp_q_id'].apply(fratutils.datautils.FeatureEngineering().check_is_core)
