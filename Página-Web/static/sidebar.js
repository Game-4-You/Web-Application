window.onload = function () {
    var sidebarToggleOff = document.getElementById('sidebarToggleOff');
    var sidebarToggleOn = document.getElementById('sidebarToggleOn');
    var sidebar = document.getElementById('Sidebar');
    var logoutButton = document.getElementById('Logout');

    logoutButton.addEventListener('click', function () {
        window.location.href = logoutUrl;
    });

    if (sidebarToggleOff && sidebarToggleOn && sidebar) {
        sidebarToggleOn.addEventListener('click', function () {
            console.log('El botón sidebarToggleOn ha sido presionado.');
            sidebar.style.display = 'flex';
        });

        sidebarToggleOff.addEventListener('click', function () {
            console.log('El botón sidebarToggleOff ha sido presionado.');
            sidebar.style.display = 'none';
        });

        var sidebarButtons = sidebar.getElementsByTagName('button');
        for (var i = 0; i < sidebarButtons.length; i++) {
            sidebarButtons[i].addEventListener('click', function () {
                console.log('El botón ' + this.innerText + ' ha sido presionado.');
                switch (this.id) {
                    case 'Inicio':
                        window.location.href = inicioUrl;
                        break;
                    case 'Explorar':
                        window.location.href = exploreUrl;
                        break;
                    case 'Suscripción':
                        window.location.href = SubscriptionUrl;
                        break;
                }
            });
        }
    } else {
        console.log('Something went wrong: Exception at sidebar.js onload function.');
    }
}