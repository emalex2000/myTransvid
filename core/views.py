from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from pytube import YouTube
from django.conf import settings
import os
import assemblyai as aai
import openai
from .models import BlogPost
from django.core import serializers



@login_required
def homepage(request):
    return render (request, "homepage.html")


@csrf_exempt
def generate_article(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            youtube_link = data['link']
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid Data Sent'}, status=400)
        
        #youtube title
        title = youtube_title(youtube_link)

        #youtube transcript
        transcription = get_transript(youtube_link)

        if not transcription:
            return JsonResponse({'error': "failed to get transcript"})
        
        blog_content = generate_article_with_openai(transcription)
        if not blog_content:
            return JsonResponse({'error': "failed to generate blog article"})
        
        #save article in database
        new_blopost_to_db = BlogPost.objects.create(
            user = request.user,
            video_title = title,
            video_link  = youtube_link,
            generated_content = blog_content
        )

        new_blopost_to_db.save()


        #return blog article
        return JsonResponse({'content': blog_content})

    else:
        return JsonResponse({'error': 'Invalid Request Method'}, status=405)

def youtube_title(link):
    yt = YouTube(link)
    title = yt.title
    return title

def download_audio(link):
    yt = YouTube(link)
    stream = yt.streams.filter(only_audio=True).first()
    out_file = stream.download(output_path=settings.MEDIA_ROOT)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    return new_file


def get_transript(link):
    audio_file = download_audio(link)
    aai.settings.api_key = f"6ffa57bdf97549f184e289e4d3780a03"

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)
    complete_transcript = transcript.text
    return complete_transcript


def generate_article_with_openai(transcription):
    openai.api_key = "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"

    prompt = f"based on this transcript from a youtube video, i would like you to create a blog article for me. do not make it look like a youtube video. make it look like a proper blog article: \n\n{transcription}\n\nArticle"
    response = openai.ChatCompletion.create(
        model = "text-davinci-003",
        prompt=prompt,
        max_tokens=1000
    )
    generated_content = response.choices[0].text.strip()
    return generated_content


def user_login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error_message = 'Invalid Username and Password'
            return render(request, 'login.html', {'error_message':error_message})
    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        username= request.POST['username']
        email= request.POST['email']
        password= request.POST['password']
        repeatPassword= request.POST['password2']

        if password == repeatPassword:
            
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                login(request, user)
                return redirect('/')
            except:
                error_message = 'Error Creating Account'
                return render(request, 'signup.html', {'error_message':error_message})
            
        else:
            error_message = 'Password Do Not Match'
            return render(request, 'signup.html', {'error_message':error_message})
        
    return render (request, 'signup.html')


def blog_pages(request):

    blog_articles = BlogPost.objects.filter(user = request.user)
    blog_articles_json = serializers.serialize('json', blog_articles)
    print(blog_articles_json)
    return render(request, "blog.html", {'blog_articles': blog_articles_json})
    #return JsonResponse(request, 'blog.html', {'blog_articles':blog_articles})


def blog_details(request):
    return render(request, 'blog-details.html')


def user_logout(request):
    logout(request)
    return redirect('/')
# Create your views here.
