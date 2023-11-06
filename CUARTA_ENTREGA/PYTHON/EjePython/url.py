import json
import pyodbc
from flask import Flask, jsonify, render_template, send_from_directory

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)

# Estableciendo la clave secreta para Flask
app.config['SECRET_KEY'] = '12345678'



def connect_to_sql_server():
    server = 'DESKTOP-8IT19L4\SQLSERVER'
    database = 'DWH_Divisas'
    driver = '{ODBC Driver 17 for SQL Server}'

    # Usar autenticación de Windows
    connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    conn = pyodbc.connect(connection_string)
    return conn

def fetch_data_from_db():
    connection = connect_to_sql_server()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM CurrencyExchange")
    rows = cursor.fetchall()
    connection.close()

    # Convertir las filas a diccionarios
    data = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
    return data

data = fetch_data_from_db()

# Opcional: Guardar la data en formato JSON en el archivo 'data.json'
with open('data.json', 'w') as json_file:
    json.dump(data, json_file)

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(data)

@app.route('/download', methods=['GET'])
def download_data():
    return send_from_directory('.', 'data.json', as_attachment=True)
####################################################################
####################################################################

class EmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Enviar')

@app.route('/sendEmail', methods=['GET', 'POST'])
def send_email():
    form = EmailForm()
    if form.validate_on_submit():
        subject = "Tu archivo PDF"
        msg = MIMEMultipart()
        msg['From'] = 'jonhninoa@gmail.com'  # Cambia a tu correo
        msg['To'] = form.email.data
        msg['Subject'] = subject

        body = "Aquí está el archivo PDF que solicitaste."
        msg.attach(MIMEText(body, 'plain'))

        filename = 'data.json'  # Cambia esto por tu archivo PDF
        attachment = open(filename, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {filename}")
        msg.attach(part)
        text = msg.as_string()

        # Enviar el correo
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login('@gmail.com', 'contrsena')
            ############################### 
            ############################### 
            server.sendmail('@gmail.com', form.email.data, text)

        return "Correo enviado!"

    return render_template('send_email.html', form=form)

@app.route('/')
def home():
    return '''
        ¡Bienvenido a nuestra plataforma de datos monetarios!<br>
        <a href="/data">Visualiza la información aquí</a><br>
        <a href="/download">Descarga la información aquí</a><br>
        <a href="/sendEmail">Enviar por correo</a>
    '''

if __name__ == '__main__':
    app.run(debug=True)