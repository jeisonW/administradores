var ctxProveedor = document.getElementById('proveedores').getContext('2d');
var miGraficoProveedor = new Chart(ctxProveedor, {
  type: 'bar', // Tipo de gráfico bar
  data: {
    labels: [],
    datasets: [
      {
        label: 'Cantidad de Productos',
        data: [],
        backgroundColor: 'rgba(180, 180, 180,1)',
        borderColor: 'rgba(180, 180, 180, 1)',
        borderWidth: 1
      }
    ]
  },
  options: {
    responsive: true,
    scales: {
      x: {
        beginAtZero: true
      },
      y: {
        ticks: {
          autoSkip: false,
          maxRotation: 45,
          minRotation: 45
        }
      }
    }
  }
});

// Función para obtener los datos de proveedores y actualizar el gráfico
function actualizarDatosProveedor() {
  axios.get('/dataP')
    .then(function (response) {
      // Actualiza los datos del gráfico con los datos obtenidos
      miGraficoProveedor.data.labels = response.data.labels;
      miGraficoProveedor.data.datasets[0].data = response.data.data.map(Number); // Convierte los datos a números si es necesario
      miGraficoProveedor.update();
    })
    .catch(function (error) {
      console.log(error);
    });
}

// Llama a la función para actualizar los datos de proveedores al cargar la página
actualizarDatosProveedor();
