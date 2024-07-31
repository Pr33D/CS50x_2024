// additional theme functions
// theme load + themebutton text functions are direct @layout!

export function themeChange() {
        // Change Theme on Click

        if (localStorage.getItem("theme") === "light") {
            localStorage.setItem("theme", "dark");
            document.querySelector("#themebtn").innerHTML = "Switch to Light";
        } 
        else if (localStorage.getItem("theme") === "dark") {
            localStorage.setItem("theme", "light");
            document.querySelector("#themebtn").innerHTML = "Switch to Dark";
        }

        document.querySelector("html").setAttribute("data-bs-theme", localStorage.getItem("theme"));
}