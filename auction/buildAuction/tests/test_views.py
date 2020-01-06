from django.test import TestCase
from buildAuction.models import User
#from buildAuction.models import Category
from buildAuction.models import Auction
from buildAuction.models import Access
from buildAuction.models import Item
from buildAuction.models import Photo
#from buildAuction.models import Favorite
from buildAuction.models import Tx
import unittest
import random
from django.urls import reverse
from django import views
import urllib

class auctionTest(unittest.TestCase):
    # retrieves a RANDOM already created user
    def get_rand_user(self):
        user_count = User.objects.count()
        a = random.randint(1, user_count)
        return User.objects.get(pk=a)
    
    # retreives an already created auction
    def get_rand_auction(self):
        auction_count = Auction.objects.count()
        a = random.randint(1, auction_count)
        return Auction.objects.get(pk=a)

    # retrieves a random already created item
    def get_rand_item(self):
        item_count = Item.objects.count()
        a = random.randint(1, item_count)
        return Item.objects.get(pk=a)

    # retrieves a random already created tx
    def get_rand_tx(self):
        tx_count = Tx.objects.count()
        a = random.randint(1, tx_count)
        return Tx.obbjects.get(pk=a)

 # Begin views Unit tests ###############################################################
    def test_login(self):
        url = reverse("login")
        resp = urllib.request.urlopen("http://localhost:8000" + url)
        self.assertEqual(resp.status, 200)

    def test_logout(self):
        url = reverse("login")
        resp = urllib.request.urlopen("http://localhost:8000" + url)
        self.assertEqual(resp.status, 200)

    def test_create(self):
        url = reverse("create")
        resp = urllib.request.urlopen("http://localhost:8000" + url)
        self.assertEqual(resp.status, 200)
    
    def test_settings(self):
        url = reverse("settings")
        resp = urllib.request.urlopen("http://localhost:8000" + url)
        self.assertEqual(resp.status, 200)

    def test_myBids(self):
        url = reverse("myBids")
        resp = urllib.request.urlopen("http://localhost:8000" + url)
        self.assertEqual(resp.status, 200)

    def test_itemView(self):
        randomItem = self.get_rand_item().id
        url = reverse("itemView", args=[randomItem])
        resp = urllib.request.urlopen("http://localhost:8000" + url)
        self.assertEqual(resp.status, 200)

    def test_auctions(self):
        url = reverse("auctions")
        resp = urllib.request.urlopen("http://localhost:8000" + url)
        self.assertEqual(resp.status, 200)

    def test_auciton(self):
        randomAuction = self.get_rand_auction().id
        url = reverse("auction", args=[randomAuction])
        resp = urllib.request.urlopen("http://localhost:8000" + url)
        self.assertEqual(resp.status, 200)
    
    def test_itemHistory(self):
        randomItem = self.get_rand_item().id
        url = reverse("itemHistory", args=[randomItem])
        resp = urllib.request.urlopen("http://localhost:8000" + url)
        self.assertEqual(resp.status, 200)

    def test_processBid2(self):
        randomItem = self.get_rand_item().id
        url = reverse("processBid2", args=[randomItem])
        resp = urllib.request.urlopen("http://localhost:8000" + url)
        self.assertEqual(resp.status, 200)

    def test_bidConfirmation(self):
        url = reverse("bidConfirmation")
        resp = urllib.request.urlopen("http://localhost:8000" + url)
        self.assertEqual(resp.status, 200)

    def test_register(self):
        url = reverse("registration")
        resp = urllib.request.urlopen("http://localhost:8000" + url)
        self.assertEqual(resp.status, 200)

    def test_docs(self):
        url = reverse("docs")
        resp = urllib.request.urlopen("http://localhost:8000" + url)
        self.assertEqual(resp.status, 200)

    def test_itemPrices(self):
        url = reverse("itemPrices")
        resp = urllib.request.urlopen("http://localhost:8000" + url)
        self.assertEqual(resp.status, 200)

    def test_itemPricesItem(self):
        randomItem = self.get_rand_item().id
        url = reverse("itemPricesItem", args=[randomItem])
        resp = urllib.request.urlopen("http://localhost:8000" + url)
        self.assertEqual(resp.status, 200)

    def test_adminWinnerList(self):
        url = reverse("adminWinnerList")
        resp = urllib.request.urlopen("http://localhost:8000" + url)
        self.assertEqual(resp.status, 200)

    def test_processLiveBid(self):
        randomItem = self.get_rand_item().id
        url = reverse("processLiveBid", args=[randomItem])
        resp = urllib.request.urlopen("http://localhost:8000" + url)
        self.assertEqual(resp.status, 200)

    def test_userList(self):
        url = reverse("userList")
        resp = urllib.request.urlopen("http://localhost:8000" + url)
        self.assertEqual(resp.status, 200)
