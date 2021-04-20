#!/bin/bash

source ~/.virtualenvs/airfloweco/bin/activate

for file in /Users/loki/UTS_MDSI/code_practices/loki_kpmg/data/SFS_Res*
do
    in2csv "$file" > "/Users/loki/UTS_MDSI/code_practices/loki_kpmg/data/temp.csv"
    csvcut -c "RESP_ID","RESP_SURVEY_ID","RESP_Q_ID","RESP_POINTS","RESP_COMMENT","RESP_FORM_KEY" "/Users/loki/UTS_MDSI/code_practices/loki_kpmg/data/temp.csv" > "/Users/loki/UTS_MDSI/code_practices/loki_kpmg/data/SFS_Responses.csv"
    rm "/Users/loki/UTS_MDSI/code_practices/loki_kpmg/data/temp.csv"
done

for file in /Users/loki/UTS_MDSI/code_practices/loki_kpmg/data/SFS_Sur*
do
    in2csv $file > "/Users/loki/UTS_MDSI/code_practices/loki_kpmg/data/temp.csv"
    csvcut -c "SUR_ID","SUR_YEAR","SUR_SUBJECT_CODE","SUR_SUBJECT_ID","SUR_SUBJECT_NAME","SUR_FACULTY_ID","SUR_FACULTY_NAME","SUR_ACADUNIT_ID","SUR_ACADUNIT_NAME","SUR_STUDENT_COUNT" "/Users/loki/UTS_MDSI/code_practices/loki_kpmg/data/temp.csv" > "/Users/loki/UTS_MDSI/code_practices/loki_kpmg/data/SFS_Surveys.csv"
    rm "/Users/loki/UTS_MDSI/code_practices/loki_kpmg/data/temp.csv"
done

deactivate
