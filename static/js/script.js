
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

/*DROPDOWN MENU*/
document.addEventListener('DOMContentLoaded', function () {
    const dropdownButton = document.getElementById('dropdown_button');
    const dropdownMenu = document.getElementById('dropdown_menu');
    const dropdownIcon = document.getElementById('dropdown_icon');
    const dropdownItems = document.querySelectorAll('.dropdown_item');
    const dropdownText = dropdownButton.querySelector('span');

    dropdownButton.addEventListener('click', function () {
        // Alterna o menu dropdown
        dropdownMenu.classList.toggle('hidden');

        // Alterna a rotação do ícone
        const isOpen = !dropdownMenu.classList.contains('hidden');
        dropdownIcon.style.transform = isOpen ? 'rotate(180deg)' : 'rotate(0deg)';
    });

    dropdownItems.forEach(item => {
        item.addEventListener('click', function () {
            // Atualiza o texto do botão com a opção selecionada
            dropdownText.textContent = this.textContent;

            // Fecha o menu dropdown
            dropdownMenu.classList.add('hidden');
            dropdownIcon.style.transform = 'rotate(0deg)';
        });
    });

    // Fecha o menu ao clicar fora
    document.addEventListener('click', function (event) {
        if (!dropdownButton.contains(event.target) && !dropdownMenu.contains(event.target)) {
            dropdownMenu.classList.add('hidden');
            dropdownIcon.style.transform = 'rotate(0deg)';
        }
    });
});
