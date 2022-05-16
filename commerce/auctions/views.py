from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django import forms

from django.db import IntegrityError
from django.forms.fields import URLField, URLInput
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Max, Min, Avg

import pyshorteners
from uuid import uuid4
from .models import User, Category, Auction_listing, Active_Deactive, Comment, Bid, Watchlist, ClosedBids
from time import sleep


class createForm(forms.Form):
    """Formulario para Subasta entregado por el usuario."""
    url_img = forms.URLField(label="Image url", widget=forms.TextInput(attrs={"placeholder": "Enter url image"}))
    choose_category = forms.ChoiceField(label="Choose category", choices=Category.lista_categorias)
    name_product = forms.CharField(label="Product name", widget=forms.TextInput(attrs={"placeholder": "Maximum 64 characters"}))
    put_auction = forms.ChoiceField(label="Put to auction", choices=Active_Deactive.opciones)
    price = forms.FloatField(widget=forms.NumberInput(attrs={"min": "0.0", "placeholder": "$ 0.0", "step": "0.1"}))
    description = forms.CharField(widget=forms.Textarea(attrs={"maxlength": "1024", "placeholder": "Maximum 1024 characters"}))


class createComments(forms.Form):
    """Formulario comentarios"""
    comments = forms.CharField(widget=forms.Textarea(attrs={"maxlength": "1024", "placeholder": "Enter your comments, maximum 1024 characters."}))


class bidForm(forms.Form):
    price = forms.CharField(widget=forms.NumberInput(attrs={"placeholder": "Your Bid", "step": "0.1"}))


class filtradoCategorias(forms.Form):
    categoria = forms.ChoiceField(label="Select category", choices=Category.lista_categorias)


class ConfirmCloseBid(forms.Form):
    confirm = forms.put_auction = forms.ChoiceField(label="You're sure to close this bid?", choices=Active_Deactive.opciones)


def index(request):
    """Indice, Muestra todas las subastas Activas"""

    listUuidBidClosed = []
    queryUuidsBids = ClosedBids.objects.all().values("UuidAuctionUser")
    for item in queryUuidsBids:
        listUuidBidClosed.append(item["UuidAuctionUser"])

    return render(request, "auctions/index.html", {
        "Activos": Auction_listing.objects.filter(auction_si_no_id=2),
        "listClosedAuctions": listUuidBidClosed
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")



def create_listing(request):
    """Crea una Subasta con UUID, almacenado en tabla 'Auction_listing'."""
    if request.method == "POST":
        formulario = createForm(request.POST)
        if formulario.is_valid():
            objects_matches = len(Auction_listing.objects.filter(product_name=formulario.cleaned_data["name_product"]))
            if objects_matches < 1:
                formatImageSupported = ["apng", "avif", "jpg", "jpeg", "jfif", "pjpeg", "pjp", "png", "webp"]
                formatUrlEntered = str(formulario.cleaned_data["url_img"])[-3:].lower()
                if formatUrlEntered in formatImageSupported:
                    url_img = pyshorteners.Shortener().tinyurl.short(formulario.cleaned_data["url_img"])
                else:
                    return render(request, "auctions/create_auctions.html", {
                        "formulario": formulario,
                        "formatImageNOTsupported": f"It must have an image extension, '.{formatUrlEntered}' not accepted."
                        })
                choose_category_id = Category.objects.get(category=formulario.cleaned_data["choose_category"]).id

                name_product = formulario.cleaned_data["name_product"]

                put_auction_si_no_id = Active_Deactive.objects.get(options=formulario.cleaned_data["put_auction"]).id

                price = formulario.cleaned_data["price"]

                description_bid = formulario.cleaned_data["description"]
                id_user = request.user.id

                uuid_for_auction = str(uuid4())

                auction_listingModel = Auction_listing(
                    url_dir=url_img,
                    user_id=id_user,
                    category_id=choose_category_id,
                    auction_si_no_id=put_auction_si_no_id,
                    uuid_auction_user=uuid_for_auction,
                    product_name=name_product,
                    cost=price,
                    username=User.objects.get(pk=id_user),
                    description=description_bid,
                )
                auction_listingModel.save()
                auction_listingModel.auction_si_no.add(put_auction_si_no_id)
                auction_listingModel.categories.add(choose_category_id)

                return HttpResponseRedirect(reverse("my_auctions"))

        else:
            return render(request, "auctions/create_auctions.html", {
                "formulario": formulario
                })
    return render(request, "auctions/create_auctions.html", {
        "formulario": createForm()
    })


def edit_my_auctions(request, uuid_auction):
    """Permite editar Una Subasta existente usando uuid_auction, borra los datos antiguos y guarda los nuevos."""
    auction_editar = Auction_listing.objects.get(uuid_auction_user=uuid_auction)
    comment_Bid = Comment.objects.filter(uuidlink_access=uuid_auction)
    if request.method == "POST":
        auction_editar.delete()

        forma = createForm(request.POST)
        if forma.is_valid():
            url = forma.cleaned_data["url_img"]
            cat = Category.objects.get(category=forma.cleaned_data["choose_category"]).id
            prod = forma.cleaned_data["name_product"]
            quest = Active_Deactive.objects.get(options=forma.cleaned_data["put_auction"]).id
            price = forma.cleaned_data["price"]
            description = forma.cleaned_data["description"]

            auction_listing = Auction_listing(
                url_dir=url,
                user_id=request.user.id,
                category_id=cat,
                auction_si_no_id=quest,
                uuid_auction_user=uuid_auction,
                product_name=prod,
                cost=price,
                username=User.objects.get(pk=request.user.id),
                description=description,
            )
            auction_listing.save()
            auction_listing.auction_si_no.add(quest)
            auction_listing.categories.add(cat)

            return HttpResponseRedirect(reverse("my_auctions"))

    forma = createForm(initial={
        "url_img": auction_editar.url_dir,
        "choose_category": Category.objects.get(pk=auction_editar.category_id),
        "name_product": auction_editar.product_name,
        "put_auction": Active_Deactive.objects.get(pk=auction_editar.auction_si_no_id),
        "price": auction_editar.cost,
        "description": auction_editar.description
    })

    return render(request, "auctions/edit_my_auction.html", {
        "Editar_mi_auction": forma,
        "uuid": uuid_auction,
        "name_product": auction_editar.product_name,
    })



def bids(request, uuid_product):
    """Carga la Subasta con los datos y permite pujar, agregar a seguimiento y si es dueño editar."""
    listUuidBidClosed = []
    queryUuidsBids = ClosedBids.objects.all().values("UuidAuctionUser")
    for item in queryUuidsBids:
        listUuidBidClosed.append(item["UuidAuctionUser"])
    try:
        auction_view = Auction_listing.objects.filter(uuid_auction_user=uuid_product)[0]
        bid_offer_uuid = str(uuid4())
        cant_offersBid = len(Bid.objects.filter(product_uuid=uuid_product))
        bidders = Bid.objects.filter(product_uuid=uuid_product).values("username").distinct()
        totalbidders = len(bidders)

        try:
            max_offerBid = Bid.objects.filter(product_uuid=uuid_product).aggregate(Max("bid_cost"))["bid_cost__max"]
            topUserBid = Bid.objects.filter(product_uuid=uuid_product).filter(bid_cost=max_offerBid).values("user_id")[0]
            NameTopUserBid = User.objects.get(pk=topUserBid["user_id"])
        except:
            max_offerBid = 0
            NameTopUserBid = ""


        if float(auction_view.cost) > float(max_offerBid):
            valor_maximo = auction_view.cost
        else:
            valor_maximo = max_offerBid

        if request.method == "POST":
            comentarios_forma = createComments(request.POST)
            forma_bid = bidForm(request.POST)
            if forma_bid.is_valid():
                min_float = float(auction_view.cost)

                print(float(request.POST["price"]), float(auction_view.cost))
                print(float(request.POST["price"]) > float(auction_view.cost))
                print(float(request.POST["price"]), float(max_offerBid))
                print(float(request.POST["price"]) >  float(max_offerBid))

                if float(request.POST["price"]) > float(auction_view.cost):
                    if float(request.POST["price"]) > float(max_offerBid):
                            offer = forma_bid.cleaned_data["price"]
                            bid_model = Bid(
                                username = User.objects.get(pk=request.user.id),
                                user_id = request.user.id,
                                uuid_bid = bid_offer_uuid,
                                bid_cost = offer,
                                product_uuid = uuid_product
                            )
                            bid_model.save()
                            return HttpResponseRedirect(reverse("bids", args=[uuid_product]))
                    else:
                        return render(request, "auctions/bids.html", {
                                "advertencia": f"You need to raise your bid over $ {valor_maximo}",
                                "TopUser": NameTopUserBid,
                                "formulario": forma_bid,
                                "cant_offers": cant_offersBid,
                                "bidders": totalbidders,
                                "offer_top": max_offerBid,
                                "uid": uuid_product,
                                "auction_value": Auction_listing.objects.filter(uuid_auction_user=uuid_product)[0],
                                "img_url": auction_view.url_dir,
                                "username": auction_view.username,
                                "category": Category.objects.get(pk=auction_view.category_id),
                                "name_product": auction_view.product_name,
                                "cost_initial":auction_view.cost,
                                "description": auction_view.description,
                                "uuiInCloseList": listUuidBidClosed,
                                })
                else:
                    return render(request, "auctions/bids.html", {
                            "advertencia": f"You need to raise your bid over $ {valor_maximo}",
                            "TopUser": NameTopUserBid,
                            "formulario": forma_bid,
                            "cant_offers": cant_offersBid,
                            "bidders": totalbidders,
                            "offer_top": max_offerBid,
                            "uid": uuid_product,
                            "auction_value": Auction_listing.objects.filter(uuid_auction_user=uuid_product)[0],
                            "img_url": auction_view.url_dir,
                            "username": auction_view.username,
                            "category": Category.objects.get(pk=auction_view.category_id),
                            "name_product": auction_view.product_name,
                            "cost_initial":auction_view.cost,
                            "description": auction_view.description,
                            "uuiInCloseList": listUuidBidClosed,
                            })
            if comentarios_forma.is_valid():
                comment = Comment(
                    uuid = str(uuid4()),
                    uuidlink_access = uuid_product,
                    user_id = request.user.id,
                    username = User.objects.get(pk=request.user.id),
                    comments = comentarios_forma.cleaned_data["comments"],
                )
                comment.save()

                return HttpResponseRedirect(reverse("bids", args=[uuid_product]))




        commentsForBid = Comment.objects.filter(uuidlink_access=uuid_product)
        forma_bid = bidForm(initial={"price": valor_maximo})

        return render(request, "auctions/bids.html", {
                "advertencia": "",
                "TopUser": NameTopUserBid,
                "formulario": forma_bid,
                "cant_offers": cant_offersBid,
                "bidders": totalbidders,
                "offer_top": max_offerBid,
                "uid": uuid_product,
                "auction_value": Auction_listing.objects.filter(uuid_auction_user=uuid_product)[0],
                "img_url": auction_view.url_dir,
                "username": auction_view.username,
                "category": Category.objects.get(pk=auction_view.category_id),
                "name_product": auction_view.product_name,
                "cost_initial":auction_view.cost,
                "description": auction_view.description,
                "fomrulario_comentarios": createComments(),
                "allcomments": commentsForBid,
                "uuiInCloseList": listUuidBidClosed,
                })
    except IndexError:
        return HttpResponseRedirect(reverse("index"))


def categories(request):
    """Filtra todas las subastas por categoria."""
    listUuidBidClosed = []
    queryUuidsBids = ClosedBids.objects.all().values("UuidAuctionUser")
    for item in queryUuidsBids:
        listUuidBidClosed.append(item["UuidAuctionUser"])

    if request.method == "POST":
        listFiltered = Auction_listing.objects.filter(categories=Category.objects.get(category=request.POST["categoria"]).id).filter(auction_si_no_id=2)
        print(len(listFiltered))
        return render(request, "auctions/select_categories.html", {
            "select_categories": filtradoCategorias(),
            "listFiltered": listFiltered,
            "isFinishedmyBid": listUuidBidClosed
            })

    return render(request, "auctions/select_categories.html", {
        "select_categories": filtradoCategorias(),
        "listFiltered": ""
    })


def watchlist(request):
    """Agrega a la lista de seguimiento y redirige hacia la subasta."""
    uuidAuction = str(request.META["HTTP_REFERER"].strip()[-36:])
    itemProduct = Auction_listing.objects.filter(uuid_auction_user=uuidAuction)
    maxBidOffer = Bid.objects.filter(product_uuid=uuidAuction).aggregate(Max("bid_cost"))["bid_cost__max"]

    if maxBidOffer is None:
        maxBidOffer = 0.0
    if float(itemProduct[0].cost) > float(maxBidOffer):
        current_price = itemProduct[0].cost
    else:
        current_price = maxBidOffer

    addWatchlist = Watchlist(
        User_Id = User.objects.get(pk=request.user.id),
        uuidAuction = Auction_listing.objects.get(uuid_auction_user=uuidAuction),
        priceCurrent = float(current_price),
    )
    addWatchlist.save()

    return HttpResponseRedirect(reverse(bids, args=[uuidAuction]))


def mywatchlist(request):
    """Muestra todas las subastas que estas siguiendo."""
    listUuidBidClosed = []
    queryUuidsBids = ClosedBids.objects.all().values("UuidAuctionUser")
    for item in queryUuidsBids:
        listUuidBidClosed.append(item["UuidAuctionUser"])

    objectsWatch = Watchlist.objects.filter(User_Id=request.user.id)
    return render(request, "auctions/watchlist.html", {
            "listwatchlist": objectsWatch,
            "isFinishedmyBid": listUuidBidClosed
    })


def my_auctions(request):
    """Obtiene todas las subastas del usuario que lo consulta."""

    listUuidBidClosed = []
    queryUuidsBids = ClosedBids.objects.all().values("UuidAuctionUser")
    for item in queryUuidsBids:
        listUuidBidClosed.append(item["UuidAuctionUser"])

    lista_por_usuario = Auction_listing.objects.filter(user_id=request.user.id)
    return render(request, "auctions/my_auctions.html", {
        "lista_productos": lista_por_usuario,
        "isFinishedmyBid": listUuidBidClosed,
        })


def CloseConfirm(request, uuid_product):
    """Confirmacion de Cerrar Bid y crea un registro en modelo ClosedBids."""
    if request.method == "POST":
        forma = ConfirmCloseBid(request.POST)
        if forma.is_valid():
            if forma.cleaned_data["confirm"] == "Yes":
                max_offerBid = Bid.objects.filter(product_uuid=uuid_product).aggregate(Max("bid_cost"))["bid_cost__max"]
                userWinnerBid = Bid.objects.get(bid_cost=max_offerBid)
                bidAuction = Auction_listing.objects.get(uuid_auction_user=uuid_product)

                entryBidClosed = ClosedBids(
                    urlDir = bidAuction.url_dir,
                    categoryId = bidAuction.category_id,
                    userId = bidAuction.user_id,
                    UserName = bidAuction.username,
                    UuidAuctionUser = bidAuction.uuid_auction_user,
                    ProductName = bidAuction.product_name,
                    Cost = bidAuction.cost,
                    Description = bidAuction.description,
                    WinnerBid = userWinnerBid.username,
                    PriceWinnerBid = float(userWinnerBid.bid_cost),
                )
                entryBidClosed.save()

                return HttpResponseRedirect(reverse("Finished", args=[uuid_product]))
            else:
                return HttpResponseRedirect(reverse("bids", args=[uuid_product]))

    objetoAuction = Auction_listing.objects.get(uuid_auction_user=uuid_product)
    return render(request, "auctions/confirmClose.html", {
        "formulario": ConfirmCloseBid(),
        "uid": uuid_product,
        "imageUrl": objetoAuction.url_dir,
        "productName": objetoAuction.product_name,
    })


def Finished(request, uuid_product):
    cant_offersBid = len(Bid.objects.filter(product_uuid=uuid_product))
    bidders = Bid.objects.filter(product_uuid=uuid_product).values("username").distinct()
    totalbidders = len(bidders)

    try:
        max_offerBid = Bid.objects.filter(product_uuid=uuid_product).aggregate(Max("bid_cost"))["bid_cost__max"]
        topUserBid = Bid.objects.filter(product_uuid=uuid_product).filter(bid_cost=max_offerBid).values("user_id")[0]
        NameTopUserBid = User.objects.get(pk=topUserBid["user_id"])
    except:
        max_offerBid = 0
        NameTopUserBid = ""

    auctionlist = Auction_listing.objects.get(uuid_auction_user=uuid_product)

    return render(request, "auctions/finished.html", {
        "uuid_product": uuid_product,
        "finishBid": ClosedBids.objects.get(UuidAuctionUser=uuid_product),
        "allcomments": Comment.objects.filter(uuidlink_access=uuid_product),
        "bidders": totalbidders,
        "TopUser": NameTopUserBid,
        "img_url": auctionlist.url_dir,
        "cant_offersBid": len(Bid.objects.filter(product_uuid=uuid_product)),
        "cost_initial": auctionlist.cost,
        "username": auctionlist.username,
        "category": Category.objects.get(pk=auctionlist.category_id),
        "description": auctionlist.description,
    })

    # return render(request, "auctions/closed_bid.html", {
    #     "urlDir": objectWinnerBid.urlDir,
    #     "categoryId": Category.objects.get(pk=objectWinnerBid.categoryId),
    #     "UserName": objectWinnerBid.UserName,
    #     "UuidAuctionUser": objectWinnerBid.UuidAuctionUser,
    #     "ProductName": objectWinnerBid.ProductName,
    #     "Cost": objectWinnerBid.Cost,
    #     "Description": objectWinnerBid.Description,
    #     "WinnerBid": objectWinnerBid.WinnerBid,
    #     "PriceWinnerBid": objectWinnerBid.PriceWinnerBid,
    #     })
