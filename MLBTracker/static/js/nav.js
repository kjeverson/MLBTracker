function updateNav(page) {
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.classList.remove("active")

        if(link.pathname == page) {
            link.classList.add("active");
        }
    });


}