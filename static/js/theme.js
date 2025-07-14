function applyTheme(mode) {
    const modeIcon = document.querySelector('.modeIcon');
    const macroIcon = document.querySelectorAll('.macroButton i');
    const macroButton = document.querySelectorAll('.macroButton');

    if (mode === 'moon') {
        if (modeIcon) {
            modeIcon.classList.remove('fa-regular', 'fa-sun');
            modeIcon.classList.add('fa-solid', 'fa-moon');
        }
        document.body.style.backgroundColor = '#f4f4f5';
        document.body.style.color = '#09090b';
        macroButton.forEach((button, key) => {
            if (macroIcon[key]) {
                macroIcon[key].style.color = '#09090b';
                macroButton[key].style.borderColor = '#09090b';
            }
        });
    } else {
        if (modeIcon) {
            modeIcon.classList.remove('fa-solid', 'fa-moon');
            modeIcon.classList.add('fa-regular', 'fa-sun');
        }
        document.body.style.backgroundColor = '#09090b';
        document.body.style.color = '#f4f4f5';
        macroButton.forEach((button, key) => {
            if (macroIcon[key]) {
                macroIcon[key].style.color = '#f4f4f5';
                macroButton[key].style.borderColor = '#f4f4f5';
            }
        });
    }
}

function changeMode() {
    const current = localStorage.getItem('themeMode') || 'sun';
    const next = current === 'sun' ? 'moon' : 'sun';
    localStorage.setItem('themeMode', next);
    applyTheme(next);
}

// Apply the saved theme immediately after DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const savedMode = localStorage.getItem('themeMode') || 'sun';
    applyTheme(savedMode);
});
