#! /usr/bin/python3.6
# -*-coding:utf-8 -* 

import re 
import pyttsx3
import speech_recognition as sr 

def speak(text):
    """ A function which makes to assistant speaks and say text """
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def getAudio():
    """ A function to make the assistant listen and process the audio data """

    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio_data = r.listen(source)
        speech = ''

    try:
        speech = r.recognize_google(audio_data)
    except Exception as exc:
        print('Error: ', exc)
    else:
        return speech

def parseText(text, deaths_dict, cases_dict):
    """ A function to parse the text we said, find the mentionned country, search about on it in our dictionnaries and 
        return a text with the following format : There are X cases in COUNTRY'
        -Our text will have the following format :
        'How many cases/deaths are there in COUNTRY'
    """
    try:
        words_list = text.split(' ')
    except Exception as exc:
        print('Error: ', exc)
    else:

        #Total cases
        if words_list[2] == 'cases':
            number_cases = cases_dict[words_list[6]]
            answer = 'There are {} cases in {}'.format(number_cases, words_list[6])
            print(answer)
            speak(answer)

        #Number of deaths
        elif words_list[2] == 'deaths':
            number_cases = deaths_dict[words_list[6]]
            answer = 'There are {} deaths in {}'.format(number_cases, words_list[6])
            print(answer)
            speak(answer)
    

    

