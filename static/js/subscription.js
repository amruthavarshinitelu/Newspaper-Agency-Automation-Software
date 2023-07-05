
var updateButtons = document.getElementsByClassName('update-subscription');
console.log('Hello World');
for (var x = 0; x < updateButtons.length; x++) {
    updateButtons[x].addEventListener('click', function() {
        var prodID = this.dataset.product;  // Use 'data-product' instead of 'data-publication'
        var action = this.dataset.action;
        console.log('prodID:', prodID, 'action:', action);
        console.log('USER:', user);
        if (user === 'AnonymousUser') {
            console.log('Not Logged In');
        } else {
            updateSubscription(prodID, action);
        }
    });
}

function updateSubscription(prodID, action) {
    console.log('processing data');
    var url = '/updateitem/';
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'prodID': prodID, 'action': action })
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log('data:', data);
        location.reload();
    });
}

