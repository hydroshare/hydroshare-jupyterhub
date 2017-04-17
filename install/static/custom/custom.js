
$(document).ready(function(){
    // put username in notebook header
    var header = $("#header-container")[0];
    var username = document.URL.split('/')[4];
    var div = document.createElement("div");
    div.style.color = "#0da3d4";
    div.innerHTML = "Welcome "+username;
    div .style.margin = "6px 4px 5px 2px";
    div.className = "pull-right"
    header.appendChild(div);
});
