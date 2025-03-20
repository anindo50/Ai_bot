from .unit import text_gen
import requests
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Conversation
from django.conf import settings
from .froms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views as auth_views
from django.contrib.auth import login, authenticate
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from django.contrib.auth import logout

def text_genaration(request):
    if "chat_history" not in request.session:
        request.session["chat_history"] = []  
    if request.method == "POST":
        text = request.POST.get("text")
        if text:
            gen_tex = text_gen(text)
            if gen_tex:
                request.session["chat_history"].append({"user": text, "bot": gen_tex})  
                request.session.modified = True  

    return render(request, "text.html", {"chat_history": request.session["chat_history"]})




def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect("chat")  
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})

def custom_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("chat") 
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_score = analyzer.polarity_scores(text)['compound']  
    if sentiment_score >= 0.05:
        return "positive"
    elif sentiment_score <= -0.05:
        return "negative"
    else:
        return "neutral"

@login_required
def text_generatior(request):
    
    chat_history = Conversation.objects.filter(user=request.user).order_by("-timestamp")[:10]

    if request.method == "POST":
        user_input = request.POST.get("text")
        
        if user_input:
            
            bot_response = text_gen(user_input)

            sentiment_score = analyze_sentiment(user_input)

            
            if sentiment_score == "positive":
            
                bot_response += f"\n\nYay! 😊 It seems like you're in a great mood! How can I make your day even better?"
            elif sentiment_score == "negative":
               
                bot_response += f"\n\nI'm really sorry you're feeling down. 😞 I'm here for you. How can I help?"
            else:
                
                bot_response += f"\n\nGot it! Let me know if you need any help."

            
            Conversation.objects.create(user=request.user, user_input=user_input, bot_response=bot_response)

            
            chat_history = Conversation.objects.filter(user=request.user).order_by("-timestamp")[:10]


    return render(request, "chat.html", {"chat_history": chat_history})


def custom_logout(request):
    if request.method == "POST":
        logout(request)
    return redirect("login")
   