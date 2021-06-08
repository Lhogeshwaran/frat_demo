from nltk.corpus.reader import xmldocs
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

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
    