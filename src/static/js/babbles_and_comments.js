function like(id){
    var request = new XMLHttpRequest();
    request.open('POST', '/like', true);
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    request.onreadystatechange = function() {
        if(request.readyState == XMLHttpRequest.DONE){
            document.getElementById("like" + id).innerHTML = request.responseText + "&nbsp &nbsp";
        }
    }
    request.send("id=" + id);
}

function likeComment(commentID){
    var request = new XMLHttpRequest();
    request.open('POST', '/likeComment', true);
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    request.onreadystatechange = function() {
        if(request.readyState == XMLHttpRequest.DONE){
            document.getElementById("commentLike" + commentID).innerHTML = "&nbsp"+request.responseText + "&nbsp &nbsp";
        }
    }
    request.send("commentID=" + commentID);
}

function user_exists(username){
    var request = new XMLHttpRequest();
    request.open('GET', '/users/' + username, false);
    request.send()
    if(request.responseText == 'True'){
        return true;
    }
    else{
        return false;
    }
}

function link_mensions(message){
    var matches = message.match(/@([a-z\d_]+)/gi);
    if(matches == null){
        return message;
    }
    var link = "";
    for ( i = 0 ; i < matches.length ; i++){
        var user = matches[i].substr(1);
        var exists = user_exists(user);
        if(exists){
            link = "<a href=\"/babblers/"+user+"\">@"+user+"</a>";
            var position = message.indexOf(user);
            message = message.substr(0, position-1) + link + message.substr(position + user.length);
        }
    }
    return message;
}

function link_tags_and_mentions(message){
    message = message.replace(/#([a-z\d_]+)/ig, "<a href=\"/tag/$1\">#$1</a>");
    message = link_mensions(message);
    return message;
}

/* Si on passe le message du babble direct à partir du html, les new lines causent problème */
function link_tags_and_mentions_babble(babble){
    return link_tags_and_mentions(babble['message']);
}

function delete_babble(id){
    var request = new XMLHttpRequest();
    request.open('POST', '/deleteBabble', true);
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    request.onreadystatechange = function() {
        if(request.readyState == XMLHttpRequest.DONE){
            var post = document.getElementById("delete" + id);
            post.parentNode.removeChild(post);
        }
    }
    request.send("id=" + id);
}

function delete_comment(commentID){
    var request = new XMLHttpRequest();
    request.open('POST', '/deleteComment', true);
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    request.onreadystatechange = function() {
        if(request.readyState == XMLHttpRequest.DONE){
            var comment = document.getElementById("deleteComment" + commentID);
            comment.parentNode.removeChild(comment);
        }
    }
    request.send("commentID=" + commentID);
}

function showOrHideCommentArea(id, babbles){
    if(document.getElementById("commentArea" + id).childNodes.length <= 0){
        var commentArea = document.createElement('TEXTAREA');
        commentArea.setAttribute('placeholder', 'Your comment...');
        commentArea.setAttribute('id', 'commentTextBox' + id);
        commentArea.setAttribute('class', 'comment');
        commentArea.setAttribute('onkeypress', 'sendComment('+id+');');
        document.getElementById("commentArea" + id).innerHTML +=  " &nbsp &nbsp";
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

function getComments(babbleID, username){
    var request = new XMLHttpRequest();
    request.open('POST', '/getComments', true);
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    request.onreadystatechange = function() {
        if(request.readyState == XMLHttpRequest.DONE){
            var res = JSON.parse(request.response)
             for (comment of res['response']){
                createCommentCard(babbleID, comment, username);
             }

        }
    }
    request.send("id=" + babbleID);
}

/***************** WARNING : BIG MONSTER *****************/
function createCommentCard(babbleID, comment, loggedUser){
    /************* PICTURE *****************/
    var img = document.createElement("IMG");
    img.setAttribute('src', '/static/images/'+comment['username']+'.jpg');

    var figure = document.createElement("FIGURE");
    figure.setAttribute('class', 'image is-64x64');
    figure.appendChild(img);

    var media_left = document.createElement("div");
    media_left.setAttribute('class', 'media-left');
    media_left.appendChild(figure);

    /********* NAME TIME AND MESSAGE **********/
    var username = document.createElement("a");
    username.setAttribute('href', '/babblers/'+comment['username']);
    username.innerHTML = "<strong>@" + comment['username']+"</strong>";

    var elapsed = document.createElement("SMALL");
    elapsed.innerHTML = "&nbsp"+comment['elapsed']+" ago";

    var message = document.createElement("div");
    message.setAttribute('style', 'white-space: pre-line;');
    message.innerHTML = link_tags_and_mentions(comment['message']);

    var p1 = document.createElement("P");
    p1.appendChild(username);
    p1.appendChild(elapsed);
    p1.innerHTML += "<br>";
    p1.appendChild(message);

    var content = document.createElement("div");
    content.setAttribute('class', 'content');
    content.appendChild(p1);

    /************** LIKES *****************/
    var fas_fa_heart = document.createElement("I");
    fas_fa_heart.setAttribute('class', 'fas fa-heart');

    var icon_is_small = document.createElement("SPAN");
    icon_is_small.setAttribute('class', 'icon is-small');
    icon_is_small.innerHTML += "&nbsp";
    icon_is_small.appendChild(fas_fa_heart);

    var level_item = document.createElement("a");
    level_item.setAttribute('class', 'level-item');
    level_item.setAttribute('onclick', 'likeComment('+comment['commentID']+')');
    level_item.appendChild(icon_is_small);

    var p2 = document.createElement("P");
    p2.setAttribute('id', 'commentLike'+comment['commentID']);
    p2.innerHTML = "&nbsp"+comment['nbLikes'];

    var level_left = document.createElement("div");
    level_left.setAttribute('class', 'level-left');
    level_left.appendChild(level_item);
    level_left.appendChild(p2);

    var level_is_mobile = document.createElement("NAV");
    level_is_mobile.setAttribute('class', 'level is-mobile');
    level_is_mobile.appendChild(level_left);

    var media_content = document.createElement("div");
    media_content.setAttribute('class', 'media-content');
    media_content.appendChild(content);
    media_content.appendChild(level_is_mobile);

    /**************** DELETE *******************/
    var fas_fa_trash_alt = document.createElement("I");
    fas_fa_trash_alt.setAttribute('class', 'fas fa-trash-alt');

    var icon_is_small2 = document.createElement("SPAN");
    icon_is_small2.setAttribute('class', 'icon is-small');
    icon_is_small2.setAttribute('onclick', 'delete_comment('+comment['commentID']+')');
    icon_is_small2.appendChild(fas_fa_trash_alt);

    var a = document.createElement("a");
    a.appendChild(icon_is_small2);

    var media_right = document.createElement("div");
    media_right.setAttribute('class', 'media-right');
    media_right.appendChild(a);

    var media = document.createElement("ARTICLE");
    media.setAttribute('class', 'media');
    media.appendChild(media_left);
    media.appendChild(media_content);
    if(loggedUser == comment['username']){
        media.appendChild(media_right);
    }

    var box = document.createElement("div");
    box.setAttribute('class', 'box');
    box.setAttribute('id', "deleteComment" + comment['commentID'])
    box.appendChild(media);

    document.getElementById("showComments" + babbleID).appendChild(box);
}

function showComments(babbleID, username){
     getComments(babbleID, username);
     document.getElementById("showComments" + babbleID).innerHTML += "<br>";
     document.getElementById("showComments" + babbleID).style.display = '';
}

function hideComments(babbleID){
    document.getElementById("showComments" + babbleID).innerHTML = "";
    document.getElementById("showComments" + babbleID).style.display = 'none';
}

function showHideComments(babble, username){
    if(document.getElementById("showComments" + babble['id']).style.display == 'none'){
        showComments(babble['id'], username);
    }
    else{
        hideComments(babble['id']);
    }
}
