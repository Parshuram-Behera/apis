from appwrite.client import Client
import os
from pytube import YouTube


# This is your Appwrite function
# It's executed each time we get a request


def getDownloadUrls(userUrl) :
    url = str(userUrl)
    youtubeObj = YouTube(url)
    vidStreams = youtubeObj.streams.filter( mime_type="video/mp4",type="video").order_by('resolution')

    streamUrls = []

    for stream in vidStreams :
        streamUrls.append(stream.url)

    return streamUrls



def main(context):
    # Why not try the Appwrite SDK?
    #
    # client = (
    #     Client()
    #     .set_endpoint("https://cloud.appwrite.io/v1")
    #     .set_project(os.environ["APPWRITE_FUNCTION_PROJECT_ID"])
    #     .set_key(os.environ["APPWRITE_API_KEY"])
    # )

    if context.req.method == "GET":
        # Extract the value from query parameters
        value = context.req.query.get("value")

        if value:
            # Send a response with the extracted value
            return context.res.send(f"Got A GET REQUEST with value: {value}")
        else:
            # Send a response if the value is missing
            return context.res.send("Value parameter is missing in GET REQUEST")

    # `ctx.res.json()` is a handy helper for sending JSON
    return context.res.json(

        "Hello Parshuram Behera"
    )
