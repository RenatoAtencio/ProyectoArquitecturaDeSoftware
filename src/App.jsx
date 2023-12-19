import React from 'react';

function App() {
  const startBuscaminas = () => {
    fetch('http://localhost:5000/start_buscaminas')
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.error('Error:', error));
  };

  return (
    <div>
      <h1>Buscaminas</h1>
      <button onClick={startBuscaminas}>Comenzar Juego</button>
    </div>
  );
}

export default App;
