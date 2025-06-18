// Accede a React, ReactDOM, Axios desde las variables globales
const { useState } = React;
const ReactDOM = window.ReactDOM;
const axios = window.axios;

// Accede a DatePicker desde la variable global de react-datepicker
const DatePicker = window.ReactDatePicker ? window.ReactDatePicker.default : null;

const Booking = () => {
  const [date, setDate] = useState(new Date());
  const [service, setService] = useState('');
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Submitting booking:', { date, service, email });
    axios.post('http://localhost:5000/api/booking', { date, service, email })
      .then(response => setMessage('Reserva confirmada!'))
      .catch(error => setMessage('Error al realizar la reserva'));
  };

  return (
    React.createElement('div', { className: 'booking' },
      React.createElement('h1', null, 'Reservar Servicio'),
      React.createElement('form', { onSubmit: handleSubmit },
        React.createElement('label', null,
          'Fecha:',
          DatePicker ? React.createElement(DatePicker, { selected: date, onChange: setDate }) : React.createElement('input', { type: 'date', value: date.toISOString().split('T')[0], onChange: e => setDate(new Date(e.target.value)) })
        ),
        React.createElement('label', null,
          'Servicio:',
          React.createElement('select', { value: service, onChange: e => setService(e.target.value) },
            React.createElement('option', { value: '' }, 'Seleccionar'),
            React.createElement('option', { value: 'corte' }, 'Corte de Pelo'),
            React.createElement('option', { value: 'entrenamiento' }, 'Entrenamiento Personal')
          )
        ),
        React.createElement('label', null,
          'Email:',
          React.createElement('input', { type: 'email', value: email, onChange: e => setEmail(e.target.value), required: true })
        ),
        React.createElement('button', { type: 'submit' }, 'Reservar')
      ),
      message && React.createElement('p', null, message)
    )
  );
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(React.createElement(Booking));