window.onload = () => {
    document.querySelectorAll('form').forEach(form => form.reset());
}

let currentMode = 'sun';

function changeMode() {
    const macroIcon = document.querySelectorAll('.macroButton i');
    const macroButton = document.querySelectorAll('.macroButton')
    const modeIcon = document.querySelector('.modeIcon')
    
    if (currentMode === 'sun') {
        modeIcon.classList.remove('fa-regular', 'fa-sun');
        modeIcon.classList.add('fa-solid', 'fa-moon');
        document.body.style.backgroundColor = '#f4f4f5'
        document.body.style.color = '#09090b'
        macroButton.forEach((button,key) => {
            macroIcon[key].style.color = '#09090b'
            macroButton[key].style.borderColor = '#09090b'
        })
        currentMode = 'moon';
    } else {
        modeIcon.classList.remove('fa-solid', 'fa-moon');
        modeIcon.classList.add('fa-regular', 'fa-sun');
        document.body.style.backgroundColor = '#09090b'
        document.body.style.color = '#f4f4f5'
        macroButton.forEach((button,key) => {
            macroIcon[key].style.color = '#f4f4f5'
            macroButton[key].style.borderColor = '#f4f4f5'
        })
        currentMode = 'sun';
    }
}