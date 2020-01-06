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

class modelsTest(unittest.TestCase):
    # Creates and saves a RANDOM user
    def create_user(self):
        a = random.randint(0, 10000)
        name = "FullName #" + str(a)
        email="Email #" + str(a)
        username = "Username #" + str(a)
        password=None
        pdl = a
        user = User.objects.create(fullName=name, email=email, username=username, paddle=pdl, password_hashed=password)
        user.save()
        return user

    # takes a user object, and creates/saves and Access table entry with admin_level as true
    def insert_access_admin(self, admin):
        adminaccess = Access.objects.create(user=admin, admin_level=True)
        adminaccess.save()
        return adminaccess

    # creates and saves a new auction with live as true
    def create_auction(self, islive):
        user = self.create_user()
        a = random.randint(0, 10000)
        title = "Live Auction Title #" + str(a)
        self.insert_access_admin(user)
        liveauction = Auction.objects.create(user=user, is_live=islive, title=title)
        liveauction.save()
        return liveauction

    # takes a user object, and creates/saves and Access table entry with admin_level as false
    def insert_access_user(self, user):
        useraccess = Access.objects.create(user=user, admin_level=False)
        useraccess.save()
        return useraccess

    # creates/saves a new RANDOM item with a randomly selected auction
    def create_item(self):
        auction = self.get_rand_auction()
        a = random.randint(0, 1000000)
        title = "Item Title #" + str(a)
        item = Item.objects.create(auction=auction, title=title, current_price="1.00")
        item.save()
        return item

    # creates/saves a tx for a random user, random auction and random item
    def create_tx(self):
        user = self.get_rand_user()
        auction = self.get_rand_auction()
        item = self.get_rand_item()
        prevamt = item.current_price
        if prevamt is None:
            amt = 5
        else:
            amt = prevamt + 5
        tx = Tx.objects.create(user=user, item=item, amount=amt, auction=auction)
        tx.save()
        return tx

    # loops to set up objects in model - you can change the numbers (smaller than 10, 20 might not be large enough)
    # This method should only be ran once. If you run it multiple times, then some errors will occur. 
    def setup(self):
        for i in range(1, 10):
            self.create_user()
            self.create_auction(True)
            self.create_auction(False)
        for i in range(1, 20):
            self.create_item()
            self.create_tx()
        pass
    
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

 # Begin unit tests for models ####################################################
    # This should be the first test ran. Because they are ran in alphabetical order, I called it test_aaaaacreation.
    def test_aaaaacreation(self):
        self.setup()
        pass

    def test_create_user(self):
        i = self.create_user()
        self.assertTrue(isinstance(i, User))

    def test_create_auction(self):
        i = self.create_auction(True)
        self.assertTrue(isinstance(i, Auction))

    def test_create_user_access(self):
        u = self.create_user()
        i = self.insert_access_admin(u)
        self.assertTrue(isinstance(i, Access))

    def test_create_admin_access(self):
        u = self.create_user()
        i = self.insert_access_admin(u)
        self.assertTrue(isinstance(i, Access))

    def test_create_item(self):
        i = self.create_item()
        self.assertTrue(isinstance(i, Item))

