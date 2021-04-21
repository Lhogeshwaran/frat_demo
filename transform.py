import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import sys
import fratutils
from scipy import stats

engine = create_engine('postgresql+psycopg2://postgres:Loki@1990@localhost/airfloweco')
resp = pd.read_sql_query('SELECT * FROM sfs_resp', con=engine)
surv = pd.read_sql_query('SELECT * FROM sfs_surv', con=engine)

# Pre-processing
resp_fields = {'category':['resp_survey_id', 'resp_q_id'], 'datetime':[],
                     'integer':['resp_id', 'resp_survey_id', 'resp_q_id', 'resp_points']}
resp = fratutils.PreProcessing(resp).dtype_modifier(fields=resp_fields)

surv_fields = {'category':['sur_id', 'sur_year', 'sur_subject_code', 'sur_subject_id',
       'sur_subject_name', 'sur_faculty_id', 'sur_faculty_name',
       'sur_acadunit_id', 'sur_acadunit_name'], 'datetime':[],
       'integer':['sur_id', 'sur_year', 'sur_subject_id', 'sur_student_count']}
surv = fratutils.PreProcessing(surv).dtype_modifier(fields=surv_fields)

qb = pd.read_excel('data/questionbank.xlsx')

# Feature engineering
## Number of respondents to each survey in surv
## Get count of students to whom survey went to from surv table on left,
# and 'left' merge with count of respondents from resp table on right 
# using survey unique ID and response form unique ID. Merge the two dataframes into "surv".
# Drop unwanted columns and rename "sur_resp_count".
surv = pd.merge(surv, pd.DataFrame(resp.groupby('resp_survey_id')['resp_form_key'].nunique()).reset_index(), 
    how='left', left_on='sur_id', right_on='resp_survey_id')
surv.drop(columns=['resp_survey_id'], inplace=True)
surv.rename(columns={'resp_form_key':'sur_resp_count'}, inplace=True)

## Add question type to resp files
resp = pd.merge(resp, qb, how='left', left_on='resp_q_id', right_on='Item ID')
resp.drop(columns=['Item ID', 'Item Text'], inplace=True)
resp.rename(columns={'Item Type':'resp_item_type'}, inplace=True)
resp['resp_comment'].fillna('', inplace=True)

## Check if the question type in open-ended and if the open-ended question
## has a free-text response.
### RECOMMENDATION: There are free-text responses for 'C' type questions as well!


def check_qual_resp(x):

    if x['resp_item_type']=='O':
        if (str(x['resp_comment'])=='nan') | (str(x['resp_comment'])==''):
            return 0
        return 1
    return 0


ls = ['resp_comment', 'resp_item_type']
resp['resp_qualitative_yes'] = resp[ls].apply(check_qual_resp, axis=1)

## Add number of responses with comments to surv files.
tmp = pd.DataFrame(resp[resp['resp_qualitative_yes']==1].groupby('resp_survey_id')['resp_form_key'].nunique()).reset_index()
tmp.rename(columns={'resp_survey_id': 'sur_id'}, inplace=True)
surv = pd.merge(surv, tmp, how='left', on='sur_id')
surv.rename(columns={'resp_form_key': 'resp_qualitative_yes'}, inplace=True)
surv['resp_qualitative_no'] = surv['sur_resp_count'] - surv['resp_qualitative_yes']

## Check if resp_form_key had a qualitative response
tmp = pd.DataFrame(resp.groupby('resp_form_key')['resp_qualitative_yes'].max()).reset_index()
tmp.rename(columns={'resp_qualitative_yes':'has_qualitative_resp'}, inplace=True)
resp = pd.merge(resp, tmp, how='left', on='resp_form_key')

# Statistical testing
# DataFrame 1 for study of differnce in means. 
df = pd.DataFrame(resp[resp['resp_item_type']=='C'].groupby(['resp_q_id', 'has_qualitative_resp'])['resp_points'].agg(['mean', 'std', 'count']).dropna()).reset_index()
df = pd.DataFrame(df.pivot(index='resp_q_id', columns='has_qualitative_resp'))
df.columns = [col[0]+'_'+str(col[1]) for col in df.columns]
df.reset_index(inplace=True)

df = pd.merge(df, qb, how='left', left_on='resp_q_id', right_on='Item ID')
df.drop(columns=['Item ID', 'Item Type'], inplace=True)


def get_tstat(x):
    q1 = resp[(resp['resp_q_id']==x) & (resp['has_qualitative_resp']==1)]['resp_points'].dropna()
    q0 = resp[(resp['resp_q_id']==x) & (resp['has_qualitative_resp']==0)]['resp_points'].dropna()            
    tstat = stats.ttest_ind(q1, q0, equal_var=False)
    
    return round(tstat[0], 5)


def get_pval(x):
    q1 = resp[(resp['resp_q_id']==x) & (resp['has_qualitative_resp']==1)]['resp_points'].dropna()
    q0 = resp[(resp['resp_q_id']==x) & (resp['has_qualitative_resp']==0)]['resp_points'].dropna()            
    tstat = stats.ttest_ind(q1, q0, equal_var=False)
    
    return round(tstat[1], 5)


def check_signigicance(x):

       return 0 if x < 0.05 else 1


def check_signigicance_2(x):

       return 'significantly different' if x < 0.05 else 'same'


df['tstat'] = df['resp_q_id'].apply(get_tstat)
df['pval'] = df['resp_q_id'].apply(get_pval)
df['null_hyp'] = df['pval'].apply(check_signigicance)
df['sig_hyp'] = df['pval'].apply(check_signigicance_2)


def plot_t_test(q_id):

    mu0 = df[df['resp_q_id']==q_id]['mean_0']
    sigma0 = df[df['resp_q_id']==q_id]['std_0']
    x0 = np.linspace(mu0-3*sigma0, mu0+3*sigma0, 100)
    mu1 = df[df['resp_q_id']==q_id]['mean_1']
    sigma1 = df[df['resp_q_id']==q_id]['std_1']
    x1 = np.linspace(mu1-3*sigma1, mu1+3*sigma1, 100)

    plt.subplot(2, 1, 1)
    plt.plot(x0, stats.norm.pdf(x0, mu0, sigma0), color='#5e216e', label='Responses w/o comments')
    plt.plot(x1, stats.norm.pdf(x1, mu1, sigma1), color='orange', label='Responses with comments')
    plt.xlabel('Points')
    plt.ylabel('Probability density')
    plt.title('T2-test for Question Id: '+str(q_id)+'\n'+str(df[df['resp_q_id']==q_id]['Item Text'].item()))
    plt.subplot(2, 1, 2)
    val = df[df['resp_q_id']==q_id]['pval']
    ar = np.arange(0, 1)
    plt.plot(np.zeros_like(ar)+val, np.zeros_like(ar)+val, 'x', color='steelblue')
    plt.xlim(-0.05, 1)
    plt.axvline(x=0.05, color='red', alpha=0.1)
    plt.yticks([])
    plt.title('p-value & significance line'+'\n'+'t-statistic: '+str(df[df['resp_q_id']==q_id]['tstat'].item())+'\n'+'p-value consensus: Means are '+str(df[df['resp_q_id']==q_id]['sig_hyp'].item()))
    plt.xlabel('p-value')
    plt.tight_layout()
#    plt.savefig(str(df[df['res_q_id']==q_id]['Item Text'].item())+'.png', dpi=300)
    plt.show()

plot_t_test(3131)
plot_t_test(3200)


# Sentiment analysis
from nltk.corpus import stopwords
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import Counter
from textblob import Word


## Core-items :: 3707, 3708, 3131, 3709, 1053, 1070
def check_is_core(x):

    return 1 if x in [3707, 3708, 3131, 3709, 1053, 1070] else 0 



resp['is_core'] = resp['resp_q_id'].apply(check_is_core)
resp_sent = resp[resp['is_core']==1]

resp_sent['resp_comment'] = resp_sent['resp_comment'].astype(str)
resp_sent['resp_comment_processed'] = resp_sent['resp_comment'].apply(lambda x: " ".join(x.lower() for x in x.split()))
resp_sent['resp_comment_processed'] = resp_sent['resp_comment_processed'].str.replace('[^\w\s]','')
stop = stopwords.words('english')
frat_stop = [line.strip() for line in open('data/frat_stop_words.txt')]
stop = stop + frat_stop
resp_sent['resp_comment_processed'] = resp_sent['resp_comment_processed'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
resp_sent['resp_comment_processed'] = resp_sent['resp_comment_processed'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))

# Sentiment analysis and banding
analyser = SentimentIntensityAnalyzer()


def sentiment_analyzer_scores(sentence):
    return analyser.polarity_scores(sentence)


# Get sentiment score for each feedback
resp_sent['sent_score'] = resp_sent[resp_sent['resp_qualitative_yes']==1]['resp_comment_processed'].apply(sentiment_analyzer_scores)
resp_sent['sent_neg'] = resp_sent[resp_sent['resp_qualitative_yes']==1]['sent_score'].apply(lambda x: x['neg'])
resp_sent['seng_neu'] = resp_sent[resp_sent['resp_qualitative_yes']==1]['sent_score'].apply(lambda x: x['neu'])
resp_sent['sent_pos'] = resp_sent[resp_sent['resp_qualitative_yes']==1]['sent_score'].apply(lambda x: x['pos'])
resp_sent['sent_comp'] = resp_sent[resp_sent['resp_qualitative_yes']==1]['sent_score'].apply(lambda x: x['compound'])
resp_sent.drop(columns='sent_score', inplace=True)


# Function to categorize the sentiment bands based on info from github source
def sent_band(val):
    if val >= 0.05:
        return 'Positive'
    elif val <= -0.05:
        return 'Negative'
    return 'Neutral'


resp_sent['sent_band'] = resp_sent[resp_sent['resp_qualitative_yes']==1]['sent_comp'].apply(lambda x: sent_band(x))
resp_sent[(resp_sent['resp_item_type']=='O') & (resp_sent['has_qualitative_resp']==1)].head()
