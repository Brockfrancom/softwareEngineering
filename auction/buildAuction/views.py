from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from urllib.parse import urlencode
from django.conf import settings
from .models import Item
from .models import Auction
from .models import Tx
from .models import User
from .models import Photo
from .login import login_init, checkAdmin, createUser, getUser, checkPwd, setPwd
from .login import login as login2
import decimal
import random

import json
from .messages import addMessage, getMessages

def documentation(request):
    return render(request, "buildAuction/docs.html", {})

def add_a_random_smattering_of_items_to_an_auction(a):
    for i in range(5):
        item = Item()
        item.auction = a
        item.title = "Item " + str(i)
        item.donator = "Gill Bates - Super Philanthropist"
        item.description = "A computer"
        item.current_price = 1.00
        item.save()
        add_a_few_random_images_to_items(item)

def add_a_few_random_images_to_items(item):
    photo = Photo()
    photo.auction = item.auction
    photo.item = item
    photo.is_cover = True
    photo.photo = "images/" + str(random.randint(1,13)) + ".jpg"
    photo.save()
    for i in range(1,5):
        photo = Photo()
        photo.auction = item.auction
        photo.item = item
        photo.photo = "images/" + str(random.randint(1,13)) + ".jpg"
        photo.save()

def debug_init(request):
    request.session.flush()
    b = login_init()
    a = Auction(user=b, title="A Live Auction")
    a.is_live = True
    a.save()
    add_a_random_smattering_of_items_to_an_auction(a)
    a = Auction(user=b, title="A dead Auction")
    a.save()
    add_a_random_smattering_of_items_to_an_auction(a)
    return HttpResponseRedirect("/")

def getPermissions(request):
    admin_access = False
    if request.session.get("username"):
            admin_access = checkAdmin(request.session.get("username"))
    return {"usersss": request.session.get("logged"), "admin": admin_access, "uname": request.session.get("username"), "uid": request.session.get("uid")}

def logout(request):
    try:
        request.session.flush()
    except KeyError:
        pass
    return HttpResponseRedirect("/")

def login(request):
    if request.method == "POST":
        log = login2(request.POST.get("username"), request.POST.get("pass"), request)
        if not log:
            addMessage(request, {"text": "Invalid User Credentials", "type":"danger"})
            HttpResponseRedirect("/login")
    if request.session.get("logged"):
        return HttpResponseRedirect("/")
    context = {"messages": getMessages(request)}
    context.update(getPermissions(request))
    return render(request, "buildAuction/LoginPage.html", context)

def change_password(request):
    context = getPermissions(request)
    if not context["usersss"]:
        return HttpResponseRedirect("/login")
    if request.method != "POST":
        return HttpResponseRedirect("/settings")
    if not request.POST.get("pass"):
        addMessage(request, {"type":"danger", "text":"Invalid password change request. You must provide your current password."})
    elif not request.POST.get("new_pass"):
        addMessage(request, {"type":"danger", "text":"Invalid password change request. You must provide your a new password."})
    else:
        user = getUser(context["uname"])
        if not checkPwd(request.POST.get("pass"), user):
            addMessage(request, {"text":"Password could not be changed, current password was incorrect.", "type":"danger"})
            return HttpResponseRedirect("/settings")
        setPwd(request.POST.get("new_pass"), user)
        addMessage(request, {"text":"Password change was successful.", "type":"success"})
        return HttpResponseRedirect("/settings")
        

def register(request):
    fail = False
    if request.session.get("logged"):
        return HttpResponseRedirect("/")
    if request.method == "POST":
        if not request.POST.get("name"):
            fail = True
            addMessage(request, {"type":"danger", "text":"A full name was not provided!"})
        if not request.POST.get("email"):
            fail = True
            addMessage(request, {"type":"danger", "text":"A email was not provided!"})
        if not request.POST.get("username"):
            fail = True
            addMessage(request, {"type":"danger", "text":"A username was not provided!"})
        if not request.POST.get("pass"):
            fail = True
            addMessage(request, {"type":"danger", "text":"A password name was not provided!"})
        if fail:
            context = {"messages": getMessages(request)}
            context.update(getPermissions(request))
            return render(request, "buildAuction/Register.html", context)
        if createUser(request.POST.get("username"), request.POST.get("pass"), request.POST.get("name"), request.POST.get("email")):
            login2(request.POST.get("username"), request.POST.get("pass"), request)
        else:
            addMessage(request, {"text": "The username `{}` is already being used!".format(request.POST.get("username")), "type":"danger"})
    if request.session.get("logged"):
        return HttpResponseRedirect("/")
    context = {"messages": getMessages(request)}
    context.update(getPermissions(request))
    return render(request, "buildAuction/Register.html", context)

def userSettings(request):
    context = getPermissions(request)
    context.update({'nbar':'settings','messages':getMessages(request)})
    if context["usersss"] == None:
        return HttpResponseRedirect("/")
    return render(request, "buildAuction/UserSettings.html", context)

def create(request):
    context = getPermissions(request)
    if (not context['admin']):
        return HttpResponseRedirect("/")
    return render(request, "buildAuction/CreateAuction.html", context)

def auctionList(request):
    auction_list = Auction.objects.all()
    context = {
        'auctions': auction_list,
        'nbar': "home",
    }
    context.update(getPermissions(request))
    return render(request, "buildAuction/auctions.html", context)

def auction(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id)
    context = getPermissions(request)
    context.update({'auction': auction, 'nbar': "home"})
    return render(request, "buildAuction/auctionView.html", context)

def itemListView(request, auction_id):
    auction = Auction.objects.get(pk=auction_id) 
    item_list = Item.objects.filter(auction=auction)
    photo_list = Photo.objects.all()
    context = {
        'auction' : auction,
        'item_list' : item_list,
        'photo_list' : photo_list,
        'nbar': "home",
    }
    context.update(getPermissions(request))
    return render(request, "buildAuction/itemListView.html", context)

def itemView(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    auction = item.auction 
    photo_list = Photo.objects.filter(item=item_id)
    username = request.session.get("username")
    messages = {}
    context = {
        'item' : item,
        'auction' : auction,
        'photo_list' : photo_list,
        'nbar': 'home',
    }
    context.update(getPermissions(request))
    context.update({"messages": getMessages(request)})
    return render(request, "buildAuction/itemView.html", context)

def myBids(request):
    permissions = getPermissions(request)
    if not permissions["usersss"]:
        return HttpResponseRedirect("/");
    username = request.session.get("username")
    user = User.objects.get(username=username)
    all_bid_list = Tx.objects.filter(user=user)
    items = all_bid_list.values_list('item_id', flat=True).distinct()
    item_list = Item.objects.filter(id__in=items)
    userTotal = decimal.Decimal(0.00)
    bid_list=[]
    for item in item_list:
        if item.current_winner == user:
            userTotal += item.current_price
        temp = all_bid_list.filter(item=item).order_by('amount')
        bid_list.append(temp[len(temp)-1])
    context = {
        'auction' : auction,
        'user' : user,
        'userTotal' : userTotal,
        'bid_list' : bid_list,
        'item_list' : item_list,
        'nbar': 'myBids',
    }
    context.update(permissions)
    return render(request, "buildAuction/myBids.html", context)


def itemHistory(request, item_id):
    permissions = getPermissions(request)
    if not permissions["usersss"]:
        return HttpResponseRedirect("/");
    item = Item.objects.get(pk=item_id)
    bid_list = Tx.objects.filter(item=item)
    context = {
        'bid_list' : bid_list,
        'item' : item,
        'nbar': 'admin',
    }
    context.update(permissions)
    return render(request, "buildAuction/ItemHistoryPage.html", context)

def processBid2(request, item_id):
    context = getPermissions(request)
    if not context["usersss"]:
        return HttpResponseRedirect("/auction/itemView/" + str(item_id))
    if request.method == "POST":
        try:
            theBid = decimal.Decimal(request.POST.get('customBid'))
        except Exception:
            error = "An error occured while processing. Make sure your bid is less than $99,999,999,999,999,999.99"
            addMessage(request, {"text": error, "type":"danger"})
            return HttpResponseRedirect("/auction/itemView/" + str(item_id) )
        if( theBid > decimal.Decimal(99999999999999999.99)):
            error = "This auction has a bid cap of $100,000,000,000,000,000.00. Make sure your bid is less than $99,999,999,999,999,999.99. If you wish to bid more, please contact the auction admin."
            addMessage(request, {"text": error, "type":"danger"})
            return HttpResponseRedirect("/auction/itemView/" + str(item_id) )
        item=Item.objects.get(pk=item_id)
        if(theBid > item.current_price ):
            user = User.objects.get(username=request.session.get("username"))
            item.current_price = theBid
            item.current_winner = user
            item.save()
            tx = Tx()
            tx.item = item
            tx.auction = item.auction
            tx.user = User.objects.get(username=context["uname"])
            tx.amount = item.current_price
            tx.save()
            error = "Your bid of ${} was processed successfully.".format(theBid)
            addMessage(request, {"text":error, "type":"success"})
        else:
            error = "The given bid was too low: ${}".format(theBid)
            addMessage(request, {"text": error, "type":"danger"})
    return HttpResponseRedirect("/auction/itemView/" + str(item_id) )


def voidedTx(request):
    # this method is to be called when the admin hits the delete/void transaction on an items bid
    # this method gets the next highest bid and makes it the current bid (and updates the items current winner/amt)
    # I don't know which view render after this - i think it should be the item history the admin was just looking
        # at (but updated with the voided tx being grayed out)
    if request.method == "POST":
        assoc_item = Item.objects.get(request.POST.get("theItem"))

        auction = Auction.objects.get(pk=request.POST.get("theAuction"))
        user = User.objects.get(pk= request.POST.get("theUser"))

        tx_list = Tx.objects.filter(Tx.item == assoc_item)
        next_bid = tx_list[0]
        for element in tx_list:
            if element.amount > next_bid.amount:
                next_bid = element
        assoc_item.current_price = next_bid.amount
        assoc_item.current_winner = next_bid.user
    pass

def addPaddle(paddle_number, entered_username, is_new_user):
    #is_new_user is a boolean (true if they don't have a profile)
    current_paddles = User.objects.get(User.has_paddle_num==True)
    current_users = User.objects.all()
    unique_paddle = True
    new_username_valid = True
    matching_username_valid = True
    for element in current_paddles:
        if paddle_number == element.paddle:
            unique_paddle = False
            # THE PADDLE NUMBER THE ADMIN ENTERED IS ALREADY IN USE - NOT ALLOWED - WILL NOT UPDATE
    if unique_paddle == True:
        if is_new_user == True:
            for element in current_users:
                if entered_username == element.username:
                    new_username_valid = False
                    # THE USERNAME ENTERED (FOR A NEW PROFILE) IS ALREADY IN USE - WILL NOT UPDATE
            if(new_username_valid==True):
                #create new user with username and paddle number
                user = User()
                user.username = entered_username
                user.paddle = paddle_number
                user.has_paddle_num = True
                user.save()
        elif is_new_user == False:
            user = User.objects.filter(username=entered_username)
            # IF IT DOESN'T EXIST - NO MATCHING USER NAME - WILL NOT UPDATE
            if user.exists():
                user.paddle = paddle_number
                user.has_paddle_num = True
    pass

def catagories(request):
    return render(request, "buildAuction/CategoryPage.html",getPermissions(request))

def bidConfirmation(request):
    return render(request,"buildAuction/BidConfirmation.html", getPermissions(request))

def itemPricesItem(request, item_id):
    try:
        item = Item.objects.get(pk=item_id)
        item_view = {}
        item_view = {"title": item.title, "price": float(item.current_price), "auction_id": item.auction.id, "id": item.id}
        return HttpResponse(json.dumps(item_view), content_type="application/json")
    except:
        return HttpResponse('{"error":"Item not found"}', content_type="application/json")

def itemPrices(request):
    global counter
    items = Item.objects.all()
    item_list = []
    for item in items:
        if request.GET.get("auction"):
            if item.auction.id != int(request.GET.get("auction")):
                continue
        item_list.append({'title':item.title, 'price':float(item.current_price), 'auction_id':item.auction.id, "id": item.id})
        if item.current_winner:
            item_list[-1]["winner"] = item.current_winner.username
    return HttpResponse(json.dumps(item_list), content_type="application/json")

def testUpdate(request):
    id = Auction.objects.all().order_by('-id')[0].id
    addMessage(request, {"text":"Boo", "type":"danger"})
    addMessage(request, {"text":"Boo", "type":"success"})
    addMessage(request, {"text":"Boo", "type":"warning"})
    context = getPermissions(request)
    context.update({'id':id, 'messages': getMessages(request)})
    return render(request, "buildAuction/updater.html", context)

def testUpdate2(request):
    item = Item.objects.all().order_by('-id')[0]
    id = item.id
    title = item.title
    context = getPermissions(request)
    context.update({'id':id, 'title': title})
    return render(request, "buildAuction/updateItem.html", context)

def adminWinnerList(request):
    permissions = getPermissions(request)
    if not permissions["usersss"]:
        return HttpResponseRedirect("/");
    bid_list = Tx.objects.all()
    item_list = Item.objects.all()
    context = {
        'bid_list' : bid_list,
        'item_list' : item_list,
    }
    context.update(permissions)
    return render(request, "buildAuction/adminWinnerList.html", context)

def processLiveBid(request, item_id):
    context = getPermissions(request)
    if not context["usersss"]:
        return HttpResponseRedirect("/auction/itemView/" + str(item_id))
    if request.method == "POST":
        try:
            theBid = decimal.Decimal(request.POST.get('WinPrice'))
        except Exception:
            error = "An error occured while processing. Make sure your bid is less than $99,999,999,999,999,999.99"
            addMessage(request, {"text": error, "type":"danger"})
            return HttpResponseRedirect("/auction/itemView/" + str(item_id) )
        if( theBid > decimal.Decimal(99999999999999999.99)):
            error = "This auction has a bid cap of $100,000,000,000,000,000.00. Make sure your bid is less than $99,999,999,999,999,999.99. If you wish to bid more, please contact the auction admin."
            addMessage(request, {"text": error, "type":"danger"})
            return HttpResponseRedirect("/auction/itemView/" + str(item_id) )
        item=Item.objects.get(pk=item_id)
        if(theBid > item.current_price ):
            try:
                 user = User.objects.get(paddle=int(request.POST.get("LiveUserId")))
            except:
                 error = "The paddle number was not recognized, please try again. Paddle: {}".format(request.POST.get("LiveUserId"))
                 addMessage(request, {"text":error, "type":"danger"})
                 return HttpResponseRedirect("/auction/itemView/" + str(item_id) )
            item.current_price = theBid
            item.current_winner = user
            item.save()
            tx = Tx()
            tx.item = item
            tx.auction = item.auction
            tx.user = user
            tx.amount = item.current_price
            tx.save()
            success = "Your bid of ${} was processed successfully.".format(theBid)
            addMessage(request, {"text":success, "type":"success"})
        else:
            error = "The given bid was below the current price, your bid: {}".format(theBid)
            addMessage(request, {"text":error, "type":"danger"})
    return HttpResponseRedirect("/auction/itemView/" + str(item_id) )

def userList(request):
    permissions = getPermissions(request)
    if not permissions["usersss"]:
        return HttpResponseRedirect("/");
    all_user_list = User.objects.all()
    all_item_list = Item.objects.all()
    list = []
    for user in all_user_list:
        user_list = {}
        userTotal = decimal.Decimal(0.00)
        user_list.update({'User':user})
        item_dct = {}
        for item in all_item_list:
            if item.current_winner == user:
                item_dct.update({item:item})
                userTotal += item.current_price
        user_list.update({'Items':item_dct})
        user_list.update({'UserTotal':userTotal})
        list.append(user_list)
    context = {
        'all_user_list' : all_user_list,
        'item_list' : all_item_list,
        'list' : list,
    }
    context.update(permissions)
    return render(request, "buildAuction/userList.html", context)
