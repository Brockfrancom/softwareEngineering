from django.contrib import admin

from .models import *

admin.site.register(User)
admin.site.register(Auction)
#admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Photo)
admin.site.register(Tx)
#admin.site.register(Favorite)
admin.site.register(Access)
