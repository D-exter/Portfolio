function showMedia(selected) {
	document.getElementById("main-video").style.display = "none";
	document.getElementById("main-img-0").style.display = "none";
	document.getElementById("main-img-1").style.display = "none";
	document.getElementById("main-img-2").style.display = "none";
	document.getElementById("main-img-3").style.display = "none";

	document.getElementById("thumb-video").style.borderColor = "#285A48";
	document.getElementById("thumb-0").style.borderColor = "#285A48";
	document.getElementById("thumb-1").style.borderColor = "#285A48";
	document.getElementById("thumb-2").style.borderColor = "#285A48";
	document.getElementById("thumb-3").style.borderColor = "#285A48";

	if (selected === "video") {
		document.getElementById("main-video").style.display = "block";
		document.getElementById("thumb-video").style.borderColor = "#B0E4CC";
	} else {
		document.getElementById("main-img-" + selected).style.display = "block";
		document.getElementById("thumb-" + selected).style.borderColor = "#B0E4CC";
	}
}