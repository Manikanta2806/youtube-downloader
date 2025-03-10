from flask import Flask, render_template, request, jsonify
import os

# Try importing yt-dlp, handle missing dependencies gracefully
try:
    import yt_dlp
except ModuleNotFoundError:
    raise ImportError("yt_dlp is not installed. Run 'pip install -r requirements.txt' and try again.")

app = Flask(__name__)

def get_download_link(video_url):
    """
    Extract the direct video download URL using yt-dlp with cookies.
    :param video_url: URL of the video to download
    :return: Direct video download link or None if an error occurs
    """
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'cookies-from-browser': 'chrome',  # Change to 'firefox' if using Firefox
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(video_url, download=False)
            return info.get('url')  # Return the URL of the video for download
        except Exception as e:
            print(f"Error: {e}")
            return None

@app.route('/')
def home():
    """
    Render the home page with the video download form.
    :return: Rendered HTML template
    """
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    """
    Handle the video download request, process the video URL and return the download link.
    :return: JSON response with download link or error message
    """
    video_url = request.form.get('video_url')  # Get the video URL from the form
    if not video_url:
        return jsonify({'error': 'No video URL provided. Please try again.'})

    download_link = get_download_link(video_url)  # Get the download link using yt-dlp

    if download_link:
        return jsonify({'download_link': download_link})  # Return download link if successful
    else:
        return jsonify({'error': 'Failed to fetch video. Please try again.'})  # Return error if it fails

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Run the app on all interfaces
