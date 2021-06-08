from nltk.corpus.reader import xmldocs
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class Sentiment:

    def __init__(self):
        self.analyser = SentimentIntensityAnalyzer()

    def sentiment_analyzer_scores(self, x):
        return self.analyser.polarity_scores(x)
