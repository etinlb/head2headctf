function setAvatar() {
	var img = document.getElementById(this.value + "_hero");
	var choice = document.getElementById(choice.options[choice.selectedIndex].text + "_hero");
	for (i = 0; i < choice.options.length; i++) {
		var hero_img = document.getElementById(choice.options[choice.selectedIndex].text + "_hero");
		hero_img.style.display = "none";
	}
	img.style.display = "block";
	return false;
}

window.onload = function() {
	var img = document.getElementById("image");
	var choice = document.getElementById("avatar_id")
	var default_img = document.getElementById(choice.options[choice.selectedIndex].text + "_hero");
	default_img.style.display = "block";
	choice.onchange = setAvatar;
}
