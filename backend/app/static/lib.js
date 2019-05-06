function ajax(url, data) {
	contentbox.innerHTML = "";
	var loading = document.createElement("img");
	loading.width = 50;
	loading.src = "static/gear.gif";
	contentbox.appendChild(loading);
	var req = new XMLHttpRequest();
	req.open("post", url, true);
	req.onreadystatechange = function() {
		try {
			contentbox.innerHTML = this.responseText;
		}
		catch (e) {
			contentbox.innerHTML = "error:" + e.toString();
		}
	};
	req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
	req.send(data);
}
