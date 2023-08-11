from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate 
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
import pandas as pd
import pickle
import numpy as np
import os.path
import pandas as pd
import pickle
import os
import re
import string
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
set(stopwords.words('english'))
import snscrape.modules.twitter as sntwitter
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

model = pickle.load(open("models/tweets_analyzer.pkl", "rb"))
feature_extraction = pickle.load(open("models/feature_extractor.pkl", "rb"))

# Create your views here.
def index(request):
    return render(request, "index.html")

def signup(request): 
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        if User.objects.filter(username=username):
            messages.error(request, "Username Already Exist")
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('signup')

        my_user = User.objects.create_user(username, email, password)
        my_user.save()
        return redirect("login")

    return render(request, "signup.html")

def login(request):
    if request.method == "POST":
        global username
        username = request.POST["username"]
        password = request.POST["password"]

        user_login = authenticate(username=username, password=password)
        if user_login is not None:
            auth_login(request, user_login)
            return render(request, "app.html")
        else:
            return render(request, "index.html")

    return render(request, "login.html")

def logout(request):
    auth_logout(request)
    return render(request, "index.html")

def predict_with_text(request):
    text_of_tweet = request.POST["text_of_tweet"]
    input_tweet = [text_of_tweet]
    input_data_features = feature_extraction.transform(input_tweet)
    prediction = model.predict(input_data_features)
    if (prediction[0]==1):
        result="Looks like a Negative Tweet"
    else:
        result="Looks like a Positive Tweet"

    # emotion based analysis
    stop_words = stopwords.words('english')
    text1 = text_of_tweet.lower()
    text_final = ''.join(c for c in text1 if not c.isdigit())
    processed_doc1 = ' '.join([word for word in text_final.split() if word not in stop_words])

    sa = SentimentIntensityAnalyzer()
    dd = sa.polarity_scores(text=processed_doc1)
    positive_score = round(dd['pos']*100, 2)
    negative_score = round(dd['neg']*100, 2)
    neutral_score = round(dd['neu']*100, 2)

    return render(request, "display_preds.html", {"result":result, "positive_score":positive_score, "negative_score":negative_score, "neutral_score":neutral_score, "text_of_tweet":text_of_tweet})

def predict_with_twitter_handle(request):
    twitter_handle = request.POST["twitter_handle"]
    query = "(from:"+twitter_handle+")"
    tweets_list = []
    limit = 10
    for tweet in sntwitter.TwitterSearchScraper(query).get_items():
        if len(tweets_list) == limit:
            break
        else:
            tweets_list.append([tweet.content])

    tweets_str = ','.join(str(item) for innerlist in tweets_list for item in innerlist)
    input_tweet = [tweets_str]
    input_data_features = feature_extraction.transform(input_tweet)
    prediction = model.predict(input_data_features)
    if (prediction[0]==1):
        result="Looks like a Negative Tweet"
    else:
        result="Looks like a Positive Tweet"

    # emotion based analysis
    stop_words = stopwords.words('english')
    text1 = tweets_str.lower()
    text_final = ''.join(c for c in text1 if not c.isdigit())
    processed_doc1 = ' '.join([word for word in text_final.split() if word not in stop_words])

    sa = SentimentIntensityAnalyzer()
    dd = sa.polarity_scores(text=processed_doc1)
    positive_score = round(dd['pos']*100, 2)
    negative_score = round(dd['neg']*100, 2)
    neutral_score = round(dd['neu']*100, 2)

    return render(request, "display_preds.html", {"result":result, "positive_score":positive_score, "negative_score":negative_score, "neutral_score":neutral_score, "text_of_tweet":tweets_str})


def use_app(request):
    return render(request, "app.html")