function showOrHideCommentArea(id){
    if(document.getElementById("commentArea" + id).childNodes.length <= 0){
        var commentArea = document.createElement('TEXTAREA');
    commentArea.setAttribute('placeholder', 'Your comment...');
    commentArea.setAttribute('id', 'commentTextBox' + id);
    commentArea.setAttribute('class', 'comment');
    commentArea.setAttribute('onkeypress', 'sendComment('+id+');')
    document.getElementById("commentArea" + id).appendChild(commentArea);
    }
    else{
        document.getElementById("commentArea" + id).innerHTML = "";
    }
}

function hideHasComment(id){
    document.getElementById("has-comment" + id).style.display = 'none';
}

function sendComment(id){
    if(window.event.keyCode == 13){
        //If the user want to add a new line without sending, he has to hold shift in the same time
        if(window.event.shiftKey){
             document.getElementById("commentTextBox" + id).innerHTML += "<br>";
        }
        else{
            var message = document.getElementById("commentTextBox" + id).value
            var request = new XMLHttpRequest();
            request.open('POST', '/comment', true);
            request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            request.onreadystatechange = function() {
                if(request.readyState == XMLHttpRequest.DONE){
                    console.log(request.responseText);
                    document.getElementById("commentArea" + id).innerHTML = "";
                    document.getElementById("has-comment" + id).style.display = '';
                }
            }
            request.send("id=" + id + "&message=" + message);
        }
    }
}
