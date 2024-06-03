function mostrarDetalles(abastecimientoId) {
  // Realizar una solicitud al servidor para obtener los detalles del abastecimiento
  fetch('/verdetalles_productos/' + abastecimientoId)
      .then(response => response.json())
      .then(data => {

        var cuerpoTabla = document.querySelector('#detallesModal tbody');

      cuerpoTabla.innerHTML = '';

      // los detalles enviados de la funcion son estos,  estoy iterando sobre ellos
      data.forEach(function(detalle) {
          var fila = cuerpoTabla.insertRow();

          var celdas = ['Talla','ColorProducto','Stock' ]

          celdas.forEach(function(celda) {
              var td = fila.insertCell();
              td.innerHTML = detalle[celda];
          });
      })
      })
      .catch(error => console.error('Error al obtener detalles:', error));
}



$(document).ready(function() {
    
    $('.editar-producto').click(function() {
        var id = $(this).data('id');
        var nombre = $(this).data('nombre');
       
        var precio = $(this).data('precio'); 
        var imagen = $(this).data('imagen'); //predefinida

      
         // Llenar los campos de la ventana modal con los datos del producto
        $('#imagenProductos').attr('src', imagen);
        $('#nombreProducto').val(nombre);
       
        $('#idProducto').val(id);
        $('#precioProducto').val(precio);

      // Mostrar la ventana modal
      $('#editarModal').modal('show');
    });

    $('.ocultar').click(function() {
      $('#editarModal').modal('hide');
    });
    /* $('.guardar-cambios').click(function() {
     
      var id =  $('#idProducto').val();
      var nombre = $('#nombreProducto').val();
      var color = $('#colorProducto').val();
      var talla = $('#tallaProducto').val();
      var precio = $('#precioProducto').val();
      var imagen =  $('#imageninput')[0].files[0];

      var formData = new FormData();
      formData.append('id', id);
      formData.append('nombre', nombre);
      formData.append('color', color);
      formData.append('precio', precio);
      formData.append('talla', talla);
      formData.append('imagen', imagen);

      $.ajax({
        url: '/editproduct',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function(response) {
          // Manejar la respuesta del servidor si es necesario
          window.location.href = "http://127.0.0.1:5000/productos";
          //console.log(response);
        },
        
      });

      // Cerrar la ventana modal
      $('#editarModal').modal('hide');
    });
    */

    /*$('.buscar').click(function() {
      var textobuscar = $('#inputbuscar').val();
      var filtro = $('#dropdown').val();
    
      console.log(filtro);
      console.log(textobuscar);
    
      $.ajax({
        url: '/productos',
        type: 'POST',
        data: {
          textobuscar: textobuscar,
          filtro: filtro
        },
        success: function(response) {
          // Manejar la respuesta del servidor si es necesario
          console.log(response);

        },
        error: function(error) {
          // Manejar el error si ocurre
          console.error(error);
        }
      });

    });*/
    
});