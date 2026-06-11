import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory,
    flash
)

from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "mysecretkey"

ALLOWED_EXTENSIONS = {
    'pdf',
    'png',
    'jpg',
    'jpeg'
}


def allowed_file(filename):
    return (
        '.' in filename and
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route('/')
def home():

    uploaded_files = os.listdir('uploads')

    return render_template(
        'index.html',
        files=uploaded_files
    )


@app.route('/upload', methods=['POST'])
def upload():

    if 'file' not in request.files:
        flash("❌ No file selected")
        return redirect(url_for('home'))

    file = request.files['file']

    if file.filename == '':
        flash("❌ No file selected")
        return redirect(url_for('home'))

    if not allowed_file(file.filename):
        flash("❌ Only PDF, PNG, JPG, JPEG files are allowed")
        return redirect(url_for('home'))

    filename = secure_filename(file.filename)

    file.save(
        os.path.join(
            'uploads',
            filename
        )
    )

    flash("✅ File Uploaded Successfully")

    return redirect(url_for('home'))


@app.route('/download/<path:filename>')
def download_file(filename):

    return send_from_directory(
        'uploads',
        filename,
        as_attachment=True
    )


@app.route('/delete/<path:filename>')
def delete_file(filename):

    filepath = os.path.join(
        'uploads',
        filename
    )

    if os.path.exists(filepath):
        os.remove(filepath)
        flash("🗑 File Deleted Successfully")

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)