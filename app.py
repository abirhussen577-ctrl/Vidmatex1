from flask import Flask, render_template, request
import yt_dlp
import os

app = Flask(__name__)

# ফোনের Downloads ফোল্ডার
DOWNLOAD_FOLDER = os.path.expanduser('~/storage/downloads')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url', '').strip()
    if not url:
        return '❌ কোনো URL দেননি', 400

    # ফাইলনেম: ভিডিও টাইটেল + আইডি
    outtmpl = os.path.join(DOWNLOAD_FOLDER, '%(title).80s-%(id)s.%(ext)s')

    ydl_opts = {
        'format': 'bv*+ba/b',
        'outtmpl': outtmpl,
        'merge_output_format': 'mp4',
        'noplaylist': True,
        'restrictfilenames': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return f"✅ ভিডিও ডাউনলোড সম্পন্ন!\nফাইল পাওয়া যাবে: {DOWNLOAD_FOLDER}"
    except Exception as e:
        return f"❌ Error: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

