from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator

class User(AbstractUser):
    pass


class Category(models.Model):
    lista_categorias = [
    ("Toys", "Toys"),
    ("Home", "Home"),
    ("Electronics", "Electronics"),
    ("Sports", "Sports"),
    ("Hobbies", "Hobbies"),
    ("Clothing", "Clothing"),
    ("Food", "Food"),
    ("Not Specified", "Not Specified"),
    ("None", "None"),
    ]
    class Meta:
        verbose_name_plural = "Category"

    category = models.CharField(max_length=30, choices=lista_categorias, default="None")

    def __str__(self):
        return f"{self.category}"


class Active_Deactive(models.Model):
    opciones = [
    ("Yes", "Yes"),
    ("No", "No"),
    ("None", "None")
    ]
    options = models.CharField(max_length=4, choices=opciones, default="None")

    def __str__(self):
        return f"{self.options}"


class Bid(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="Username_Bid")
    user_id = models.IntegerField(blank=True, null=True)
    uuid_bid = models.CharField(max_length=36, blank=True)
    bid_cost = models.FloatField(default=0.0)
    product_uuid = models.CharField(max_length=36, blank=True)

    def __str__(self):
        return f"{self.id}, {User.objects.get(pk=self.user_id)}, {self.uuid_bid}, {self.bid_cost}"


class Auction_listing(models.Model):
    url_dir = models.CharField(max_length=32, blank=True)
    categories = models.ManyToManyField(Category, related_name="Product_Category")
    category_id = models.IntegerField(blank=True, null=True)
    user_id = models.CharField(max_length=64, blank=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="UserName")
    uuid_auction_user = models.CharField(max_length=36, blank=True)
    product_name = models.CharField(max_length=64, blank=True, null=True)
    cost = models.FloatField(default=0.0)
    auction_si_no = models.ManyToManyField(Active_Deactive, related_name="Active_auction")
    auction_si_no_id = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=1024,blank=True)

    def __str__(self):
        """ Return string of values: primary_key, user_id, username, product_name, cost"""
        return f"id: {self.id}, User_id: {self.user_id}, Username: {User.objects.get(pk=self.user_id)}, UUID_Auction: {self.uuid_auction_user}, Category: {Category.objects.get(pk=self.category_id)}, Name_Product: {self.product_name}, Cost: {self.cost}, Url_Imge: {self.url_dir}, Auction_active: {Active_Deactive.objects.get(pk=self.auction_si_no_id)}"


class ClosedBids(models.Model):
    urlDir = models.CharField(max_length=64, blank=True)
    categoryId = models.IntegerField(blank=True, null=True)
    userId = models.IntegerField(blank=True, null=True)
    UserName = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="User_Name")
    UuidAuctionUser = models.CharField(max_length=36, blank=True)
    ProductName = models.CharField(max_length=64, blank=True, null=True)
    Cost = models.FloatField(default=0.0)
    Description = models.CharField(max_length=1024,blank=True)
    WinnerBid = models.CharField(max_length=32, blank=True)
    PriceWinnerBid = models.FloatField(default=0.0)

    class Meta:
        verbose_name_plural = "Closed Bids"

    def __str__(self):
        return f"Id:{self.id}, Bid user: {self.UserName}, UUId Bid: {self.UuidAuctionUser}, Product name: {self.ProductName}, Cost: {self.Cost}, User Winner: {self.WinnerBid}, Price winner $: {self.PriceWinnerBid}"


class Comment(models.Model):
    uuid = models.CharField(max_length=36, blank=True)
    uuidlink_access = models.CharField(max_length=36, blank=True)
    user_id = models.IntegerField(null=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="Username")
    comments = models.CharField(max_length=1024, blank=True)

    def __str__(self):
        """Return id, User_id, uuid_for_auction, Comment"""
        return f"{self.id}, UserID: {self.user_id}, Username: {self.username}, CommentUUID: {self.uuid}, UUID_Auction_listing: {self.uuidlink_access}, Comment: {self.comments}"


class Watchlist(models.Model):
    User_Id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="Watchlist_User")
    uuidAuction = models.ForeignKey(Auction_listing, on_delete=models.CASCADE, blank=True, null=True, related_name="Uuid_linked_Auction")
    priceCurrent = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.id}, Watchlist User: {self.User_Id}, {self.uuidAuction}, Current Price: $ {self.priceCurrent}"


class FilterCategories(models.Model):
    pass
