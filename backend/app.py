from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
CORS(app)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="reservas_db"
)

def send_confirmation_email(user_email, booking_details):
    msg = MIMEText(f"Tu reserva: {booking_details}")
    msg['Subject'] = 'Confirmación de Reserva'
    msg['From'] = 'tu_email@ejemplo.com'
    msg['To'] = user_email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('naranjomaximiliano984@gmail.com', 'computadora23')
        server.send_message(msg)

@app.route('/api/booking', methods=['POST'])
def create_booking():
    data = request.get_json()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO bookings (date, service, email) VALUES (%s, %s, %s)",
        (data['date'], data['service'], data['email'])
    )
    db.commit()
    cursor.close()
    send_confirmation_email(data['email'], f"Fecha: {data['date']}, Servicio: {data['service']}")
    return jsonify({'message': 'Reserva creada'})

if __name__ == '__main__':
    app.run(debug=True)