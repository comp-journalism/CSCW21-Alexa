from __future__ import print_function
import io
import os
import time
import boto3
import logging
import argparse
import ConfigParser

__author__ = 'HK Dambanemuya'
__version__ = 'Python2'

'''
    Amazon Transcribe: 
        Code to transcribe Alexa voice responses to text
'''

def main(filename):
    logging.info(filename)
    # Specifiy audio file location
    job_uri = "https://alexa-audit.s3.us-east-2.amazonaws.com/pronunciations/Audio/Audit/{0}".format(filename)

    try: # Transcribe voice response
        transcribe.start_transcription_job(
            TranscriptionJobName=filename,
            LanguageCode='en-US',
            Media={'MediaFileUri': job_uri},
            MediaFormat='mp3',
            OutputBucketName="alexa-audit")

        while True: # Check transcription status
            status = transcribe.get_transcription_job(TranscriptionJobName=filename)
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                break
            logging.info("Working...")
            time.sleep(5)
        logging.info(status)
    # Log all exception errors
    except Exception as e:
        logging.error(e)

if __name__ in "__main__":
        logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s] %(message)s',
                        datefmt='%Y-%m-%d,%H:%M:%S')
        directory = "/Users/henrydambanemuya/Documents/Smart-Speaker-AI/Audio/Pronunciations/Audit/"
        with open("config.ini") as f: aws_config = f.read()
        config = ConfigParser.RawConfigParser(allow_no_value=True)
        config.readfp(io.BytesIO(aws_config))

        transcribe = boto3.client('transcribe', 
                            aws_access_key_id=config.get("auth", "AWSAccessKeyId"),          
                            aws_secret_access_key=config.get("auth", "AWSSecretKey"),
                            region_name='us-east-2')

        for filename in os.listdir(directory):
            main(filename)