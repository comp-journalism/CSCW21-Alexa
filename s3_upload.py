import io
import os
import boto3
from botocore.exceptions import NoCredentialsError
import ConfigParser
import logging

'''
    Helper Code:
        Code to upload Alexa voice responses to S3 for transcription
'''

def upload_to_aws(local_file, bucket, s3_file):
    # Initialize AWS-S3 client
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try: # Upload file to S3 bucket
        s3.upload_file(local_file, bucket, s3_file)
        logging.info("Upload Successful")
        return True
    # Handle file not found exception
    except FileNotFoundError:
        logging.error("The file was not found")
        return False
    # Handle AWS credentials exception
    except NoCredentialsError:
        logging.error("Credentials not available")
        return False

if __name__ in "__main__":
        logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s] %(message)s',
                        datefmt='%Y-%m-%d,%H:%M:%S')

        with open("config.ini") as f: aws_config = f.read()
        config = ConfigParser.RawConfigParser(allow_no_value=True)
        config.readfp(io.BytesIO(aws_config))

        ACCESS_KEY = config.get("auth", "AWSAccessKeyId")
        SECRET_KEY = config.get("auth", "AWSSecretKey")

        voices = ['Audit']

        for voice in voices:
            directory = "Audio/Pronunciations/{0}/".format(voice)

            for filename in os.listdir(directory):
                upload_to_aws('Audio/Pronunciations/{0}/{1}'.format(voice, filename), 'alexa-audit', 'pronunciations/Audio/{0}/{1}'.format(voice, filename))
