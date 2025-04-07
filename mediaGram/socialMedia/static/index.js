    // Bootstrap validation starter script
    (() => {
        'use strict'

        // Fetch all the forms we want to apply custom Bootstrap validation to
        const forms = document.querySelectorAll('.needs-validation')

        // Loop over them and prevent submission if invalid
        Array.from(forms).forEach(form => {
            form.addEventListener('submit', event => {
                if (!form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                }

                form.classList.add('was-validated')
            }, false)
        })
    })()



const togglePassword = document.getElementById('togglePassword');
const passwordField = document.getElementById('pass1');
const toggleIcon = document.getElementById('toggleIcon');

togglePassword.addEventListener('click', function () {
// Toggle input type
const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
passwordField.setAttribute('type', type);

// Toggle icon class
toggleIcon.classList.toggle('bi-eye');
toggleIcon.classList.toggle('bi-eye-slash');
});

const toastElList = document.querySelectorAll('.toast')
const toastList = [...toastElList].map(toastEl => new bootstrap.Toast(toastEl, option))