from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory
from PIL import Image
import io
import os
from .processing import process_image

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('logo-animation.html') #place here index.html

@main.route('/index.html')   #in case of any failure remove linens 13-15
def i_2():
    return render_template('index.html')

@main.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(url_for('main.index'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('main.index'))
    if file:
        content = file.read()
        try:
            raw_image = Image.open(io.BytesIO(content))
            output_image = process_image(raw_image)
            output_image_path = os.path.join('app/static', 'output.png')
            output_image.save(output_image_path)
            return render_template('result.html', output_image='output.png')
        except Exception as e:
            return render_template('result.html', error=str(e))
    return redirect(url_for('main.index'))

@main.route('/download')
def download():
    directory = os.path.join(main.root_path, 'static')
    filename = 'output.png'
    return send_from_directory(directory, filename, as_attachment=True)
