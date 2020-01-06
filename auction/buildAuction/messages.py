__name__ = "messages"

def addMessage(request, message):
    if not request.session.get("messages"):
        request.session["messages"] = []
    request.session["messages"].append(message)

def getMessages(request):
    if request.session.get("messages"):
        msg = request.session["messages"]
        del request.session["messages"]
        return msg
    return []
