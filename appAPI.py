import os
from flask import Flask, request
import json
from flask_cors import CORS
import base64
import train_onnx 

app = Flask(__name__)
cors = CORS(app)
datasetPath = 'data'

@app.route('/api/upload_canvas', methods=['POST'])
def upload_canvas():
    data = json.loads(request.data.decode('utf-8'))
    image_data = data['image'].split(',')[1].encode('utf-8')
    className = data['filename'].split('_')[0]
    fileName = data['filename']
    os.makedirs(datasetPath+'/'+ className +'/'+"image", exist_ok=True)
    with open(datasetPath+'/'+ className +'/'+"image"+'/'+ fileName, 'wb') as fh:
        fh.write(base64.decodebytes(image_data))
    return "Successfully Stored Image"
@app.route('/api/test', methods=['POST', 'GET'])
def test():
    # print('TEST')
    data = json.loads(request.data.decode('utf-8'))
    image_data = data['image'].split(',')[1].encode('utf-8')
    className = data['filename'].split('_')[0]
    fileName = data['filename']
    os.makedirs(datasetPath+'/'+ className +'/'+"image", exist_ok=True)
    with open(datasetPath+'/'+ className +'/'+"image"+'/'+ fileName, 'wb') as fh:
        fh.write(base64.decodebytes(image_data))
    # return (datasetPath+'/'+ className +'/'+"image"+'/'+ fileName)
    return train_onnx.test(datasetPath+'/'+ className +'/'+"image"+'/'+ fileName)
