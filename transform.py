import pandas as pd
from sqlalchemy import create_engine
import sys
import fratutils

engine = create_engine('postgresql+psycopg2://postgres:Loki@1990@localhost/airfloweco')
resp = pd.read_sql_query('SELECT * FROM sfs_resp', con=engine)
surv = pd.read_sql_query('SELECT * FROM sfs_surv', con=engine)

# Pre-processing
resp_fields = {'category':['resp_survey_id', 'resp_q_id'], 'datetime':[],
                     'integer':['resp_id', 'resp_survey_id', 'resp_q_id', 'resp_points']}
resp = fratutils.PreProcessing(resp).dtype_modifier(fields=resp_fields)

surv_fields = {'category':['sur_id', 'sur_year', 'sur_subject_code', 'sur_subject_id',
       'sur_subject_name', 'sur_faculty_id', 'sur_faculty_name',
       'sur_acadunit_id', 'sur_acadunit_name'], 'datetime':[], 'integer':['resp_points']}
surv = fratutils.PreProcessing(resp).dtype_modifier(fields=surv_fields)

qb = pd.read_excel('data/questionbank.xlsx')

# Feature engineering
## Number of respondents to each survey in surv
## Get count of students to whom survey went to from surv table on left,
# and 'left' merge with count of respondents from resp table on right 
# using survey unique ID and response form unique ID. Merge the two dataframes into "surv".
# Drop unwanted columns and rename "sur_resp_count".
surv = pd.merge(surv, pd.DataFrame(resp.groupby('resp_survey_id')['resp_form_key'].nunique()).reset_index(), 
    how='left', left_on='resp_survey_id', right_on='resp_survey_id')
surv.rename(columns={'resp_form_key_y':'surv_resp_count'}, inplace=True)

## Add question type to RES files
resp = pd.merge(resp, qb, how='left', left_on='resp_q_id', right_on='Item ID')
resp.drop(columns=['Item ID', 'Item Text'], inplace=True)
resp.rename(columns={'Item Type':'resp_item_type'}, inplace=True)

## Check if the question type in open-ended and if the open-ended question
## has a free-text response.
### RECOMMENDATION: There are free-text responses for 'C' type questions as well!


def check_qual_resp(x):

    if x['resp_item_type']=='O':
        if str(x['resp_comment'])=='nan':
            return 0
        return 1
    return 0


ls = ['resp_comment', 'resp_item_type']
resp['resp_qualitative_yes'] = resp[ls].apply(check_qual_resp, axis=1)

## Check if RESP_FORM_KEY had a qualitative response
tmp = pd.DataFrame(resp.groupby('resp_form_key')['resp_qualitative_yes'].max()).reset_index()
tmp.rename(columns={'resp_qualitative_yes':'has_qualitative_resp'}, inplace=True)
resp = pd.merge(resp, tmp, how='left', on='resp_form_key')

### Datafile for descriptive statistics by SURVEY_ID
resp.groupby(['resp_survey_id', 'resp_q_id', 'has_qualitative_resp'])['resp_points'].mean()
df = pd.DataFrame(res.groupby('resp_survey_id')['resp_points'].agg(['mean', 'std'])).reset_index()

