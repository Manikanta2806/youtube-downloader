from flask import Flask, render_template, request, jsonify
import yt_dlp
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

def get_download_link(video_url):
    """Extract the direct video download URL using yt-dlp with browser cookies."""
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'quiet': True,
        'noplaylist': True,  # Ensure only one video is fetched
        'geo_bypass': True,  # Bypass geo-restrictions if needed
        'cookies-from-browser': ('chrome', {'strict': False})  # Use cookies from Chrome browser
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return info.get('url') or (info['formats'][-1]['url'] if 'formats' in info else None)
    except Exception as e:
        logging.error(f"Error fetching video: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form.get('video_url')

    if not video_url:
        return jsonify({'error': 'Invalid request. Please provide a video URL.'}), 400

    download_link = get_download_link(video_url)

    if download_link:
        return jsonify({'download_link': download_link})
    else:
        return jsonify({'error': 'Failed to fetch video. Please check the URL and try again.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
