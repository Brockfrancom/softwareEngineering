from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from . import views

urlpatterns = [
	path('', views.auctionList, name='home'),
	path('init', views.debug_init, name='init'),
	path('login', views.login, name='login'),
	path('logout', views.logout, name='login'),
	path('create', views.create, name='create'),
	path('settings', views.userSettings, name='settings'),
	path('myBids', views.myBids, name = "myBids"),
	path('itemView/<int:item_id>', views.itemView, name='itemView'),
	path('auctions', views.auctionList, name='auctions'),
	path('auction/<int:auction_id>', views.itemListView, name='auction'),
	path('itemHistory/<int:item_id>', views.itemHistory, name='itemHistory'),
	path('processBid2/<int:item_id>', views.processBid2, name='processBid2'),
	path('categories',views.catagories,name = "categories"),
	path('bidConfirmation',views.bidConfirmation,name = 'bidConfirmation'),
	path('register',views.register, name="registration"),
	path('docs',views.documentation, name="docs"),
	path('prices',views.itemPrices, name="itemPrices"),
    path('price/<int:item_id>',views.itemPricesItem, name="itemPricesItem"),
	path('test',views.testUpdate, name="testUpdate"),
	path('test2',views.testUpdate2, name="testUpdate2"),
	path('adminWinnerList', views.adminWinnerList, name = "adminWinnerList"),
	path('processLiveBid/<int:item_id>', views.processLiveBid, name='processLiveBid'),
	path('userList', views.userList, name = "userList"),
        path('changePwd', views.change_password),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
