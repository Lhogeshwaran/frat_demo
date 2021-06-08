import pandas as pd
import fratutils
from textblob import Word

resp = pd.read_csv('data/sfs_resp.csv')

resp['is_core'] = resp['resp_q_id'].apply(fratutils.datautils.PreProcessingText().check_is_core)

# Processing steps for 'resp_comment' for performing sentiment analysis.
resp['resp_comment'] = resp['resp_comment'].astype(str)
resp['resp_comment_processed'] = resp['resp_comment'].apply(lambda x: " ".join(x.lower() for x in x.split()))
resp['resp_comment_processed'] = resp['resp_comment_processed'].str.replace('[^\w\s]','')
resp['resp_comment_processed'] = resp['resp_comment_processed'].apply(fratutils.datautils.PreProcessingText().remove_stopwords)
resp['resp_comment_processed'] = resp['resp_comment_processed'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))
