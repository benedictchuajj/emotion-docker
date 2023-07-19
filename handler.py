from sentiment_analysis_model import SentimentAnalyser
from simplified_emotions_model import SimpleEmotionsModel

sentiment_analyser = SentimentAnalyser()
emotions_recogniser = SimpleEmotionsModel()

def handler(event, context):
    input_text = event.get('sentence', '')
    print(input_text)

    try:
        sentiment_score = sentiment_analyser.predict(input_text)
        top5_emotions = emotions_recogniser.predict(input_text)
        emotion = top5_emotions[0]['name'] if top5_emotions[0]['value'] >= 0.5 else "neutral"
        
        return {"statusCode": 200, "sentiment_score": sentiment_score, "emotion": emotion, "top5_emotions": top5_emotions}

    except:
        return {"statusCode": 500, "sentiment_score": 0, "emotion": "neutral", "top5_emotions": "" }

if __name__ == '__main__':
    sentence = "hi :) my name is bob. nice to meet you"

    print(handler({'sentence': sentence}, {}))