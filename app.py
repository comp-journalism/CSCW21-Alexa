#!/usr/bin/python
# -*- coding: utf-8 -*-
import io
import os
import csv
import time
import boto3
import logging
import argparse
import requests
import datetime
import ConfigParser
from db import Database
from bs4 import BeautifulSoup
from playsound import playsound
import speech_recognition as sr

__author__ = 'HK Dambanemuya'
__version__ = 'Python2'

'''
    Main Alexa Audit Code
'''

class Audit():
    
    def __init__(self, speaker):
        self.messages = list() # List of text queries
        self.filenames = list() # List of text query file names

        # Read queries from text file
        with open("queries.txt", "rb") as f:
            self.messages = f.read().splitlines()

        # Synthesise text queries into voice queries
        for message in self.messages:
            self.synthesize(message.encode('utf-8'), "Queries")

        # Write queries to file
        with open(str('Data/Queries/queries_' + datetime.datetime.now().strftime('%m_%d_%y') + '.csv'), 'wb') as f:
            wr = csv.writer(f, delimiter="\n")
            wr.writerow(self.filenames)

    '''
        Method to synthesize text queries to voice queries
        Input: Text file with queries
        Output: Folder with voice queries in .mp3 format
    '''    
    def synthesize(self, message,folder):
        # Call Amazon Polly client instance with text query
        response = polly_client.synthesize_speech(
                                VoiceId='Matthew',
                                OutputFormat='mp3', 
                                Text = message)
        # Create timestamp variable
        timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"))
        # Save synthesized voice query in .mp3 format
        with open('Audio/Pilot/{0}/{1}.mp3'.format(folder, timestamp +"-"+message.encode('utf-8').replace(" ", "_")), 'wb') as f:
                # Save audio file as mp3
                f.write(response['AudioStream'].read())
                # Add file name to list
                self.filenames.append(timestamp + "-"+message.encode('utf-8').replace(" ", "_"))

def main(speaker):
    # Create database object to store text queries and responses
    db_name = str('Data/DB/audit_' + datetime.datetime.now().strftime('%m_%d_%y') + '.db')
    db = Database(db_name)
    # Initialize Audit class
    audit = Audit("Alexa")
    # Initialize list of responses
    responses = list()

    # Iterate through voice queries
    for filename, message in zip(audit.filenames, audit.messages):
        # Play audio file with wake word e.g. "Alexa", or "Hey, Siri"
        playsound("Audio/Wake/{0}.mp3".format(speaker))
        # Wait 2 Seconds
        time.sleep(2) 
        # Play voice query
        playsound("Audio/Pilot/Queries/{0}.mp3".format(filename))

        # Initialize microphone instance
        engine = sr.Recognizer()
        with sr.Microphone() as source:  
            try:
                # Listen for ambient noise
                engine.adjust_for_ambient_noise(source)
                # Listen for smart speaker response
                audio = engine.listen(source)
                # Save smart speaker response in .wav format
                with open("Audio/Pilot/Responses/{0}.wav".format(filename), "wb") as f:
                    f.write(audio.get_wav_data())
                    # Transcribe smart speaker response to text
                    response = engine.recognize_google(audio)
                    # Save query and response to database
                    db.write_response("Alexa", filename, response)
                    responses.append(response)
                    logging.info("Alexa" + ": " + response)
            # Handle speech recognition service exception
            except sr.UnknownValueError:
                responses.append("Speech Recognition could not understand audio")
                logging.error("Speech Recognition could not understand audio")
            # Handle speech recognition request error exception
            except sr.RequestError as e:
                responses.append("Could not request results from Speech Recognition service; {0}".format(e))
                logging.error("Could not request results from Speech Recognition service; {0}".format(e))
        # Wait 1 minute between subsequent queries
        time.sleep(60)

if __name__ in "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s] %(message)s',
                        datefmt='%Y-%m-%d,%H:%M:%S')

    with open("config.ini") as f: aws_config = f.read()
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.readfp(io.BytesIO(aws_config))

    polly_client = boto3.Session(aws_access_key_id=config.get("auth", "AWSAccessKeyId"),          
                            aws_secret_access_key=config.get("auth", "AWSSecretKey"),
                            region_name='us-west-2').client('polly')

    parser = argparse.ArgumentParser(description='')

    parser.add_argument('--speaker',
                        dest='speaker',
                        type=str,
                        default='Alexa',
                        help='Specify speaker type e.g. Alexa, Siri, Cortana, Google')

    args = parser.parse_args()

    main(args.speaker)