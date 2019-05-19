import os
from flask import request, send_from_directory
from restoweb import app
import mimetypes


static_path = app.config['STATIC_PATH']
static_files = set()
# r=root, d=directories, f = files
for r, d, f in os.walk(static_path):
    for file in f:
        static_files.add('/' + os.path.relpath(os.path.join(r, file), static_path))


# Custom router for application
@app.before_request
def before_request():
    json_accept = 'application/json'
    html_accept = 'text/html'
    accepted = [html_accept, json_accept]
    best_match = request.accept_mimetypes.best_match(accepted, default=html_accept)
    if best_match == json_accept:
        # Go to default routing
        return None
    else:
        sendpath = os.path.join(static_path, 'index.html')
        # Check if there exists a file
        if request.path in static_files:
            sendpath = os.path.join(static_path, request.path[1:])
        mime, _ = mimetypes.guess_type(sendpath)
        prefix, filename = os.path.split(sendpath)
        return send_from_directory(prefix, filename, mimetype=mime)
