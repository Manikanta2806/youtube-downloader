from flask import Flask, render_template, request, jsonify
import os

# Try importing yt_dlp, handle missing dependencies gracefully
try:
    import yt_dlp
except ModuleNotFoundError:
    raise ImportError("yt_dlp is not installed. Run 'pip install -r requirements.txt' and try again.")

app = Flask(__name__)

# Ensure cookies file exists
COOKIE_FILE = 'cookies.txt'
if not os.path.exists(COOKIE_FILE):
    print("Warning: cookies.txt not found. Some videos may not work.")

def get_download_link(video_url):
    """Extract the direct video download URL using yt-dlp with cookies"""
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'cookiefile': COOKIE_FILE,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(video_url, download=False)
            return info.get('url')
        except Exception as e:
            print(f"Error: {e}")
            return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form.get('video_url')
    download_link = get_download_link(video_url)

    if download_link:
        return jsonify({'download_link': download_link})
    else:
        return jsonify({'error': 'Failed to fetch video. Please try again.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
