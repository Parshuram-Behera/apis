from appwrite.client import Client
import os
import logging
import yt_dlp


def get_download_urls(video_url):
    try:
        ydl_opts = {
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            formats = info_dict.get('formats', [])

            # Filter and sort formats by resolution
            sorted_formats = sorted(
                [(f['format_id'], f.get('resolution', 'unknown'), f['url']) for f in formats if 'url' in f],
                key=lambda x: int(x[1].split('p')[0]) if 'p' in x[1] and x[1].split('p')[0].isdigit() else 0
            )

            # Return the sorted formats as strings
            return [f'Resolution: {resolution}, URL: {url}' for fmt_id, resolution, url in sorted_formats]

    except Exception as e:
        logging.error(f"Error processing URL {video_url}: {e}")
        raise e

def main(context):
    if context.req.method == "GET":
        value = context.req.query.get("value")

        if value:
            try:
                download_urls = get_download_urls(value)
                result_string = '\n'.join(download_urls)
                return context.res.send(result_string)
            except Exception as e:
                return context.res.send(f"Error processing URL: {str(e)}")
        else:
            return context.res.send("Value parameter is missing in GET REQUEST")

    return context.res.json({
        "message": "Hello Parshuram Behera"
    })
