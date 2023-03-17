import re
from flask import Flask, request, jsonify
import instaloader

app = Flask(__name__)

def download_instagram_video(url):
    L = instaloader.Instaloader()
    shortcode = re.search(r'instagram.com/p/([^/?]+)', url).group(1)
    post = instaloader.Post.from_shortcode(L.context, shortcode)

    if post.is_video:
        L.download_post(post, target=f'video_{shortcode}')
        return True
    else:
        return False

@app.route('/download_video', methods=['POST'])
def download_video():
    url = request.json.get('url', None)
    if url:
        result = download_instagram_video(url)
        if result:
            return jsonify({"status": "success", "message": "Video downloaded"})
        else:
            return jsonify({"status": "failed", "message": "The provided URL is not a video post"})
    else:
        return jsonify({"status": "failed", "message": "URL is required"}), 400

if __name__ == '__main__':
    app.run(debug=True)
