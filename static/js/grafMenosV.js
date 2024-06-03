var ctx = document.getElementById('main').getContext('2d');
var myChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: [],
    datasets: [
      {
        label: 'Cantidad de Salida',
        data: [],
        backgroundColor: 'rgba(54, 162, 235, 0.2)', // Cambia el color de fondo a azul
        borderColor: 'rgba(54, 162, 235, 1)', // Cambia el color del borde a azul
        borderWidth: 1
      }
    ]
  },
  options: {
    responsive: true,
    scales: {
      x: {
        ticks: {
          autoSkip: false,
          maxRotation: 45,
          minRotation: 45
        }
      },
      y: {
        beginAtZero: true
      }
    }
  }
});

// Función para actualizar los datos del gráfico de productos menos vendidos
function actualizarDatosMenosVendidos() {
  axios.get('/dataM')
    .then(function (response) {
      // Actualiza los datos del gráfico con los datos obtenidos
      myChart.data.labels = response.data.labels;
      myChart.data.datasets[0].data = response.data.data.map(Number); // Convierte los datos a números si es necesario
      myChart.update();
    })
    .catch(function (error) {
      console.log(error);
    });
}

// Realiza una solicitud HTTP para obtener los datos del servidor utilizando Axios
axios.get('/dataM')
  .then(response => {
    // Los datos se han recibido correctamente
    var data = response.data;

    // Actualiza los datos de la gráfica
    myChart.data.labels = data.labels;
    myChart.data.datasets[0].data = data.data;

    // Actualiza la gráfica
    myChart.update();

    // Llama a la función para actualizar los datos de los productos menos vendidos
    actualizarDatosMenosVendidos();
  })
  .catch(error => {
    console.log(error);
  });
