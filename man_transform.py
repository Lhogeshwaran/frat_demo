import pandas as pd
import fratutils

resp = pd.read_csv('data/sfs_resp.csv')

resp['is_core'] = resp['resp_q_id'].apply(fratutils.datautils.FeatureEngineering().check_is_core)

resp['resp_comment'] = resp['resp_comment'].astype(str)
resp['resp_comment_processed'] = resp['resp_comment'].apply(lambda x: " ".join(x.lower() for x in x.split()))
resp['resp_comment_processed'] = resp['resp_comment_processed'].str.replace('[^\w\s]','')
resp['resp_comment_processed'] = resp['resp_comment_processed'].apply(fratutils.datautils.FeatureEngineering().remove_stopwords)
