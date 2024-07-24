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

    # You can log messages to the console

    context.log("Hello, Logs!")

    # If something goes wrong, log an error
    context.error("Hello, Errors!")

    # The `ctx.req` object contains the request data
    if context.req.method == "GET":
        # Send a response with the res object helpers
        # `ctx.res.send()` dispatches a string back to the client
        return context.res.send("Got A GET REQUEST")

    # `ctx.res.json()` is a handy helper for sending JSON
    return context.res.json(

        "Hello Parshuram Behera"
    )
