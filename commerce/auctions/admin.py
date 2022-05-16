from django.contrib import admin

from .models import Category, Auction_listing, Active_Deactive, Comment, Bid, Watchlist, ClosedBids

# Register your models here.
admin.site.register(Category)
admin.site.register(Auction_listing)
admin.site.register(Active_Deactive)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Watchlist)
admin.site.register(ClosedBids)
