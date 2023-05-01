var updateButtons=document.getElementsByClassName('update-subscription')

for(var x=0;x<updateButtons.length;x++){
    updateButtons[x].addEventListener('click',function(){
        var prodID=this.dataset.publication
        var action=this.dataset.action
        console.log('prodID:',prodID, 'action:', action)

        console.log('USER:', user)
        if(user==='AnonymousUser'){
            console.log('Not Logged In')
        }else{
            updateSubscrition(prodID,action)
        }
    })
}

function updateSubscription(prodID,action){
    console.log('processing data')
    var url='/updateitem/'
    fetch(url,{
        method:'POST',
        headers:{'Content-Type':'application/json',
        'X-CSRFToken':csrftoken,
    },
        body:JSON.stringify({'prodID':prodID,'action':action})
    })

    .then((response)=>{ 
        return response.json()
    })
    .then((data)=>{
        console.log('data:',data)
        location.reload()
    })
}

function confirmRequest() {
  // Display an alert to the user and wait for confirmation
    const confirmed = confirm('Are you sure you want to go for the weekend');

    if (confirmed) {
        // Send an AJAX request to the server to record the request

        const xhttp = new XMLHttpRequest();
        
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                // Display a message to the user indicating that the request has been applied
                alert('Request applied');
            }
        };

        xhttp.setRequestHeader("X-CSRFToken", csrfToken);
        xhttp.open('POST', 'apply_request/', true);
        alert('Hello applied');
        xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
        xhttp.send();

        // Store the current time in a cookie
        const now = new Date().getTime();
        const expirationTime = now + (7 * 24 * 60 * 60 * 1000); // 1 week from now
        document.cookie = 'request_time=' + now + '; expires=' + new Date(expirationTime).toUTCString() + '; path=/';
    }

}


