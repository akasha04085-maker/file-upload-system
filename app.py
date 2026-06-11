import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template,request
from flask import send_from_directory
from flask import redirect, url_for


app = Flask(__name__)

ALLOWED_EXTENSIONS = {
    'pdf',
    'png',
    'jpg',
    'jpeg'
}

def allowed_file(filename):
    return(
        '.' in filename and 
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )

@app.route('/')
def home():
    files = os.listdir('uploads')
    return render_template('index.html',files=files)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    
    if file.filename == '':
        return "No File Selected"
    
    if not allowed_file(file.filename):
        return "only PDF, PNG, JPG, JPEG FILES are allowed"
    
    filename = secure_filename(file.filename)
    file.save(f'uploads/{file.filename}')
    
    return "File Uploaded Successfully"

@app.route('/files')
def files():
    
    uploaded_files = os.listdir('uploads')
    
    return{
        "files": uploaded_files
    }
    
@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(
        'uploads',
        filename,
        as_attachment=True
    )
    
@app.route('/delete/<path:filename>')
def delete_file(filename):
    filepath = os.path.join('uploads', filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    return redirect(url_for('home'))
if __name__ == '__main__':
    app.run(debug=True)