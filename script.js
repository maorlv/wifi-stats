/*
|   Maor Levy
|   @ https://github.com/redspade91
|   2020
*/

function fill(best_gate, worst_gate, value, container) {
    container.parentNode.setAttribute("val", (value > best_gate) ? "best" : (value > worst_gate) ? "ok" : "worst");
    container.textContent = value;
}

function toggleNightMode(next_mode) {
    localStorage.setItem("ng_mode", next_mode);
    document.querySelector("html").setAttribute("ngmode", next_mode);
}

// set up night mode control
ng_mode = localStorage.getItem("ng_mode");
ng_mode = (ng_mode == null) ? document.querySelector("html").getAttribute("ngmode") : ng_mode;

ng_button = document.getElementById("night_mode");
ng_button.checked = (ng_mode == "true") ? true : false;
toggleNightMode(ng_button.checked);

ng_button.addEventListener("change", ()=>{
    toggleNightMode(ng_button.checked);
});


// get info and change colors
var containers = document.querySelectorAll(".det span");
setInterval(()=>{
    fetch("./stats.txt")
    .then(txt=>txt.text())
    .then(txt => {
        let values = txt.split(",");

        // reception
        fill(50, 35, parseInt(values[2]), containers[1]);

        // speed
        fill(50, 20, parseFloat(values[1]), containers[2]);

        // ssid
        containers[0].textContent = values[0];
    })
    .catch(()=>{
        for (container of containers)
            container.textContent = "- - ";
    });
}, 500);