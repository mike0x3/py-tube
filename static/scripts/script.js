function toFeatures(){
	var el = document.getElementById("toFeatures");
	el.scrollIntoView(); 
}

function toTutorial(){
	var tut = document.getElementById("toTutorial");
	tut.scrollIntoView();
}

//adaptive mobile header
function mobileNavbar() {
	var el = document.getElementById("header-right");
	if (el.style.display === "flex") {
    el.classList.toggle("mobile-visible");
    } else {
    el.classList.toggle("mobile-visible");
    el.style.animation = "animatenavbar 0.3s";
    }
}

function toTop() {
	window.scrollTo(0,0);
}

function navbarAnimation(x) {
		x.classList.toggle("change");
}