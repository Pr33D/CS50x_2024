import { themeLoad, themeChange } from "./theme.js";


window.onload = () => {
    // initial load

    themeLoad();
}

// themebutton -> change theme
document.querySelector("#themebtn").addEventListener("click", () => { themeChange(); });


// contact form
document.addEventListener('DOMContentLoaded', () => {

document.querySelector('#contactform').addEventListener('submit', (e) => {
    e.preventDefault();

    let name = document.querySelector('#name');
    let email = document.querySelector('#mail');
    let message = document.querySelector('#message');
    alert('Thanks for your interest, ' + name.value + ' (' + email.value + ')\nYour mail was not sent, because we have no script for that.' + '\nYour message was:\n' + message.value);
});
});