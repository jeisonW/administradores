  window.addEventListener('load', function() {
    var menu_btn = document.querySelector("#menu-btn");
    var sidebar = document.querySelector("#sidebar");
    var container = document.querySelector(".my-container");
    
    //esto es para que no cree conflicto si no encuentra el nombre de los contenedores
    if (menu_btn && sidebar && container) {
      menu_btn.addEventListener("click", function() {
        sidebar.classList.toggle("active-nav");
        container.classList.toggle("active-cont");
      });
  
      // Activar el menú al cargar la página
      sidebar.classList.add("active-nav");
      container.classList.add("active-cont");
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