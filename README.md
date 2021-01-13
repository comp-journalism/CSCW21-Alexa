# Auditing the Information Quality of News-Related Queries on the Alexa Voice Assistant

Smart speakers are becoming increasingly ubiquitous in society and are now used for satisfying a variety of information needs, from asking about the weather or traffic to accessing the latest breaking news information. Their growing use for news and information consumption presents new questions related to the quality, source diversity, and comprehensiveness of the news-related information they convey. These questions have significant implications for voice assistant technologies acting as algorithmic information intermediaries, but systematic information quality audits have not yet been undertaken. To address this gap, we develop a methodological approach for evaluating information quality in voice assistants for news-related queries. We demonstrate the approach on the Amazon Alexa voice assistant, first characterising Alexa's performance in terms of response relevance, accuracy, and timeliness, and then further elaborating analyses of information quality based on query phrasing, news category, and information provenance. We discuss the implications of our findings for future audits of information quality on voice assistants and for the consumption of news information via such algorithmic intermediaries more broadly. 

## Code Description

This repository contains the source code necessary to facilitate replicating the data collection methods used in the paper described above.

### Requirements

Python 2+ required (for python build)

Install required modules (boto3, sqlite3, requests, speech_recognition, etc).

    pip install -r requirements.txt

### Amazon Web Services (AWS) Credentials

Create a config.ini file to securely store your private AWS access and secret keys

    [auth]
    AWSAccessKeyId=XXXXXXXXXX
    AWSSecretKey=XXXXXXXXXX

### Code Execution

1. Fetching Google's Top 20 Daily Search Trends
     
        python google_trends.py
    
2. Synthesizing text queries to voice queries using Amazon Polly
     
        python speech_synthesis.py --args
     
3. Issuing voice queries to the Alexa smart speaker and saving voice responses 
    
        python app.py --args
     
4. Uploading Alexa voice responses to S3 for transcription
     
        python s3_upload.py
     
5. Transcribing Alexa voice responses with Amazon Transcribe
 
        python speech_transcription.py
     
## Acknowledgments

This work is supported by the National Science Foundation Grant, Award IIS-1717330. The authors would like to thank Sophie Liu, Victoria Cabales, Benjamin Scharf, and the Knight Lab Studio at Northwestern University for their support and assistance in a related pilot study.
