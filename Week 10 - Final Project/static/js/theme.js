export function themeLoad() {
    // load theme from local storage

    if(!localStorage.getItem("theme"))
    {
        localStorage.setItem("theme", "light");
        document.querySelector("html").setAttribute("data-bs-theme", "light");
        document.querySelector("#themebtn").innerHTML = "Dark";
    } else {
        document.querySelector("html").setAttribute("data-bs-theme", localStorage.getItem("theme"));
        switch(localStorage.getItem("theme")) {
            case "dark":
                document.querySelector("#themebtn").innerHTML = "Light";
                break;
            case "light":
                document.querySelector("#themebtn").innerHTML = "Dark";
                break;
        }
    }
}


export function themeChange() {
        // Change Theme on Click

        if (localStorage.getItem("theme") === "light") {
            localStorage.setItem("theme", "dark");
        } 
        else if (localStorage.getItem("theme") === "dark") {
            localStorage.setItem("theme", "light");
        }
    themeLoad();
}