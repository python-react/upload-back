# -*- coding: utf-8 -*-
import os
from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from json import dumps
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin

UPLOAD_FOLDER = 'folder'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
CORS(app)
api = Api(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class UploadFiles(Resource):
    def post(self):
        if 'file' not in request.files:
            return make_response(jsonify({"message":"Arquivo obrigatório!"}), 500) 
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return make_response(jsonify({"message":"Upload realizado com sucesso!"}), 200) 

api.add_resource(UploadFiles, '/') 

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

