import io
import boto3
import string
import logging
import argparse
import datetime
import ConfigParser

__author__ = 'HK Dambanemuya'
__version__ = 'Python2'

'''
    Amazon Polly: 
        Code to synthesize text queries to voice queries
'''

class Polly():

        def __init__(self, speaker, voice):
                self.speaker = speaker
                self.voice = voice 
                with open("config.ini") as f: aws_config = f.read()
                self.config = ConfigParser.RawConfigParser(allow_no_value=True)
                self.config.readfp(io.BytesIO(aws_config))
                self.polly_client = boto3.Session(aws_access_key_id=self.config.get("auth", "AWSAccessKeyId"),          
                                aws_secret_access_key=self.config.get("auth", "AWSSecretKey"),
                                region_name='us-east-2').client('polly')
        
        # Method to remove punctuation 
        # Necessary as the Polly synthesizer will pronounce the punctuations
        # e.g. "U dot S dot A when pronouncing U.S.A"
        def strip_punctuation(self, s):
                return ''.join(c for c in s if c not in string.punctuation)

        # Method to synthesize voice queries from text
        def synthesize(self, folder, message, in_time=False):
                response = self.polly_client.synthesize_speech(
                                        VoiceId=self.voice,
                                        OutputFormat='mp3', 
                                        Text = message)
                # Handle timestamps
                if in_time:
                        timestamp = in_time
                else:
                        timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"))
                # Save voice query to .mp3 file
                with open('Audio/Pronunciations/{0}/{1}.mp3'.format(folder, timestamp +"-"+self.strip_punctuation(message.encode('utf-8')).replace(" ", "_")), 'wb') as f:
                        f.write(response['AudioStream'].read())

def main(speaker, folder, message, voice):
        # Initialize Polly class
        polly = Polly(speaker)
        # Call speech synthesis method
        polly.synthesize(folder, polly.strip_punctuation(message), polly.voice)


if __name__ in "__main__":
        logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s] %(message)s',
                        datefmt='%Y-%m-%d,%H:%M:%S')

        parser = argparse.ArgumentParser(description='')

        parser.add_argument('--speaker',
                        dest='speaker',
                        type=str,
                        default='Alexa',
                        help='Specify speaker type e.g. Alexa, Siri, Cortana, Google')
        parser.add_argument('--message',
                        dest='message',
                        type=str,
                        default="Alexa",
                        help='Specify the message e.g. Can you tell me about Ilhan Omar today')
        parser.add_argument('--folder',
                        dest='folder',
                        type=str,
                        default="Wake",
                        help='Specify the type of speech synthesis e.g. Wake for wake word, Queries for query')

        args = parser.parse_args()

        main(args.speaker, args.folder, args.message)