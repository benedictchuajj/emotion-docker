from transformers import pipeline

"""
Wrapper classes of the pretrained Sentiment DistilBERT model.

Possible Enhancements:
- To be updated.
"""

model_path = "models/nlptown-bert_base_multilingual_uncased-sentiment/snapshots/e06857fdb0325a7798a8fc361b417dfeec3a3b98"

class SentimentAnalyser:
    def __init__(self):
        self.classifier = pipeline('sentiment-analysis', model=model_path, return_all_scores=True)

    ## credits for formula: https://www.kaggle.com/code/pavlofesenko/python-libraries-for-sentiment-analysis/notebook
    def scaled_average(self, a):
        output = 0
        for i, x in enumerate(a):
            output += x['score'] * (i + 1) 
        output = (output - 3) / 2
        return output

    def predict(self, sentence):
        score =  self.classifier(sentence)[0]
        return self.scaled_average(score)
