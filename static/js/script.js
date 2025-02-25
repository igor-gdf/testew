
/*Eye Closed*/
document.addEventListener('DOMContentLoaded', function () {
    const togglePassword = document.querySelector('.toggle_password');
    const passwordInput = document.querySelector('#senha');
    const passwordIcon = document.querySelector('.password_icon');


    const eyeIcon = togglePassword.getAttribute('data-eye');
    const eyeSlashIcon = togglePassword.getAttribute('data-eye-slash');

    let isPasswordVisible = false; 

    togglePassword.addEventListener('click', function () {

        const type = passwordInput.type === 'password' ? 'text' : 'password';
        passwordInput.type = type;

        isPasswordVisible = !isPasswordVisible;

        passwordIcon.setAttribute('src', isPasswordVisible ? eyeSlashIcon : eyeIcon);

        passwordIcon.setAttribute('alt', isPasswordVisible ? 'Ocultar senha' : 'Mostrar senha');
    });
});

/* time out for flash messages tlgd */
setTimeout(function () {
    let flashMessages = document.querySelector('.flash-messages');
    if (flashMessages) {
        flashMessages.style.transition = "opacity 0.5s";
        flashMessages.style.opacity = "0";
        setTimeout(() => flashMessages.remove(), 500);
    }
}, 5000);

