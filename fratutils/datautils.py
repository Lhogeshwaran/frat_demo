import pandas as pd
import json
from nltk.corpus import stopwords


class PreProcessing:

    def __init__(self):
        self.cfg = self._read_configs()

    def _read_configs(self):
        with open('fratutils/manual_configs.json') as f:
            cfg = json.loads(f.read())
        return cfg

    def check_is_core(self, x):
        return 1 if x in self.cfg['core_items'] else 0

    def check_text_resp(self, x):
        '''Checks if the text field has text or empty.'''         
        return 0 if str(x)=='nan' or str(x)=='' else 1


class PreProcessingText(PreProcessing):

    def __init__(self):
        PreProcessing.__init__(self)

    def remove_stopwords(self, x):
        all_stopwords = stopwords.words('english') + self.cfg['frat_stopwords']
        return " ".join(x for x in x.split() if x not in all_stopwords)
