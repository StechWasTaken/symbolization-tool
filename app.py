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

    if form.validate_on_submit():
        file = form.video.data.stream
        video = VideoCapture(file.name)
        success, images = video.read()
        gray_video = cvtColor(images, COLOR_BGR2GRAY)

        count = 0
        for frame in gray_video:
            pixels = []
            for pixel in frame:
                pixels.append(pixel)
            frames['frame_' + str(count)] = str(pixels)
            count += 1

    return render_template('index.html', form=form, frames=frames)

if __name__ == "__main__":
    app.run(debug=True)