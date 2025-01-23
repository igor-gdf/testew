
/*Eye Closed*/ 
document.addEventListener('DOMContentLoaded', function() {
    const togglePassword = document.querySelector('.toggle_password');
    const passwordInput = document.querySelector('#senha');   
    const passwordIcon = document.querySelector('.password_icon');

    // Obtenha os caminhos das imagens a partir dos atributos data-
    const eyeIcon = togglePassword.getAttribute('data-eye');
    const eyeSlashIcon = togglePassword.getAttribute('data-eye-slash');

    let isPasswordVisible = false; // Inicializa a variável

    togglePassword.addEventListener('click', function() {
        
        const type = passwordInput.type === 'password' ? 'text' : 'password';
        passwordInput.type = type;
        
        isPasswordVisible = !isPasswordVisible;
       
        passwordIcon.setAttribute('src', isPasswordVisible ? eyeSlashIcon : eyeIcon);

        passwordIcon.setAttribute('alt', isPasswordVisible ? 'Ocultar senha' : 'Mostrar senha');
    });
});

