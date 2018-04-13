function link_tags(message, tags){
    for (tag of tags){
        message = message.replace('#'+tag['tag'], "<a href=\"/tag/"+tag['tag']+"\">#"+tag['tag']+"</a>");
    }
    return message;
}