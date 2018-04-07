function like(id){
    var request = new XMLHttpRequest();
    request.open('POST', '/like', true);
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    request.onreadystatechange = function() {
        if(request.readyState == XMLHttpRequest.DONE){
            document.getElementById(id).innerHTML = request.responseText;
        }
    }
    request.send("id=" + id);
    }