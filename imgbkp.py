import os
import hashlib
import json
from flask import Flask, request, render_template_string, render_template, send_from_directory, make_response, url_for
from flask_basicauth import BasicAuth
import requests
import time
import argparse
from waitress import serve
import humanize

app = Flask(__name__)

# Command-line arguments
parser = argparse.ArgumentParser(description='File Management App')
parser.add_argument('--username', default='admin', help='Username for basic authentication')
parser.add_argument('--password', default='admin', help='Password for basic authentication')
parser.add_argument('--host', default='0.0.0.0', help='Host IP address')
parser.add_argument('--port', type=int, default=8833, help='Port for the Flask application')
args = parser.parse_args()

# Basic HTTP Authentication Configuration
app.config['BASIC_AUTH_USERNAME'] = args.username
app.config['BASIC_AUTH_PASSWORD'] = args.password
basic_auth = BasicAuth(app)

# Directory to store downloaded files and metadata
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.template_filter('humanize_naturalsize')
def humanize_naturalsize_filter(value):
    return humanize.naturalsize(value)


@app.route('/bkp/', methods=['GET', 'POST'])
@basic_auth.required
def admin():
    uploaded_files = []
    if request.method == 'POST':
        for uploaded_file in request.files:
            uploaded_file = request.files[uploaded_file]
            try:
                # Generate a unique filename using MD5 hash
                md5_hash = hashlib.md5(uploaded_file.read()).hexdigest()
                file_extension = os.path.splitext(uploaded_file.filename)[-1].lower()
                if file_extension:
                    filename = md5_hash + file_extension
                else:
                    filename = md5_hash
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                # Save the uploaded file
                uploaded_file.seek(0)
                uploaded_file.save(file_path)

                # Save metadata with file extension
                metadata = {
                    'filename': filename,
                    'timestamp': int(time.time()),  # Unix timestamp
                    'mime_type': uploaded_file.content_type,
                    'file_size_bytes': os.path.getsize(file_path),
                    'file_extension': file_extension,  # Include the file extension
                }
                metadata_file_path = os.path.join(app.config['UPLOAD_FOLDER'], md5_hash + '.json')
                if not os.path.exists(metadata_file_path):
                    with open(metadata_file_path, 'w') as metadata_file:
                        json.dump(metadata, metadata_file)

                return f"File '{filename}' has been uploaded and saved."
            except Exception as e:
                return f"Error: {str(e)}"

        # Check if a URL was provided
        url = request.form.get('url')
        if url:
            try:
                response = requests.get(url, stream=True)
                response.raise_for_status()
                content_type = response.headers.get('content-type')
                md5_hash = hashlib.md5(url.encode()).hexdigest()
                file_extension = os.path.splitext(url)[-1].lower()
                if file_extension:
                    filename = md5_hash + file_extension
                else:
                    filename = md5_hash
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                # Save metadata with file extension
                metadata = {
                    'url': url,
                    'mime_type': content_type,
                    'filename': filename,
                    'timestamp': int(time.time()),  # Unix timestamp
                    'status_code': response.status_code,
                    'headers': dict(response.headers),
                    'file_size_bytes': len(response.content),
                    'file_extension': file_extension,  # Include the file extension
                }
                metadata_file_path = os.path.join(app.config['UPLOAD_FOLDER'], md5_hash + '.json')
                if not os.path.exists(metadata_file_path):
                    try:
                        # Save metadata inside a try-except block
                        with open(metadata_file_path, 'w') as metadata_file:
                            json.dump(metadata, metadata_file)

                        # Save the file
                        if not os.path.exists(file_path):
                            with open(file_path, 'wb') as file:
                                for chunk in response.iter_content(chunk_size=1024):
                                    file.write(chunk)

                        return f"File saved as {filename} with MIME type {content_type}"
                    except Exception as e:
                        # Handle the exception and return an error message
                        return f"Error saving file: {str(e)}"
            except Exception as e:
                return f"Error: {str(e)}"
    elif request.method == 'GET':
        # Get the list of uploaded files
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            if filename.endswith('.json'):
                metadata_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                with open(metadata_file_path, 'r') as metadata_file:
                    metadata = json.load(metadata_file)
                    uploaded_files.append(metadata)

    return render_template('admin.html', files=uploaded_files, css_file=url_for('static', filename='style.css'))

@app.route('/bkp/<file_md5>')
def get_file(file_md5):
    metadata_file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_md5 + '.json')
    if os.path.exists(metadata_file_path):
        try:
            with open(metadata_file_path, 'r') as metadata_file:
                metadata = json.load(metadata_file)
                mime_type = metadata.get('mime_type')
                file_extension = metadata.get('file_extension')
                if mime_type:
                    if file_extension:
                        filename_with_extension = file_md5 + file_extension
                        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename_with_extension)
                    else:
                        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_md5)
                    if os.path.exists(file_path):
                        response = make_response(send_from_directory(app.config['UPLOAD_FOLDER'], filename_with_extension))
                        response.headers['Content-Type'] = mime_type
                        return response
                    else:
                        return "File not found."
                else:
                    return "MIME type not found in metadata."
        except Exception as e:
            return f"Error: {str(e)}"
    else:
        return "File not found."

if __name__ == '__main__':
    serve(app, host=args.host, port=args.port)
