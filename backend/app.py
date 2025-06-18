from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
CORS(app)

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",
        database="reservas_db"
    )
except mysql.connector.Error as e:
    print(f"Error connecting to database: {e}")
    exit(1)

def send_confirmation_email(user_email, booking_details):
    try:
        msg = MIMEText(f"Tu reserva: {booking_details}")
        msg['Subject'] = 'Confirmación de Reserva'
        msg['From'] = 'naranjomaximiliano984@gmail.com'  # Usa tu email
        msg['To'] = user_email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('naranjomaximiliano984@gmail.com', 'computadora23')  # Reemplaza con App Password
            server.send_message(msg)
    except smtplib.SMTPAuthenticationError as e:
        print(f"SMTP Authentication Error: {e}")
        return False
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
    return True

@app.route('/api/booking', methods=['POST'])
def create_booking():
    try:
        data = request.get_json()
        if not data or 'date' not in data or 'service' not in data or 'email' not in data:
            return jsonify({'error': 'Datos incompletos'}), 400

        # Convertir fecha a formato MySQL (YYYY-MM-DD)
        from datetime import datetime
        date_str = datetime.fromisoformat(data['date'].replace('Z', '+00:00')).strftime('%Y-%m-%d')

        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO bookings (date, service, email) VALUES (%s, %s, %s)",
            (date_str, data['service'], data['email'])
        )
        db.commit()
        cursor.close()

        email_success = send_confirmation_email(data['email'], f"Fecha: {date_str}, Servicio: {data['service']}")
        return jsonify({'message': 'Reserva creada' + (' (email enviado)' if email_success else ' (fallo email)')}), 200
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Error en la base de datos'}), 500
    except ValueError as e:
        print(f"Date format error: {e}")
        return jsonify({'error': 'Formato de fecha inválido'}), 400
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({'error': 'Error interno'}), 500

if __name__ == '__main__':
    app.run(debug=True)