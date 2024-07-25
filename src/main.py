from appwrite.client import Client
import os
import logging
import yt_dlp




def getDownloadUrls(video_url):
    global sorted_video_streams
    try:
        ydl_opts = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            formats = info_dict.get('formats', [])

            # Filter and sort formats by resolution
            sorted_formats = sorted(
                [(f['format_id'], f.get('resolution', 'unknown'), f['url']) for f in formats if 'url' in f],
                key=lambda x: int(x[1].split('p')[0]) if 'p' in x[1] and x[1].split('p')[0].isdigit() else 0
            )

            # Add the sorted formats as strings to the global list
            sorted_video_streams.extend(
                [f'Resolution: {resolution}, URL: {url}' for fmt_id, resolution, url in sorted_formats]
            )

    except Exception as e:
        logging.error(f"Error processing URL {video_url}: {e}")
        raise e


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

    # `context.res.json()` is a handy helper for sending JSON
    return context.res.json({
        "message": "Hello Parshuram Behera"
    })
