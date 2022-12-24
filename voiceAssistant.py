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
from AppOpener import run
import randfacts
from dotenv import load_dotenv # you don't need this unless you're loading from a .env file
import os
import json
import tkinter as tk

def getvar():
    load_dotenv()

getvar()


# This should be the default chrome path, but you may need to change it
chromePath = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chromePath))

# checking if github still works


# make everything equal to ' ' if you don't want to use them, make sure to tell the GUI that as well
openai.api_key = os.getenv('openai_key') # Replace with your open ai API key https://beta.openai.com/account/api-keys
spotifyUser = os.getenv('spotifyUser') # Replace with your spotify username
# Go to https://developer.spotify.com/dashboard/login and create an App
spotifyClientID = os.getenv('spotifyClientID') # Replace with your spotify client ID https://developer.spotify.com/dashboard/login
spotifyClientSecret = os.getenv('spotifyClientSecret') # Replace with your spotify client secret https://developer.spotify.com/dashboard/login
# Go to "Edit Settings" in your app, and add "http://localhost/" as a Redirect URI
spotify_redirect_uri = 'http://localhost/'

def get_user_data():
    with open("user_info.json","r") as f:
        user = json.load(f)

    return user

def open_data():
    user = get_user_data()

    if 'name' in user:
        return False  
    else:
        user['gender'] = 'NA'
        user['name'] = 'NA'
        user['spotify'] = False
        user['openai'] = False
        


    with open("user_info.json", "w") as f:
        json.dump(user,f, indent=4)
    return True

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

#define a function for greeting the user
def wishMe():
    data = get_user_data()
    name = data['name']

    if name == 'NA':
        name = 'mate'

    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak(f"Good Morning {name}")

    elif hour>=12 and hour<18:
        speak(f"Good Afternoon {name}")

    else:
        speak(f"Good Evening {name}")



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
    num_words_after = len(wordList[index+1:]) # find the number of keywords
    finalString = ''

    newList = wordList[-num_words_after:] # create a list of all the keywords


    for i in range(num_words_after): # create a string that combines the keywords
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

    newList = wordList[-num_words_after:]

    return newList

# a version of multipleArguments, except it gets the keywords in between two words in the query. It also returns a list instead of a string
def get_values_between(lst, item1, item2):
  start_index = lst.index(item1)
  end_index = lst.index(item2)
  return lst[start_index+1:end_index]


def list_matchup(list1,list2): # function to check if any item in one list matches up with any item in another list
    match = [False]
    for i in list1:
        if i in list2:
            match = [True,i]

    return match


open_data()

root = tk.Tk()

var = tk.IntVar()

root.title("Close this window when you're done. Green means disabled, Red means enabled")

root.geometry('720x400')

def spotifyButtonFunc():
    data = get_user_data()
    if var.get() == 0:
        var.set(1)
        if data['spotify'] == False:
            spotifyButton.config(bg='red')
            data['spotify'] = True
    else:
        var.set(0)
        if data['spotify'] == True:
            spotifyButton.config(bg='green')
            data['spotify'] = False


    with open("user_info.json", "w") as f:
        json.dump(data,f, indent=4)

def openaiButtonFunc():
    data = get_user_data()
    if var.get() == 0:
        var.set(1)
        if data['openai'] == False:
            aiButton.config(bg='red')
            data['openai'] = True
    else:
        var.set(0)
        if data['openai'] == True:
            aiButton.config(bg='green')
            data['openai'] = False
    
    with open("user_info.json", "w") as f:
        json.dump(data,f, indent=4)


def find_button_color(type):
    data = get_user_data()

    if data[type] == False:
        return 'green'

    else:
        return 'red'


spotifyButton = tk.Button(root, text='Spotify Enable/Disable', bg=find_button_color('spotify'), command=spotifyButtonFunc)

spotifyButton.pack(side = 'top')

aiButton = tk.Button(root, text='OpenAI Enable/Disable', bg=find_button_color('openai'), command=openaiButtonFunc)

aiButton.pack(side = 'top')

root.mainloop()
wishMe()

while True:

    data = get_user_data()
    gender = data['gender']

    if gender == 'NA':
        gender = 'mate'

    nameList = ['gervais','jarvis','garvis','jervis'] # speech recognition is garbage
    query = takeCommand().lower()
    gratitudeList = [f'No problem {gender}',f'My pleasure {gender}',f"You're welcome {gender}",f"Have a good day {gender}"]
    redditList = ["our slash","r /",'r slash','reddit','read it']
    mcList = ['minecraft','lunar','client']
    browserList = ['chrome','browser','google']
    genderList = ['male','female','man','woman','non-binary','enby','in b','MB','envy','NB'] # i didn't add a way to input a different gender cause difficult lmao. feel free to add anything to this list, it'll still work the same. also had to add the last few values cause speech recognition is garbage

    if any(name in query for name in nameList):

        if 'name' in query or "i'm" in query or 'am' in query: # this is the code to put values into the user data
            query_string = query #there was a bug where it would pick up the "is" in Jarvis, so this is my best solution
            query = query.split()
            name = 'NA'
            gender = 'NA'
            gender_matchup = list_matchup(query,genderList) # find if the user is declaring their gender

            if gender_matchup != [False]:
                gender = gender_matchup[1]


                if gender in ['man','male']: # decide what to refer to the user as
                    greeting = 'sir'
                if gender in ['female','woman']:
                    greeting = "ma'am"
                if gender in ['non-binary','enby','in b','MB','envy','NB']:
                    greeting = 'mate'

                data['gender'] = greeting
                speak(f"That's good to know {greeting}")

            else:
                if "i'm" in query: # this turned into an unintentional dad joke machine, if you say "i'm hungry", it'll respond with "nice to meet you, hungry"
                    name = multipleArguments(query_string, "i'm")
                elif 'is' in query: # check for if the user said "my name is ..."
                    name = multipleArguments(query_string, "is")

                elif 'am' in query:
                    name = multipleArguments(query_string, 'am')

                data['name'] = name
                

                speak(f"Nice to meet you, {name}")


            with open("user_info.json", "w") as f:
                json.dump(data,f, indent=4)
            
        elif 'open youtube' in query:
            if 'to' in query:
                finalString = multipleArguments(query, 'to')

                openSite(f"https://www.youtube.com/results?search_query={finalString}")
            else:
                openSite("youtube.com")

            speak(random.choice(gratitudeList))

        elif 'search' in query: # annoying bug rn where it adds a slash to the end of every search, even if it isnt a 
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
                
            elif "spotify" in query:
                run("Spotify")

            elif any(google in query for google in browserList):
                run("Google Chrome")

            elif "steam" in query:
                run("Steam")

            else:
                run(multipleArguments(query,'open'))

            speak(random.choice(gratitudeList))
        elif 'fact' in query:
            fact = randfacts.get_fact()
            speak(fact)
        else:
            speak("Unrecognized phrase, please repeat sir")

    
        
  


    