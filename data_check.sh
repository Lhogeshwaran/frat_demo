#!/bin/bash

in2csv "data/SFS_Responses_Export_File_2017-1_to_2017-2(wo CIC TDI).xlsx" > "data/SFS_Responses_Export_File_2017-1_to_2017-2(wo CIC TDI).csv"
csvcut -c "RESP_ID","RESP_SURVEY_ID","RESP_Q_ID","RESP_POINTS","RESP_COMMENT","RESP_FORM_KEY" "data/SFS_Responses_Export_File_2017-1_to_2017-2(wo CIC TDI).csv" > "data/SFS_Responses_2017.csv"
rm "data/SFS_Responses_Export_File_2017-1_to_2017-2(wo CIC TDI).csv"

in2csv "data/SFS_Surveys_Export_File_2017-1_to_2017-2.xlsx" > "data/SFS_Surveys_Export_File_2017-1_to_2017-2.csv"
csvcut -c "SUR_ID","SUR_YEAR","SUR_HALFYEAR","SUR_SUBJECT_CODE","SUR_SUBJECT_ID","SUR_SUBJECT_NAME","SUR_FACULTY_ID","SUR_FACULTY_NAME","SUR_ACADUNIT_ID","SUR_ACADUNIT_NAME","SUR_STUDENT_COUNT" "data/SFS_Surveys_Export_File_2017-1_to_2017-2.csv" > "data/SFS_Surveys_2017.csv"
rm "data/SFS_Surveys_Export_File_2017-1_to_2017-2.csv"
