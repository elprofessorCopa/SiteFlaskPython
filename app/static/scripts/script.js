const body = document.querySelector("body"),
  sidebar = body.querySelector("nav"),
  toggle = body.querySelector(".toggle"),
  searchBtn = body.querySelector(".search-box"),
  modeSwitch = body.querySelector(".toggle-switch"),
  modeText = body.querySelector(".mode-text");

toggle.addEventListener("click", () => {
  sidebar.classList.toggle("close");
});

searchBtn.addEventListener("click", () => {
  sidebar.classList.remove("close");
});

modeSwitch.addEventListener("click", () => {
  body.classList.toggle("dark");

  if (body.classList.contains("dark")) {
    modeText.innerText = "Light mode";
  } else {
    modeText.innerText = "Dark mode";
  }
});


// Get the elements from the document
const optionsButton = document.getElementById("optionsButton");
const taskOptions = document.getElementById("taskOptions");

// Add an event listener to the options button
optionsButton.addEventListener("contextmenu", function(e) {
  // Prevent the default context menu from showing
  e.preventDefault();
  // Show the task-options list
  taskOptions.style.display = "block";
  // Position the task-options list at the mouse coordinates
  taskOptions.style.left = e.pageX + "px";
  taskOptions.style.top = e.pageY + "px";
});

// Add an event listener to the document
document.addEventListener("click", function(e) {
  // Hide the task-options list if the user clicks anywhere else
  if (e.target !== optionsButton && e.target !== taskOptions) {
    taskOptions.style.display = "none";
  }
});

// Add event listeners to the task-options items
taskOptions.addEventListener("click", function(e) {
  // Get the clicked element
  const target = e.target;
  // Check if the clicked element is a link
  if (target.tagName === "A") {
    // Get the icon element
    const icon = target.querySelector("i");
    // Get the icon class
    const iconClass = icon.className;
    // Perform different actions based on the icon class
    switch (iconClass) {
      case "bx bx-edit":
        // Edit the task
        alert("Edit the task");
        break;
      case "bx bx-trash":
        // Delete the task
        alert("Delete the task");
        break;
      case "bx bx-star":
        // Mark the task as favorite
        alert("Mark the task as favorite");
        break;
    }
    // Hide the task-options list
    taskOptions.style.display = "none";
  }
});



// my js
// Fonction pour afficher la boîte de dialogue ou le formulaire modal
function showConfirmationModal(billetId) {
  // Récupérer l'ID de l'utilisateur à partir du backend
  getUserIdFromBackend()
      .then(userId => {
          if (userId) {
              // Afficher la boîte de dialogue ou le formulaire modal
              const modal = document.getElementById("reservationModal");
              modal.style.display = "block";

              // Ajouter un événement au bouton de confirmation dans le modal
              const confirmButton = modal.querySelector("button");
              confirmButton.onclick = function() {
                  // Appeler la fonction pour confirmer la réservation avec l'ID du billet
                  confirmReservation(userId, billetId);
              };
          } else {
              // Rediriger l'utilisateur vers la page de connexion s'il n'est pas connecté
              window.location.href = '/connect';
          }
      })
      .catch(error => {
          console.error('Error:', error);
      });
}

// Fonction pour fermer le modal
function closeModal() {
  const modal = document.getElementById("reservationModal");
  modal.style.display = "none";
}

// Ajouter des gestionnaires d'événements aux boutons "Book Now"
const bookButtons = document.querySelectorAll(".btn-book");
bookButtons.forEach(button => {
  button.addEventListener("click", function() {
    // Récupérer l'ID du billet à partir de l'attribut de données
    const billetId = button.getAttribute("data-billet-id");
    // Afficher le modal de confirmation avec l'ID du billet
    showConfirmationModal(billetId);
  });
});

// Fonction pour récupérer l'ID de l'utilisateur à partir du backend
function getUserIdFromBackend() {
  return fetch('/get_user_id')
          .then(response => response.json())
          .then(data => {
              return data.user_id; // Retourner l'ID de l'utilisateur
          })
          .catch(error => {
              console.error('Error:', error);
          });
}
