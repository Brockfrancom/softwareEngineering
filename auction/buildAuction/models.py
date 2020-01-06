from django.db import models
from django import forms
from django.core.validators import validate_comma_separated_integer_list

import os

class User(models.Model):
    # primary key not specified because django’s default will make the auto incrementing integer primary key for us
    fullName = models.CharField(max_length=100, null=False, default="Jack")
    email = models.CharField(max_length=100, null=False, default="Jill")
    username = models.CharField(unique=True,max_length=200, null=False)
    paddle = models.IntegerField(null=True, blank=True, default=None)
        # I can't set unique=True on this because then it will not allow more than 1 null/blank entry
        # but if it is not null then it CANNOT BE A NUMBER ALREADY USED!

    password_hashed = models.CharField(max_length=256, null=True, blank=False)
        # password can be null in the scenario where admin adds a username for a live auction for a user who
            # does not have a profile already.
    has_paddle_num=models.BooleanField(default=False, null=False, blank=False)
    # These fetures are not added yet
    notif_on_bidded_items = models.BooleanField(default=True, null=False, blank=False)
    notif_on_fav_items = models.BooleanField(default=False, null=False, blank=False)

    def __str__(self):
        return self.username


class Auction(models.Model):
    # primary key not specified because django’s default will make the auto incrementing integer primary key for us
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # this user is the user id to the creator of the auction

    is_live = models.BooleanField(default=False)
    end_time = models.DateField(null=True)
    # defaults to NULL since admin might create auction long before they know details of what time to end it.

    title=models.CharField(max_length=50, null=False)
    description = models.TextField(null=True, blank=True)
    event_closed = models.BooleanField(default=False, null=False, blank=False)

    def __str__(self):
        return self.title


# class Category(models.Model):
#     category=models.CharField(max_length=30, primary_key=True, null=False, blank=False)
#     description=models.TextField(null=True, blank=True,)

#     def __str__(self):
#         return "%s" % (self.category)


class Access(models.Model):
    # primary key not specified because django’s default will make the auto incrementing integer primary key for us
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    admin_level=models.BooleanField(default=False, null=False, blank=False)

    def __str__(self):
        # implement printable form of access
        return self.user.username + ": " + str(self.admin_level)


class Item(models.Model):
    # primary key not specified because django’s default will make the auto incrementing integer primary key for us

    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    title=models.CharField(max_length=50, null=False, blank=False)
    min_price=models.DecimalField(max_digits=20,decimal_places=2, default=0.00)
    current_price=models.DecimalField(max_digits=20,decimal_places=2, null=True)
    current_winner=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    donator=models.CharField(max_length=50, null=True, blank=True)
    description=models.TextField(null=True, blank=True)
    # category=models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    # DO NOT USE live_position - this member will be deleted soon
    # live_position=models.PositiveSmallIntegerField(null=True, blank=True)


    is_hidden=models.BooleanField(default=False, null=False, blank=False)
    is_closed=models.BooleanField(default=False, null=False, blank=False)
    is_paid=models.BooleanField(default=False, null=False, blank=False)

    def __str__(self):
        # implement printable form of item
        return self.title


class Photo(models.Model):
    # primary key not specified because django’s default will make the auto incrementing integer primary key for us

    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, null=False, blank=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='images/')

    is_cover = models.BooleanField(default=False, null=False, blank=False)

    def __str__(self):
        # implement printable form of photo?
        return self.item.__str__()

class Tx(models.Model):
    # primary key not specified because django’s default will make the auto incrementing integer primary key for us

    timestamp=models.DateTimeField(auto_now_add=True, null=False, blank=False, editable=False)
    user=models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # Do nothing means if the user is deleted nothing happens with their Tx so USERS SHOULD NOT BE DELETED -
        # AUCTIONS ARE WHAT WILL BE DELETED
    item=models.ForeignKey(Item, on_delete=models.CASCADE)
    # What is your guys' preference - if an item is deleted should proof of the user transaction
    # remain or should we just delete them?
    amount=models.DecimalField(max_digits=20,decimal_places=2, null=False, blank=False)
    bid_event=models.BooleanField(default=True, blank=False, null=False)
    auction=models.ForeignKey(Auction, on_delete=models.CASCADE, null=False, blank=False)

    voided=models.BooleanField(default=False, null=False, blank=False)
    # This value is true of admin voided the transaction - if this happens a
    # notification to the user involved should be sent

    manual=models.BooleanField(default=False, null=False, blank=False)
    # This value is True if admin entered final winner manually

    def __str__(self):
        return str(self.timestamp)


# class Favorite(models.Model):
#     # primary key not specified because django’s default will make the auto incrementing integer primary key for us

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     item=models.ForeignKey(Item, on_delete=models.CASCADE)
#     auction=models.ForeignKey(Auction, on_delete=models.CASCADE, null=False, blank=False)

#     def __str__(self):
#         # define printable form?
#         pass

#########################################################################

    # the username and password are stored here but yah...:) goes here - the user will give their password
    # and we'll hash it down to a 6 char value or semthing and then store it in our db. :)
    class UserForm(forms.ModelForm):
        username = models.CharField(max_length=200)
        password = forms.CharField(widget=forms.PasswordInput)
        # impelement method to convert this to a 6 char string and then we'll store it in db (it's not safe
        # to store password in normal form in a db)
        pub_date = models.DateTimeField('date published')

