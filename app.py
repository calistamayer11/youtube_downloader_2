from flask import Flask, render_template, send_file, request
from pytube import YouTube
from io import BytesIO

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/download/")
def download():
    # print(youtube_link)
    youtube_link = request.args.get("youtube")
    options = request.args.get("options")
    print(options)
    buffer = BytesIO()
    if options == "720p" or options == "480p":
        video = (
            YouTube(youtube_link)
            .streams.filter(file_extension="mp4", res=options)
            .first()
        )
    else:
        video = YouTube(youtube_link).streams.get_audio_only()

    title = video.title
    print(title)
    video.stream_to_buffer(buffer)
    buffer.seek(0)
    # return {"test": "test"}
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"{title}.mp4",
        mimetype="video/mp4",
    )
