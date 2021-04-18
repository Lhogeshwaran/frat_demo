#!/bin/bash

for file in data/SFS_Res*
do
    in2csv "$file" > "data/temp.csv"
    csvcut -c "RESP_ID","RESP_SURVEY_ID","RESP_Q_ID","RESP_POINTS","RESP_COMMENT","RESP_FORM_KEY" "data/temp.csv" > "data/SFS_Responses.csv"
    rm "data/temp.csv"
done

for file in data/SFS_Sur*
do
    in2csv $file > "data/temp.csv"
    csvcut -c "SUR_ID","SUR_YEAR","SUR_HALFYEAR","SUR_SUBJECT_CODE","SUR_SUBJECT_ID","SUR_SUBJECT_NAME","SUR_FACULTY_ID","SUR_FACULTY_NAME","SUR_ACADUNIT_ID","SUR_ACADUNIT_NAME","SUR_STUDENT_COUNT" "data/temp.csv" > "data/SFS_Surveys.csv"
    rm "data/temp.csv"
done
