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
    # The `context.req` object contains the request data
    if context.req.method == "GET":
        # Extract the value from query parameters
        value = context.req.query.get("value")

        if value:
            try:
                # Call the getDownloadUrls function with the extracted value
                download_urls = getDownloadUrls(value)
                # Convert the list to a string
                result_string = str(download_urls)
                # Send the result string to the user
                return context.res.send(result_string)
            except Exception as e:
                # Handle exceptions and send an error response
                return context.res.send(f"Error processing URL: {str(e)}")
        else:
            # Send a response if the value is missing
            return context.res.send("Value parameter is missing in GET REQUEST")

    # `ctx.res.json()` is a handy helper for sending JSON
    return context.res.json(

        "Hello Parshuram Behera"
    )
