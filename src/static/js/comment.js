function showOrHideCommentArea(id, babbles){
    if(document.getElementById("commentArea" + id).childNodes.length <= 0){
        document.getElementById("showComments" + id).innerHTML = "";
        var commentArea = document.createElement('TEXTAREA');
        commentArea.setAttribute('placeholder', 'Your comment...');
        commentArea.setAttribute('id', 'commentTextBox' + id);
        commentArea.setAttribute('class', 'comment');
        commentArea.setAttribute('onkeypress', 'sendComment('+id+');')
        for (b of babbles){
            document.getElementById("commentArea" + b['id']).innerHTML = "";
        }
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
                    hideComments(id);
                    showComments(id);
                }
            }
            request.send("id=" + id + "&message=" + message);
        }
    }
}

function getComments(babbleID, comments){
    var request = new XMLHttpRequest();
    request.open('POST', '/getComments', true);
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    request.onreadystatechange = function() {
        if(request.readyState == XMLHttpRequest.DONE){
            var res = JSON.parse(request.response)
             for (comment of res['response']){
                createCommentCard(babbleID, comment)
             }

        }
    }
    request.send("id=" + babbleID);
}

/***************** WARNING : BIG MONSTER *****************/
function createCommentCard(babbleID, comment){
    var img = document.createElement("IMG");
    img.setAttribute('src', '/static/images/'+comment['username']+'.jpg');

    var figure = document.createElement("FIGURE");
    figure.setAttribute('class', 'image is-64x64');
    figure.appendChild(img);

    var media_left = document.createElement("div");
    media_left.setAttribute('class', 'media-left');
    media_left.appendChild(figure);

    /****************************************/
    var username = document.createElement("a");
    username.setAttribute('href', '/babblers/'+comment['username']);
    username.innerHTML = "<strong>@" + comment['username']+"</strong>";

    var elapsed = document.createElement("SMALL");
    elapsed.innerHTML = comment['elapsed']+" ago";

    var message = document.createElement("div");
    message.setAttribute('style', 'white-space: pre-line;');
    message.innerHTML = comment['message'];

    var p1 = document.createElement("P");
    p1.appendChild(username);
    p1.appendChild(elapsed);
    p1.innerHTML += "<br>";
    p1.appendChild(message);

    var content = document.createElement("div");
    content.setAttribute('class', 'content');
    content.appendChild(p1);

    var media_content = document.createElement("div");
    media_content.setAttribute('class', 'media-content');
    media_content.appendChild(content);

    var media = document.createElement("ARTICLE");
    media.setAttribute('class', 'media');
    media.appendChild(media_left);
    media.appendChild(media_content);

    var box = document.createElement("div");
    box.setAttribute('class', 'box');
    box.appendChild(media);

    document.getElementById("showComments" + babbleID).appendChild(box);
}

function showComments(babbleID){
     getComments(babbleID)
     document.getElementById("showComments" + babbleID).style.display = '';
}

function hideComments(babbleID){
    document.getElementById("showComments" + babbleID).innerHTML = "";
    document.getElementById("showComments" + babbleID).style.display = 'none';
}

function showHideComments(babble){
    if(document.getElementById("showComments" + babble['id']).style.display == 'none'){
        showComments(babble['id']);
    }
    else{
        hideComments(babble['id']);
    }
}
