modal = {
	show: function(p) {
		function addStyles(el, styles) {
			for (var prop in styles) {
				el.style.setProperty(prop.replace(/([A-Z])/g, '-$1').toLowerCase(), styles[prop]);
			}
		}
		var outer = document.createElement("div");
		addStyles(outer, {
			display: "table",
			position: "fixed",
			width: "100%",
			height: "100%",
			minHeight: "100%",
			top: "0",
			left: "0",
			zIndex: "2048",
		});
		outer.id = "outermodaldialog";
		var inner = document.createElement("div");
		addStyles(inner, {
			display: "table-cell",
			verticalAlign: "middle",
			textAlign: "center",
			background: "rgba(0, 0, 0, .25)",
			transition: ".25s all ease",
			opacity: "0",
		});
		var box = document.createElement("div");
		addStyles(box, {
			display: "inline-block",
			color: "#000",
			background: "#fff",
			boxShadow: "slategrey 0 0 7px",
			padding: "25px",
			fontFamily: "Roboto, sans-serif",
			transform: "translate(0, 300px)",
			transition: ".25s all ease",
		});
		var title = document.createElement("div");
		addStyles(title, {
			color: "#000",
			fontFamily: "Ubuntu, sans-serif",
			fontWeight: "400",
			fontSize: "24px",
			marginBottom: "15px",
		});
		if (p && p.title) {
			title.innerHTML = p.title;
		} else {
			title.innerHTML = "Default";
		}
		var button = document.createElement("a");
		if (p && p.button) {
			button.innerHTML = p.button;
		} else {
			button.innerHTML = "Close";
		}
		addStyles(button, {
			display: "inline-block",
			color: "#000",
			background: "#fff",
			boxShadow: "slategrey 0 0 7px, slategrey 0 0 0 inset",
			transition: ".25s all ease",
			padding: "15px",
			cursor: "pointer",
			marginTop: "15px",
		});
		if (p && p.click) {
			button.addEventListener("click", p.click);
		} else {
			button.addEventListener("click", modal.close);
		}
		button.addEventListener("mouseover", function() {button.style.boxShadow = "slategrey 0 0 0, slategrey 0 0 7px inset"});
		button.addEventListener("mouseout", function() {button.style.boxShadow = "slategrey 0 0 7px, slategrey 0 0 0 inset"});
		box.appendChild(title);
		if (p && p.text) {
			box.innerHTML += p.text + "<br />";
		} else {
			box.innerHTML += "Default Body Text<br />";
		}
		box.appendChild(button);
		inner.appendChild(box);
		outer.appendChild(inner);
		document.body.appendChild(outer);
		setTimeout(function() {
			addStyles(inner, {
				opacity: "1",
			});
			addStyles(box, {
				transform: "translate(0, 0)",
			});
		}, 50);
	},
	close: function() {
		document.getElementById("outermodaldialog").parentNode.removeChild(document.getElementById("outermodaldialog"));
	}
}