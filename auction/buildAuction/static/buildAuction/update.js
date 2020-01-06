function updateAuction(items, id) {
	for (i in items) {
		item = items[i];
		price_slot = document.getElementById(`price_${item.id}`);
	}
	setTimeout(function() {fetchAndUpdateAuction(id)}, 1500);
}

function fetchAndUpdateAuction(id) {
	fetch(`/prices?auction=${id}`).then(A=>A.json()).then(A=>updateAuction(A, id));
}

var increments = [1,5,10,50];

function update(item, id) {
	lols = document.getElementsByName(`price_${ item.id }`);
	for (lol in lols) {
		target = lols[lol];
		target.innerHTML = item.price;
	}
	for (i in increments) {
		if (a = $(`#customBid${increments[i]}`)) {
			a.value = item.price+increments[i];
		}
		if (b = $(`#bid-button-${increments[i]}`)) {
			b.value = item.price+increments[i];
		}
	}

	setTimeout(function() {fetchAndUpdate(id)}, 1500);
}

function fetchAndUpdate(id) {
	fetch(`/price/${ id }`).then(A=>A.json()).then(A=>update(A, id));
}
