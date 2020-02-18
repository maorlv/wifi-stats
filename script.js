/*
|   Maor Levy
|   @ https://github.com/redspade91
|   2020
*/

function colorize(best_gate, worst_gate, value, container) {
    container.setAttribute("val", (value > best_gate) ? "best" : (value > worst_gate) ? "OK" : "worst");
}

function toggleNightMode() {
    next_mode = (document.querySelector("html").getAttribute("ngmode") == "false") ? "true" : "false";
    localStorage.setItem("ng_mode", next_mode);
    document.querySelector("html").setAttribute("ngmode", next_mode);
}

// set up night mode control
ng_mode = localStorage.getItem("ng_mode");
ng_mode = (ng_mode == null) ? "true" : ng_mode;

ng_button = document.getElementById("night_mode");
ng_button.checked = true;

if (ng_mode == "false") {
    toggleNightMode();
    ng_button.checked = false;
}

ng_button.addEventListener("change", ()=>{
    toggleNightMode()
});

// get info and change colors
var containers = document.querySelectorAll(".det span");
setInterval(function(){
    fetch("./stats.txt")
    .then(txt=>txt.text())
    .then(txt => {
        let values = txt.split(",");

        containers[1].textContent = values[2] + "%";
        colorize(50, 35, parseInt(values[2]), containers[1]);

        containers[2].textContent = values[1] + " Mbps";
        colorize(50, 20, parseFloat(values[1]), containers[2]);

        containers[0].textContent = values[0];
    });
}, 500);