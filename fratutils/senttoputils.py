from nltk.corpus.reader import xmldocs
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from .datautils import PreProcessing

class Sentiment:

    def __init__(self):
        self.analyser = SentimentIntensityAnalyzer()

    def sentiment_analyzer_scores(self, x):
        return self.analyser.polarity_scores(x)

    def get_sent_band(self, x, pos=0.05, neg=-0.05):
        '''Return sentiment positive/negative/neutral'''
        if x >= pos:
            return 'Positive'
        elif x <= neg:
            return 'Negative'
        return 'Neutral'


class Topic(PreProcessing):

    def __init__(self):
        PreProcessing.__init__(self)
        self.D = dict(zip(self.cfg['frat_topics'], [0]*len(self.cfg['frat_topics'])))

    def topic_scorer(self, x):
            
        for i in x.split(): 
            if i in self.D.keys():
                self.D[x[i]] = 1
    
        if any(self.D.values()) != 1:
            self.D['others'] = 1
    
        return self.D
