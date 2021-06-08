import pandas as pd
import json
from nltk.corpus import stopwords


class PreProcessing:
    '''
    Contains transformation methods.
    params:
        df: A pandas DataFrame object.
    '''

    def __init__(self, df):

        self.df = df
        self.res_fields = {'category':['RESP_SURVEY_ID', 'RESP_Q_ID'],
                            'datetime':['RESP_DATE']}
        self.sur_fields = {'category':['SUR_YEAR', 'SUR_SUBJECT_CODE',
                            'SUR_SUBJECT_ID', 'SUR_SUBJECT_NAME',
                            'SUR_FACULTY_ID', 'SUR_FACULTY_NAME',
                            'SUR_ACADUNIT_ID', 'SUR_ACADUNIT_NAME']}

    def dtype_modifier(self, fields=1):
        
        '''
        Method to convert datatype for memory usage optimization.
        params:
            fields: A dict object like "{'category:['colnames'], 'datetime':['colnames']}
        Returns:
            A pandas DataFrame object.
        '''

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

        for i in fields['integer']:
            try:
                self.df[i] = self.df[i].astype('int64')
            except:
                ValueError
                
        return self.df


class PreProcessing:

    def __init__(self):
        self.cfg = self._read_configs()
        self.core_items = self.cfg['core_items']

    def _read_configs(self):
        with open('fratutils/manual_configs.json') as f:
            cfg = json.loads(f.read())
        return cfg

    def check_is_core(self, x):
        return 1 if x in self.core_items else 0


class PreProcessingText(PreProcessing):

    def __init__(self):
        PreProcessing.__init__(self)
        self.all_stopwords = stopwords.words('english') + self.cfg['frat_stopwords']

    def remove_stopwords(self, x):
        return " ".join(x for x in x.split() if x not in self.all_stopwords)
