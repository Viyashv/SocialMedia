// Bootstrap validation starter script
(() => {
  "use strict";

  // Fetch all the forms we want to apply custom Bootstrap validation to
  const forms = document.querySelectorAll(".needs-validation");

  // Loop over them and prevent submission if invalid
  Array.from(forms).forEach((form) => {
    form.addEventListener(
      "submit",
      (event) => {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }

        form.classList.add("was-validated");
      },
      false
    );
  });
})();

// Hide Show Password below
const togglePassword = document.getElementById("togglePassword");
const passwordField = document.getElementById("pass1");
const toggleIcon = document.getElementById("toggleIcon");

togglePassword.addEventListener("click", function () {
  // Toggle input type
  const type =
    passwordField.getAttribute("type") === "password" ? "text" : "password";
  passwordField.setAttribute("type", type);

  // Toggle icon class
  toggleIcon.classList.toggle("bi-eye");
  toggleIcon.classList.toggle("bi-eye-slash");
});
// Hide Show Password End

const toastElList = document.querySelectorAll(".toast");
const toastList = [...toastElList].map(
  (toastEl) => new bootstrap.Toast(toastEl, option)
);

// Toggle the "collapsed" class on the sidebar when clicking the button
// Manual toggle button for demo purposes; toggles sidebar collapsed state.
function sideBar() {
  document.getElementById("sidebar").classList.toggle("collapsed");
};

// Function to check if the sidebar's content overflows the visible area.
function checkSidebarOverflow() {
  const sidebar = document.getElementById("sidebar");

  // Calculate whether the inner content overflows vertically.
  if (sidebar.scrollHeight > sidebar.clientHeight) {
    // If it overflows, ensure that the sidebar is in its collapsed state.
    sidebar.classList.add("collapsed");
  } else {
    // Otherwise, you can optionally remove the collapsed state.
    // If you want auto expand when content fits, uncomment the next line.
    sidebar.classList.remove('collapsed');
  }
}

// Run overflow check on window resize and initial load.
window.addEventListener("resize", checkSidebarOverflow);
window.addEventListener("load", checkSidebarOverflow);
