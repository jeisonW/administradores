document.addEventListener("DOMContentLoaded", function() {
    setTimeout(function() {
      var alerta1 = document.getElementById("alerta1");
      if (alerta1) {
        alerta1.remove();
      }
    }, 3000);
});

  function filterDropdown() {
    var input, filter, ul, li, i;
    input = document.getElementById("searchInput1");
    filter = input.value.toUpperCase();
    ul = document.querySelector(".tres");
    li = ul.getElementsByTagName("li");

    for (i = 1; i < li.length; i++) { // Comenzamos desde 1 para omitir el primer elemento (campo de búsqueda)
        var cardTitle = li[i].querySelector(".card-title");
        var cardText = li[i].querySelector(".card-text");
        var searchText = cardTitle.innerText + " " + cardText.innerText;
        
        if (searchText.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}

  function obtenerDatos(id) {
        // Obtener el elemento del desplegable basado en el ID
        var elemento = document.getElementById(id);
        // Eliminar el producto previamente seleccionado, si existe
        var datosSeleccionadosList = document.getElementById("datosSeleccionadosList");
        var productosSeleccionados = datosSeleccionadosList.getElementsByClassName("producto-seleccionado");
        if (productosSeleccionados.length > 0) {
            productosSeleccionados[0].remove();
        }

        // Obtener los datos correspondientes al elemento seleccionado
        var foto = elemento.querySelector('.foto img').src;
        var codigoProducto = elemento.querySelector('.card-title').innerText;
        var nombreProducto = elemento.querySelector('.card-text').innerText;
        var cantidad = elemento.querySelector('.card-texts').innerText;

        

        // Crear un nuevo elemento <div> con la misma estructura y agregar los datos
        var nuevoElemento = document.createElement('div');
        nuevoElemento.classList.add('card', 'mb-3', 'nombreMarca', 'producto-seleccionado');
        nuevoElemento.style.maxWidth = '540px';
        nuevoElemento.innerHTML = `
            <div class="row g-0">
                <div class="col-md-4">
                    <img src="${foto}" class="img-fluid rounded-start" alt="...">
                </div>
                <div class="col-md-8">
                    <div class="card-body">
                        <input type="hidden" name="codigo" value="${id}" id="codigoproducto">

                        <h5 class="card-title">${codigoProducto}</h5>
                        <p class="card-text">${nombreProducto}</p>
                        <p class="card-texts">${cantidad}</p>

                    </div>
                </div>
            </div>
        `;

        // Agregar el nuevo elemento al contenedor de datos seleccionados
        datosSeleccionadosList.appendChild(nuevoElemento);
    
    }




function fecha(){
  var fechaInput = document.getElementById('FechaSalida').value;
 
    
    var partesFecha = fechaInput.split('-');
    
    if (partesFecha.length === 3) {
      var anio = parseInt(partesFecha[0], 10);
      var mes = parseInt(partesFecha[1], 10) - 1; // Restamos 1 porque los meses comienzan en 0
      var dia = parseInt(partesFecha[2], 10);
    
      var fechaActual = new Date();
      var fechaSeleccionadaObj = new Date(anio, mes, dia);
    
      if (fechaSeleccionadaObj > fechaActual) {
        document.getElementById('FechaSalida').style.borderColor = "red";
        document.getElementById('message_fecha').textContent = 'fecha invalida';
        setTimeout(color , 2000)
      
      }
      else
      {
        document.getElementById('FechaSalida').style.borderColor = "";
        document.getElementById('message_fecha').textContent = '';

      }
    } 
    else 
    {
      alert('Formato de fecha no válido.');
    }

}


function fecha2(){
  var fecha_add = document.getElementById('add_fecha').value;

  console.log(fecha_add);
  if (fecha_add )
  {

  var partes = fecha_add.split('-');

  if (partes.length === 3) {
    var anio = parseInt(partes[0], 10);
    var mes = parseInt(partes[1], 10) - 1; // Restamos 1 porque los meses comienzan en 0
    var dia = parseInt(partes[2], 10);

    var fechaActual = new Date();
    var fechaSeleccionadaObj = new Date(anio, mes, dia);

    if (fechaSeleccionadaObj > fechaActual) {
      document.getElementById('add_fecha').style.borderColor = "red";
      document.getElementById('messagefecha').textContent = 'fecha invalida';
      setTimeout(color2 , 2000)
     
    }
    else
    {
      document.getElementById('add_fecha').style.borderColor = "";
      document.getElementById('messagefecha').textContent = '';

    }

  }
  else 
  {
    alert('Formato de fecha no válido.');
  }

}

}


function color(){
  var hiddenfecha = document.getElementById('hiddenfecha').value;
  document.getElementById('FechaSalida').style.borderColor = "";
  document.getElementById('message_fecha').textContent = '';
  document.getElementById('FechaSalida').value = hiddenfecha;

}
function color2(){
  document.getElementById('add_fecha').style.borderColor = "";
  document.getElementById('messagefecha').textContent = '';
  document.getElementById('add_fecha').value = '';
}


