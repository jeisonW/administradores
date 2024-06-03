window.addEventListener('load', function() {
  var menu_btn = document.querySelector("#menu-btn");
  var sidebar = document.querySelector("#sidebar");
  var container = document.querySelector(".my-container");
  
  // Verificar si los elementos existen
  if (menu_btn && sidebar && container) {
    menu_btn.addEventListener("click", function() {
      sidebar.classList.toggle("active-nav");
      container.classList.toggle("active-nav");
    });
  }
});


/*colorea si se le dio click*/
window.addEventListener('DOMContentLoaded', function() {
  var currentLocation = window.location.href;

  var navLinks = document.querySelectorAll(".nav-link");

  navLinks.forEach(function(navLink) {
    if (navLink.href === currentLocation) {
      navLink.classList.add("active");
    }
  });
});


/*Hace que el icono de la flecha se cambie*/
function rotar(elemento) {
  var icono = elemento.querySelector('.icono');

  if (icono) {
    var liPrinItems = document.querySelectorAll('.liPrin');
    liPrinItems.forEach(function(item) {
      var itemIcono = item.querySelector('.icono');

      if (item === elemento) {
        // Si el elemento actual es el mismo que se hizo clic
        if (icono.classList.contains('fa-caret-right')) {
          // Si el icono está en posición hacia la derecha, cambiarlo hacia abajo
          icono.classList.remove('fa-caret-right');
          icono.classList.add('fa-caret-down');
        } else if (icono.classList.contains('fa-caret-down')) {
          // Si el icono está en posición hacia abajo, cambiarlo hacia la derecha
          icono.classList.remove('fa-caret-down');
          icono.classList.add('fa-caret-right');
        }
      } else if (itemIcono) {
        // Si el elemento actual no es el mismo que se hizo clic, asegurarse de que esté en posición hacia la derecha
        itemIcono.classList.remove('fa-caret-down');
        itemIcono.classList.add('fa-caret-right');
      }
    });
  }
}




/*


        function showDropdown(element) {
          if (element.classList.contains("show")) {
            return;
          }
          var dropdownMenu = element.querySelector(".dropdown-menu");
          element.classList.add("show");
          dropdownMenu.classList.add("show");
        }
        
        function hideDropdown(element) {
          var dropdownMenu = element.querySelector(".dropdown-menu");
          element.classList.remove("show");
          dropdownMenu.classList.remove("show");
        }
        
        document.addEventListener("DOMContentLoaded", function() {
          var dropdown = document.querySelector(".dropdown");
          dropdown.addEventListener("mouseenter", function() {
            showDropdown(this);
          });
          dropdown.addEventListener("mouseleave", function() {
            hideDropdown(this);
          });
        });
*/