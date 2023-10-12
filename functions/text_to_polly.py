import boto3
from decouple import config

def convert_text_to_speech(message):
    # Set up AWS credentials and Polly client
    aws_access_key_id = config("AWS_ACCESS_KEY")
    aws_secret_access_key = config("AWS_SECRET_KEY")
    region_name = "us-west-2"  # Change this to your desired AWS region
    
    polly_client = boto3.client(
        "polly",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )

    # Choose the voice and output format
    voice_id = "Joanna"  # Change this to your desired Amazon Polly voice
    output_format = "mp3"  # You can choose other formats like "ogg_vorbis", "pcm", etc.

    # Request speech synthesis
    response = polly_client.synthesize_speech(
        Text=message,
        VoiceId=voice_id,
        OutputFormat=output_format
    )

    # Check if the response is successful
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return response["AudioStream"].read()
    else:
        return None
