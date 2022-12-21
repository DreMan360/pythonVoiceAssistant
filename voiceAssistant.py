#import necessary libraries
import speech_recognition as sr
import webbrowser
import time
import playsound
import os
import random
from gtts import gTTS
import datetime
import openai
from datetime import date
from os.path import exists
import spotipy
import keyboard
import requests
from AppOpener import run
import randfacts
from dotenv import load_dotenv
import os

def getvar():
    load_dotenv()

getvar()


# This should be the default chrome path, but you may need to change it
chromePath = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chromePath))



openai.api_key = os.getenv('openai_key') # Replace with your open ai API key
spotifyUser = os.getenv('spotifyUser') # Replace with your spotify username
spotifyClientID = os.getenv('spotifyClientID') # Replace with your spotify client ID
spotifyClientSecret = os.getenv('spotifyClientSecret') # Replace with your spotify client secret
spotify_redirect_uri = 'http://localhost/'


def openSite(item):
    webbrowser.get('chrome').open(item)


def getSong(ID,Secret,URI, context):
    oauth_object = spotipy.SpotifyOAuth(spotifyClientID,spotifyClientSecret,spotify_redirect_uri)
    token_dict = oauth_object.get_access_token()
    token = token_dict['access_token']
    spotifyObject = spotipy.Spotify(auth=token)
    user_name = spotifyObject.current_user()  

    if 'spotify' in query:
        queryList = query.split()
        if context == 'on':
            newList = get_values_between(queryList,'play','on')
            finalString =''
            for i in range(len(newList)):
                if i == 0:
                    finalString += f"{newList[i]}"
                elif i != 0:
                    finalString += f" {newList[i]}"
        else:
            finalString = multipleArguments(query, 'play')


        results = spotifyObject.search(finalString, 1, 0, "track")
        songs_dict = results['tracks']
        song_items = songs_dict['items']
        song = song_items[0]['external_urls']['spotify']
        return song

  
def activateAI(query):
    response = openai.Completion.create(
#        model="ada:ft-personal:contextchecker1-2022-12-13-05-39-24",
        model = "text-davinci-003",
        prompt=query,
        temperature=0.5,
        max_tokens=500,
    )
    return response["choices"][0]["text"] 

#define function for speaking
def speak(text):
    tts = gTTS(text=text, tld='co.uk', lang="en")
    filename = f"{random.randrange(2345)}.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

def shutUp():
    playsound.playsound('empty.mp3')

#define a function for wishing good morning
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning Sir")

    elif hour>=12 and hour<18:
        speak("Good Afternoon Sir")

    else:
        speak("Good Evening Sir")

#listen for commands
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone(device_index=4) as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)
        print("Say that again please...")
        return "None"
    return query

# if you want to search for something specific
# cut is the last word before the arguments
def multipleArguments(string, cut):
    wordList = string.split()
    index = wordList.index(cut)
    num_words_after = len(wordList[index+1:])
    print('THIS YOU IDIOT' + str(num_words_after))
    finalString = ''

    newList = wordList[-num_words_after:]

    print(newList)
    for i in range(num_words_after):
        if i == 0:
            finalString += f'{newList[i]}'
        else:
            finalString += f' {newList[i]}'

    return finalString  

# A version of multipleArguments, except it returns the list
def multipleArgumentsButWorse(string, cut):
    wordList = string.split()
    index = wordList.index(cut)
    num_words_after = len(wordList[index+1:])
    print('THIS YOU IDIOT' + str(num_words_after))

    newList = wordList[-num_words_after:]

    return newList

def get_values_between(lst, item1, item2):
  start_index = lst.index(item1)
  end_index = lst.index(item2)
  return lst[start_index+1:end_index]

def sequences_contain_same_items(a, b):
    for item in a:
        try:
            i = b.index(item)
        except ValueError:
            return False
        b = b[:i] + b[i+1:]
    return not b

wishMe()
while True:
    nameList = ['gervais','jarvis','garvis']
    query = takeCommand().lower()
    gratitudeList = ['No problem sir','My pleasure sir',"You're welcome sir","Have a good day sir"]
    redditList = ["our slash","r /",'r slash','reddit','read it']
    mcList = ['minecraft','lunar','client']
    browserList = ['chrome','browser','google']

    if any(name in query for name in nameList):

        if 'open youtube' in query:
            if 'to' in query:
                finalString = multipleArguments(query, 'to')

                openSite(f"https://www.youtube.com/results?search_query={finalString}")
            else:
                openSite("youtube.com")

            speak(random.choice(gratitudeList))

        elif 'search' in query:
            if 'up' in query:
                finalString = multipleArguments(query, 'up')
            else:
                finalString = multipleArguments(query, 'search')
            openSite(finalString)

            speak(random.choice(gratitudeList))

        elif 'open stackoverflow' in query:
            openSite("stackoverflow.com")

            speak(random.choice(gratitudeList))
        
        elif 'time' in query and 'play' not in query:
            today = date.today()
            now = datetime.datetime.now()
            d2 = today.strftime("%B %d, %Y")
            d3 = now.strftime("%H:%M:%S")
            speak(f"It is {d2} at {d3}")

        elif 'play' in query:
            if 'spotify' in query:
                song = getSong(spotifyClientID,spotifyClientSecret,spotify_redirect_uri,'on')
                openSite(song)
            
            elif 'spotify' not in query:
                song = getSong(spotifyClientID,spotifyClientSecret,spotify_redirect_uri,'play')
                openSite(song)

            speak(random.choice(gratitudeList))

        elif any(reddit in query for reddit in redditList):
            programmerHumor = ["programming","programmer","humor"]
            memeList = ['memes','meme']
            if 'slash' not in query and '/' not in query and "reddit" in query:
                openSite("reddit.com")
                
            elif 'slash' in query:
                subredd = multipleArguments(query,'slash')
                if subredd == 'holdup':
                    subredd = 'holup'
                openSite(f"reddit.com/r/{subredd}")
            elif '/' in query:
                subredd = multipleArguments(query,'/')
                if subredd == 'holdup':
                    subredd = 'holup'
                openSite(f"reddit.com/r/{subredd}")                        
            else:
                openSite("reddit.com")
                
            speak(random.choice(gratitudeList))

        elif ('ai' in query.split() and 'ask' in query.split()) or ('ai' in query.split() and 'asked' in query.split()):
            multipleArguments(query, 'ai')
            text = activateAI(query)
            print(text)
            speak(random.choice(gratitudeList))

        elif "open" in query:
            if any(mc in query for mc in mcList):
                run("Lunar Client")
                
            if "spotify" in query:
                run("Spotify")

            if any(google in query for google in browserList):
                run("Google Chrome")

            if "steam" in query:
                run("Steam")

            else:
                run(multipleArguments(query,'open'))

            speak(random.choice(gratitudeList))
        elif 'fact' in query:
            fact = randfacts.get_fact()
            speak(fact)
        else:
            speak("Unrecognized phrase, please repeat sir")
        
  


    