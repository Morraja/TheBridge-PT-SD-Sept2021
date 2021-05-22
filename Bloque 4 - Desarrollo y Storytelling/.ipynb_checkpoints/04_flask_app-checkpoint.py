import json
import pickle as p

import numpy as np
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/health/', methods=['GET'])
def health():
    return 'everything ok here'

@app.route('/api/', methods=['POST'])
def makecalc():
    data = request.get_json()
    prediction = np.array2string(model.predict(data))

    return jsonify(prediction)

if __name__ == '__main__':
    modelfile = './models/model.pkl'
    model = p.load(open(modelfile, 'rb'))
    app.run(debug=True)