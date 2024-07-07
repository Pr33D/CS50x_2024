window.onload = () => {
    // initial load

    themeLoad();
}

function themeLoad() {
    // load theme from local storage

    if(!localStorage.getItem("theme"))
    {
        localStorage.setItem("theme", "light");
        document.querySelector("html").setAttribute("data-bs-theme", "light");
    } else {
        document.querySelector("html").setAttribute("data-bs-theme", localStorage.getItem("theme"));
    }

    return ;
}


document.querySelector("#themebtn").addEventListener("click", () => {
    if (localStorage.getItem("theme") === "light") {
        localStorage.setItem("theme", "dark");
    } else if (localStorage.getItem("theme") === "dark") {
        localStorage.setItem("theme", "light");
}
themeLoad();
return ;
});