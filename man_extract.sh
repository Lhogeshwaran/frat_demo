#!/bin/bash

source ~/.virtualenvs/airfloweco/bin/activate

mkdir data/temp

for file in /Users/loki/UTS_MDSI/code_practices/frat_demo/data/SFS_Surv*
do
    in2csv $file > "/Users/loki/UTS_MDSI/code_practices/frat_demo/data/temp/temp.csv"
    csvcut -c "SUR_ID","SUR_YEAR","SUR_SUBJECT_CODE","SUR_SUBJECT_ID","SUR_SUBJECT_NAME","SUR_FACULTY_ID","SUR_FACULTY_NAME","SUR_ACADUNIT_ID","SUR_ACADUNIT_NAME","SUR_STUDENT_COUNT" "/Users/loki/UTS_MDSI/code_practices/frat_demo/data/temp/temp.csv" > "/Users/loki/UTS_MDSI/code_practices/frat_demo/data/temp/SFS_SURV.csv"
    cat data/temp/SFS_SURV.csv | sed 's/SUR_ID/sur_id/g' | sed 's/SUR_YEAR/sur_year/g' | sed 's/SUR_SUBJECT_CODE/sur_subject_code/g' | sed 's/SUR_SUBJECT_ID/sur_subject_id/g' | sed 's/SUR_SUBJECT_NAME/sur_subject_name/g' | sed 's/SUR_FACULTY_ID/sur_faculty_id/g' | sed 's/SUR_FACULTY_NAME/sur_faculty_name/g' | sed 's/SUR_ACADUNIT_ID/sur_acadunit_id/g' | sed 's/SUR_ACADUNIT_NAME/sur_acadunit_name/g' | sed 's/SUR_STUDENT_COUNT/sur_student_count/g' > "/Users/loki/UTS_MDSI/code_practices/frat_demo/data/sfs_surv.csv"
done

for file in /Users/loki/UTS_MDSI/code_practices/frat_demo/data/SFS_Resp*
do
    in2csv "$file" > "/Users/loki/UTS_MDSI/code_practices/frat_demo/data/temp/temp.csv"
    csvcut -c "RESP_ID","RESP_SURVEY_ID","RESP_Q_ID","RESP_POINTS","RESP_COMMENT","RESP_FORM_KEY" "/Users/loki/UTS_MDSI/code_practices/frat_demo/data/temp/temp.csv" > "/Users/loki/UTS_MDSI/code_practices/frat_demo/data/temp/SFS_RESP.csv"
    cat data/temp/SFS_RESP.csv | sed 's/RESP_ID/resp_id/g' | sed 's/RESP_SURVEY_ID/resp_survey_id/g' | sed 's/RESP_Q_ID/resp_q_id/g' | sed 's/RESP_POINTS/resp_points/g' | sed 's/RESP_COMMENT/resp_comment/g' | sed 's/RESP_FORM_KEY/resp_form_key/g' > "/Users/loki/UTS_MDSI/code_practices/frat_demo/data/sfs_resp.csv"
done

rm -rf data/temp

deactivate
