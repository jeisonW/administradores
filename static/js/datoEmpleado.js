$(document).ready(function() {
    
    $('.editar-empleado').click(function() {
        var id = $(this).data('idempleado');
        var nombre = $(this).data('nombreempleado');
        var correo = $(this).data('correo');
        var telefono = $(this).data('telefono'); 
        var direc = $(this).data('dirreccion');
        var salario = $(this).data('salario'); 
      
         // Llenar los campos de la ventana modal con los datos del empleado
        $('#IDempleado').val(id);
        $('#NombreEmpleado').val(nombre);
        $('#Correo').val(correo);
        $('#Telefono').val(telefono);
        $('#Dirreccion').val(direc);
        $('#salario').val(salario);

      // Mostrar la ventana modal
      $('#editarModal').modal('show');
    });

    $('.ocultar').click(function() {
        $('#editarModal').modal('hide');
      });
    
});
