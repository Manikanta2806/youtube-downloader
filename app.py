from flask import Flask, render_template, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

def get_download_link(video_url):
    """Extracts the direct video download URL using yt-dlp with cookies from environment variable."""

    # Read cookies from the environment variable
    cookies_string = os.getenv("YOUTUBE_COOKIES", "")

    # Check if cookies exist
    if not cookies_string:
        return None  # Return None if cookies are missing

    # Write the cookies to a temporary file
    with open("cookies.txt", "w", encoding="utf-8") as f:
        f.write(cookies_string.replace(" ", "\n"))  # Convert spaces back into new lines

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        'geo_bypass': True,
        'cookies': 'cookies.txt'  # Use dynamically created cookies file
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(video_url, download=False)
            return info.get('url') or (info['formats'][-1]['url'] if 'formats' in info else None)
        except Exception as e:
            print(f"Error fetching video: {e}")
            return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form.get('video_url')
    
    if not video_url:
        return jsonify({'error': 'Please provide a valid video URL.'})

    download_link = get_download_link(video_url)

    if download_link:
        return jsonify({'download_link': download_link})
    else:
        return jsonify({'error': 'Failed to fetch video. Please try again or check cookies.'})

if __name__ == '__main__':
    app.run(debug=True)
