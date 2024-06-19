window.onload = function() {
    var sidebarToggleOff = document.getElementById('sidebarToggleOff');
    var sidebarToggleOn = document.getElementById('sidebarToggleOn');
    var sidebar = document.getElementById('Sidebar');

    if (sidebarToggleOff && sidebarToggleOn && sidebar) {
        sidebarToggleOn.addEventListener('click', function() {
            console.log('El botón sidebarToggleOn ha sido presionado.');
            sidebar.style.display = 'flex';
        });

        sidebarToggleOff.addEventListener('click', function() {
            console.log('El botón sidebarToggleOff ha sido presionado.');
            sidebar.style.display = 'none';
        });

        var sidebarButtons = sidebar.getElementsByTagName('button');
        for (var i = 0; i < sidebarButtons.length; i++) {
            sidebarButtons[i].addEventListener('click', function() {
                console.log('El botón ' + this.innerText + ' ha sido presionado.');
            });
        }
    } else {
        console.log('sidebarToggleOff, sidebarToggleOn or sidebar is null');
    }
}