import csv
import json
from flask import Flask, jsonify, send_from_directory

app = Flask(__name__)

# Leer el archivo CSV y almacenar los datos en la variable 'data'
data = []
with open('Total.csv') as file:
    csv_reader = csv.DictReader(file, delimiter=',')
    for row in csv_reader:
        data.append(row)

# Guardar la data en formato JSON en el archivo 'data.json'
with open('data.json', 'w') as json_file:
    json.dump(data, json_file)

# Función que maneja la ruta '/data'.
# Retorna la información almacenada en formato JSON para visualización en la web.
@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(data)

#Función que maneja la ruta '/download'.
# Permite al usuario descargar el archivo 'data.json' directamente a su directorio de descargas.
@app.route('/download', methods=['GET'])
def download_data():
      return send_from_directory('.', 'data.json', as_attachment=True)

# Función que maneja la ruta raíz '/'.
# Proporciona una interfaz sencilla con enlaces para visualizar o descargar la información.
@app.route('/')
def home():
    
    return '''
        ¡Bienvenido a nuestra plataforma de datos monetarios!<br>
        <a href="/data">Visualiza la información aquí</a><br>
        <a href="/download">Descarga la información aquí</a>
    '''

# 
if __name__ == '__main__':
    app.run(debug=True)
