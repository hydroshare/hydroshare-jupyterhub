
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

    // add page footer
    var foot = document.createElement('div');
    foot.id = 'footer';
    foot.style.height = '110px';
  
    var left = document.createElement('div');
    left.id = "footer-left";
    left.className = 'centering';
    
    var center = document.createElement('div');
    center.id = "footer-center";
    center.className = 'centering';
    
    var right = document.createElement('div');
    right.id = "footer-right";
    right.className = 'centering';
    
    var par = document.createElement("p");
    par.className = 'footerpar';
    par.innerHTML = 'HydroShare-JupyterHub Version 1.2';
    par.style.valign='middle';
    right.appendChild(par);
  
    var par = document.createElement("p");
    par.className = 'footerpar';
    par.innerHTML = 'Find us on <a href="https://github.com/hydroshare/hydroshare-jupyterhub" target="_blank">Github</a> ';
    right.appendChild(par);
    
    var par = document.createElement("p");
    par.className = "footerpar";
    par.innerHTML = 'Contact us at <a href="mailto:help@cuahsi.org?Subject=JupyterHub">help.cuahsi.org</a>';
    right.appendChild(par);
    
    var img = document.createElement('img');
    img.className = 'footerimg';
    img.src = 'https://www.cuahsi.org/assets/images/logo.png';
    img.style.width = "50%";
    left.appendChild(img);
  
    var nimg = document.createElement('img');
    img.className = 'footerimg';
    nimg.src = 'http://grid.ncsa.illinois.edu/ncsalogo_sm.gif';
    nimg.style.width = "15%";
    left.appendChild(nimg);
    
    foot.appendChild(left);
    foot.appendChild(center);
    foot.appendChild(right);
    
    // insert the footer at the bottom of the page 
    document.getElementById('notebook_panel').appendChild(foot);

});
