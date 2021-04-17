from flask import Flask, render_template, url_for, redirect, request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import FileField, SubmitField, ValidationError
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
from cv2 import *
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'notverysecret'

class VideoForm(FlaskForm):
    video = FileField('video', validators=[FileRequired(), FileAllowed(['mp4'], 'mp4 only!')])
    submit = SubmitField('Create')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = VideoForm()
    frames = {}
    width = 0
    height = 0
    total_frames = 0
    frame_time = 0

    if form.validate_on_submit():
        file = form.video.data.stream
        video = VideoCapture(file.name)
        width = int(video.get(CAP_PROP_FRAME_WIDTH)) // 12
        height = int(video.get(CAP_PROP_FRAME_HEIGHT)) // 12
        total_frames = int(video.get(CAP_PROP_FRAME_COUNT))
        frame_time = 1000 / video.get(CAP_PROP_FPS)

        # possibly add compression to the algorithm to make processing faster!
        i = 0
        while True:
            video.set(CAP_PROP_POS_FRAMES, i)
            success, image = video.read()
            if success:
                try:
                    gray_image = cvtColor(image, COLOR_BGR2GRAY)
                    gray_image = resize(gray_image, (width, height))
                    image = []
                    for pixels in gray_image:
                        for pixel in pixels:
                            image.append(pixel)
                    frames['frame_' + str(i)] = str(image)
                    i += 1
                except:
                    break
            else:
                break

    return render_template('index.html', form=form, frames=frames, size=(width, height), total_frames=total_frames, frame_time=frame_time)

if __name__ == '__main__':
    app.run(debug=True)