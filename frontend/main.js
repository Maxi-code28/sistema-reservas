import React, { useState } from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';
import DatePicker from 'react-datepicker';
import './styles.css';

const Booking = () => {
  const [date, setDate] = useState(new Date());
  const [service, setService] = useState('');
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post('http://localhost:5000/api/booking', { date, service, email })
      .then(response => setMessage('Reserva confirmada!'))
      .catch(error => setMessage('Error al realizar la reserva'));
  };

  return (
    <div className="booking">
      <h1>Reservar Servicio</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Fecha:
          <DatePicker selected={date} onChange={date => setDate(date)} />
        </label>
        <label>
          Servicio:
          <select value={service} onChange={e => setService(e.target.value)}>
            <option value="">Seleccionar</option>
            <option value="corte">Corte de Pelo</option>
            <option value="entrenamiento">Entrenamiento Personal</option>
          </select>
        </label>
        <label>
          Email:
          <input type="email" value={email} onChange={e => setEmail(e.target.value)} required />
        </label>
        <button type="submit">Reservar</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

ReactDOM.render(<Booking />, document.getElementById('root'));