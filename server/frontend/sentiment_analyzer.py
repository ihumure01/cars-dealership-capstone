from textblob import TextBlob

def sentiment_analyzer(text_to_analyze):
    analysis = TextBlob(text_to_analyze)
    polarity = analysis.sentiment.polarity
    if polarity > 0:
        sentiment = "positive"
    elif polarity < 0:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    return {"text": text_to_analyze, "polarity": polarity, "subjectivity": analysis.sentiment.subjectivity, "sentiment": sentiment}
