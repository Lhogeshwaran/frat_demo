import pandas as pd
import fratutils
from textblob import Word

resp = pd.read_csv('data/sfs_resp.csv')

resp['is_core'] = resp['resp_q_id'].apply(fratutils.datautils.PreProcessing().check_is_core)
resp['has_text'] = resp['resp_comment'].apply(fratutils.datautils.PreProcessing().check_text_resp)

# Processing steps for 'resp_comment' for performing sentiment analysis.
resp['resp_comment'] = resp['resp_comment'].astype(str)
resp['resp_comment_processed'] = resp['resp_comment'].apply(lambda x: " ".join(x.lower() for x in x.split()))
resp['resp_comment_processed'] = resp['resp_comment_processed'].str.replace('[^\w\s]','')
resp['resp_comment_processed'] = resp['resp_comment_processed'].apply(fratutils.datautils.PreProcessingText().remove_stopwords)
resp['resp_comment_processed'] = resp['resp_comment_processed'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))

# Steps for getting sentiment scores
resp['sent_score'] = resp[resp['has_text']==1]['resp_comment_processed'].apply(fratutils.senttoputils.Sentiment().sentiment_analyzer_scores)
resp['sent_neg'] = resp[resp['has_text']==1]['sent_score'].apply(lambda x: x['neg'])
resp['seng_neu'] = resp[resp['has_text']==1]['sent_score'].apply(lambda x: x['neu'])
resp['sent_pos'] = resp[resp['has_text']==1]['sent_score'].apply(lambda x: x['pos'])
resp['sent_comp'] = resp[resp['has_text']==1]['sent_score'].apply(lambda x: x['compound'])
resp.drop(columns='sent_score', inplace=True)

resp['sent_band'] = resp['sent_comp'].apply(lambda x: fratutils.senttoputils.Sentiment().get_sent_band)

resp['topic_score'] = resp['resp_comment_processed'].apply(lambda x: fratutils.senttoputils.Topic().topic_scorer(x))