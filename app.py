from flask import Flask, render_template,request

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
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    
    if file.filename == '':
        return "No File Selected"
    
    if not allowed_file(file.filename):
        return "only PDF, PNG, JPG, JPEG FILES are allowed"
    
    file.save(f'uploads/{file.filename}')
    
    return "File Uploaded Successfully"
if __name__ == '__main__':
    app.run(debug=True)