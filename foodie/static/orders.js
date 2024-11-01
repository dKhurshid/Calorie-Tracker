document.getElementById('theme-toggle').addEventListener('click', function() {
    document.body.classList.toggle('dark-mode');
    var icon = this.querySelector('.material-symbols-outlined');
    if (document.body.classList.contains('dark-mode')) {
        icon.textContent = 'dark_mode';
    } else {
        icon.textContent = 'light_mode';
    }
});
