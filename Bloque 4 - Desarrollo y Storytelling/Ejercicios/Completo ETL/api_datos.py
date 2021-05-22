"""
Funcion principal que recibe los datos en un diccionario en Json lo reenvia a la funcion genera_resultado y devuelve
el dataframe para pintar.
"""

import json
from flask import Flask, jsonify, request

import genera_resultado

app = Flask(__name__)

@app.route('/api/', methods=['POST'])
def recibe_datos():
    data = request.get_json()
    df_fin = genera_resultado.recibe_datos(data)
    return df_fin

if __name__ == '__main__':

    app.run(debug=True)
