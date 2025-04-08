const btn = document.getElementById("btn");
let passwordField1 = document.getElementById("pass2");
let toggleIcon1 = document.getElementById("toggleIcon1");

btn.addEventListener("click", function () {
//   console.log("satisfy");
    const type1 =
      passwordField1.getAttribute("type") === "password" ? "text" : "password";
    passwordField1.setAttribute("type", type1);

    // Toggle icon class
    toggleIcon1.classList.toggle("bi-eye");
    toggleIcon1.classList.toggle("bi-eye-slash");
});
// // Hide Show Password End