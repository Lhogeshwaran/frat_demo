import pandas as pd


Class PreProcessing:

    def __init__(self, df):

        self.df = df
        self.res_fields = {'category':['RESP_SURVEY_ID', 'RESP_Q_ID',
                            'datetime':['RESP_DATE']]}
        self.sur_fields = {'category':['SUR_YEAR', 'SUR_SUBJECT_CODE',
                            'SUR_SUBJECT_ID', 'SUR_SUBJECT_NAME',
                            'SUR_FACULTY_ID', 'SUR_FACULTY_NAME',
                            'SUR_ACADUNIT_ID', 'SUR_ACADUNIT_NAME']}

    def dtype_modifier(self, fields=1):

        if fields==1:
            fields = self.res_fields
        elif fields==2:
            fields = self.sur_fields

        for i in fields['category']:
            try:
                self.df[i] = self.df[i].astype('category')
            except:
                KeyError
                print(f'Warning: Column "{i}" expected but not present.')

        for i in fields['datetime']:
            try:
                self.df[i] = pd.to_datetime(self.df[i])
            except:
                KeyError
                print(f'Warning: Column "{i}" expected but not present.')


Class FeatureEngineering(PreProcessing):

        def __init__(self, df):

            PreProcessing.__init__(self, df)

        def get_perc(self):

            try:
                return round((self.df['SUR_RESP_COUNT'] / self.df['SUR_STUDENT_COUNT']), 2)
            except:
                ZeroDivisionError
