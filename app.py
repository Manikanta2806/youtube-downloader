from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

def get_download_link(video_url):
    """Extract the direct video download URL using yt-dlp"""
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'cookies-from-browser': 'chrome'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(video_url, download=False)
            return info['url']  # Direct video URL
        except Exception as e:
            return None

@app.route('/')
def index():
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
    app.run(debug=True)
